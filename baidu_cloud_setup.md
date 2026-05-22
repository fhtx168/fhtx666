# 百度网盘同步配置指南

## 会员权益确认

**年度会员已激活** - 充分利用 2TB+ 同步空间

### 开通同步空间步骤

1. **打开百度网盘客户端**
2. **进入"同步空间"**（左侧菜单）
3. **开通同步空间**（会员免费）
4. **选择同步文件夹**

---

## 推荐同步配置

### 方案：智能分层同步

```
E:\CloudSync\
├── 01_Documents\          # 文档（实时同步）
│   ├── 工作文档\
│   ├── 个人资料\
│   └── 学习笔记\
│
├── 02_Projects\           # 项目代码（实时同步）
│   ├── opcclawai\
│   └── 其他项目\
│
├── 03_Desktop\            # 桌面（实时同步）
│   └── (桌面文件自动同步)
│
├── 04_Backup\             # 备份数据（每周手动）
│   ├── 系统备份\
│   ├── 数据归档\
│   └── 历史版本\
│
└── 05_Media\              # 媒体文件（选择性同步）
    ├── 照片\
    └── 视频\
```

---

## 自动同步脚本

### 每日备份到百度网盘

```powershell
# backup_to_baidu.ps1
# 每日自动备份重要数据到百度网盘

$sourcePaths = @(
    "E:\Users\Admin\Documents",
    "E:\Users\Admin\Desktop",
    "E:\opcclawai\project"
)

$backupDest = "E:\CloudSync\04_Backup\daily_$(Get-Date -Format 'yyyy-MM-dd')"

# 创建备份目录
New-Item -ItemType Directory -Force -Path $backupDest | Out-Null

# 复制文件
foreach ($src in $sourcePaths) {
    if (Test-Path $src) {
        $name = Split-Path $src -Leaf
        Copy-Item $src "$backupDest\$name" -Recurse -Force
        Write-Host "✓ 备份：$name"
    }
}

Write-Host "备份完成：$backupDest"
# 百度网盘会自动同步 E:\CloudSync 目录
```

---

## 百度网盘同步设置

### 1. 添加同步文件夹

打开百度网盘客户端 → 同步空间 → 添加同步文件夹：

| 本地路径 | 云端路径 | 同步模式 |
|---------|----------|----------|
| `E:\CloudSync\01_Documents` | `/同步空间/文档` | 双向同步 |
| `E:\CloudSync\02_Projects` | `/同步空间/项目` | 双向同步 |
| `E:\CloudSync\03_Desktop` | `/同步空间/桌面` | 双向同步 |
| `E:\CloudSync\04_Backup` | `/同步空间/备份` | 仅上传 |

### 2. 同步设置优化

**设置 → 传输**：
- [x] 启用智能带宽分配
- [x] 闲时全速传输（23:00-07:00）
- [ ] 限制上传速度（根据网络情况）

**设置 → 同步**：
- [x] 自动同步（实时）
- [x] 同步冲突时保留两个版本
- [x] 删除时先移动到回收站

---

## 自动化配置

### 创建定时任务（每日备份）

```powershell
# 创建每日备份任务
$action = New-ScheduledTaskAction `
  -Execute "PowerShell" `
  -Argument "-ExecutionPolicy Bypass -File `"C:\Users\Admin\opcclawai\project\backup_to_baidu.ps1`""

$trigger = New-ScheduledTaskTrigger `
  -Daily `
  -At 2am  # 凌晨 2 点备份

Register-ScheduledTask `
  -TaskName "BaiduCloud-Backup" `
  -Action $action `
  -Trigger $trigger `
  -RunLevel Highest `
  -Force
```

### 百度网盘自动启动

```powershell
# 添加到开机启动
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\百度网盘.lnk")
$shortcut.TargetPath = "C:\Program Files (x86)\Baidu\BaiduNetdisk\BaiduNetdisk.exe"
$shortcut.Save()
```

---

## 数据验证

### 每周检查清单

- [ ] 百度网盘同步正常（无冲突）
- [ ] 云端空间充足（<80% 使用率）
- [ ] 备份文件可访问
- [ ] 版本历史正常

### 恢复测试（每月一次）

1. 从云端下载一个测试文件
2. 验证文件完整性
3. 测试版本恢复功能

---

## 成本效益分析

### 年度会员价值

| 功能 | 免费版 | 会员版 | 价值 |
|------|--------|--------|------|
| 存储空间 | 2 TB | 5 TB+ | ¥200/年 |
| 同步空间 | ❌ | 2 TB | ¥100/年 |
| 传输速度 | 限速 | 全速 | ¥100/年 |
| 在线解压 | ❌ | ✅ | ¥50/年 |
| 版本历史 | 7 天 | 30 天 | ¥50/年 |
| **总价值** | - | - | **¥500/年** |

**你的成本**：已支付年度会员（约 ¥200-300）

**利用率**：
- 如不使用：浪费 ¥200-300/年
- 充分利用：节省 ¥500+（相当于免费 + 赚钱）

---

## 三层保护验证

### 数据安全性测试

```
测试场景 1：本地文件误删
→ E 盘 junction 仍保留
→ 百度网盘可恢复
→ 结果：✅ 安全

测试场景 2：E 盘故障
→ C 盘 junction 失效（可重建）
→ 百度网盘可恢复
→ 结果：✅ 安全

测试场景 3：云端账号问题
→ 本地 E 盘有完整数据
→ 云电脑不受影响
→ 结果：✅ 安全
```

---

## 下一步行动

### 立即执行（今天）
1. ✅ 运行 `migrate_phase2.ps1`（继续迁移）
2. ⏳ 打开百度网盘，开通同步空间
3. ⏳ 配置同步文件夹

### 本周内
1. ⏳ 测试同步功能
2. ⏳ 创建备份脚本
3. ⏳ 配置定时任务

### 本月内
1. ⏳ 评估云电脑扩容
2. ⏳ 完整恢复测试
3. ⏳ 文档化配置

---

**充分利用会员权益，建立三层数据保护！** 🛡️
