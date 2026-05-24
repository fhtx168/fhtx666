# WeChatFerry 安装指南

## 📥 第一步：安装微信客户端

### 需要版本
WeChatFerry 支持特定版本的微信，推荐：
- **微信版本**: 3.9.10.27 (最稳定)
- **下载地址**: https://github.com/lich0821/WeChatFerry/releases

### 安装步骤
1. 下载微信 3.9.10.27
2. 安装到默认路径：`C:\Program Files\Tencent\WeChat`
3. **不要启动微信**（先安装 WeChatFerry）

---

## 📥 第二步：安装 WeChatFerry

### 方法一：下载预编译版本（推荐）

1. **下载地址**
   - GitHub: https://github.com/lich0821/WeChatFerry/releases
   - 选择最新版本（如 v39.2.4）
   - 下载 `WeChatFerry.v39.2.4.zip`

2. **解压安装**
   ```
   解压到：C:\Users\Admin\WeChatFerry
   ```

3. **注入 DLL**
   - 以管理员身份运行：`C:\Users\Admin\WeChatFerry\install.bat`
   - 或手动复制 DLL 到微信目录

### 方法二：使用 OpenClaw 技能（如有）

检查是否有内置技能：
```bash
openclaw skills list | findstr wechat
```

---

## 🔧 第三步：配置 OpenClaw

### 修改配置文件

编辑 `C:\Users\Admin\.opcclaw\openclaw.json`：

```json
{
  "channels": {
    "openclaw-weixin": {
      "enabled": true,
      "mode": "wcf",  // 切换到 WeChatFerry 模式
      "wcf": {
        "host": "127.0.0.1",
        "port": 10086
      }
    }
  }
}
```

### 重启网关
```bash
openclaw gateway restart
```

---

## 📱 第四步：扫码登录

### 启动 WeChatFerry
```bash
cd C:\Users\Admin\WeChatFerry
python main.py
```

### 扫码
- 二维码会显示在终端
- 或保存到：`qrcode.png`
- 用微信扫描二维码

---

## 🧪 第五步：测试连接

### 发送测试消息
```bash
openclaw weixin send "测试消息"
```

### 检查状态
```bash
openclaw weixin status
```

---

## ⚠️ 注意事项

### 1. 版本匹配
WeChatFerry 版本必须与微信版本匹配：
| WeChatFerry | 微信版本 |
|-------------|---------|
| v39.2.4 | 3.9.10.27 |
| v39.2.0 | 3.9.9.43 |
| v39.1.0 | 3.9.8.25 |

### 2. 管理员权限
注入 DLL 需要管理员权限

### 3. 防封号风险
- 不要频繁发送消息
- 不要用于营销/骚扰
- 建议用小号测试

### 4. 依赖安装
```bash
pip install wechatferry
```

---

## 🚀 快速安装脚本

创建 `install-wcf.bat`：

```batch
@echo off
echo 正在安装 WeChatFerry...

REM 下载微信 3.9.10.27
echo 下载微信...
curl -L https://github.com/lich0821/WeChatFerry/releases/download/v39.2.4/WeChatSetup-3.9.10.27.exe -o %TEMP%\WeChatSetup.exe
%TEMP%\WeChatSetup.exe /S

REM 下载 WeChatFerry
echo 下载 WeChatFerry...
curl -L https://github.com/lich0821/WeChatFerry/releases/download/v39.2.4/WeChatFerry.v39.2.4.zip -o %TEMP%\wcf.zip
powershell -command "Expand-Archive -Path %TEMP%\wcf.zip -DestinationPath C:\Users\Admin\WeChatFerry"

REM 安装依赖
echo 安装 Python 依赖...
pip install wechatferry

echo 安装完成！
echo 请运行：cd C:\Users\Admin\WeChatFerry && python main.py
pause
```

---

## 📞 获取帮助

- GitHub Issues: https://github.com/lich0821/WeChatFerry/issues
- 文档：https://wechatferry.readthedocs.io/

---

**最后更新**: 2026-05-07
**状态**: 待安装
