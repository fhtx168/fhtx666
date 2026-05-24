# 渠道适配说明

## Channel 输出规则

| Channel | 输出格式 | 说明 |
|---------|----------|------|
| webchat | Markdown | 完整输出，不裁剪数据 |
| web | Markdown | 完整输出，不裁剪数据 |
| feishu | 飞书卡片 | 卡片消息，包含按钮 |
| 其他 | Markdown | 默认等同于 webchat 输出 |

## 调用前提示

所有渠道都会在调用前打印提示信息：

```
收到！🎬 正在生成PPT，任务执行时间较长，请稍候...
```

## 飞书渠道

### 输出结构
- 使用卡片展示结果
- 完整输出 summary + 产出物按钮
- 标题：`✨ 纳米 视频PPT 完成`
- 模板颜色：成功(blue) / 失败(red)

### 产出物按钮
- 🎬 查看视频
- 🖼️ 查看图片
- 🔗 查看详情

### 错误处理
显示红色错误卡片：
```
❌ 纳米 视频PPT 执行出错
错误信息：xxx
```

## Web/Webchat/其他渠道

输出 Markdown 格式，完整输出 summary：

```markdown
## ✨ 纳米 视频PPT

完整 summary 内容...

### 🎬 视频
- [▶️ 查看视频](https://xxx)

### 🖼️ 图片
- [🖼️ 查看图片](https://xxx)

### 💡
xxx

---

🔗 **[查看详情](https://xxx)**
```

## 自动识别

优先顺序：
1. 命令行 `--channel` 参数
2. 环境变量 `OPENCLAW_CHANNEL`
3. 默认 `webchat`

## data 字段结构

脚本返回的 `data` 字段结构：

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

### 展示顺序
1. summary
2. video (视频)
3. image (图片)
4. other (其他)
5. final_tips (补充提示)
6. share_url (查看详情)
