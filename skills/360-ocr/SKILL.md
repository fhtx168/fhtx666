# 360AI OCR - 免费图片文字识别

使用 360AI 免费 API 进行图片文字识别。支持中文、英文混合识别，适合截图、文档、资讯图片等场景。

## 触发条件
当用户需要：
- OCR 文字识别
- 图片转文字
- 截图内容提取
- 读取图片中的文档/资讯内容
- 扫描识别

## 使用方法

```bash
{baseDir}/scripts/360-ocr.js <image_path> [output_format]
```

**参数**：
- `<image_path>`: 本地图片文件路径（jpg, png, webp, gif, bmp）
- `[output_format]`: 可选，默认为 `markdown`，可以是 `text`、`json` 等

## 示例

```bash
# 转换为 markdown（默认）
{baseDir}/scripts/360-ocr.js /path/to/image.jpg

# 转换为纯文本
{baseDir}/scripts/360-ocr.js /path/to/image.png text
```

## API 配置

API Key 已在 `~/.opcclaw/.env` 中配置：
- `360AI_API_KEY=ra1FOy6ZVHvyPZeOkaEge41rKeB2YScu904s3iq4WO`

## 注意事项
- 仅支持本地图片文件
- 远程 URL 需先下载到本地
- 支持中英文混合识别
- 免费额度，适合日常使用
