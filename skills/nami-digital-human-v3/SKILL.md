---
name: nami-digital-human-v3
description: |
  纳米 数字人 3.0。基于个人形象照与声音，生成单人数字人口播/故事视频。
  触发场景：
  (1) 用户说"数字人"、"AI数字人"
  (2) 用户说"生成口播视频"、"AI主播"
  (3) 用户说"虚拟人视频"、"形象照生成视频"
  (4) 用户说"生成个人代言视频"
metadata:
  {
    "openclaw": {
      "emoji": "👤",
      "requires": { "bins": ["python3", "curl"] },
    },
  }
---

# 纳米 数字人 3.0

基于个人形象照与声音，生成单人数字人口播/故事视频。

## 快速开始

```bash
# 先发送开始提示
message 发送 "收到！👤 正在生成数字人视频，任务执行时间较长，请稍候..."

# 基本用法
python3 scripts/nami_digital_human_v3.py -p "生成一个口播视频"

# 飞书渠道需要加 --channel feishu 才会输出卡片
python3 scripts/nami_digital_human_v3.py -p "需求" --channel feishu

```

## Channel 输出规则

| Channel | 输出格式 | 说明 |
|---------|----------|------|
| web | Markdown | 完整输出，不裁剪数据 |
| feishu | 飞书卡片 | 卡片消息，包含按钮 |
| 其他 | Markdown | 默认等同于 web 输出 |

## 输出说明

脚本输出 JSON 格式结果，包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `markdown` | string | Web 格式 Markdown |
| `card` | object | 飞书卡片 (仅 feishu) |
| `data` | object | 原始结果数据 |

### data 字段结构

```json
{
  "summary": "摘要文本",
  "final_tips": "补充提示",
  "share_url": "查看详情链接",
  "image": [{"title": "", "url": "", "description": ""}],
  "video": [{"title": "", "url": "", "description": ""}],
  "other": []
}
```

## 渠道适配

### Feishu 渠道
- 发送开始提示消息
- 使用卡片展示结果
- 包含总结完整数据
- 显示产出物按钮 (视频/图片)

### Web/其他渠道
- 输出 Markdown 格式
- 完整数据，不裁剪
- 包含所有产出物链接

## 输出示例

### Web 输出 (Markdown)

```markdown
# 👤 纳米 数字人 3.0

您的数字人视频已生成，生成链接为：https://xxx.n.cn。

🎬 视频：https://xxx.n.cn

🔗 查看详情：https://xxx.n.cn
```

### Feishu 输出 (卡片)

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "👤 纳米 数字人 3.0 完成"},
    "template": "green"
  },
  "elements": [
    {"tag": "div", "text": {"tag": "plain_text", "content": "您的数字人视频已生成..."}},
    {"tag": "hr"},
    {
      "tag": "action",
      "actions": [
        {"tag": "button", "text": {"tag": "plain_text", "content": "🎬 查看视频"}, "type": "primary", "url": "https://..."}
      ]
    }
  ]
}
```

## 常见错误

- **无视频URL**：prompt 需要明确要求生成"视频"
- **超时**：视频生成耗时较长，默认 3 小时足够
- **上传失败**：检查本地文件路径是否正确

## 详细参考

- 完整参数说明 → [references/parameters.md](references/parameters.md)
- 渠道适配细节 → [references/channels.md](references/channels.md)
- API 签名说明 → [references/api-signature.md](references/api-signature.md)
