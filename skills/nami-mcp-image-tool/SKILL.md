---
name: 纳米图片工具（分割/超分）
description: 图片实用处理工具，支持图片分割（切成4宫格或9宫格）和图片超分辨率增强（提升清晰度，最高4倍放大）。当用户需要"把图片切成九宫格"、"图片分割"、"图片超分"、"图片放大"、"提升图片清晰度"时，加载此 skill。
---

# 纳米图片工具（分割/超分）

提供图片分割和超分辨率增强两项核心能力，共 **2 个工具**。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有图片处理任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`nami-mcp-image-tool`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出工具**：`mcporter list nami-mcp-image-tool --schema`
- **调用工具**：`mcporter call nami-mcp-image-tool.<tool> key=value`

---

## 快速决策

**用户想把图片切成九宫格 / 四宫格 / 分割图片**
→ 通过 mcporter 调用 `nami_image_split`
→ `part=9`（3x3，默认）或 `part=4`（2x2）
→ 示例：
```
mcporter call nami-mcp-image-tool.nami_image_split url="https://example.com/image.jpg" part=9
```

**用户想提升图片清晰度 / 图片超分 / 图片放大**
→ 通过 mcporter 调用 `nami_image_upscale`
→ `factor` 选择放大倍数（1/2/3/4，默认2倍）
→ 示例：
```
mcporter call nami-mcp-image-tool.nami_image_upscale --args '{"urls":["https://example.com/image.jpg"],"factor":"4"}'
```

---

## 工具说明

### nami_image_split（图片分割）

将一张图片切割为多个部分，常用于制作社交媒体九宫格图。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 需要分割的图片 URL |
| `part` | "4" \| "9" | ❌ | 分割份数：`4`（2x2四宫格）或 `9`（3x3九宫格），默认 `9` |

**示例**：
```
# 九宫格分割（默认）
mcporter call nami-mcp-image-tool.nami_image_split url="https://example.com/photo.jpg"

# 四宫格分割
mcporter call nami-mcp-image-tool.nami_image_split url="https://example.com/photo.jpg" part=4
```

---

### nami_image_upscale（图片超分辨率增强）

使用 AI 超分辨率技术提升图片清晰度，支持多张图片并发处理。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `urls` | string[] | ✅ | 需要超分的图片 URL 列表（支持多张并发） |
| `factor` | "1"\|"2"\|"3"\|"4" | ❌ | 放大倍数，默认 `2` |
| `max` | number | ❌ | 最大分辨率限制（长边），超过则不处理，`0` 表示不限制，默认 `2048` |
| `noface` | "0"\|"1" | ❌ | 是否无人脸模式：`0`=有人脸（默认），`1`=无人脸 |

**示例**：
```
# 单张图片2倍超分（默认）
mcporter call nami-mcp-image-tool.nami_image_upscale --args '{"urls":["https://example.com/photo.jpg"]}'

# 多张图片4倍超分，无人脸模式
mcporter call nami-mcp-image-tool.nami_image_upscale --args '{"urls":["https://example.com/a.jpg","https://example.com/b.jpg"],"factor":"4","noface":"1"}'
```

---

## 注意事项

- 图片 URL 需为**可公开访问的 HTTP/HTTPS 链接**
- 超分时若图片长边超过 `max` 值（默认2048px），则不进行处理；设 `max=0` 可取消限制
- 人像图片建议使用 `noface=0`（有人脸模式），普通风景/产品图可用 `noface=1`
- 调用任何工具前，请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `nami-mcp-image-tool` 对应的配置
