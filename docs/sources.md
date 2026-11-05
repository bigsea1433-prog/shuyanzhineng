# 来源、公开代码与核验记录

核验日期：2026-11-05。以下为资料与代码研究入口；本文不承诺服务性能、模型来源、价格或可用性。

| 来源 | 本仓库使用的内容 |
| --- | --- |
| [官网关于页面](https://www.shuyanai.com/about) | 公司公开的 MaaS、数据处理与模型服务定位 |
| [开放文档首页](https://doc.shuyanai.com/) | 接口和开发工具文档入口 |
| [Chat Completions](https://doc.shuyanai.com/doc-8784048) | 对话路径、Bearer 鉴权与请求响应约定 |
| [API 密钥与额度综合接口](https://doc.shuyanai.com/doc-8652765) | 模型调用地址、当前 Key 模型列表 |
| [API Key 指南](https://doc.shuyanai.com/doc-8441886) | 模型与搜索阅读 Key 的区分 |
| [旧 Models 单页](https://doc.shuyanai.com/api-417863696) | 文档差异记录，不能与当前综合文档无条件混用 |
| [Reader 接口](https://doc.shuyanai.com/api-288269246) | 网页阅读工具资料入口，示例尚未实现 |
| [官方 Dify 相关文章](https://www.shuyanai.com/blogs/16) | 平台数据工具与 Dify 生态的关联资料 |

## 可以研究哪些公开代码

- [dataeyesai/dataeyes-mcp-server](https://github.com/dataeyesai/dataeyes-mcp-server)：提供搜索和网页读取的 MCP 服务。[中文说明](https://github.com/dataeyesai/dataeyes-mcp-server/blob/main/README_zh.md)明确数眼智能支持并标注 MIT 许可。适合研究工具定义、凭证配置、传输方式和错误边界。
- [dataeyesai/dataeyes](https://github.com/dataeyesai/dataeyes)：Dify 数据工具插件，可通过[市场页面](https://marketplace.dify.ai/plugin/dataeyesai/dataeyes)交叉核对。此次未确认根目录中完整授权条件，本仓库只链接参考。

没有查到可核验的完整大模型聚合平台后台开源实现。上述项目不能据此被称为其完整后台源码。

本仓库未复制这些项目的实现，Python 接入示例依据接口规范独立编写。后续若复制第三方文件，应逐个核对对应版本的许可证并保留必要声明。公开可见本身不等于授权随意复制。

## 文档差异如何处理

聊天文档及综合接口文档使用 `platform.shuyanai.com` 作为模型调用入口；旧 Models 页面使用另一个域名且标注开发中。本仓库采用综合文档配置，未进行带真实 Key 的连通性验证。接入前以最新控制台和官方说明复核。

## 写文章时标记证据

| 内容类型 | 推荐写法 |
| --- | --- |
| 官方能力 | “官方文档列出……”，附具体页面和日期 |
| 作者方案 | “本文建议……”，说明适用条件和取舍 |
| 实测结果 | 给出模型、日期、环境、样本与统计方法 |
| 暂未验证 | 直接写“未验证”，不填推测数值 |

原创文章和原创代码的授权方式由仓库维护者另行明确；第三方内容始终适用其原有授权。
