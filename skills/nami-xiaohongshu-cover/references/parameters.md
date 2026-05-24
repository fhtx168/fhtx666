# 参数说明

## 命令行参数

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | `-p` | **必填** | 用户创意需求 |
| `--file` | - | `[]` | 附件 JSON 字符串 |
| `--flow-id` | - | (见技能) | 智能体 flow ID |
| `--format` | `-F` | `markdown` | 输出格式 |
| `--timeout` | - | `7200` | 请求超时（秒） |
| `--channel` | - | 自动识别 | 消息渠道 |
| `--verbose` | `-v` | `true` | 打印详细日志 |

## file 参数结构

```json
[
  {
    "title": "文件名",
    "local_path": "/path/to/file",
    "url": "",
    "file_type": 1,
    "size": 12345,
    "sequential_title": "素材1",
    "ext": "docx"
  }
]
```

### file_type 取值

| 值 | 类型 |
|----|------|
| 1 | 文档 |
| 2 | 图片 |
| 3 | 音/视频 |

## 超时说明

> **重要**：超时时间固定为 **10800 秒（3 小时）**，不支持修改。

## 输出格式

| Channel | 格式 |
|---------|------|
| feishu | 飞书卡片 (card 字段) |
| web/webchat/其他 | Markdown (markdown 字段) |
