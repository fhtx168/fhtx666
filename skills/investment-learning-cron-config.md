# 投研学习系统 - Cron 定时任务配置

> 创建时间：2026-05-06  
> 状态：待测试通过后启用

---

## Cron 任务列表

### 1. 全网监测任务

```json
{
  "id": "investment-learning-monitor",
  "name": "投研学习 - 全网监测",
  "schedule": {
    "kind": "cron",
    "expr": "0 */2 * * *"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "python C:/Users/Admin/.opcclaw/workspace/skills/investment-learning-monitor.py"
  },
  "enabled": false,
  "notifyOnSuccess": false,
  "notifyOnFailure": true
}
```

**执行频率**：每 2 小时执行一次  
**说明**：监测搜狗微信、微博、财经资讯等平台

---

### 2. 叶荣添专项监测

```json
{
  "id": "yerongtian-special-monitor",
  "name": "投研学习 - 叶荣添专项",
  "schedule": {
    "kind": "cron",
    "expr": "0 */1 * * *"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "python C:/Users/Admin/.opcclaw/workspace/skills/investment-learning-monitor.py --target=yerongtian"
  },
  "enabled": false,
  "notifyOnSuccess": false,
  "notifyOnFailure": true
}
```

**执行频率**：每 1 小时执行一次  
**说明**：重点监测叶荣添全平台更新

---

### 3. 知识库清理任务

```json
{
  "id": "knowledge-cleanup",
  "name": "投研学习 - 知识库清理",
  "schedule": {
    "kind": "cron",
    "expr": "0 3 * * 0"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "python C:/Users/Admin/.opcclaw/workspace/skills/knowledge-cleanup.py"
  },
  "enabled": false,
  "notifyOnSuccess": false,
  "notifyOnFailure": true
}
```

**执行频率**：每周日凌晨 3:00  
**说明**：清理重复、过时、低质内容

---

### 4. 周报生成任务

```json
{
  "id": "weekly-report-generate",
  "name": "投研学习 - 周报生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 20 * * 0"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "python C:/Users/Admin/.opcclaw/workspace/skills/generate-weekly-report.py"
  },
  "enabled": false,
  "notifyOnSuccess": false,
  "notifyOnFailure": true
}
```

**执行频率**：每周日 20:00  
**说明**：生成投研学习周报

---

### 5. 周报推送任务

```json
{
  "id": "weekly-report-push",
  "name": "投研学习 - 周报推送",
  "schedule": {
    "kind": "cron",
    "expr": "0 21 * * 0"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "python C:/Users/Admin/.opcclaw/workspace/skills/push-weekly-report.py"
  },
  "enabled": false,
  "notifyOnSuccess": false,
  "notifyOnFailure": true
}
```

**执行频率**：每周日 21:00  
**说明**：推送周报给用户

---

## 启用步骤

### 前提条件

- [x] 监测脚本手动测试通过
- [ ] 知识库目录创建完成
- [ ] 周报脚本测试通过
- [ ] 推送通道验证正常

### 启用流程

1. **验证测试**：运行 `test-investment-learning.py`，确保全部通过
2. **配置 Cron**：将上述任务添加到 `cron-tasks.json`
3. **设置 enabled: true**：逐个启用任务
4. **监控运行**：观察首次执行结果
5. **调整优化**：根据运行情况调整频率

---

## 监控与告警

### 监控指标

| 指标 | 正常范围 | 告警阈值 |
|------|----------|----------|
| 监测成功率 | >95% | <80% |
| 内容抓取量 | >10 篇/天 | <5 篇/天 |
| 归档成功率 | >95% | <80% |
| 周报生成率 | 100% | 失败 |

### 告警方式

- **推送失败**：即时微信通知
- **连续失败 3 次**：即时微信通知 + 日志记录
- **系统异常**：即时微信通知

---

## 首次周报时间

**2026 年 5 月 18 日（周日）21:00**

---

_配置版本：v1.0_  
_最后更新：2026-05-06_
