"""数眼智能公开接口的原创最小客户端；仅使用 Python 3.10+ 标准库。"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_BASE_URL = "https://platform.shuyanai.com/v1"
DEFAULT_PROMPT = "请为《大模型聚合平台的工程设计》写一个文章大纲，区分事实与设计建议。"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class ClientError(Exception):
    """可以直接展示、不会携带密钥或上游错误正文的错误。"""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # 对任何跳转都拒绝重发，避免 Authorization 被带到另一个地址。
        return None


@dataclass(frozen=True)
class Config:
    base_url: str
    api_key: str
    model: str
    timeout: float


def _clean_text(value: str, name: str, *, required: bool = True) -> str:
    value = value.strip()
    if required and not value:
        raise ClientError(f"请设置 {name}。")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ClientError(f"{name} 不能包含控制字符。")
    return value


def load_config(*, dry_run: bool = False, list_models: bool = False) -> Config:
    base_url = os.environ.get("SHUYANAI_BASE_URL", DEFAULT_BASE_URL).strip().rstrip("/")
    try:
        parsed = urllib.parse.urlsplit(base_url)
    except ValueError:
        raise ClientError("SHUYANAI_BASE_URL 不是有效的 HTTPS 根地址。") from None
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or any(char.isspace() for char in base_url)
    ):
        raise ClientError("SHUYANAI_BASE_URL 必须是无账号、查询参数或片段的 HTTPS 根地址。")
    try:
        parsed.port
    except ValueError:
        raise ClientError("SHUYANAI_BASE_URL 的端口无效。") from None
    try:
        timeout = float(os.environ.get("SHUYANAI_TIMEOUT", "60"))
    except ValueError:
        raise ClientError("SHUYANAI_TIMEOUT 必须是秒数。") from None
    if not math.isfinite(timeout) or not 0 < timeout <= 300:
        raise ClientError("SHUYANAI_TIMEOUT 必须大于 0 且不超过 300 秒。")

    model = _clean_text(
        os.environ.get("SHUYANAI_MODEL", ""),
        "SHUYANAI_MODEL",
        required=not dry_run and not list_models,
    )
    # 离线模式不读取密钥，不创建 Authorization。
    api_key = "" if dry_run else _clean_text(os.environ.get("SHUYANAI_API_KEY", ""), "SHUYANAI_API_KEY")
    return Config(base_url=base_url, api_key=api_key, model=model, timeout=timeout)


def request_spec(config: Config, *, list_models: bool, prompt: str, max_tokens: int) -> dict[str, Any]:
    if list_models:
        return {"method": "GET", "url": config.base_url + "/models", "body": None}
    if not prompt.strip():
        raise ClientError("--prompt 不能为空。")
    if max_tokens <= 0:
        raise ClientError("--max-tokens 必须是正整数。")
    return {
        "method": "POST",
        "url": config.base_url + "/chat/completions",
        "body": {
            "model": config.model or "<从控制台或模型列表选择模型ID>",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": max_tokens,
        },
    }


def call_api(config: Config, spec: dict[str, Any]) -> dict[str, Any]:
    data = None if spec["body"] is None else json.dumps(spec["body"], ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        spec["url"],
        data=data,
        method=spec["method"],
        headers={"Authorization": "Bearer " + config.api_key, "Content-Type": "application/json"},
    )
    opener = urllib.request.build_opener(NoRedirect())
    try:
        # 只请求一次；POST 超时后服务端可能已生成并计费，不能盲目重试。
        with opener.open(request, timeout=config.timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as error:
        status = error.code
        error.close()
        if 300 <= status < 400:
            message = "接口返回重定向，已拒绝跟随；请核对 HTTPS 根地址。"
        elif status == 401:
            message = "鉴权失败（401），请检查 AI 模型 API Key。"
        elif status == 403:
            message = "访问被拒绝（403），请检查密钥权限、模型权限及平台访问规则。"
        elif status == 429:
            message = "请求被限流（429），请查看配额与平台限制，稍后人工重试。"
        elif 500 <= status < 600:
            message = f"服务暂时异常（{status}）；请先确认调用状态，再决定是否重试。"
        else:
            message = f"接口请求失败（HTTP {status}），请核对参数和官方文档。"
        raise ClientError(message) from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        raise ClientError("网络连接失败或超时；本次未自动重试，请检查调用状态和网络。") from None
    if len(raw) > MAX_RESPONSE_BYTES:
        raise ClientError("响应过大，已停止解析。")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ClientError("接口响应不是有效的 UTF-8 JSON。") from None
    if not isinstance(payload, dict):
        raise ClientError("接口响应结构异常：应返回 JSON 对象。")
    return payload


def format_result(payload: dict[str, Any], *, list_models: bool) -> str:
    if list_models:
        data = payload.get("data")
        if not isinstance(data, list) or any(
            not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in data
        ):
            raise ClientError("模型列表响应结构异常。")
        return "\n".join(item["id"] for item in data) or "当前密钥没有返回可用模型。"
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise ClientError("对话响应结构异常，未找到文本回答。") from None
    if not isinstance(content, str):
        raise ClientError("响应没有文本内容；本例不处理工具调用或纯推理字段。")
    usage = payload.get("usage")
    if isinstance(usage, dict):
        safe_usage = {
            key: usage[key]
            for key in ("prompt_tokens", "completion_tokens", "total_tokens")
            if type(usage.get(key)) is int and usage[key] >= 0
        }
        if safe_usage:
            content += "\n\n用量（平台响应）：" + json.dumps(safe_usage, ensure_ascii=False)
    return content


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="数眼智能 API 接入示例（非官方 SDK）")
    parser.add_argument("--list-models", action="store_true", help="列出当前密钥可调用的模型")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="发送给模型的纯文本提示词")
    parser.add_argument("--max-tokens", type=int, default=512, help="输出 Token 上限（默认 512）")
    parser.add_argument("--dry-run", action="store_true", help="离线预览请求，不读取或发送密钥")
    args = parser.parse_args(argv)
    try:
        config = load_config(dry_run=args.dry_run, list_models=args.list_models)
        spec = request_spec(config, list_models=args.list_models, prompt=args.prompt, max_tokens=args.max_tokens)
        if args.dry_run:
            print(json.dumps(spec, ensure_ascii=False, indent=2))
            return 0
        output = format_result(call_api(config, spec), list_models=args.list_models)
        # 即使异常上游把密钥放入生成内容，本示例也不把该密钥输出到终端。
        print(output.replace(config.api_key, "[REDACTED]"))
        return 0
    except ClientError as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
