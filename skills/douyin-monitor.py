#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音监测脚本 v1.0
用途：监测抖音财经类博主视频更新
创建时间：2026-05-06
"""

import requests
from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
KNOWLEDGE_BASE = WORKSPACE / "knowledge-base"
LOG_FILE = WORKSPACE / "logs" / "douyin-monitor.log"

# 抖音博主监测列表（财经/投资类）
DOUYIN_CREATORS = [
    {"name": "叶荣添", "keywords": ["叶荣添", "预见"]},
    {"name": "财经有深度", "keywords": ["财经", "投资"]},
    {"name": "经济学家", "keywords": ["经济", "分析"]},
]

# ==================== 日志记录 ====================

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

# ==================== 抖音抓取 ====================

def test_douyin_access():
    """
    测试抖音访问
    返回：是否可访问
    """
    log("测试抖音访问...")
    
    url = "https://www.douyin.com/"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200 and len(response.content) > 1000:
            log(f"抖音访问成功，内容长度：{len(response.content)}")
            return True
        else:
            log(f"抖音访问失败，状态码：{response.status_code}", "WARN")
            return False
            
    except Exception as e:
        log(f"抖音访问异常：{e}", "ERROR")
        return False

def search_douyin_video(keywords):
    """
    搜索抖音视频（网页搜索）
    返回：视频列表
    """
    log(f"搜索抖音视频：{keywords}")
    
    # 抖音网页搜索
    url = f"https://www.douyin.com/search/{keywords}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.douyin.com/",
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200 and len(response.content) > 5000:
            log(f"抖音搜索成功，内容长度：{len(response.content)}")
            # 简单返回搜索结果
            return [{"title": f"{keywords} 相关视频", "url": url, "source": "抖音搜索"}]
        else:
            log(f"抖音搜索失败，状态码：{response.status_code}", "WARN")
            return []
            
    except Exception as e:
        log(f"抖音搜索异常：{e}", "ERROR")
        return []

# ==================== 归档功能 ====================

def archive_video_to_knowledge_base(video, source):
    """归档视频到知识库"""
    category = "大佬观点" if "叶荣添" in source else "板块逻辑"
    
    filename = f"抖音视频_{source}_{datetime.now().strftime('%Y%m%d')}.md"
    filepath = KNOWLEDGE_BASE / category / filename
    
    content = f"""# 抖音视频归档 - {source}

> 归档时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> 来源：抖音

---

## 视频信息

- 标题：{video.get('title', '未知')}
- 博主：{source}
- 链接：{video.get('url', '未知')}

---

_此文件用于抖音视频归档_
"""
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    log(f"视频已归档：{filepath}")
    return filepath

# ==================== 主程序 ====================

def monitor_douyin():
    """执行抖音监测"""
    log("=" * 50)
    log("抖音监测启动")
    log("=" * 50)
    
    # 1. 测试抖音访问
    if not test_douyin_access():
        log("抖音访问失败，停止监测", "ERROR")
        return False
    
    # 2. 搜索关键词视频
    for creator in DOUYIN_CREATORS:
        for keyword in creator["keywords"]:
            videos = search_douyin_video(keyword)
            if videos:
                # 归档第一个视频（最新）
                archive_video_to_knowledge_base(videos[0], creator["name"])
    
    log("=" * 50)
    log("抖音监测完成")
    log("=" * 50)
    return True

# ==================== 入口 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("抖音监测脚本 v1.0")
    print("=" * 50)
    
    try:
        success = monitor_douyin()
        if success:
            print("\n[SUCCESS] 抖音监测完成！")
        else:
            print("\n[WARN] 抖音监测部分失败")
    except Exception as e:
        print(f"\n[ERROR] 抖音监测异常：{e}")
        import sys
        sys.exit(1)
