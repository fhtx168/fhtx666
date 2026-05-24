---
name: Wolfram Alpha数学科学计算
description: 使用 Wolfram Alpha 进行复杂数学计算、符号运算、科学问题求解。当用户需要"数学计算"、"公式求解"、"微积分"、"方程求解"、"科学计算"时，加载此 skill。
---

# Wolfram Alpha数学科学计算

使用 Wolfram Alpha 进行复杂数学和科学计算，共 **1 个工具**。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的计算任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。读取该文件并**仅使用 `mcp-wolfram-alpha-cloud` 对应的配置**。
- **调用工具**：`mcporter call mcp-wolfram-alpha-cloud.query_wolfram query="<问题>"`

---

## 快速使用

```
mcporter call mcp-wolfram-alpha-cloud.query_wolfram query="integrate x^2 from 0 to 3"
mcporter call mcp-wolfram-alpha-cloud.query_wolfram query="solve x^2 + 2x - 3 = 0"
mcporter call mcp-wolfram-alpha-cloud.query_wolfram query="population of China"
```

---

## 适用场景

- 复杂数学计算（微积分、线性代数、方程求解）
- 符号运算（化简、因式分解、展开）
- 科学查询（物理常数、化学元素、天文数据）
- 统计计算

---

## 注意事项

- 建议用**英文**输入问题，效果更好
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `mcp-wolfram-alpha-cloud` 对应的配置
