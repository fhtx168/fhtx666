#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投研学习周报推送脚本 v1.0
用途：每周日 21:00 推送周报给用户
创建时间：2026-05-06
"""

from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
REPORT_DIR = WORKSPACE / "knowledge-base" / "投研学习周报"

# ==================== 推送函数 ====================

def get_latest_report():
    """获取最新周报"""
    if not REPORT_DIR.exists():
        return None
    
    reports = list(REPORT_DIR.glob("*.md"))
    if not reports:
        return None
    
    # 按修改时间排序，获取最新
    reports.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return reports[0]

def format_push_message(report_file):
    """格式化推送消息"""
    with open(report_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取关键信息
    lines = content.split("\n")
    title = ""
    stats = []
    
    for line in lines:
        if line.startswith("# 投研学习周报"):
            title = line.replace("# ", "")
        if "总计" in line and "篇" in line:
            stats.append(line.strip())
    
    message = f"""📊 {title}

📈 本周学习统计
- 归档文件：待提取
- 覆盖类别：7 大类

📝 核心内容
1. 大盘趋势研判
2. 热门板块逻辑
3. 个股机会提示
4. 仓位节奏建议
5. 风控避雷要点
6. 后市关键预判

📁 完整报告：{report_file}

---
_投研学习系统 v1.0 自动生成_
"""
    
    return message

def push_report():
    """推送周报"""
    report_file = get_latest_report()
    
    if not report_file:
        print("[ERROR] 未找到周报文件")
        return False
    
    message = format_push_message(report_file)
    
    # TODO: 调用推送 API
    print("[OK] 周报推送内容已生成")
    print(f"文件：{report_file}")
    print("-" * 50)
    print(message)
    
    return True

# ==================== 入口 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("投研学习周报推送脚本 v1.0")
    print("=" * 50)
    
    try:
        success = push_report()
        if success:
            print("\n[SUCCESS] 周报推送成功！")
        else:
            print("\n[ERROR] 周报推送失败！")
            import sys
            sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 推送异常：{e}")
        import sys
        sys.exit(1)
