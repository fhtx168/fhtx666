---
name: dns-detection-repair
description: 诊断并修复 DNS 服务问题、DNS 解析问题、网页打开慢、网页打不开。当用户遇到与 DNS 相关的网络连接问题时使用此技能，例如网页打开缓慢、网站无法访问或 DNS 服务错误。
cn-name: DNS检测和修复
---

# DNS 检测与修复技能

本技能为 Windows 系统提供全面的 DNS 诊断和修复功能。

## 功能概述

诊断和修复与 DNS 相关的网络问题，包括 DNS 服务故障、解析问题、网页加载缓慢和网站无法访问。

## 使用场景

当用户报告以下情况时使用此技能：

- 网页加载缓慢或无法打开
- DNS 服务错误或故障
- 与 DNS 相关的网络连接问题
- 请求 DNS 检测和修复

## 使用方法

### 检测流程

1. **检查 DNS 服务状态**
   - 验证 DHCP 客户端服务是否正在运行
   - 验证 DNS 客户端服务是否正在运行

2. **检测 DNS 解析问题**
   - 测试 DNS 服务器响应能力
   - 测量 DNS 查询延迟
   - 检查解析失败情况

3. **分析网络连通性**
   - 测试网关连通性
   - 验证外部 DNS 服务器可达性

### 修复流程

当检测到 DNS 服务未正常运行时：

1. **尝试启动 DNS 服务**
   - 启动 DHCP 客户端服务
   - 启动 DNS 客户端服务
   - 设置服务为自动启动

2. **DNS 延迟修复**
   - 分析 DNS 响应时间
   - 提供优化建议

3. **提供手动修复建议**
   - 刷新 DNS 缓存 (`ipconfig /flushdns`)
   - 续订 IP 配置 (`ipconfig /renew`)
   - 建议使用备用 DNS 服务器（例如 114.114.114.114、8.8.8.8）

### 脚本使用

从 `./scripts/` 目录执行检测和修复脚本：

```bash
# 运行 DNS 检测
C:\360openclaw\skills\-root--openclaw-skills\skills\Python313\Python313\python.exe /mnt/c/360openclaw/skills/-root--openclaw-workspace-skills/skills/dns-detection-repair/scripts/dns_detect.py
```

```bash
# 运行 DNS 修复
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe Start-Process 'C:\360openclaw\skills\-root--openclaw-skills\skills\Python313\Python313\python.exe' 'C:\360openclaw\skills\-root--openclaw-workspace-skills\skills\dns-detection-repair\scripts\dns_repair.py' -Verb runAs
```

绿色版 `python.exe` 固定路径：
`C:\360openclaw\skills\-root--openclaw-skills\skills\Python313\Python313\python.exe`

## 打包资源

### 脚本 (`scripts/`)

- `dns_detect.py` - DNS 服务和解析检测脚本
- `dns_repair.py` - DNS 服务修复脚本
- `dns_utils.py` - DNS 操作的共享工具函数

## 输出格式

以结构化格式提供诊断结果：

- 服务状态（运行中/已停止）
- DNS 延迟测量
- 解析成功率/失败率
- 采取的修复操作
- 建议的后续步骤
