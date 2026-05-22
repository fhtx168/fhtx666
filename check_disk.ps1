# 查找 C 盘大文件
$files = Get-ChildItem C:\ -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { $_.Length -gt 100MB } | 
    Sort-Object Length -Descending | 
    Select-Object -First 30

foreach ($f in $files) {
    $sizeMB = [math]::Round($f.Length / 1MB, 2)
    Write-Host "$sizeMB MB`t$($f.FullName)"
}

Write-Host "`n=== 大目录 ==="
$dirs = Get-ChildItem C:\ -Directory -ErrorAction SilentlyContinue
foreach ($d in $dirs) {
    try {
        $size = (Get-ChildItem $d.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        if ($size -gt 0) {
            $sizeGB = [math]::Round($size / 1GB, 2)
            if ($sizeGB -gt 0.5) {
                Write-Host "$sizeGB GB`t$($d.Name)"
            }
        }
    } catch {}
}
