#!/bin/bash
# Workspace 自动 Git 备份脚本
# 工作日每小时执行，纯 Shell 零 LLM 消耗

set -e

cd /c/Users/Admin/opcclawai/project

# 检查是否有变更
if git status --porcelain | grep -q .; then
    git add -A
    git commit -m "auto-backup $(date '+%Y-%m-%d %H:%M')"
    git push origin main
    echo "[$(date)] Backup completed"
else
    echo "[$(date)] No changes to commit"
fi
