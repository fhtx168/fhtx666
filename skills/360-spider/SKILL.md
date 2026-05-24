---
name: 360网页爬虫抓取
description: 360网页抓取工具集，支持普通网页抓取（Markdown/HTML输出）、深度层级爬取、小红书专项抓取、网页视频采集。当用户需要"抓取网页内容"、"爬取网页"、"读取URL内容"、"抓取小红书"、"下载网页视频"、"深度爬取网站"时，加载此 skill。
---

# 360网页爬虫抓取

360专业网页抓取工具集，支持 JS 渲染、Cookie 注入、代理等高级功能，共 **4 个工具**：
- **普通网页抓取**：单页抓取，输出 Markdown 或 HTML
- **深度爬取**：从入口 URL 层级爬取，按意图筛选目标页面
- **小红书专项抓取**：专门处理小红书页面
- **视频采集**：下载网页中的视频内容

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有网页抓取任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`360-spider`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出工具**：`mcporter list 360-spider --schema`
- **调用工具**：`mcporter call 360-spider.<tool> url="<url>"`

---

## 快速决策

**抓取普通网页内容（最常用）**
→ 通过 mcporter 调用 `crawler_360`
→ 示例：
```
mcporter call 360-spider.crawler_360 url="https://example.com/article"
```

**需要同时获取正文图片**
```
mcporter call 360-spider.crawler_360 url="https://example.com/article" article_image=1
```

**抓取小红书笔记**
→ 通过 mcporter 调用 `crawler_redbook_360`
→ 示例：
```
mcporter call 360-spider.crawler_redbook_360 url="https://www.xiaohongshu.com/explore/..."
```

**从一个网站入口深度爬取多个页面**
→ 通过 mcporter 调用 `depth_crawler_360`
→ 示例：
```
mcporter call 360-spider.depth_crawler_360 url="https://news.example.com" user_intent="科技新闻" max_size=20
```

**下载网页中的视频**
→ 通过 mcporter 调用 `crawler_video_360`
→ 示例：
```
mcporter call 360-spider.crawler_video_360 url="https://example.com/video-page"
```

---

## 工具说明

### crawler_360（普通网页抓取）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 目标网页 URL |
| `markdown_out` | int | ❌ | `1`=输出 Markdown（默认），`0`=输出压缩 HTML |
| `article_image` | int | ❌ | `1`=输出正文插图，`0`=不输出（默认） |
| `force_js` | int | ❌ | `1`=强制 JS 渲染（默认），`0`=不渲染 |
| `need_image` | int | ❌ | `1`=下载图片，`0`=不下载（默认） |
| `screenshot` | int | ❌ | `1`=输出网页截图，`0`=不输出（默认） |
| `cookie_str` | string | ❌ | Cookie 字符串（用于登录/反爬） |
| `ua` | string | ❌ | 自定义 User-Agent |
| `referer` | string | ❌ | 自定义 Referer |
| `proxy` | string | ❌ | 代理服务器地址 |

### depth_crawler_360（深度层级爬取）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 入口 URL |
| `user_intent` | string | ❌ | 目标意图词，用于筛选目标页面（默认匹配新闻页面） |
| `max_depth` | int | ❌ | 最大爬取深度，默认 `10` |
| `max_size` | int | ❌ | 最大采集 HTML 条数，默认 `15`，最大 `50` |
| `cross_domain` | int | ❌ | `1`=允许跨域，`0`=不允许（默认） |
| `force_js` | int | ❌ | `1`=强制渲染（默认） |

### crawler_redbook_360（小红书专项抓取）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 小红书笔记 URL |
| `ua` | string | ❌ | 自定义 User-Agent |
| `proxy` | string | ❌ | 代理服务器地址 |

### crawler_video_360（网页视频采集）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 包含视频的网页 URL |
| `ua` | string | ❌ | 自定义 User-Agent |
| `proxy` | string | ❌ | 代理服务器地址 |

---

## 注意事项

- 默认输出 **Markdown 格式**，便于后续处理；如需 HTML 可设 `markdown_out=0`
- 遇到需要登录的页面，可传入 `cookie_str` 参数
- 深度爬取时 `max_size` 最大为 50，避免过大请求
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `360-spider` 对应的配置
