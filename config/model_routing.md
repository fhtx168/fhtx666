# 🧠 多模型路由配置

**版本**: 1.0  
**创建时间**: 2026-05-24  
**最后更新**: 2026-05-24

---

## 📌 路由策略

根据任务复杂度、所需能力、响应速度要求，自动选择最优模型。

---

## 🎯 模型能力矩阵

| 模型 | 推理能力 | 代码能力 | 中文理解 | 响应速度 | 成本 | 适用场景 |
|------|----------|----------|----------|----------|------|----------|
| **Qwen3.5-Plus** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 低 | 日常对话、中文内容、快速响应 |
| **Qwen3.5-Max** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 | 复杂推理、深度分析、长文本 |
| **Claude-Opus** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 高 | 代码生成、逻辑推理、英文内容 |
| **GPT-4o** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 高 | 多模态、图像理解、代码 |
| **Gemini-Ultra** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 高 | 长上下文、多模态 |
| **Codex** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中 | 纯代码任务 |

---

## 🔄 路由规则

### 按任务类型

| 任务类型 | 首选模型 | 备选模型 | 说明 |
|----------|----------|----------|------|
| **日常对话** | Qwen3.5-Plus | - | 快速响应，中文优化 |
| **投资分析** | Qwen3.5-Max | Claude-Opus | 需要深度推理 |
| **代码生成** | Claude-Opus | Codex | 代码质量优先 |
| **代码审查** | Qwen3.5-Plus | - | 快速反馈 |
| **文档撰写** | Qwen3.5-Max | - | 长文本连贯性 |
| **数据整理** | Qwen3.5-Plus | - | 结构化输出 |
| **图像理解** | GPT-4o | - | 多模态能力 |
| **K 线图分析** | GPT-4o | - | 视觉识别 |
| **财报图表** | GPT-4o | - | 图表解读 |
| **视频转录** | Qwen3.5-Plus | - | 中文语音识别 |
| **研报解析** | Qwen3.5-Max | - | 专业术语理解 |
| **产业链图谱** | Qwen3.5-Max | Claude-Opus | 复杂关系推理 |
| **量化回测** | Claude-Opus | Codex | 代码 + 逻辑 |
| **舆情分析** | Qwen3.5-Plus | - | 中文语义理解 |
| **微博监控** | Qwen3.5-Plus | - | 中文 + 快速 |
| **新闻扫描** | Qwen3.5-Plus | - | 中文 + 快速 |

---

### 按复杂度

| 复杂度 | 判断标准 | 模型选择 |
|--------|----------|----------|
| **简单** | 事实查询、数据提取、格式转换 | Qwen3.5-Plus |
| **中等** | 多步骤分析、对比评估、结构化输出 | Qwen3.5-Plus / Qwen3.5-Max |
| **复杂** | 深度推理、跨领域整合、创新方案 | Qwen3.5-Max / Claude-Opus |
| **极复杂** | 多智能体协作、长期规划、战略决策 | Qwen3.5-Max + Claude-Opus 协作 |

---

### 按时效性

| 时效要求 | 响应时间 | 模型选择 |
|----------|----------|----------|
| **实时** | <5 秒 | Qwen3.5-Plus |
| **快速** | <30 秒 | Qwen3.5-Plus |
| **标准** | <2 分钟 | Qwen3.5-Max |
| **深度** | <10 分钟 | Qwen3.5-Max / Claude-Opus |
| **过夜** | 无限制 | Qwen3.5-Max + Claude-Opus 协作 |

---

## ⚙️ 配置示例

### Cron 任务模型指定

```yaml
# 叶荣添微博监控 (简单任务)
model: qwen-portal/qwen3.5-plus
thinking: moderate
timeoutSeconds: 180

# 财经新闻扫描 (中等任务)
model: qwen-portal/qwen3.5-plus
thinking: moderate
timeoutSeconds: 240

# 深度投资分析报告 (复杂任务)
model: qwen-portal/qwen3.5-max
thinking: on
timeoutSeconds: 600

# 代码生成/回测 (代码任务)
model: anthropic/claude-opus
thinking: on
timeoutSeconds: 300
```

### sessions_spawn 模型指定

```yaml
# 简单子任务
runtime: subagent
model: qwen-portal/qwen3.5-plus

# 复杂分析任务
runtime: subagent
model: qwen-portal/qwen3.5-max

# ACP 编码任务
runtime: acp
agentId: anthropic/claude-opus
```

---

## 📊 成本优化策略

### 降级策略
当首选模型不可用或超时时：
1. Qwen3.5-Max → Qwen3.5-Plus
2. Claude-Opus → Qwen3.5-Max
3. GPT-4o → Qwen3.5-Plus

### 升级策略
当任务复杂度超出预期时：
1. Qwen3.5-Plus → Qwen3.5-Max (自动重试)
2. 单次失败 → 拆分任务 → 并行执行

### 批量任务优化
- 简单批量任务：使用 Qwen3.5-Plus 批量处理
- 复杂批量任务：拆分为子任务，使用 Qwen3.5-Max 并行

---

## 🎛️ 手动覆盖

用户可显式指定模型：
- "用更强模型分析" → Qwen3.5-Max
- "用 Claude 写代码" → Claude-Opus
- "快速回答" → Qwen3.5-Plus
- "用 GPT-4o 看图" → GPT-4o

---

## 📈 性能监控

### 指标追踪
- 任务完成率
- 平均响应时间
- 模型切换频率
- 成本/任务

### 优化循环
每周回顾：
1. 哪些任务频繁超时？→ 升级模型或优化 prompt
2. 哪些任务杀鸡用牛刀？→ 降级模型
3. 哪些任务反复失败？→ 拆分或更换方法

---

**文件位置**: `config/model_routing.md`  
**维护频率**: 每月回顾更新  
**负责人**: 飞鸿 + 福晶科技
