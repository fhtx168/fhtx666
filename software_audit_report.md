# 云电脑软件检查报告 - 可卸载清单

**检查时间**：2026-05-22 08:27  
**C 盘剩余**：16.20 GB（安全 ✅）

---

## 📊 已安装软件总览

### 核心开发工具（保留 ✅）

| 软件 | 版本 | 大小 | 状态 |
|------|------|------|------|
| **Python 3.14.4** | 3.14.4150.0 | ~200 MB | ✅ 保留（开发必需） |
| **Node.js** | 25.2.1 | ~100 MB | ✅ 保留（开发必需） |
| **Visual Studio Community 2022** | 16.11.x | ~5 GB | ✅ 保留（开发工具） |
| **Windows SDK 10.1** | 10.1.19041.5609 | ~3 GB | ✅ 保留（VS 依赖） |
| **WSL** | 2.7.3.0 | ~500 MB | ✅ 保留（Linux 开发） |

---

### 办公软件（部分可卸载 ⚠️）

| 软件 | 版本 | 大小 | 建议 |
|------|------|------|------|
| **Microsoft Office 16** | 16.0.19929.x | ~2 GB | ✅ 保留（办公必需） |
| **WPS Office** | 未知 | ~500 MB | ⚠️ **与 Office 重复，可卸载** |
| **JHOfficeAI** | 未知 | ~100 MB | ⚠️ **金山办公 AI，不用可卸载** |
| **JHOfficeAIPlugin** | 未知 | ~50 MB | ⚠️ **JHOfficeAI 插件，可卸载** |
| **MOfficePlus** | 未知 | ~200 MB | ⚠️ **Office 插件，不用可卸载** |

---

### 云存储/同步（部分冗余 ⚠️）

| 软件 | 版本 | 大小 | 建议 |
|------|------|------|------|
| **Microsoft OneDrive** | 内置 | ~300 MB | ✅ 保留（已迁移 E 盘） |
| **Ecloud AI Assist** | 未知 | ~100 MB | ⚠️ **亿联云 AI，不用可卸载** |
| **EcloudDrive** | 未知 | ~200 MB | ⚠️ **亿联云盘，不用可卸载** |
| **百度网盘** | 未知 | ~300 MB | ✅ **保留（已启用同步）** |

---

### 安全软件（可能冗余 ⚠️）

| 软件 | 版本 | 大小 | 建议 |
|------|------|------|------|
| **Windows Defender** | 内置 | - | ✅ 保留（系统自带） |
| **360 安全卫士** | 未知 | ~500 MB | ⚠️ **与 Defender 重复，可卸载** |
| **PCAS** | 未知 | ~100 MB | ⚠️ **360 组件，可卸载** |
| **Tencent QQPCMgr** | 未知 | ~300 MB | ⚠️ **腾讯电脑管家，可卸载** |

---

### 输入法/浏览器（按需保留）

| 软件 | 版本 | 大小 | 建议 |
|------|------|------|------|
| **Sogou 输入法** | 未知 | ~200 MB | ⚠️ **如用 Windows 自带输入法可卸载** |
| **Internet Explorer** | 内置 | ~100 MB | ⚠️ **已淘汰，可禁用** |
| **LAV** | 未知 | ~50 MB | ⚠️ **音视频解码器，不用可卸载** |

---

### 虚拟化/云电脑组件（保留 ✅）

| 软件 | 版本 | 大小 | 建议 |
|------|------|------|------|
| **QEMU guest agent** | 4.2.0 | ~50 MB | ✅ 保留（云电脑必需） |
| **Virtio-win-driver** | 0.1.266 | ~100 MB | ✅ 保留（虚拟化驱动） |
| **vmtool** | 未知 | ~50 MB | ✅ 保留（VM 工具） |
| **Cloudbase-Init** | 1.1.0 | ~20 MB | ✅ 保留（云初始化） |

---

### 其他（清理 🗑️）

| 软件 | 版本 | 大小 | 建议 |
|------|------|------|------|
| **AlibabaProtect** | 未知 | ~100 MB | 🗑️ **阿里保护组件，不用可卸载** |
| **Windows App Certification Kit** | 10.1.19041.5609 | ~200 MB | 🗑️ **应用认证工具，非开发可卸载** |
| **Application Verifier** | 10.1.19041.5609 | ~50 MB | 🗑️ **调试工具，非开发可卸载** |
| **WinAppDeploy** | 10.1.19041.5609 | ~30 MB | 🗑️ **应用部署工具，非开发可卸载** |

---

## 🎯 推荐卸载清单（可回收 ~3-5 GB）

### P1 - 立即卸载（明显冗余）

```
1. 360 安全卫士（~500 MB）
   - 已有 Windows Defender，无需第三方杀毒
   
2. WPS Office（~500 MB）
   - 已有 Microsoft Office，功能重复
   
3. 腾讯电脑管家（~300 MB）
   - 与 360/Defender 重复
   
4. JHOfficeAI + 插件（~150 MB）
   - 金山办公 AI，不用可卸载
```

**小计**：~1.45 GB

---

### P2 - 建议卸载（按需）

```
5. Sogou 输入法（~200 MB）
   - 如习惯 Windows 自带输入法可卸载
   
6. Ecloud AI Assist + Drive（~300 MB）
   - 亿联云，如用百度网盘可卸载
   
7. LAV 解码器（~50 MB）
   - 如用 VLC/其他播放器可卸载
   
8. MOfficePlus（~200 MB）
   - Office 插件，不用可卸载
```

**小计**：~750 MB

---

### P3 - 开发工具清理（非开发可卸载）

```
9. Windows App Certification Kit（~200 MB）
10. Application Verifier（~50 MB）
11. WinAppDeploy（~30 MB）
12. Windows SDK 部分组件（~1 GB）
    - 如不做 Windows 应用开发可卸载
```

**小计**：~1.28 GB

---

### P4 - 可禁用（无需卸载）

```
- Internet Explorer（系统组件，建议禁用而非卸载）
- AlibabaProtect（如不用阿里软件可卸载）
```

---

## 📋 卸载步骤

### 方法 1：控制面板（推荐）

```
1. Win + R → appwiz.cpl
2. 找到目标软件
3. 右键 → 卸载
```

### 方法 2：PowerShell（批量）

```powershell
# 卸载 360 安全卫士
Get-Package *360* | Uninstall-Package -Force

# 卸载 WPS Office
Get-Package *WPS* | Uninstall-Package -Force

# 卸载腾讯电脑管家
Get-Package *QQPCMgr* | Uninstall-Package -Force
```

### 方法 3：Geek Uninstaller（推荐工具）

```
1. 下载 Geek Uninstaller（免费）
2. 强制删除顽固软件
3. 清理注册表残留
```

---

## ⚠️ 注意事项

### 不要卸载的软件

| 软件 | 原因 |
|------|------|
| **Python 3.14** | 开发环境必需 |
| **Node.js** | 开发环境必需 |
| **Visual Studio** | 开发工具核心 |
| **QEMU/Virtio** | 云电脑虚拟化驱动 |
| **Cloudbase-Init** | 云电脑初始化组件 |
| **Windows SDK** | VS 依赖，卸载会导致开发环境损坏 |
| **Microsoft .NET** | 系统框架，卸载会导致应用无法运行 |

### 谨慎卸载的软件

| 软件 | 说明 |
|------|------|
| **OneDrive** | 已迁移到 E 盘，卸载会影响同步 |
| **Windows Defender** | 卸载后系统将无实时防护 |
| **Internet Explorer** | 建议禁用而非卸载 |

---

## 📊 预期效果

| 类别 | 可回收空间 | 风险 |
|------|------------|------|
| **P1 - 立即卸载** | ~1.45 GB | ⭐ 低 |
| **P2 - 建议卸载** | ~750 MB | ⭐⭐ 中 |
| **P3 - 开发工具** | ~1.28 GB | ⭐⭐⭐ 高（如开发） |
| **总计** | **~3.5 GB** | - |

**卸载后 C 盘**：16.20 GB + 3.5 GB = **~20 GB**

---

## 🎯 建议执行顺序

### 今天（立即执行）
1. ✅ 卸载 360 安全卫士（如有其他安全软件）
2. ✅ 卸载 WPS Office（已有 Microsoft Office）
3. ✅ 卸载腾讯电脑管家

### 本周内
4. ⏳ 检查 JHOfficeAI/MOfficePlus 是否使用
5. ⏳ 检查 Sogou 输入法使用习惯
6. ⏳ 检查亿联云使用情况

### 本月内
7. ⏳ 评估开发工具需求
8. ⏳ 清理 Windows SDK 组件
9. ⏳ 禁用 Internet Explorer

---

## 🔍 百度网盘同步验证

**已启用** - 请确认以下文件夹已同步：

- [ ] `E:\CloudSync\OneDrive`
- [ ] `E:\CloudSync\WPSDrive`
- [ ] `E:\Users\Admin\Documents`
- [ ] `E:\Users\Admin\Desktop`
- [ ] `E:\opcclawai\project`

**检查方法**：
1. 打开百度网盘客户端
2. 进入"同步空间"
3. 确认上述文件夹在同步列表中
4. 检查同步状态（绿色✓表示正常）

---

**建议先卸载 P1 清单（360/WPS/腾讯管家），立即可回收 ~1.5 GB！** 🎉
