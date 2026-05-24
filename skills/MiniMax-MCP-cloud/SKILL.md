---
name: 纳米MiniMax全能AI（TTS/视频/图片/音乐）
description: MiniMax全功能AI套件，支持文字转语音、音色克隆、文生视频（含导演模式镜头控制）、图生视频、批量视频生成、文生图、AI音乐生成，共7个工具。当用户需要"MiniMax全功能"、"镜头控制视频"、"导演模式视频"时，加载此 skill。
---

# 纳米MiniMax全能AI（TTS/视频/图片/音乐）

MiniMax 全功能 AI 套件，共 **7 个工具**，支持语音、视频、图片、音乐全媒体生成。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有生成任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。读取该文件并**仅使用 `MiniMax-MCP-cloud` 对应的配置**。
- **列出工具**：`mcporter list MiniMax-MCP-cloud --schema`
- **调用工具**：`mcporter call MiniMax-MCP-cloud.<tool> key=value`

---

## 快速决策

**文字转语音**
```
mcporter call MiniMax-MCP-cloud.text_to_audio text="欢迎使用MiniMax语音合成"
```

**文生视频（普通）**
```
mcporter call MiniMax-MCP-cloud.generate_video \
  prompt="夕阳下奔跑的少女，电影感" model="T2V-01"
```

**文生视频（导演模式，控制镜头）**
```
mcporter call MiniMax-MCP-cloud.generate_video \
  prompt="[Push in] 城市夜景，霓虹灯闪烁 [Zoom out]" model="T2V-01-Director"
```

**图生视频**
```
mcporter call MiniMax-MCP-cloud.generate_video \
  prompt="镜头缓慢推进" model="I2V-01" \
  first_frame_image="https://example.com/photo.jpg"
```

**批量生成视频**
```
mcporter call MiniMax-MCP-cloud.batch_generate_video \
  --args '{"prompts":["场景1描述","场景2描述"],"model":"T2V-01"}'
```

**文生图（可批量）**
```
mcporter call MiniMax-MCP-cloud.text_to_image \
  prompt="赛博朋克城市夜景" aspect_ratio="16:9" n=1
```

**AI音乐生成**
```
mcporter call MiniMax-MCP-cloud.music_generation \
  prompt="流行音乐，伤感，适合雨夜" \
  lyrics="[Verse]\n我站在雨中等你\n[Chorus]\n你却已远去"
```

---

## 工具全览

| 工具名 | 功能 |
|--------|------|
| `text_to_audio` | 文字转语音（TTS） |
| `list_voices` | 查询可用音色列表 |
| `voice_clone` | 音色克隆 |
| `generate_video` | 生成单个视频（T2V/I2V，支持导演模式） |
| `batch_generate_video` | 批量生成视频 |
| `text_to_image` | 文生图（最多9张） |
| `music_generation` | AI音乐生成（最长1分钟） |

---

## 导演模式镜头指令

使用 `T2V-01-Director` 或 `I2V-01-Director` 模型时，prompt 中可插入镜头指令：

| 指令 | 效果 |
|------|------|
| `[Truck left]` / `[Truck right]` | 横移镜头 |
| `[Pan left]` / `[Pan right]` | 平移镜头 |
| `[Push in]` / `[Pull out]` | 推进/拉远 |
| `[Pedestal up]` / `[Pedestal down]` | 升降镜头 |
| `[Tilt up]` / `[Tilt down]` | 俯仰镜头 |
| `[Zoom in]` / `[Zoom out]` | 变焦 |
| `[Shake]` | 抖动效果 |
| `[Tracking shot]` | 跟随镜头 |
| `[Static shot]` | 静止镜头 |

---

## 注意事项

- ⚠️ **`text_to_audio`、`voice_clone`、`generate_video`、`batch_generate_video`、`text_to_image`、`music_generation` 会产生 API 调用费用**，请仅在用户明确需要时调用
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `MiniMax-MCP-cloud` 对应的配置
