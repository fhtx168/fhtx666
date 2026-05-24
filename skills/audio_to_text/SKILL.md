---
name: audio_to_text
description: 音频转文字工具，支持将音频文件转换为文字内容（语音识别/ASR）。当用户需要将音频转文字、语音识别、音频内容提取、录音转文字时使用此 skill。触发关键词：音频转文字、语音识别、ASR、录音转文字、音频识别、语音转文字、音频内容提取。
compatibility:
  - server: audio_to_text
    tools: []
---

# audio_to_text — 音频转文字（语音识别）

纳米AI音频转文字服务，将音频文件通过 ASR（自动语音识别）技术转换为文字内容。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有音频转文字任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`audio_to_text`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出服务器/工具**：`mcporter list audio_to_text --schema` 查看工具详情。
- **调用工具**：`mcporter call audio_to_text.<tool> key=value`
- 本 skill 的工具列表定义了可用的 MCP 服务器/工具；请仅通过 mcporter 调用它们，并使用全局配置文件中对应的配置项。

---

## 使用方式

首先通过 mcporter 查询可用工具：
```bash
mcporter list audio_to_text --schema
```

然后根据返回的工具列表调用相应工具（通常传入音频 URL）：
```bash
mcporter call audio_to_text.<tool_name> url="https://example.com/audio.mp3"
```

---

## 注意事项

- 调用工具前，请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `audio_to_text` 的配置
- 如连接失败（HTTP 502），服务可能暂时不可用，请稍后重试
- 使用前建议先执行 `mcporter list audio_to_text --schema` 确认服务状态和可用工具
