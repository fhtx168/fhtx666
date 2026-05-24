---
name: 智阅图片文字提取（OCR）
description: 提取图片中的文本内容（OCR识别）。当用户需要"识别图片文字"、"图片OCR"、"提取图片中的文本"时，加载此 skill。
---

# 智阅图片文字提取（OCR）

从图片中提取文本内容，共 **1 个工具**。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的图片文字提取任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。读取该文件并**仅使用 `zhiyue-media` 对应的配置**。
- **调用工具**：`mcporter call zhiyue-media.zhiyue_media_extract file_url="<图片URL>"`

---

## 快速使用

```
mcporter call zhiyue-media.zhiyue_media_extract \
  file_url="https://example.com/document_image.jpg"
```

---

## 工具说明

### zhiyue_media_extract（图片文字提取）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_url` | string | ✅ | 图片文件 URL |

---

## 注意事项

- 图片 URL 需为**可公开访问的 HTTP/HTTPS 链接**
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `zhiyue-media` 对应的配置
