#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库清理脚本 v1.0
用途：自动清理重复、过时、无价值的冗余资讯
创建时间：2026-05-06
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
KNOWLEDGE_BASE = WORKSPACE / "knowledge-base"
HISTORY_ARCHIVE = WORKSPACE / "knowledge-base-history"
LOG_FILE = WORKSPACE / "logs" / "knowledge-cleanup.log"

# 清理规则配置
CLEANUP_CONFIG = {
    "duplicate_detection": {
        "enabled": True,
        "similarity_threshold": 0.85,  # 相似度阈值
        "keep_best_source": True,  # 保留最权威来源
    },
    "old_content_archive": {
        "enabled": True,
        "days_threshold": 30,  # 超过 30 天
        "preserve_long_term": True,  # 保留长期价值内容
    },
    "quality_assessment": {
        "enabled": True,
        "min_word_count": 100,  # 最少字数
        "require_logic": True,  # 要求有逻辑
        "require_data": False,  # 不强制要求数据
    },
    "preserve_categories": [
        "大盘逻辑",
        "板块思路",
        "选股观点",
        "风控要点",
        "政策解读",
        "大佬观点",
    ]
}

# ==================== 日志记录 ====================

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

# ==================== 重复检测 ====================

def calculate_file_hash(filepath):
    """计算文件哈希值"""
    with open(filepath, "rb") as f:
        content = f.read()
        return hashlib.md5(content).hexdigest()

def find_duplicates():
    """查找重复文件"""
    log("开始检测重复内容...")
    
    hash_map = {}
    duplicates = []
    
    for category in KNOWLEDGE_BASE.iterdir():
        if not category.is_dir():
            continue
        
        for file in category.glob("*.md"):
            file_hash = calculate_file_hash(file)
            
            if file_hash in hash_map:
                duplicates.append({
                    "file": str(file),
                    "duplicate_of": hash_map[file_hash],
                    "category": category.name
                })
                log(f"发现重复：{file.name}")
            else:
                hash_map[file_hash] = str(file)
    
    log(f"共发现 {len(duplicates)} 个重复文件")
    return duplicates

def keep_best_source(duplicates):
    """保留最权威来源"""
    # 权威度排序
    authority_rank = {
        "叶荣添": 1,
        "但斌": 2,
        "林园": 3,
        "中信证券": 4,
        "中金公司": 5,
        "财联社": 6,
    }
    
    for dup_group in duplicates:
        # TODO: 比较来源权威性，保留最好的
        pass

# ==================== 过时归档 ====================

def find_old_files(days=30):
    """查找超过指定天数的文件"""
    log(f"查找超过{days}天的文件...")
    
    old_files = []
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for category in KNOWLEDGE_BASE.iterdir():
        if not category.is_dir():
            continue
        
        # 跳过核心分类
        if category.name in CLEANUP_CONFIG["preserve_categories"]:
            log(f"跳过核心分类：{category.name}")
            continue
        
        for file in category.glob("*.md"):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime < cutoff_date:
                old_files.append({
                    "file": str(file),
                    "age_days": (datetime.now() - mtime).days,
                    "category": category.name
                })
    
    log(f"共发现 {len(old_files)} 个过期文件")
    return old_files

def has_long_term_value(filepath):
    """判断是否有长期价值"""
    # TODO: 实现长期价值判断逻辑
    # 1. 是否包含深度分析
    # 2. 是否有数据支撑
    # 3. 是否是重要事件记录
    return False

def archive_to_history(files):
    """归档到历史库"""
    log("开始归档过期文件...")
    
    for file_info in files:
        if has_long_term_value(file_info["file"]):
            log(f"保留长期价值文件：{file_info['file']}")
            continue
        
        src = Path(file_info["file"])
        dst = HISTORY_ARCHIVE / src.relative_to(KNOWLEDGE_BASE)
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        src.rename(dst)
        log(f"归档：{src.name} -> {dst}")

# ==================== 质量评估 ====================

def assess_quality():
    """评估内容质量"""
    log("开始质量评估...")
    
    low_quality = []
    
    for category in KNOWLEDGE_BASE.iterdir():
        if not category.is_dir():
            continue
        
        for file in category.glob("*.md"):
            quality_score = evaluate_file_quality(file)
            
            if quality_score < 60:  # 低于 60 分标记为低质
                low_quality.append({
                    "file": str(file),
                    "score": quality_score,
                    "reason": get_quality_issue_reason(quality_score)
                })
    
    log(f"共发现 {len(low_quality)} 个低质文件")
    return low_quality

def evaluate_file_quality(filepath):
    """评估单个文件质量"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    score = 100
    
    # 字数检查
    if len(content) < CLEANUP_CONFIG["quality_assessment"]["min_word_count"]:
        score -= 30
    
    # 逻辑检查（简化版：检查是否有结构化内容）
    if "##" not in content and "- " not in content:
        score -= 20
    
    # 数据检查
    if not any(char.isdigit() for char in content):
        score -= 10
    
    return max(0, score)

def get_quality_issue_reason(score):
    """获取质量问题原因"""
    if score < 40:
        return "内容过短且无结构"
    elif score < 60:
        return "内容质量较低"
    else:
        return "质量一般"

def mark_as_low_quality(files):
    """标记低质文件"""
    for file_info in files:
        filepath = Path(file_info["file"])
        # 添加低质标记
        with open(filepath, "r+", encoding="utf-8") as f:
            content = f.read()
            if "> 质量标记：低质" not in content:
                f.seek(0, 0)
                f.write("> 质量标记：低质\n\n" + content)
        log(f"标记低质：{filepath.name}")

# ==================== 清理报告 ====================

def generate_cleanup_report(duplicates, old_files, low_quality):
    """生成清理报告"""
    report_date = datetime.now().strftime("%Y%m%d")
    report_file = KNOWLEDGE_BASE / f"清理报告_{report_date}.md"
    
    content = f"""# 知识库清理报告_{report_date}

> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 清理统计

| 类型 | 数量 | 操作 |
|------|------|------|
| 重复内容 | {len(duplicates)} | 待处理 |
| 过时资讯 | {len(old_files)} | 待归档 |
| 低质内容 | {len(low_quality)} | 待标记 |

---

## 详细信息

### 重复内容
{chr(10).join(f"- {d['file']}" for d in duplicates)}

### 过时资讯
{chr(10).join(f"- {f['file']} ({f['age_days']}天)" for f in old_files)}

### 低质内容
{chr(10).join(f"- {l['file']} ({l['reason']})" for l in low_quality)}

---

_下次清理：{datetime.now() + timedelta(days=7):%Y-%m-%d}_
"""
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    log(f"清理报告已生成：{report_file}")
    return report_file

# ==================== 主程序 ====================

def cleanup_knowledge_base():
    """执行知识库清理"""
    log("=" * 50)
    log("知识库清理启动")
    log("=" * 50)
    
    # 1. 重复检测
    duplicates = find_duplicates()
    if duplicates:
        keep_best_source(duplicates)
    
    # 2. 过时归档
    old_files = find_old_files(days=30)
    if old_files:
        archive_to_history(old_files)
    
    # 3. 质量评估
    low_quality = assess_quality()
    if low_quality:
        mark_as_low_quality(low_quality)
    
    # 4. 生成报告
    generate_cleanup_report(duplicates, old_files, low_quality)
    
    log("=" * 50)
    log("知识库清理完成")
    log("=" * 50)

# ==================== 入口 ====================

if __name__ == "__main__":
    print("知识库清理脚本 v1.0")
    print("=" * 50)
    
    # 检查配置
    print(f"知识库目录：{KNOWLEDGE_BASE}")
    print(f"历史归档目录：{HISTORY_ARCHIVE}")
    print("=" * 50)
    
    # 执行清理
    cleanup_knowledge_base()
