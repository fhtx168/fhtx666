#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投研学习周报生成脚本 v1.0
用途：每周日自动生成投研学习周报
创建时间：2026-05-06
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
KNOWLEDGE_BASE = WORKSPACE / "knowledge-base"
REPORT_DIR = KNOWLEDGE_BASE / "投研学习周报"
OUTPUT_DIR = WORKSPACE / "reports"

# ==================== 周报生成 ====================

def get_week_range():
    """获取本周日期范围"""
    today = datetime.now()
    # 本周日
    sunday = today - timedelta(days=today.weekday() + 1)
    # 下周六
    next_saturday = sunday + timedelta(days=6)
    return sunday.strftime("%Y-%m-%d"), next_saturday.strftime("%Y-%m-%d")

def count_knowledge_base_files():
    """统计知识库文件数量"""
    stats = {}
    categories = [
        "大盘趋势",
        "板块逻辑",
        "个股机会",
        "政策解读",
        "风控避雷",
        "大佬观点",
        "机构研报",
    ]
    
    total = 0
    for cat in categories:
        cat_dir = KNOWLEDGE_BASE / cat
        if cat_dir.exists():
            count = len(list(cat_dir.glob("*.md")))
            stats[cat] = count
            total += count
    
    stats["total"] = total
    return stats

def get_yerongtian_views():
    """获取叶荣添观点库内容"""
    yrt_file = KNOWLEDGE_BASE / "叶荣添观点库.md"
    
    if not yrt_file.exists():
        return "暂无数据"
    
    with open(yrt_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取最新观点
    if "七张底牌" in content:
        return "七张底牌已发布：硅光、大国芯片、国产芯片供应链、涨价之王、CPU 供应链、散热"
    else:
        return "持续跟踪中"

def generate_weekly_report():
    """生成周报"""
    week_start, week_end = get_week_range()
    stats = count_knowledge_base_files()
    yrt_views = get_yerongtian_views()
    
    report_date = datetime.now().strftime("%Y-%m-%d")
    week_num = datetime.now().isocalendar()[1]
    
    report_content = f"""# 投研学习周报 第{week_num}周（{week_start} 至 {week_end}）

> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> 系统版本：投研学习系统 v1.0

---

## 📊 本周学习统计

| 类别 | 归档数量 |
|------|----------|
| 大盘趋势 | {stats.get('大盘趋势', 0)} 篇 |
| 板块逻辑 | {stats.get('板块逻辑', 0)} 篇 |
| 个股机会 | {stats.get('个股机会', 0)} 篇 |
| 政策解读 | {stats.get('政策解读', 0)} 篇 |
| 风控避雷 | {stats.get('风控避雷', 0)} 篇 |
| 大佬观点 | {stats.get('大佬观点', 0)} 篇 |
| 机构研报 | {stats.get('机构研报', 0)} 篇 |
| **总计** | **{stats.get('total', 0)} 篇** |

---

## 一、大盘趋势研判

### 核心观点
- 上证指数：持续跟踪中
- 目标点位：待更新
- 时间窗口：待更新

### 大佬观点汇总

**叶荣添**：{yrt_views}

**但斌**：待更新

**林园**：待更新

### 综合判断
- 趋势方向：待更新
- 关键变量：待更新

---

## 二、热门板块逻辑

### 主线板块

| 板块 | 逻辑 | 大佬支持 | 持续性 |
|------|------|----------|--------|
| AI 算力 | 待更新 | 叶荣添 | 高 |
| 芯片半导体 | 待更新 | 叶荣添 | 高 |
| 光模块/硅光 | 待更新 | 叶荣添 | 高 |

### 轮动板块
- 待更新

---

## 三、个股机会提示

### 龙头股
| 股票 | 逻辑 | 目标价 | 风险 |
|------|------|--------|------|
| 待更新 | 待更新 | 待更新 | 待更新 |

### 潜力股
- 待更新

---

## 四、仓位节奏建议

### 总体仓位
- 建议：待更新成

### 加减仓时机
- 加仓：待更新
- 减仓：待更新

---

## 五、风控避雷要点

### 风险警示
- 待更新

### 避雷案例
- 待更新

---

## 六、后市关键预判

### 关键时点
- 待更新

### 关键事件
- 待更新

### 核心变量
- 待更新

---

## 📁 本周归档文件

_共归档 {stats.get('total', 0)} 份文件_

### 按类别查看
- 大盘趋势：{stats.get('大盘趋势', 0)} 份
- 板块逻辑：{stats.get('板块逻辑', 0)} 份
- 个股机会：{stats.get('个股机会', 0)} 份
- 政策解读：{stats.get('政策解读', 0)} 份
- 风控避雷：{stats.get('风控避雷', 0)} 份
- 大佬观点：{stats.get('大佬观点', 0)} 份
- 机构研报：{stats.get('机构研报', 0)} 份

---

## 📅 下周重点关注

1. 叶荣添七张底牌详细解读（5.17/5.24/5.31 分批分享）
2. 大盘上攻 4200 点情况
3. 一季报后主线确认
4. 量能变化情况

---

_本周学习归档：{stats.get('total', 0)} 份_  
_下周重点关注：七张底牌详细解读、4200 点上攻、量能变化_  
_生成系统：投研学习系统 v1.0_
"""
    
    # 保存周报
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORT_DIR / f"投研学习周报_第{week_num}周_{report_date}.md"
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"[OK] 周报已生成：{report_file}")
    return report_file

# ==================== 入口 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("投研学习周报生成脚本 v1.0")
    print("=" * 50)
    
    try:
        report_file = generate_weekly_report()
        print(f"\n[SUCCESS] 周报生成成功！")
        print(f"文件位置：{report_file}")
    except Exception as e:
        print(f"\n[ERROR] 周报生成失败：{e}")
        import sys
        sys.exit(1)
