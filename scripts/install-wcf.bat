@echo off
chcp 65001 >nul
echo ============================================================
echo WeChatFerry 自动安装脚本
echo ============================================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 需要管理员权限
    echo 请右键点击此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo [1/5] 检查 Python 安装...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

echo [2/5] 下载微信 3.9.10.27...
echo 下载地址：https://github.com/lich0821/WeChatFerry/releases/download/v39.2.4/WeChatSetup-3.9.10.27.exe
echo.
echo 提示：如果下载失败，请手动下载
echo 然后运行安装程序
echo.

REM 尝试下载（可能需要代理）
curl -L -o "%TEMP%\WeChatSetup-3.9.10.27.exe" "https://github.com/lich0821/WeChatFerry/releases/download/v39.2.4/WeChatSetup-3.9.10.27.exe" 2>nul
if %errorLevel% neq 0 (
    echo [警告] 自动下载失败，请手动下载
    echo 1. 打开：https://github.com/lich0821/WeChatFerry/releases
    echo 2. 下载 WeChatSetup-3.9.10.27.exe
    echo 3. 运行安装
    echo.
) else (
    echo 正在安装微信...
    "%TEMP%\WeChatSetup-3.9.10.27.exe" /S
    echo 微信安装完成
)
echo.

echo [3/5] 下载 WeChatFerry...
set WCF_DIR=C:\Users\Admin\WeChatFerry
if not exist "%WCF_DIR%" mkdir "%WCF_DIR%"

echo 下载地址：https://github.com/lich0821/WeChatFerry/releases/download/v39.2.4/WeChatFerry.v39.2.4.zip
echo.

curl -L -o "%TEMP%\wcf.zip" "https://github.com/lich0821/WeChatFerry/releases/download/v39.2.4/WeChatFerry.v39.2.4.zip" 2>nul
if %errorLevel% neq 0 (
    echo [警告] 自动下载失败，请手动下载
    echo 1. 打开：https://github.com/lich0821/WeChatFerry/releases
    echo 2. 下载 WeChatFerry.v39.2.4.zip
    echo 3. 解压到：%WCF_DIR%
    echo.
) else (
    echo 正在解压...
    powershell -command "Expand-Archive -Path '%TEMP%\wcf.zip' -DestinationPath '%WCF_DIR%' -Force"
    echo WeChatFerry 解压完成
)
echo.

echo [4/5] 安装 Python 依赖...
pip install wechatferry -q
if %errorLevel% neq 0 (
    echo [警告] 依赖安装失败，请手动运行：pip install wechatferry
) else (
    echo 依赖安装完成
)
echo.

echo [5/5] 配置 OpenClaw...
echo 配置文件：C:\Users\Admin\.opcclaw\openclaw.json
echo 需要手动修改配置，详见：scripts\install-wcf.md
echo.

echo ============================================================
echo 安装完成！
echo ============================================================
echo.
echo 下一步：
echo 1. 启动微信（如果未启动）
echo 2. 运行 WeChatFerry: cd %WCF_DIR% ^&^& python main.py
echo 3. 扫描二维码登录
echo 4. 修改 OpenClaw 配置
echo 5. 重启 OpenClaw: openclaw gateway restart
echo.
echo 详细指南：scripts\install-wcf.md
echo.
pause
