# 阿里云 OCR - 通义千问 VL 图片识别 ✅

使用阿里云 DashScope Qwen-VL 模型进行图片文字识别。支持中文、英文混合识别，适合截图、文档、资讯图片等场景。

## 触发条件
当用户需要：
- OCR 文字识别
- 图片转文字
- 截图内容提取
- 读取图片中的文档/资讯内容
- 扫描识别

## 使用方法

```bash
{baseDir}/scripts/dashscope-ocr.js <image_path> [output_format]
```

**参数**：
- `<image_path>`: 本地图片文件路径（jpg, png, webp, gif, bmp）
- `[output_format]`: 可选，默认为 `markdown`，可以是 `text`、`json` 等

## 示例

```bash
# 转换为 markdown（默认）
{baseDir}/scripts/dashscope-ocr.js /path/to/image.jpg

# 转换为纯文本
{baseDir}/scripts/dashscope-ocr.js /path/to/image.png text
```

## API 配置

API Key 已在 `~/.opcclaw/.env` 中配置：
- `DASHSCOPE_API_KEY=sk-f8abd7b7af1c484e9b93758b5c594fea` ✅ 已测试通过

## 注意事项
- 仅支持本地图片文件
- 远程 URL 需先下载到本地
- 支持中英文混合识别
- 阿里云免费额度可用

## 测试记录
- 2026-05-17 06:37 - 测试通过，成功识别今日头条长图资讯
