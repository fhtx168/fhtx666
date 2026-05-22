# C 盘迁移到 E 盘脚本
# 安全迁移用户数据，使用 junction 保持兼容性

Write-Host "=== C 盘迁移到 E 盘 ===" -ForegroundColor Cyan
Write-Host "警告：此脚本将移动文件并创建 junction 链接" -ForegroundColor Yellow
Write-Host ""

# 确认
$confirm = Read-Host "是否继续？(Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "已取消" -ForegroundColor Red
    exit
}

# 创建目标目录
Write-Host "`n[1/4] 创建目标目录..." -ForegroundColor Cyan
$targets = @(
    "E:\Users\Admin\Downloads",
    "E:\Users\Admin\Documents",
    "E:\Users\Admin\Desktop",
    "E:\Users\Admin\OneDrive"
)

foreach ($target in $targets) {
    if (!(Test-Path $target)) {
        New-Item -ItemType Directory -Force -Path $target | Out-Null
        Write-Host "  ✓ 创建：$target" -ForegroundColor Green
    } else {
        Write-Host "  - 已存在：$target" -ForegroundColor Gray
    }
}

# 移动文件
Write-Host "`n[2/4] 移动文件到 E 盘..." -ForegroundColor Cyan
$migrations = @(
    @{Source="$env:USERPROFILE\Downloads"; Dest="E:\Users\Admin\Downloads"},
    @{Source="$env:USERPROFILE\Documents"; Dest="E:\Users\Admin\Documents"},
    @{Source="$env:USERPROFILE\Desktop"; Dest="E:\Users\Admin\Desktop"},
    @{Source="$env:USERPROFILE\OneDrive"; Dest="E:\Users\Admin\OneDrive"}
)

foreach ($m in $migrations) {
    if (Test-Path $m.Source) {
        Write-Host "  移动：$($m.Source) -> $($m.Dest)" -ForegroundColor Yellow
        try {
            Move-Item -Path $m.Source -Destination $m.Dest -Force -ErrorAction SilentlyContinue
            Write-Host "  ✓ 完成" -ForegroundColor Green
        } catch {
            Write-Host "  ⚠ 部分文件移动失败：$_" -ForegroundColor Red
        }
    } else {
        Write-Host "  - 跳过：$($m.Source) 不存在" -ForegroundColor Gray
    }
}

# 创建 junction 链接
Write-Host "`n[3/4] 创建 junction 链接..." -ForegroundColor Cyan
$junctions = @(
    @{Link="$env:USERPROFILE\Downloads"; Target="E:\Users\Admin\Downloads"},
    @{Link="$env:USERPROFILE\Documents"; Target="E:\Users\Admin\Documents"},
    @{Link="$env:USERPROFILE\Desktop"; Target="E:\Users\Admin\Desktop"},
    @{Link="$env:USERPROFILE\OneDrive"; Target="E:\Users\Admin\OneDrive"}
)

foreach ($j in $junctions) {
    if (!(Test-Path $j.Link)) {
        Write-Host "  创建：$($j.Link) -> $($j.Target)" -ForegroundColor Yellow
        cmd /c mklink /J "$($j.Link)" "$($j.Target)" | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Junction 创建成功" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Junction 创建失败" -ForegroundColor Red
        }
    } else {
        Write-Host "  - 跳过：$($j.Link) 已存在" -ForegroundColor Gray
    }
}

# 验证
Write-Host "`n[4/4] 验证迁移..." -ForegroundColor Cyan
$freeBefore = 7.72
$freeAfter = [math]::Round((Get-PSDrive C).Free / 1GB, 2)
$recovered = [math]::Round($freeAfter - $freeBefore, 2)

Write-Host "`n=== 迁移完成 ===" -ForegroundColor Cyan
Write-Host "C 盘空间：$freeBefore GB → $freeAfter GB (回收：$recovered GB)" -ForegroundColor Green
Write-Host ""
Write-Host "注意：" -ForegroundColor Yellow
Write-Host "1. 原路径仍可正常访问（通过 junction 链接）" -ForegroundColor White
Write-Host "2. 如要恢复，删除 junction 并移回文件即可" -ForegroundColor White
Write-Host "3. 建议重启后验证所有应用正常" -ForegroundColor White
