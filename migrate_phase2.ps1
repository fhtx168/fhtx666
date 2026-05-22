# 第二阶段迁移脚本 - 彻底解决 C 盘问题
# 目标：C 盘 15.99 GB → 25+ GB

Write-Host "=== C 盘彻底清理（第二阶段）===" -ForegroundColor Cyan
Write-Host "目标：回收 10+ GB，达到 25+ GB 可用空间" -ForegroundColor Yellow
Write-Host ""

# 确认
$confirm = Read-Host "是否继续？(Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "已取消" -ForegroundColor Red
    exit
}

$freeBefore = [math]::Round((Get-PSDrive C).Free / 1GB, 2)
Write-Host "当前 C 盘剩余：$freeBefore GB" -ForegroundColor Cyan
Write-Host ""

# 1. 迁移 OneDrive
Write-Host "[1/6] 迁移 OneDrive..." -ForegroundColor Cyan
try {
    taskkill /f /im OneDrive.exe 2>$null
    Start-Sleep -Seconds 2
    
    if (Test-Path "C:\Users\Admin\OneDrive") {
        New-Item -ItemType Directory -Force -Path "E:\CloudSync\OneDrive" | Out-Null
        Move-Item "C:\Users\Admin\OneDrive\*" "E:\CloudSync\OneDrive\" -Force -ErrorAction SilentlyContinue
        Remove-Item "C:\Users\Admin\OneDrive" -Recurse -Force -ErrorAction SilentlyContinue
        cmd /c mklink /J "C:\Users\Admin\OneDrive" "E:\CloudSync\OneDrive" 2>$null
        Write-Host "  ✓ OneDrive 迁移完成" -ForegroundColor Green
    } else {
        Write-Host "  - OneDrive 不存在，跳过" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ⚠ OneDrive 迁移失败：$_" -ForegroundColor Red
}

# 2. 迁移 WPSDrive
Write-Host "`n[2/6] 迁移 WPSDrive..." -ForegroundColor Cyan
try {
    if (Test-Path "C:\Users\Admin\WPSDrive") {
        New-Item -ItemType Directory -Force -Path "E:\CloudSync\WPSDrive" | Out-Null
        Move-Item "C:\Users\Admin\WPSDrive\*" "E:\CloudSync\WPSDrive\" -Force -ErrorAction SilentlyContinue
        Remove-Item "C:\Users\Admin\WPSDrive" -Recurse -Force -ErrorAction SilentlyContinue
        cmd /c mklink /J "C:\Users\Admin\WPSDrive" "E:\CloudSync\WPSDrive" 2>$null
        Write-Host "  ✓ WPSDrive 迁移完成" -ForegroundColor Green
    } else {
        Write-Host "  - WPSDrive 不存在，跳过" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ⚠ WPSDrive 迁移失败：$_" -ForegroundColor Red
}

# 3. 迁移 msys64
Write-Host "`n[3/6] 迁移 msys64 (Git Bash)..." -ForegroundColor Cyan
try {
    if (Test-Path "C:\msys64") {
        New-Item -ItemType Directory -Force -Path "E:\DevTools\msys64" | Out-Null
        Write-Host "  移动 msys64 (约 0.31 GB)..." -ForegroundColor Yellow
        Move-Item "C:\msys64" "E:\DevTools\" -Force -ErrorAction SilentlyContinue
        cmd /c mklink /J "C:\msys64" "E:\DevTools\msys64" 2>$null
        Write-Host "  ✓ msys64 迁移完成" -ForegroundColor Green
    } else {
        Write-Host "  - msys64 不存在，跳过" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ⚠ msys64 迁移失败：$_" -ForegroundColor Red
}

# 4. 清理 Windows 日志
Write-Host "`n[4/6] 清理 Windows 系统日志..." -ForegroundColor Cyan
try {
    $logPaths = @(
        "C:\Windows\Logs\*.etl",
        "C:\Windows\Logs\CBS\*.log",
        "C:\Windows\Logs\WindowsUpdate\*.etl"
    )
    
    $cleanedSize = 0
    foreach ($path in $logPaths) {
        $files = Get-Item $path -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            $cleanedSize += $file.Length
            Remove-Item $file.FullName -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "  ✓ 清理日志：$([math]::Round($cleanedSize / 1MB, 2)) MB" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ 日志清理失败：$_" -ForegroundColor Red
}

# 5. 清理临时文件（再次）
Write-Host "`n[5/6] 清理临时文件..." -ForegroundColor Cyan
try {
    Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ 临时文件清理完成" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ 临时文件清理失败：$_" -ForegroundColor Red
}

# 6. 清空回收站
Write-Host "`n[6/6] 清空回收站..." -ForegroundColor Cyan
try {
    Clear-RecycleBin -Force -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "  ✓ 回收站已清空" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ 回收站清空失败：$_" -ForegroundColor Red
}

# 结果统计
Write-Host "`n=== 迁移完成 ===" -ForegroundColor Cyan
$freeAfter = [math]::Round((Get-PSDrive C).Free / 1GB, 2)
$recovered = [math]::Round($freeAfter - $freeBefore, 2)

Write-Host "C 盘空间：$freeBefore GB → $freeAfter GB (回收：$recovered GB)" -ForegroundColor Green
Write-Host ""

if ($freeAfter -ge 25) {
    Write-Host "🎉 目标达成！C 盘剩余 $freeAfter GB (≥25 GB)" -ForegroundColor Green
} elseif ($freeAfter -ge 20) {
    Write-Host "✅ 接近目标！C 盘剩余 $freeAfter GB (建议继续清理)" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  仍需清理：C 盘剩余 $freeAfter GB (建议迁移更多软件)" -ForegroundColor Red
}

Write-Host ""
Write-Host "下一步建议：" -ForegroundColor Cyan
Write-Host "1. 配置百度网盘同步（E:\CloudSync）" -ForegroundColor White
Write-Host "2. 检查 Program Files，卸载不用的软件" -ForegroundColor White
Write-Host "3. 评估云电脑扩容需求（如持续 <15 GB）" -ForegroundColor White
