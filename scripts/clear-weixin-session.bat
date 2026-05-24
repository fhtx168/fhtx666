@echo off
REM 微信 Session 每周清零脚本
REM 删除 openclaw-weixin 通道的所有会话文件

set SESSION_DIR=%APPDATA%\OpcClaw\openclaw\state\agents\main\sessions

echo [%date% %time%] 开始清理微信 session...

REM 查找并删除包含 weixin 的 session 文件
for %%f in ("%SESSION_DIR%\*.jsonl") do (
    findstr /i "weixin" "%%f" >nul 2>&1
    if not errorlevel 1 (
        echo 删除：%%f
        del "%%f"
    )
)

echo [%date% %time%] 微信 session 清理完成
echo.
