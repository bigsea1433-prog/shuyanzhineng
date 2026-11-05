import contextlib
from email.message import Message
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import unittest
import urllib.error
import urllib.response
from unittest.mock import Mock, patch


spec = importlib.util.spec_from_file_location("shuyanai_client", Path(__file__).parents[1] / "examples" / "client.py")
client = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = client
spec.loader.exec_module(client)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.config = client.Config("https://platform.shuyanai.com/v1", "test-secret", "test-model", 12)

    def test_chat_request_and_usage(self):
        request_spec = client.request_spec(self.config, list_models=False, prompt="你好", max_tokens=42)
        payload = {"choices": [{"message": {"content": "回答"}}], "usage": {"total_tokens": 8, "unknown": "unsafe"}}
        response = io.BytesIO(json.dumps(payload).encode())
        opener = Mock()
        opener.open.return_value = response
        with patch.object(client.urllib.request, "build_opener", return_value=opener):
            result = client.call_api(self.config, request_spec)
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, "https://platform.shuyanai.com/v1/chat/completions")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertEqual(opener.open.call_args.kwargs["timeout"], 12)
        self.assertEqual(json.loads(request.data), {"model": "test-model", "messages": [{"role": "user", "content": "你好"}], "stream": False, "max_tokens": 42})
        output = client.format_result(result, list_models=False)
        self.assertIn("回答", output)
        self.assertIn('"total_tokens": 8', output)
        self.assertNotIn("unsafe", output)
        opener.open.assert_called_once()

    def test_models_needs_no_model(self):
        with patch.dict(os.environ, {"SHUYANAI_API_KEY": "test-secret"}, clear=True):
            config = client.load_config(list_models=True)
        request_spec = client.request_spec(config, list_models=True, prompt="", max_tokens=0)
        self.assertEqual(request_spec["method"], "GET")
        self.assertEqual(request_spec["url"], "https://platform.shuyanai.com/v1/models")
        self.assertIsNone(request_spec["body"])
        self.assertEqual(client.format_result({"data": [{"id": "a"}, {"id": "b"}]}, list_models=True), "a\nb")

    def test_401_hides_error_body_and_does_not_retry(self):
        opener = Mock()
        opener.open.side_effect = urllib.error.HTTPError("https://platform.shuyanai.com/v1/models", 401, "secret message", {}, io.BytesIO(b"test-secret"))
        request_spec = client.request_spec(self.config, list_models=True, prompt="", max_tokens=0)
        with patch.object(client.urllib.request, "build_opener", return_value=opener):
            with self.assertRaises(client.ClientError) as result:
                client.call_api(self.config, request_spec)
        self.assertIn("401", str(result.exception))
        self.assertNotIn("test-secret", str(result.exception))
        self.assertNotIn("secret message", str(result.exception))
        opener.open.assert_called_once()

    def test_redirect_is_not_followed(self):
        headers = Message()
        headers["Location"] = "https://evil.example/steal"
        response = urllib.response.addinfourl(io.BytesIO(), headers, "https://platform.shuyanai.com/v1/models", 302)
        response.msg = "Found"
        # 使用真实 opener/重定向处理链，只把网络传输层替换成离线响应。
        with patch.object(client.urllib.request.HTTPSHandler, "https_open", return_value=response) as transport:
            with self.assertRaisesRegex(client.ClientError, "拒绝跟随"):
                client.call_api(self.config, client.request_spec(self.config, list_models=True, prompt="", max_tokens=0))
        transport.assert_called_once()
        self.assertEqual(transport.call_args.args[0].full_url, "https://platform.shuyanai.com/v1/models")

    def test_dry_run_without_key_and_without_network(self):
        for env in ({}, {"SHUYANAI_API_KEY": "never-print-this-key"}):
            with self.subTest(env=bool(env)), patch.dict(os.environ, env, clear=True), patch.object(client, "call_api") as call, contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(client.main(["--dry-run"]), 0)
                text = output.getvalue()
                self.assertNotIn("Authorization", text)
                self.assertNotIn("never-print-this-key", text)
                self.assertIn("chat/completions", text)
                call.assert_not_called()

    def test_configuration_rejects_unsafe_values(self):
        for extra in ({"SHUYANAI_BASE_URL": "http://example.com/v1"}, {"SHUYANAI_BASE_URL": "https://user:pass@example.com/v1"}, {"SHUYANAI_TIMEOUT": "nan"}, {"SHUYANAI_TIMEOUT": "0"}):
            env = {"SHUYANAI_API_KEY": "test-secret", "SHUYANAI_MODEL": "model", **extra}
            with self.subTest(extra=extra), patch.dict(os.environ, env, clear=True):
                with self.assertRaises(client.ClientError):
                    client.load_config()

    def test_missing_model_and_invalid_response(self):
        with patch.dict(os.environ, {"SHUYANAI_API_KEY": "test-secret"}, clear=True):
            with self.assertRaisesRegex(client.ClientError, "SHUYANAI_MODEL"):
                client.load_config()
        with self.assertRaises(client.ClientError):
            client.format_result({"choices": []}, list_models=False)


if __name__ == "__main__":
    unittest.main()
