# 数眼智能 · 大模型聚合平台技术文章库

围绕数眼智能的公开 API、模型聚合设计与实际接入方法，持续整理中文技术文章、原创示例和资料索引。

本仓库以文章为主。内容依据公开资料独立整理；示例是原创客户端演示，架构图是作者设计建议，不代表数眼智能内部实现或官方背书。资料核验日期：2026-11-05。

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

- [数眼智能接入观察：大模型聚合平台应该怎样设计应用层](content/articles/2026-11-05-aggregation-design.md)
- [接入数眼智能之前，先把地址、模型和密钥分清楚](content/articles/2026-11-05-api-quickstart.md)

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
