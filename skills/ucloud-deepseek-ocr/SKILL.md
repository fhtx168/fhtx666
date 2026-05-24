# DeepSeek OCR - 图片文字识别

使用 DeepSeek-OCR 模型识别图片中的文字。支持中文、英文混合识别，适合截图、文档、资讯图片等场景。

## 触发条件
当用户需要：
- OCR 文字识别
- 图片转文字
- 截图内容提取
- 读取图片中的文档/资讯内容
- 扫描识别

## 使用方法

```bash
{baseDir}/scripts/ocr.sh <image_path> [output_format]
```

**参数**：
- `<image_path>`: 本地图片文件路径（jpg, png, webp, gif, bmp）
- `[output_format]`: 可选，默认为 `markdown`，可以是 `text`、`json` 等

## 示例

```bash
# 转换为 markdown（默认）
{baseDir}/scripts/ocr.sh /path/to/image.jpg

# 转换为纯文本
{baseDir}/scripts/ocr.sh /path/to/image.png text

# 提取表格为 JSON
{baseDir}/scripts/ocr.sh /path/to/table.jpg "extract table as json"
```

## API 配置

API Key 已在 `~/.opcclaw/.env` 中配置：
- `DEEPSEEK_API_KEY=sk-106f9d3972484484ac520c2b28ac48ca`

默认 API URL: `https://api.modelverse.cn/v1/chat/completions`

## 注意事项
- 仅支持本地图片文件
- 远程 URL 需先下载到本地
- 支持中英文混合识别
- 适合复杂布局的文档图片
