# 跨通道同步制度化协议

## 核心原则
**双向实时同步，数据完整性优先**

### 启动流程（所有会话必须执行）
1. **读取同步日志**：加载 `.sync/channel-sync.md` 获取最新状态摘要
2. **验证文件完整性**：确认关键文件已同步（战略方案/执行计划/监控体系）
3. **加载当日记忆**：读取 `memory/YYYY-MM-DD.md` 获取当天详细上下文
4. **检查Git状态**：运行 `git status` 确认无未提交变更

### 产出规范（所有操作必须遵守）
- **立即同步**：任何决策/分析/操作结果必须立即写入 `.sync/channel-sync.md`
- **文件持久化**：重要决策同时保存到对应的功能文件（如 `strategic_implementation/*.md`）
- **Git备份**：每小时自动提交，确保数据不丢失
- **三级验证**：微信端操作 → 电脑端验证 → Git记录确认

### 关键文件路径标准化
| 内容类型 | 文件路径 |
|---------|---------|
| 战略方案 | `strategic_implementation/upgraded_strategy_with_seven_cards.md` |
| 执行计划 | `strategic_implementation/weekly_execution_plan.md` |
| 交易记录 | `portfolio/today_trades.md` |
| 监控推送 | `strategic_implementation/market_monitoring_dashboard.md` |
| 分析框架 | `skills/research-framework/framework-v2.1.md` |
| 同步日志 | `.sync/channel-sync.md` |

### 自动化保障机制
- **每日15:30**：自动监控数据更新并推送
- **每次交易**：实时保存交易记录到 `portfolio/today_trades.md`
- **方案调整**：立即反映在战略方案文件中
- **Git备份**：每小时自动提交（cron任务ID: auto-git-backup-hourly）

### 质量保证标准
- **信息一致性**：所有通道看到的方案 = 完全相同的文件内容
- **跨平台同步**：无论在微信还是电脑上查看，信息完全一致  
- **零数据丢失**：绝不允许出现"失忆"或"丢数据"的情况
- **操作可追溯**：所有决策都有完整的Git提交记录

## 违规处理
违反同步协议的操作将被自动拒绝，确保数据完整性不受破坏。