---
name: 纳米360搜索（通用/学术/图片/B站）
description: 使用360纳米AI搜索引擎进行信息搜索。当用户需要搜索任何信息时都应使用此 skill，包括：通用网页搜索、最新新闻、学术论文（PubMed/arXiv/ACM/IEEE/必应学术）、论文查找、B站视频搜索、图片搜索。只要用户说"搜索"、"查找"、"找一下"、"查一下"、"有没有关于X的论文"、"找几张图片"、"B站有没有X的视频"等，都应立即加载此 skill。
---

# 纳米360搜索（通用/学术/图片/B站）

360纳米AI官方搜索引擎，覆盖通用搜索、学术文献（6大平台）、B站视频、多引擎图片搜索。共 9 个工具，按场景分为三组。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有搜索任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`so-search`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出服务器/工具**：`mcporter list`，或 `mcporter list so-search --schema` 查看指定服务器的工具详情。
- **调用工具**：`mcporter call <server.tool> key=value`（例如 `mcporter call so-search.aiso_do_search query="关键词" r=false`）。
- 本 skill 中的工具列表（见下方工具分组）定义了可用的 MCP 服务器/工具；请仅通过 mcporter 调用它们，并使用全局配置文件中对应的配置项。

---

## 快速决策

**用户想搜索信息、新闻、知识、事件**
→ 通过 mcporter 调用 `aiso_do_search`
→ `r` 参数判断：问题是否需要实时数据？
  - `r=true`：今天/最新/最近/现在/股价/天气/新闻/近期事件
  - `r=false`：历史知识/概念解释/学术内容/方法论
→ 示例：`mcporter call so-search.aiso_do_search query="人工智能最新进展" r=true`

**用户想找论文 / 文献 / 学术资料**
→ 已知标题或作者 → 通过 mcporter 调用 `aiso_paper_search`（跨库查找）
→ 按领域选库：
  - 医学/生命科学 → PubMed：`mcporter call so-search.aiso_pubmed query="..."`
  - AI/物理/数学/CS → arXiv：`mcporter call so-search.aiso_arxiv query="..."`
  - CS会议/工程实现 → ACM：`mcporter call so-search.aiso_acm query="..."`
  - 电气/电子/通信 → IEEE：`mcporter call so-search.aiso_ieee_xplore query="..."`
  - 社科/人文/跨学科 → 必应学术：`mcporter call so-search.aiso_bing_academic query="..."`

**用户想找B站视频**
→ 通过 mcporter 调用 `aiso_bilibili_search`
→ 示例：`mcporter call so-search.aiso_bilibili_search query="Python教程"`

**用户想找图片**
→ 通过 mcporter 调用 `multi_engine_image_search`
→ `mixed_re_rank=true`：需要高质量图片（PPT插图/文章配图/素材）
→ 示例：`mcporter call so-search.multi_engine_image_search query="星空摄影" mixed_re_rank=true`

---

## 工具分组

| 分组 | 工具 |
|------|------|
| 通用搜索 | `aiso_do_search` |
| 学术搜索 | `aiso_pubmed` / `aiso_arxiv` / `aiso_acm` / `aiso_bing_academic` / `aiso_ieee_xplore` / `aiso_paper_search` |
| 媒体搜索 | `aiso_bilibili_search` / `multi_engine_image_search` |

---

## 通用注意事项

- 所有工具的 `query` 建议用**中文或英文关键词**，避免长句提问
- 学术搜索的 `query` 用**英文**效果通常更好
- 图片搜索返回的 `url` 字段是实际可用链接，`origin_url` 仅供参考
- 调用任何工具前，请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用本 skill 声明的 MCP 服务器配置，再通过 mcporter 执行操作
