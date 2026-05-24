# 阿里云视频字幕识别 - Qwen-VL 视频理解

使用阿里云 DashScope Qwen-VL 模型进行视频帧分析和字幕提取。支持视频截图 OCR、关键帧文字识别。

## 触发条件
当用户需要：
- 视频字幕提取
- 视频内容理解
- 视频截图 OCR
- 叶荣添预见栏目观看整理
- 视频资讯分析

## 使用方法

```bash
{baseDir}/scripts/video-subtitle.js <video_path> [output_format]
```

**参数**：
- `<video_path>`: 本地视频文件路径（mp4, mov, avi, webm）
- `[output_format]`: 可选，默认为 `srt`，可以是 `text`、`json` 等

## 示例

```bash
# 提取字幕为 SRT 格式
{baseDir}/scripts/video-subtitle.js /path/to/video.mp4

# 提取为纯文本
{baseDir}/scripts/video-subtitle.js /path/to/video.mp4 text
```

## API 配置

API Key 已在 `~/.opcclaw/.env` 中配置：
- `DASHSCOPE_API_KEY=sk-f8abd7b7af1c484e9b93758b5c594fea` ✅

## 注意事项
- 视频需先截取关键帧
- 支持中文、英文字幕识别
- 适合财经视频、投资栏目、会议记录
