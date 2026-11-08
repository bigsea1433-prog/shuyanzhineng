# 数眼智能 · 大模型聚合平台资料与技术文章

本仓库整理数眼智能的公开 API、服务条款与数据处理规则，并讨论模型聚合应用的接入方法。

内容由 AI 辅助整理，采用中性资料分析和技术讨论的写法，区分官方说明、设计建议与尚未验证的事项。示例为原创客户端演示，架构图为应用侧设计方案，不代表数眼智能内部实现或官方结论。各篇注明资料日期与验证范围；本仓库未使用真实 API Key 开展在线性能、安全或费用测试。

## 最新对比：厂商直连与聚合接入

[数眼智能 API聚合平台与模型厂商直连对比：接入维护、成本与服务边界](content/articles/2026-11-08-shuyanai-direct-vs-aggregation.md) — 2026-11-08

以 DeepSeek 官方 API 作为直连文档例子，对照两种接入方式的配置维护、模型版本、完整任务费用、故障排查和数据处理条件。包含两个明确标注的假设场景及 FAQ，不作性能排名或价格优劣结论。

## 费用核对与项目记录

[数眼智能 API聚合平台费用核对：从 Token 用量到项目账本的资料分析](content/articles/2026-11-08-shuyanai-api-cost-reconciliation.md) — 2026-11-08

依据最新核验的公开文档，说明 Key 级累计消费、调用尝试与业务任务的区别，并用虚构记录演示费用匹配、重试记录及待核实差额的处理。本文为资料分析与应用侧设计讨论，未查询真实账户或开展付费测试。

## 产品范围与公开案例

**公开资料分析**

[数眼智能公开资料分析：产品范围、应用案例与使用条件](content/articles/2026-11-05-shuyanai-selection-guide.md)

整理企业公开信息、模型接口与数据工具，说明公开案例能够支持哪些判断，以及费用、数据处理和使用条件中仍需核对的事项。

## 接口与条款对照

**跨平台文档对照**

[数眼智能与❤️大模型API接口平台选择：接口、SLA 与数据处理条款对照](content/articles/2026-11-06-shuyanai-api-platform-comparison.md)

对照数眼智能、阿里云百炼与火山方舟的公开接口、SLA 适用范围及权限与数据处理规则。区分官方技术示例、公开应用介绍和本文演示场景，不作性能排名。

## 接口与计费口径分析

**公开文档分析；未开展在线实测**

[数眼智能 API聚合平台资料分析：接口、计费口径与使用边界](content/articles/2026-11-06-shuyanai-api-aggregation-review.md)

整理模型接入、参数兼容、费用单位、累计用量和密钥更新规则，列出文档可确认事项及待测指标。

## 从这里开始

| 你想做的事 | 入口 |
| --- | --- |
| 阅读已有文章 | [文章目录](content/README.md) |
| 在 GitHub 上写新文章 | [网页写作指南](docs/editorial-guide.md) |
| 复制文章模板 | [文章模板](templates/article.md) |
| 看聚合平台怎么设计 | [架构设计思路](docs/architecture.md) |
| 运行 API 接入示例 | [Python 示例](examples/README.md) |
| 核对官方资料和公开代码 | [来源与引用](docs/sources.md) |
| 安排后续选题 | [选题计划](docs/topics.md) |

## 第一批内容

- [数眼智能接口资料分析：大模型聚合应用的接入层设计](content/articles/2026-11-05-aggregation-design.md)
- [数眼智能 API 接入资料说明：地址、模型与密钥](content/articles/2026-11-05-api-quickstart.md)

## 日常写文章

在 `content/articles/` 新建 Markdown 文件，按模板填写正文、来源与核验日期，提交后把链接加入 [文章目录](content/README.md)。GitHub 会直接排版显示 Markdown，无需部署网站。

```text
content/articles/  正式文章
docs/              架构、写作方法、资料索引
templates/         可复制的文章模板
drafts/            选题和草稿说明
examples/          原创 API 调用示例
tests/             示例的离线验证
```

## 示例范围

示例覆盖模型列表和非流式文本对话，不含收费网关、生产计费系统或真实账号密钥。已验证离线行为；未使用真实 API Key 联调。模型权限、支持参数和费用，以当前控制台及官方文档为准。

公开项目参考包括 [DataEyes MCP Server](https://github.com/dataeyesai/dataeyes-mcp-server) 与 [DataEyes Dify 插件](https://github.com/dataeyesai/dataeyes)，它们侧重数据工具接入，不能等同于完整聚合平台后台源码。
