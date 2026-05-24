# Workspace Git Auto Backup - PowerShell 版本
# 工作日每小时执行，纯 Shell 零 LLM 消耗

$ErrorActionPreference = "Stop"
Set-Location "C:\Users\Admin\opcclawai\project"

# 检查 Git 是否有变更
$status = git status --porcelain
if ($status) {
    git add -A
    git commit -m "auto-backup $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push origin main
    Write-Host "[$(Get-Date)] Backup completed"
} else {
    Write-Host "[$(Get-Date)] No changes to commit"
}
