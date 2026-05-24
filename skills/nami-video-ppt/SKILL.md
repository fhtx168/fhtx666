---
name: nami-video-ppt
description: |
  纳米视频PPT生成。根据用户上传的文档（或链接）与需求说明，生成创意的PPT或视频演示。
  触发场景：
  (1) 用户说"生成PPT"、"做一份PPT"、"帮我做个演示文稿"
  (2) 用户说"视频PPT"、"PPT视频"、"图文视频"、"图片PPT"
  (3) 用户上传文档并要求"总结成PPT"、"讲解这个文件"、"生成图文"
  (4) 用户说"生成视频演示"、"做一个视频讲解"、"做个小视频"
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": { "bins": ["python3", "curl"] },
    },
  }
---

# 纳米 视频PPT

快速生成图文混排的 PPT 风格图片或视频讲解。

## 快速开始

```bash
# 先发送开始提示
message 发送 "收到！🎬 正在生成PPT，任务执行时间较长，请稍候..."

# 基本用法
python3 scripts/nami_video_ppt.py -p "帮我生成5张关于熬夜危害健康的图片PPT"

# 飞书渠道需要加 --channel feishu 才会输出卡片
python3 scripts/nami_video_ppt.py -p "需求" --channel feishu

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
- 显示产出物按钮 (PPT/视频/PDF)

### Web/其他渠道
- 输出 Markdown 格式
- 完整数据，不裁剪
- 包含所有产出物链接

## 输出示例

### Web 输出 (Markdown)

```markdown
# 🎬 生成多风格PPT

您提供的图片已成功转换为PPT，生成链接为：https://m8r29qxt7uw7xmy4.n.cn。

📊 PPT：https://m8r29qxt7uw7xmy4.n.cn
📄 PDF：https://mcps.beijing2.xstore.qihu.com/ppt/xxx.pdf

🔗 查看详情：https://m8r29qxt7uw7xmy4.n.cn
```

### Feishu 输出 (卡片)

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "🎬 生成多风格PPT"},
    "template": "blue"
  },
  "elements": [
    {"tag": "div", "text": {"tag": "lark_md", "content": "您提供的图片已成功转换为PPT，生成链接为：https://m8r29qxt7uw7xmy4.n.cn。"}},
    {"tag": "div", "text": {"tag": "lark_md", "content": "---"}},
    {
      "tag": "action",
      "actions": [
        {"tag": "button", "text": {"tag": "plain_text", "content": "📊 查看PPT"}, "type": "primary", "url": "https://..."},
        {"tag": "button", "text": {"tag": "plain_text", "content": "🎬 查看视频"}, "type": "primary", "url": "https://..."}
      ]
    }
  ]
}
```

## 常见错误

- **无图片URL**：prompt 需要明确要求生成"图片"而非"视频"
- **超时**：文档解析耗时较长，默认 2 小时足够
- **上传失败**：检查本地文件路径是否正确

## 详细参考

- 完整参数说明 → [references/parameters.md](references/parameters.md)
- 渠道适配细节 → [references/channels.md](references/channels.md)
- API 签名说明 → [references/api-signature.md](references/api-signature.md)
