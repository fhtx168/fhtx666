# C 盘空间清理脚本
# 解决 0.24 GB/小时的异常消耗问题

Write-Host "=== C 盘空间检查 ===" -ForegroundColor Cyan
$freeGB = [math]::Round((Get-PSDrive C).Free / 1GB, 2)
Write-Host "C 盘剩余：$freeGB GB" -ForegroundColor $(if ($freeGB -lt 10) { 'Red' } else { 'Green' })

Write-Host "`n=== 清理临时文件 ===" -ForegroundColor Cyan

# 1. 清理用户临时文件
$tempPath = "$env:TEMP"
Write-Host "清理：$tempPath" -ForegroundColor Yellow
$beforeTemp = (Get-ChildItem $tempPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
Remove-Item "$tempPath\*" -Recurse -Force -ErrorAction SilentlyContinue
$afterTemp = (Get-ChildItem $tempPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$cleanedTemp = ($beforeTemp - $afterTemp) / 1GB
Write-Host "清理临时文件：$([math]::Round($cleanedTemp, 2)) GB" -ForegroundColor Green

# 2. 清理 npm 缓存
Write-Host "`n清理 npm 缓存..." -ForegroundColor Yellow
npm cache clean --force 2>$null

# 3. 清理 pip 缓存
Write-Host "清理 pip 缓存..." -ForegroundColor Yellow
pip cache purge 2>$null

# 4. 清空回收站
Write-Host "`n清空回收站..." -ForegroundColor Yellow
Clear-RecycleBin -Force -Confirm:$false

Write-Host "`n=== 清理完成 ===" -ForegroundColor Cyan
$afterGB = [math]::Round((Get-PSDrive C).Free / 1GB, 2)
Write-Host "C 盘剩余：$afterGB GB (回收：$([math]::Round($afterGB - $freeGB, 2)) GB)" -ForegroundColor Green

Write-Host "`n=== 建议操作 ===" -ForegroundColor Cyan
Write-Host "1. 检查 C:\Program Files (x86) 是否有不用的软件" -ForegroundColor White
Write-Host "2. 配置定时清理任务（每周执行此脚本）" -ForegroundColor White
Write-Host "3. 考虑扩容 C 盘或迁移数据到其他分区" -ForegroundColor White
