# 模型配置优化方案

> 创建时间：2026-05-07 00:20  
> 状态：✅ 待飞鸿确认后执行  
> 依据：飞鸿提供的模型配置建议

---

## 📊 模型配置调整方案

### 核心改动（三条）

| 智能体 | 之前 | 现在 | 理由 |
|--------|------|------|------|
| **🦞 全能龙虾 (主)** | Qwen3.5-Plus | **DeepSeek-V4-Pro (360 免费)** | 100 万上下文，主会话不能寒酸 |
| **🧑‍💻 全栈工程师** | 默认 | **DeepSeek V4 Pro (官方)** | 代码质量要求高 |
| **🎨 UI 设计师** | 默认 | **Qwen3.5-Plus** | 界面设计够用就行 |

### 保持不变

| 智能体 | 模型 | 说明 |
|--------|------|------|
| **🦞 全能龙虾 (namiai)** | DeepSeek-V4-Pro | 不变 |
| **🧑‍🏫 专家教练** | DeepSeek-V4-Pro | 不变 |
| **🧪 测试工程师** | DeepSeek V4 Pro (官方) | 不变 |
| **💼 创业教练** | DeepSeek-V4-Pro (360 免费) | 100 万上下文够用 |
| **🧩 子代理** | DeepSeek V4 Pro (官方) | 子任务质量保障 |

---

## 🔧 需要添加的配置

### 1️⃣ DeepSeek-V4-Pro (360 免费)

**配置**：
```json
{
  "id": "deepseek-v4-pro-360",
  "name": "DeepSeek-V4-Pro (360 免费)",
  "provider": "360AI",
  "baseUrl": "https://ai.360.cn/api/v1",
  "contextWindow": 1000000,
  "maxTokens": 32768,
  "reasoning": true
}
```

**用途**：
- 全能龙虾 (主) - 主会话
- 创业教练

---

### 2️⃣ DeepSeek V4 Pro (官方)

**配置**：
```json
{
  "id": "deepseek-v4-pro-official",
  "name": "DeepSeek V4 Pro (官方)",
  "provider": "DeepSeek",
  "baseUrl": "https://api.deepseek.com/v1",
  "apiKey": "DEEPSEEK_API_KEY",
  "contextWindow": 128000,
  "maxTokens": 8192,
  "reasoning": true
}
```

**用途**：
- 全栈工程师
- 测试工程师
- 子代理

---

### 3️⃣ Qwen3.5-Plus (保留)

**配置**：保持不变

**用途**：
- UI 设计师
- 备用模型

---

## 📋 执行步骤

### 步骤 1：添加 360AI 提供商

需要 360AI API 密钥（如未配置）

### 步骤 2：更新 models.json

添加 DeepSeek-V4-Pro 配置

### 步骤 3：更新 agents 默认配置

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "360AI/deepseek-v4-pro-360",
      "fallbacks": ["Qwen/qwen3.5-plus"]
    }
  }
}
```

### 步骤 4：测试验证

- 主会话切换测试
- 代码任务测试
- UI 设计任务测试

---

## ⚠️ 注意事项

1. **360AI 密钥** - 需要确认是否已配置
2. **DeepSeek 密钥** - 已配置（`DEEPSEEK_API_KEY`）
3. **上下文限制** - 360 免费 100 万，官方 128k
4. **成本控制** - 360 免费，官方按量计费

---

## ✅ 预期效果

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 主会话上下文 | 180k | **1000k** (+455%) |
| 代码质量 | 默认 | **DeepSeek V4 Pro** |
| UI 设计 | 默认 | **Qwen3.5-Plus** (够用) |
| 子任务质量 | Qwen3.5-Plus | **DeepSeek V4 Pro** |

---

## 📝 待确认事项

**请飞鸿确认**：

1. ✅ 是否使用 360AI 免费 DeepSeek-V4-Pro？
2. ✅ 是否需要配置 360AI API 密钥？
3. ✅ 是否立即执行配置更新？

---

_创建时间：2026-05-07 00:20_  
_状态：待飞鸿确认_
