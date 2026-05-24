# WeChatFerry 快速安装指南

## 🎯 最简单方案

### 方案一：使用已有微信（推荐）⭐

如果你电脑上已经安装了微信，可以直接使用：

1. **查看微信版本**
   - 打开微信 → 左下角菜单 → 设置 → 关于微信
   - 查看版本号

2. **下载对应版本的 WeChatFerry**
   - 打开：https://github.com/lich0821/WeChatFerry/releases
   - 找到与你微信版本匹配的 WeChatFerry 版本
   - 下载 ZIP 文件

3. **版本对照表**
   | 微信版本 | WeChatFerry 版本 | 下载链接 |
   |---------|----------------|---------|
   | 3.9.10.27 | v39.2.4 | [下载](https://github.com/lich0821/WeChatFerry/releases) |
   | 3.9.9.43 | v39.2.0 | [下载](https://github.com/lich0821/WeChatFerry/releases) |
   | 3.9.8.25 | v39.1.0 | [下载](https://github.com/lich0821/WeChatFerry/releases) |

4. **解压并运行**
   - 解压到：`C:\Users\Admin\WeChatFerry`
   - 以管理员身份运行：`install.bat`
   - 启动微信
   - 运行：`python main.py`
   - 扫码登录

---

### 方案二：使用 OpenClaw 内置微信（当前可用）✅

**当前状态**：
- ✅ OpenClaw 微信插件已启用
- ✅ 配置：`C:\Users\Admin\.opcclaw\openclaw-weixin\`
- ⚠️ 当前是企业微信服务号模式

**临时使用方案**：
1. 继续使用当前 Web 聊天界面
2. 投研报告通过 Web 界面查看
3. 微信推送功能稍后配置

---

### 方案三：使用其他推送渠道

**立即可用的推送方式**：

#### 1. 邮件推送 ✅
- 配置 SMTP 服务器
- 推送报告到邮箱
- 稳定可靠

#### 2. 钉钉推送
- 创建钉钉机器人
- 配置 Webhook
- 免费稳定

#### 3. Telegram Bot
- 创建 Telegram Bot
- 配置 Token
- 需要网络环境

---

## 🔧 手动下载 WeChatFerry

### 步骤 1：打开 GitHub
访问：https://github.com/lich0821/WeChatFerry/releases

### 步骤 2：选择版本
- 点击"Releases"标签
- 选择最新版本（如 v39.2.4）
- 下载 `WeChatFerry.v39.2.4.zip`

### 步骤 3：解压
```
解压到：C:\Users\Admin\WeChatFerry
```

### 步骤 4：安装依赖
```bash
cd C:\Users\Admin\WeChatFerry
pip install -r requirements.txt
```

### 步骤 5：注入微信
```bash
# 以管理员身份运行
python install.py
```

### 步骤 6：启动
```bash
python main.py
```

---

## ⚠️ 当前问题

**自动下载失败原因**：
1. GitHub 需要网络代理
2. 版本号可能需要确认
3. 微信客户端未安装或版本不匹配

---

## 🎯 建议方案

**优先级**：

1. **继续使用 Web 界面**（立即可用）
   - 所有功能正常
   - 无需额外配置

2. **配置邮件推送**（5 分钟搞定）
   - 稳定可靠
   - 无需安装额外软件

3. **稍后配置 WeChatFerry**（需要时间研究）
   - 下载微信特定版本
   - 下载 WeChatFerry
   - 配置注入

---

## 📋 你现在可以

**请选择**：

1. **配置邮件推送** - 我帮你设置 SMTP，推送报告到邮箱
2. **继续使用 Web 界面** - 先配置投研系统，微信以后再说
3. **手动下载 WeChatFerry** - 你自己下载，我指导后续配置

请告诉我你的选择！🚀

---

**最后更新**: 2026-05-07 17:16
**状态**: 等待用户选择
