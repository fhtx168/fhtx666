---
name: 纳米SVideo AI视频生成
description: 使用 SVideo AI 模型生成视频，支持文生视频和图生视频，时长支持4/8/12秒。当用户需要"SVideo生成视频"、"AI生成短视频"、"文字转视频"时，加载此 skill。
---

# 纳米SVideo AI视频生成

基于 SVideo AI 模型，支持文生视频和图生视频，共 **1 个工具**。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有视频生成任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`nami_svideo_gen_video`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出工具**：`mcporter list nami_svideo_gen_video --schema`
- **调用工具**：`mcporter call nami_svideo_gen_video.nami_s_video prompt="<提示词>"`

---

## 快速使用

**文生视频**：
```
mcporter call nami_svideo_gen_video.nami_s_video \
  prompt="海边日落，波浪轻拍沙滩，慢镜头" \
  ratio="16:9" duration=8
```

**图生视频**：
```
mcporter call nami_svideo_gen_video.nami_s_video \
  prompt="镜头缓慢推进，风景如画" \
  image="https://example.com/landscape.jpg" \
  ratio="16:9" duration=4
```

---

## 工具说明

### nami_s_video（文生/图生视频）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 视频描述提示词 |
| `image` | string | ❌ | 图片 URL（有则为图生视频，无则为文生视频）；图片分辨率需符合目标比例要求 |
| `duration` | number | ❌ | 时长：`4`/`8`/`12`（秒），默认 `4` |
| `ratio` | string | ❌ | 比例：`16:9` / `9:16`，默认 `9:16` |

---

## 注意事项

- 时长仅支持 `4`、`8`、`12` 秒三档
- 图生视频时，**图片分辨率需符合目标比例的宽高要求**
- 图片 URL 需为**可公开访问的 HTTP/HTTPS 链接**
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `nami_svideo_gen_video` 对应的配置
