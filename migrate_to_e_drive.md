# C 盘迁移方案 - E 盘空间充足 (167 GB 可用)

## 可迁移的大文件/目录

### 1. 用户数据目录（优先级：高）
| 目录 | 预估大小 | 迁移难度 | 说明 |
|------|----------|----------|------|
| `C:\Users\Admin\Downloads` | 未知 | ⭐ 简单 | 下载文件，可安全迁移 |
| `C:\Users\Admin\Documents` | 未知 | ⭐ 简单 | 文档文件 |
| `C:\Users\Admin\Desktop` | 未知 | ⭐ 简单 | 桌面文件 |
| `C:\Users\Admin\OneDrive` | 未知 | ⭐⭐ 中等 | 云同步文件夹 |

### 2. 应用缓存（优先级：中）
| 目录 | 预估大小 | 迁移难度 | 说明 |
|------|----------|----------|------|
| `C:\Users\Admin\AppData\Local\OpcClaw` | ~0.13 GB | ⭐⭐ 中等 | OpenClaw 缓存 |
| `C:\Users\Admin\AppData\Local\Temp` | 动态 | ⭐ 简单 | 临时文件（定期清理即可） |
| `C:\Users\Admin\AppData\Local\node` | 未知 | ⭐⭐ 中等 | Node.js 缓存 |

### 3. 大型软件（优先级：低）
| 目录 | 大小 | 迁移难度 | 说明 |
|------|------|----------|------|
| `C:\Program Files (x86)` | 12.19 GB | ⭐⭐⭐ 困难 | 需重新安装或创建 junction |
| `C:\Program Files` | 9.02 GB | ⭐⭐⭐ 困难 | 需重新安装或创建 junction |
| `C:\msys64` | 0.31 GB | ⭐⭐ 中等 | Git Bash，可重新安装 |

### 4. 工作项目（优先级：中）
| 目录 | 大小 | 迁移难度 | 说明 |
|------|------|----------|------|
| `C:\Users\Admin\opcclawai` | 未知 | ⭐⭐ 中等 | Git 项目，可迁移 |
| `C:\Users\Admin\openclaw-cn` | 未知 | ⭐⭐ 中等 | Git 项目 |
| `C:\Users\Admin\WeChatFerry` | 未知 | ⭐⭐ 中等 | 微信相关 |

---

## 推荐迁移方案

### 方案 A：快速清理（推荐，回收 5-10 GB）
**迁移用户数据目录到 E 盘**

```powershell
# 1. 创建 E 盘目标目录
New-Item -ItemType Directory -Force -Path "E:\Users\Admin\Downloads"
New-Item -ItemType Directory -Force -Path "E:\Users\Admin\Documents"
New-Item -ItemType Directory -Force -Path "E:\Users\Admin\Desktop"

# 2. 移动文件（保留原目录结构）
Move-Item "C:\Users\Admin\Downloads\*" "E:\Users\Admin\Downloads\" -Force
Move-Item "C:\Users\Admin\Documents\*" "E:\Users\Admin\Documents\" -Force
Move-Item "C:\Users\Admin\Desktop\*" "E:\Users\Admin\Desktop\" -Force

# 3. 创建 junction 符号链接（保持兼容性）
cmd /c mklink /J "C:\Users\Admin\Downloads" "E:\Users\Admin\Downloads"
cmd /c mklink /J "C:\Users\Admin\Documents" "E:\Users\Admin\Documents"
cmd /c mklink /J "C:\Users\Admin\Desktop" "E:\Users\Admin\Desktop"
```

**优点**：
- 安全，不影响系统
- 应用程序无感知（junction 链接）
- 回收空间明显

---

### 方案 B：深度清理（回收 15-20 GB）
**迁移工作项目 + 应用缓存**

```powershell
# 1. 迁移 opcclawai 项目
New-Item -ItemType Directory -Force -Path "E:\opcclawai"
Move-Item "C:\Users\Admin\opcclawai\*" "E:\opcclawai\" -Force
cmd /c mklink /J "C:\Users\Admin\opcclawai" "E:\opcclawai"

# 2. 迁移 OpenClaw 缓存
Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
Move-Item "C:\Users\Admin\AppData\Local\OpcClaw" "E:\OpcClawCache" -Force
cmd /c mklink /J "C:\Users\Admin\AppData\Local\OpcClaw" "E:\OpcClawCache"
```

**注意**：需先关闭 OpenClaw Gateway

---

### 方案 C：彻底清理（回收 25+ GB）
**迁移大型软件（需重新安装）**

1. 卸载 `C:\Program Files (x86)` 中不用的软件
2. 重新安装到 E 盘
3. 或使用 junction 迁移整个目录

---

## 执行建议

**推荐顺序**：
1. 先执行 **方案 A**（用户数据，5-10 GB）
2. 观察效果，再决定是否执行 **方案 B**（工作项目，额外 5-10 GB）
3. 最后考虑 **方案 C**（大型软件，15+ GB）

**预计效果**：
- 方案 A：C 盘 7.72 GB → **15-20 GB**
- 方案 A+B：C 盘 7.72 GB → **20-30 GB**
- 方案 A+B+C：C 盘 7.72 GB → **35+ GB**

---

## 风险说明

| 风险 | 概率 | 缓解措施 |
|------|------|----------|
| junction 链接失效 | 低 | 备份原文件，测试后再删除 |
| 应用找不到缓存 | 低 | 使用 junction 保持路径不变 |
| Git 项目路径问题 | 中 | 迁移后重新配置 Git 仓库 |
| 系统不稳定 | 极低 | 不迁移系统目录 |

---

**建议**：先执行方案 A，测试效果后再决定是否继续。
