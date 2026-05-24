---
name: 纳米MiniMax AI视频生成
description: 使用 MiniMax（海螺）AI 模型生成视频，支持文生视频（T2V）、图生视频（I2V）、首尾帧生视频三种模式。当用户需要"MiniMax生成视频"、"海螺视频"、"AI生成视频"时，加载此 skill。
---

# 纳米MiniMax AI视频生成

基于 MiniMax（海螺）AI 视频模型，支持三种视频生成模式，共 **3 个工具**：
- **文生视频**（T2V）：纯文字提示词生成视频
- **图生视频**（I2V）：首帧图片 + 提示词生成视频
- **首尾帧生视频**：首帧 + 尾帧图片生成过渡视频

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有视频生成任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`nami_minimax_mcp`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出工具**：`mcporter list nami_minimax_mcp --schema`
- **调用工具**：`mcporter call nami_minimax_mcp.<tool> key=value`

---

## 快速决策

**只有文字，想生成视频**
→ 通过 mcporter 调用 `minimax_23_t2v`
→ 示例：
```
mcporter call nami_minimax_mcp.minimax_23_t2v \
  prompt="夕阳下海浪拍打礁石，慢镜头，电影感" \
  duration=6
```

**有一张图片，想让它动起来**
→ 通过 mcporter 调用 `minimax_23_i2v`
→ 示例：
```
mcporter call nami_minimax_mcp.minimax_23_i2v \
  image="https://example.com/photo.jpg" \
  prompt="镜头缓慢推进，光线柔和" \
  duration=6
```

**有首帧和尾帧，想生成中间过渡**
→ 通过 mcporter 调用 `minimax_02_start_end2v`
→ 示例：
```
mcporter call nami_minimax_mcp.minimax_02_start_end2v \
  image1="https://example.com/start.jpg" \
  image2="https://example.com/end.jpg" \
  prompt="平滑过渡，光线变化" \
  duration=6
```

---

## 工具说明

### minimax_23_t2v（文生视频）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 视频描述提示词，≤2000字 |
| `duration` | number | ❌ | 时长：`6` 或 `10`（秒），默认 `6` |
| `resolution` | string | ❌ | 分辨率：`768p`（默认）/ `1080p`（仅支持6s） |

### minimax_23_i2v（图生视频）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 首帧图片 URL |
| `prompt` | string | ❌ | 视频描述提示词，≤2000字 |
| `duration` | number | ❌ | 时长：`6` 或 `10`（秒），默认 `6` |
| `resolution` | string | ❌ | 分辨率：`768p`（默认）/ `1080p`（仅支持6s） |

### minimax_02_start_end2v（首尾帧生视频）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image1` | string | ✅ | 首帧图片 URL |
| `image2` | string | ✅ | 尾帧图片 URL |
| `prompt` | string | ❌ | 视频描述提示词，≤2000字 |
| `duration` | number | ❌ | 时长：`6` 或 `10`（秒），默认 `6` |
| `resolution` | string | ❌ | 分辨率：`768p`（默认）/ `1080p`（仅支持6s） |

---

## 注意事项

- **1080p 分辨率只支持 6 秒时长**，10 秒时长不支持 1080p
- 输入图片**仅供参考**，不会严格基于原图初始化（即生成结果可能与原图有差异）
- 图片 URL 需为**可公开访问的 HTTP/HTTPS 链接**
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `nami_minimax_mcp` 对应的配置
