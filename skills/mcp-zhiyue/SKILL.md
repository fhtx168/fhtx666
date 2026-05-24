---
name: mcp-zhiyue
description: 智阅文档处理工具，支持文档内容问答、文档文本提取、PDF翻译、脑图生成、文档图片识别。当用户需要读取文档内容、提取文件文字、翻译PDF、生成思维导图、分析文档时使用此 skill。触发关键词：读取文档、提取文本、文档翻译、PDF翻译、思维导图、脑图、文档分析、文件内容、文档问答、文档理解。
compatibility:
  - server: mcp-zhiyue
    tools:
      - rag_recognize_image_in_docment
      - zhiyue_doc_chat
      - zhiyue_doc_extract
      - zhiyue_doc_translate
      - zhiyue_generate_mindmap
---

# mcp-zhiyue — 智阅文档处理

智阅文档处理工具集，支持文档问答、文本提取、PDF翻译、脑图生成和文档图片识别，覆盖文档、音频、视频、图片等多种格式。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有文档处理任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`mcp-zhiyue`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出服务器/工具**：`mcporter list mcp-zhiyue --schema` 查看工具详情。
- **调用工具**：`mcporter call mcp-zhiyue.<tool> key=value`
- 本 skill 的工具列表定义了可用的 MCP 服务器/工具；请仅通过 mcporter 调用它们，并使用全局配置文件中对应的配置项。

---

## 快速决策

| 需求 | 工具 | 说明 |
|------|------|------|
| 基于文件内容回答问题 | `zhiyue_doc_chat` | 用于文档问答，不适合提取原始内容 |
| 提取文件原始文本 | `zhiyue_doc_extract` | 提取文档/音频/视频/图片的原始文本 |
| 翻译 PDF 文档 | `zhiyue_doc_translate` | PDF 镜像翻译，保持格式不变 |
| 生成脑图/思维导图 | `zhiyue_generate_mindmap` | 输入文本或URL，生成 Markdown 脑图 |
| 识别文档中的图片 | `rag_recognize_image_in_docment` | OCR + 多模态识别文档内图片 |

---

## 工具详情

### zhiyue_doc_chat — 文档问答
基于文件内容回答用户问题（不适合提取原始内容，原始内容请用 `zhiyue_doc_extract`）。
```bash
mcporter call mcp-zhiyue.zhiyue_doc_chat url="https://example.com/document.pdf" question="这份文档的主要内容是什么？"
```

### zhiyue_doc_extract — 文档文本提取
从文档、音频、视频、图片中提取原始文本内容。
```bash
mcporter call mcp-zhiyue.zhiyue_doc_extract url="https://example.com/document.pdf"
```
支持格式：PDF、Word、音频文件、视频文件、图片

### zhiyue_doc_translate — PDF 文档翻译
PDF 镜像翻译，翻译后保持原始格式，返回翻译后的 PDF URL。支持中英互译。
```bash
mcporter call mcp-zhiyue.zhiyue_doc_translate url="https://example.com/english-doc.pdf"
```

### zhiyue_generate_mindmap — 生成脑图
根据文本内容或 URL 生成 Markdown 格式的脑图。
```bash
# 基于文本生成脑图
mcporter call mcp-zhiyue.zhiyue_generate_mindmap text="人工智能的发展历程包括：机器学习、深度学习、大语言模型..."

# 基于URL内容生成脑图
mcporter call mcp-zhiyue.zhiyue_generate_mindmap url="https://example.com/article"
```

### rag_recognize_image_in_docment — 文档图片识别
提取文档中的所有图片并进行 OCR 和多模态识别。
```bash
mcporter call mcp-zhiyue.rag_recognize_image_in_docment url="https://example.com/document.pdf"
```
返回：图片内网/外网地址、上下文、OCR 结果、多模态识别结果

---

## 注意事项

- 调用工具前，请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `mcp-zhiyue` 的配置
- `zhiyue_doc_chat` 适合问答，`zhiyue_doc_extract` 适合提取原始内容，请根据需求选择
- PDF 翻译支持中译英和英译中，自动判断源语言
- 脑图输出为 Markdown 格式
