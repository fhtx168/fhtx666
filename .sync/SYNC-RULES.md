# 跨通道同步规则（制度化版本）

## 📋 同步机制铁律

### 消息接收流程（所有通道必须遵守）
1. **第一步**：读取 `.sync/channel-sync.md` 同步日志
2. **第二步**：运行 `git log` 检查新提交  
3. **第三步**：检查当天 `memory/YYYY-MM-DD.md` 文件
4. **第四步**：确认同步完毕后才能回复用户

### 内容产出流程（所有通道必须遵守）
1. **任何通道产出内容** → 立即写入 `.sync/channel-sync.md`
2. **重要决策和讨论** → 同时保存到 `memory/YYYY-MM-DD.md`
3. **投资策略更新** → 写入 `MEMORY.md` 相关部分
4. **文件创建/修改** → 确保路径正确并记录到同步日志

## 🔒 双向同步铁律

- **绝不允许**出现"桌面端分析了七张底牌，微信端浑然不知"的情况
- **绝不允许**出现"微信端知道而桌面端不知道"的情况  
- **任何通道的操作都会被所有其他通道实时感知**
- **数据完整性优先**，宁可延迟回复也要确保同步准确
- **强制验证**：每次回复前必须确认已读取最新同步日志

## 📁 关键文件位置标准化

### 战略方案文件
- `[三到五年翻倍方案](file:///C:/Users/Admin/opcclawai/project/strategicimplementation/upgradedstrategywithseven_cards.md)`
- `[三十维框架v2.1](file:///C:/Users/Admin/opcclawai/project/skills/research-framework/framework-v2.1.md)`

### 执行计划文件  
- `[周执行计划](file:///C:/Users/Admin/opcclawai/project/strategicimplementation/weeklyexecution_plan.md)`
- `[今日交易记录](file:///C:/Users/Admin/opcclawai/project/portfolio/today_trades.md)`

### 监控保障文件
- `[市场监控仪表盘](file:///C:/Users/Admin/opcclawai/project/strategicimplementation/marketmonitoring_dashboard.md)`
- `[同步日志](file:///C:/Users/Admin/opcclawai/project/.sync/channel-sync.md)`

## ⏰ 自动化同步保障

### 实时更新机制
- **每日15:30**：自动监控数据更新到仪表盘文件
- **每次交易**：交易记录实时保存到today_trades.md  
- **方案调整**：任何优化立即反映在方案文件中
- **Git备份**：每小时自动提交，确保数据安全

### 监控与维护
- **每日心跳**：检查同步状态和文件完整性
- **异常报告**：发现同步异常立即报告用户
- **定期清理**：过期同步日志保留30天后自动清理
- **版本控制**：所有重要文件都有Git版本历史

## ✅ 质量保证措施

### 数据一致性验证
- 所有通道看到的方案 = 完全相同的文件内容
- 任何操作都会在所有通道产生相同的效果
- 文件修改会立即同步到所有访问点

### 用户体验保障  
- 无论在微信还是电脑上查看，信息完全一致
- 不会出现"失忆"或"丢数据"的情况
- 所有历史讨论和决策都有完整记录

## 🎯 执行纪律

### 严禁行为
- ❌ 在未读取同步日志的情况下回复用户
- ❌ 依赖临时上下文而不保存到持久化存储  
- ❌ 在不同通道提供不一致的信息
- ❌ 忽略同步异常或数据不一致问题

### 必须行为
- ✅ 每次会话启动时执行完整同步流程
- ✅ 重要信息立即写入持久化存储
- ✅ 发现问题立即报告并修复
- ✅ 定期验证同步机制的有效性

---
**最后更新**：2026-05-08
**生效状态**：✅ 立即生效
**监督机制**：用户可随时验证同步状态