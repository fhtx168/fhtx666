@echo off
REM Workspace Git Auto Backup - Windows 批处理版本
REM 工作日每小时执行，纯 Shell 零 LLM 消耗

REM 检查是否为工作日（1=周一，5=周五，6=周六，7=周日）
for /f %%a in ('wmic path win32_localtime get dayofweek /format:list ^| findstr "DayOfWeek"') do set /a "dow=%%a"
if %dow% geq 5 (
    echo [%date% %time%] Weekend - skipping backup
    exit /b 0
)

cd /d C:\Users\Admin\opcclawai\project

REM 检查是否有变更
git status --porcelain | findstr . >nul 2>&1
if %errorlevel% equ 0 (
    git add -A
    git commit -m "auto-backup %date% %time%"
    git push origin main
    echo [%date% %time%] Backup completed
) else (
    echo [%date% %time%] No changes to commit
)
