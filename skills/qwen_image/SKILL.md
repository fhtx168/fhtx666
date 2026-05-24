---
name: 纳米通义万象图像视频生成
description: 使用通义万象（Qwen/Wan）系列AI模型生成图片和视频，支持文生图、图生图、文生视频、图生视频、角色参考视频、视频换人、动作迁移等，共8个工具。当用户需要"通义生图"、"万象视频"、"Wan生成视频"、"视频换人"、"角色一致性视频"时，加载此 skill。
---

# 纳米通义万象图像视频生成

基于通义万象（Qwen/Wan）系列模型，提供图像和视频生成全套能力，共 **8 个工具**。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有生成任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。读取该文件并**仅使用 `qwen_image` 对应的配置**。
- **列出工具**：`mcporter list qwen_image --schema`
- **调用工具**：`mcporter call qwen_image.<tool> key=value`

---

## 快速决策

**文字生成图片（通义万象）**
```
mcporter call qwen_image.qwen_text_to_image \
  prompt="赛博朋克城市夜景，霓虹灯，写实" ratio="16:9"
```

**文字生成图片（Wan 2.6，支持多比例）**
```
mcporter call qwen_image.wan26_t2i \
  prompt="水墨山水画，古典风格" ratio="16:9"
```

**图片生成图片（Wan 2.6，支持1-4张参考图）**
```
mcporter call qwen_image.wan26_i2i \
  prompt="将图片转为油画风格" \
  --args '{"image_urls":["https://example.com/photo.jpg"]}'
```

**文字生成视频（Wan 2.5，支持多镜头）**
```
mcporter call qwen_image.wan25_t2v_preview \
  prompt="城市日出，延时摄影，光线变化" \
  ratio="16:9" duration="8s"
```

**图片生成视频（Wan 2.5）**
```
mcporter call qwen_image.wan25_i2v_preview \
  image_url="https://example.com/photo.jpg" \
  prompt="镜头缓慢推进，风景如画" duration="5s"
```

**角色参考视频（保持角色一致性，Wan 2.6）**
```
mcporter call qwen_image.wan26_r2v_preview \
  prompt="character1在城市街道上行走" \
  --args '{"video_urls":["https://example.com/character.mp4"]}'
```

**视频换人（用图片人物替换视频主角）**
```
mcporter call qwen_image.wan22_animate_mix \
  image_url="https://example.com/person.jpg" \
  video_url="https://example.com/video.mp4"
```

**动作迁移（人物图片 + 参考动作视频）**
```
mcporter call qwen_image.wan22_animate_move \
  image_url="https://example.com/person.jpg" \
  video_url="https://example.com/dance.mp4"
```

---

## 工具全览

| 工具名 | 功能 | 必填参数 |
|--------|------|---------|
| `qwen_text_to_image` | 文生图（通义，擅长文字渲染） | `prompt` |
| `wan26_t2i` | 文生图（Wan 2.6） | `prompt` |
| `wan26_i2i` | 图生图（1-4张参考图） | `prompt`、`image_urls` |
| `wan25_t2v_preview` | 文生视频（Wan 2.5，2-15s，支持多镜头） | `prompt` |
| `wan25_i2v_preview` | 图生视频（Wan 2.5，2-15s） | `prompt`、`image_url` |
| `wan26_r2v_preview` | 角色参考视频（保持角色一致性） | `prompt`、`video_urls` |
| `wan22_animate_mix` | 视频换人（图片人物替换视频主角） | `image_url`、`video_url` |
| `wan22_animate_move` | 动作迁移（人物图片+参考动作视频） | `image_url`、`video_url` |

---

## 注意事项

- Wan 2.5 视频支持 **2-15秒**，支持 `single`/`multi` 镜头模式
- Wan 2.6 角色参考视频最多支持 **3个角色**（character1/2/3）
- `wan22_animate_mix/move` 视频要求：2-30s，≤200MB，MP4/AVI/MOV
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `qwen_image` 对应的配置
