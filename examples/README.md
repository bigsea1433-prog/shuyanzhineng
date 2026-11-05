# 数眼智能 API 接入示例

这是依据公开接口独立编写的最小 Python 客户端，使用 Python 3.10+ 标准库，无需安装依赖。它是文章配套示例，不是官方 SDK，也不是聚合平台后台。本仓库未使用真实 API Key 联调，不代表已验证服务可用性或模型效果。

接口依据（核验日期：2026-11-05）：

- [官方 Chat Completions 文档](https://doc.shuyanai.com/doc-8784048)：聊天请求为 `POST /v1/chat/completions`，必填 `model` 与 `messages`，使用 Bearer 鉴权。
- [官方综合接口文档](https://doc.shuyanai.com/doc-8652765)：AI 模型服务根地址为 `https://platform.shuyanai.com`，`GET /v1/models` 列出当前密钥可用模型。

## 先离线查看

在仓库根目录运行，无需密钥、不会联网：

```powershell
python examples/client.py --dry-run
python examples/client.py --list-models --dry-run
```

离线输出仅包含请求方式、地址与请求体，不包含鉴权字段。未设置模型时，预览中使用占位文字。

## 本地真实调用

先在数眼智能控制台取得 **AI 模型 API Key**。搜索/阅读服务的密钥不能假定可用于模型接口。请在本地设置环境变量；示例中的占位内容需要自行替换，不要将真实密钥发到文章、评论或仓库。

```powershell
$env:SHUYANAI_API_KEY = '替换为你的AI模型密钥'
python examples/client.py --list-models

$env:SHUYANAI_MODEL = '替换为当前密钥可用的模型ID'
python examples/client.py --prompt '请写一份技术文章大纲' --max-tokens 512
```

真实调用会向平台发送提示词，并可能消耗账户额度。程序只发起一次请求；超时不代表服务端没有执行，请先查看控制台的调用记录再决定是否重试。请勿发送不适合交给该服务处理的内容。

`.env.example` 只是配置说明，客户端不会自动读取 `.env` 文件。默认根地址为 `https://platform.shuyanai.com/v1`，可通过 `SHUYANAI_BASE_URL` 覆盖；只允许 HTTPS。更换地址会将密钥和提示词发给所填服务，请仅使用自己核对过的入口。`SHUYANAI_TIMEOUT` 为秒数，默认 60，允许大于 0 且不超过 300。

## 输出与限制

程序输出文本回答以及响应中提供的输入、输出、总 Token 用量，不据此推算费用。它拒绝跟随重定向，不打印密钥或上游错误正文，提供 401、403、429 和服务异常提示。示例仅实现非流式纯文本聊天与模型列表，不处理工具调用、多模态或完整生产治理；模型和参数兼容性仍需依据当前控制台与文档核对。

## 离线验证

```powershell
python -m unittest discover -s tests -v
```

测试使用模拟响应，不会调用数眼智能，也不会产生模型费用。
