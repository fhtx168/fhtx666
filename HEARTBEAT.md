# HEARTBEAT.md - 轻量级心跳（60m 间隔）
# 仅执行简单检查，有问题才记录，无问题回复 HEARTBEAT_OK

## 快速检查清单
- [ ] Git 状态：`git status --porcelain` 有未提交变更？
- [ ] 磁盘空间：C 盘剩余 < 10GB？
- [ ] 关键进程：OpenClaw Gateway 是否运行？

## 检查逻辑
1. 无异常 → 回复 `HEARTBEAT_OK`（零上下文）
2. 有异常 → 记录到 `memory/heartbeat-issues.md` 并推送微信
3. 不加载 MEMORY.md / memory/*.md（节省 97% token）
