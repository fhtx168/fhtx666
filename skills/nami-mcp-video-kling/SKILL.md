---
name: 纳米可灵（Kling）AI视频图像生成
description: 使用可灵（Kling）AI多版本模型生成视频和图片，支持文生视频、图生视频、首尾帧视频、参考生视频、视频编辑、文生图、图生图，覆盖Kling v2.6/v2.5 turbo/v3/v3 omni四个版本，共18个工具。当用户需要"可灵生成视频"、"Kling视频"、"多镜头视频"、"视频编辑"、"AI生成图片"时，加载此 skill。
---

# 纳米可灵（Kling）AI视频图像生成

基于可灵（Kling）AI 多版本模型，提供视频生成、图片生成、视频编辑等全套能力，共 **18 个工具**。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有生成任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`nami-mcp-video-kling`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出工具**：`mcporter list nami-mcp-video-kling --schema`
- **调用工具**：`mcporter call nami-mcp-video-kling.<tool> key=value`

---

## 版本选择指南

| 版本 | 特点 | 推荐场景 |
|------|------|---------|
| **Kling v3 Omni** | 最新最强，支持多镜头、4K图片、3-15s视频 | 最优质输出、多镜头叙事 |
| **Kling v3** | 高质量，支持多镜头、3-15s视频 | 高质量标准生成 |
| **Kling v2.6** | 稳定版，5s/10s | 日常生成 |
| **Kling v2.5 Turbo** | 支持ASMR/配乐提示词 | 需要音效控制 |
| **Kling O1** | 支持主体创建+参考生成+视频编辑 | 主体一致性、视频编辑 |

---

## 快速决策

**文字生成视频（推荐用 v3 omni）**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_t2v \
  multi_shot=false prompt="夕阳下奔跑的少女，电影感，慢镜头" \
  ratio="16:9" duration=5
```

**多镜头叙事视频**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_t2v \
  multi_shot=true \
  --args '{"multi_prompt":["第一幕：清晨，阳光透过窗帘","第二幕：女主角起床，伸懒腰"],"multi_duration":[4,4]}'
```

**图片生成视频**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_i2v \
  image1="https://example.com/photo.jpg" \
  prompt="镜头缓慢推进，微风吹动头发" duration=5
```

**首帧+尾帧生成视频**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_i2v \
  image1="https://example.com/start.jpg" \
  image2="https://example.com/end.jpg" \
  prompt="平滑过渡，光线变化" duration=8
```

**文字生成图片（v3 omni，最高4K）**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_t2i \
  prompt="赛博朋克城市夜景，霓虹灯，写实风格" \
  ratio="16:9" resolution="4k"
```

**图片生成图片（风格迁移/变体）**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_i2i \
  prompt="将<<<image_1>>>转换为水彩画风格" \
  --args '{"image_list":["https://example.com/photo.jpg"]}'
```

**视频编辑（给视频换背景/添加元素）**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_edit_video \
  prompt="将<<<video_1>>>的背景替换为星空" \
  --args '{"video_list":["https://example.com/video.mp4"]}'
```

**参考图生成视频（主体一致性）**
```
mcporter call nami-mcp-video-kling.kling_v30_omni_refer_video \
  prompt="<<<image_1>>>在城市街道上行走，电影感" \
  --args '{"image_list":["https://example.com/character.jpg"]}'
```

---

## 工具全览

### Kling v3 Omni（最新版，推荐）

| 工具名 | 功能 |
|--------|------|
| `kling_v30_omni_t2v` | 文生视频，支持多镜头（3-15s，1080p） |
| `kling_v30_omni_i2v` | 图生视频/首尾帧视频（3-15s，1080p） |
| `kling_v30_omni_t2i` | 文生图（1k/2k/4k） |
| `kling_v30_omni_i2i` | 图生图，支持多参考图（最多10张） |
| `kling_v30_omni_refer_video` | 参考生视频（主体一致性） |
| `kling_v30_omni_edit_video` | 视频编辑（替换背景/添加元素） |

### Kling v3

| 工具名 | 功能 |
|--------|------|
| `kling_v30_t2v` | 文生视频，支持多镜头（3-15s） |
| `kling_v30_i2v` | 图生视频/首尾帧视频（3-15s） |
| `kling_v30_t2i` | 文生图（1k/2k） |
| `kling_v30_i2i` | 图生图（单参考图） |

### Kling v2.6

| 工具名 | 功能 |
|--------|------|
| `kling_v26_t2v` | 文生视频（5s/10s，16:9/9:16/1:1） |
| `kling_v26_i2v` | 图生视频（5s/10s，1080p） |

### Kling v2.5 Turbo

| 工具名 | 功能 |
|--------|------|
| `kling_v2_5_turbo_t2v` | 文生视频，支持BGM/音效提示词，ASMR模式 |
| `kling_v2_5_turbo_i2v` | 图生视频，支持BGM/音效提示词，ASMR模式 |
| `kling_v2_5_turbo_start_end2v` | 首尾帧生视频 |

### Kling O1（主体创建+参考生成）

| 工具名 | 功能 |
|--------|------|
| `kling_o1_create_element` | 创建参考主体（用于主体一致性生成） |
| `kling_o1_refer_video` | 参考生视频（图片/主体/视频参考） |
| `kling_o1_edit_video` | 视频编辑 |

---

## 多镜头视频使用说明

`kling_v30_omni_t2v` 和 `kling_v30_t2v` 支持多镜头模式：

```
# 单镜头模式
mcporter call nami-mcp-video-kling.kling_v30_omni_t2v \
  multi_shot=false prompt="单一场景描述" duration=8

# 多镜头模式
mcporter call nami-mcp-video-kling.kling_v30_omni_t2v \
  multi_shot=true \
  --args '{"multi_prompt":["镜头1描述","镜头2描述","镜头3描述"],"multi_duration":[3,4,5]}'
```

---

## 视频编辑提示词格式

使用 `<<<>>>` 格式引用媒体：
- 引用图片：`<<<image_1>>>`（对应 `image_list` 第1张）
- 引用视频：`<<<video_1>>>`（对应 `video_list` 第1个）

示例：`prompt="将<<<video_1>>>的背景替换为雪山，保留人物"`

---

## 注意事项

- 图片宽高比需在 **1:2.5 ~ 2.5:1** 之间（适用于 i2v 工具）
- 视频编辑的参考视频：**3-10秒，≤200MB，MP4/MOV格式**
- 多镜头总时长需在 **3-15秒** 范围内
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `nami-mcp-video-kling` 对应的配置
