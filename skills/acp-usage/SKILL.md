---
name: acp-usage
description: |
  OpenClaw Agent 调用外部编码助手（Claude Code、Codex 等）的标准化流程。
  使用场景：(1) 用户要求写代码、创建项目、修复 bug (2) 需要多文件重构 (3) 复杂任务需要 ACP 执行。
  使用前必须读取 acp-router skill 获取意图检测和模式选择。
user-invocable: false
---

# acp-usage

调用外部编码助手（Claude Code 等）执行编码任务的标准化流程。

> **前置**：使用前必须先读取 `acp-router`和`acpx` skill 获取意图检测和模式选择。

---

## 1. 命令模板

### 1.1 ACP Runtime（sessions_spawn）

适用于 Discord/Telegram 持久会话。
备注：若使用ACP Runtime遇到配对问题请先使用命令`openclaw devices list`检查有没有未配对的设备。

```javascript
sessions_spawn({
  task: "任务描述（越详细越好，见第3节）",
  runtime: "acp",
  agentId: "claude",  // 或 codex, opencode 等
  thread: false,      // feishu 渠道必须 false
  mode: "run",        // run=一次性，session=持久
  runTimeoutSeconds: 180  // 根据复杂度调整
})
```

### 1.0.5 任务描述规范（强制）

**所有任务描述必须包含项目路径，格式：**
```
项目保存到：<当前agent的workspace目录>/<项目名>/
```

**示例（贪吃蛇游戏）：**
```
创建一个贪吃蛇网页游戏：
- 项目路径：<当前agent的workspace目录>/snake-game/
- 技术栈：HTML + CSS + JavaScript（单文件）
- 创建 CLAUDE.md 规范文件
- 游戏功能：蛇的移动、吃食物增长、碰撞检测、计分系统、键盘控制
- UI要求：渐变紫色主题、动画效果、最高分记录
```

**示例（React项目）：**
```
创建一个个人博客项目：
- 项目路径：<当前agent的workspace目录>/personal-blog/
- 技术栈：React + Vite + TailwindCSS
- 创建 CLAUDE.md 规范文件
- 功能：Markdown编辑器、草稿箱、标签管理、暗色模式
```

> **强制要求**：禁止将项目文件写到 /tmp/ 或其他非工作区目录

**⚠️ 启动后必须轮询并通知用户（强制）：**
```javascript
// 1. 启动后定期检查状态
sessions_list({ kinds: ["acp"], limit: 5 })

// 2. 检查 sessions 数组中的 status 字段：
// - status === "running" → 发送进度更新
// - status === "done" → 发送完成通知 + 预览方式
// - status === "error" → 发送错误摘要 + 建议
```

> **注意**：`process({ poll })` 是用于 exec 启动的 shell 进程，**不适用于 ACP 会话**。
> ACP 任务完成后系统会自动推送 `subagent_announce` 事件。

**会话管理**：
```javascript
sessions_list()                                    // 查看活跃会话
sessions_history({ sessionKey: "xxx" })           // 获取历史
sessions_send({ sessionKey: "xxx", message: "..." }) // 继续任务
subagents({ action: "kill", target: "xxx" })      // 终止
```

### 1.2 acpx CLI（exec + process）

适用于 Webchat 渠道。

```bash
# 1. 验证 acpx 可用
acpx --version

# 2. 执行任务
acpx --approve-all claude exec "任务描述"

# 3. 轮询结果（exec 返回 sessionId 时必须）
process({ action: "poll", sessionId: "<sessionId>", timeout: 600000 })

# 4. 轮询返回后通知用户（见下方通知模板）
```

**通知模板（强制）：**
- 进度更新："🔄 项目进行中：已完成 X/Y，..."
- 完成通知："✅ 项目已完成！\n启动：cd <项目路径> && npm run dev\n访问：http://localhost:5173"
- 失败通知："❌ 项目遇到问题：<错误摘要>\n建议：<下一步>"

> ⚠️ **禁止启动后沉默**：用户在等待时必须知道任务状态

**持久会话**：
```bash
acpx --approve-all claude sessions ensure --name <name>
acpx --approve-all claude -s <name> --approve-all "任务"
acpx --approve-all claude sessions close <name>
```

---

## 2. 超时建议

| 任务复杂度 | 超时 |
|-----------|------|
| 简单（单文件修改） | 60-120s |
| 中等（多文件功能） | 180-300s |
| 复杂（重构/新项目） | 300-600s |

---

## 3. 项目 CLAUDE.md 规范

每个项目根目录必须有 `CLAUDE.md`，作为项目的"大脑"。

### 初始化流程

```bash
# 1. 创建项目目录（建议在 agent workspace 下）
mkdir -p <当前agent的workspace目录>/project_name

# 2. 根据AGENTS.md的要求生成项目目录下面的CLAUDE.md（含有项目名、技术栈、命令等）用于指导claude code工作
```

### 强制注入规则

- 绝对禁止将密钥提交到代码库
- 所有对外暴露的函数必须包含类型定义
- **禁止执行 `npm run dev` 等阻塞命令**，避免 ACP 程序卡住

---

## 5. 故障自愈

| 错误类型 | 自愈流程 |
|----------|----------|
| 进程被终止/超时 | 检查改动状态 → 拆分为 RPI 工作流重新执行 |
| 会话异常 | sessions_list() → 清理无效会话 → 重新创建 |
| 权限错误 | 确认使用 --approve-all → 检查目录权限 |
| ACP Runtime卡住或者没有输出 | 切换acpx CLI来完成任务 |

**通用原则**：
- 最多重试 1 次
- 详细日志：`<当前agent的agentDir目录>/sessions/*.jsonl`
- 报告具体错误信息并请求人工介入

---

## 6. 路径速查

| 资源 | 路径 |
|------|------|
| acpx | `acpx` 或 `~/.npm-global/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx` |
| 日志 | `<当前agent的agentDir目录>/sessions/*.jsonl` |
| 项目 | `<当前agent的workspace目录>/<project_name>` |
