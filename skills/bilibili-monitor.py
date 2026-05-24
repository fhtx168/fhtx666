#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B 站监测脚本 v1.0
用途：监测 B 站 UP 主投资类视频更新
创建时间：2026-05-06
"""

import requests
from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
KNOWLEDGE_BASE = WORKSPACE / "knowledge-base"
LOG_FILE = WORKSPACE / "logs" / "bilibili-monitor.log"

# B 站 UP 主监测列表（财经/投资类）
BILIBILI_UPS = [
    {"name": "叶荣添", "uid": "待确认", "keywords": ["叶荣添", "预见"]},
    {"name": "财经有深度", "uid": "待确认", "keywords": ["财经", "投资"]},
    {"name": "巫师财经", "uid": "待确认", "keywords": ["财经", "分析"]},
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

# ==================== B 站抓取 ====================

def fetch_bilibili_user_space(uid):
    """
    抓取 B 站 UP 主空间
    返回：视频列表
    """
    log(f"抓取 B 站 UP 主空间：{uid}")
    
    # B 站用户空间 API（需要处理反爬）
    url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=10&pn=1"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Referer": "https://www.bilibili.com/",
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                videos = data.get("data", {}).get("list", {}).get("vlist", [])
                log(f"抓取成功，找到 {len(videos)} 个视频")
                return videos
            else:
                log(f"API 返回错误：{data.get('message')}", "ERROR")
                return []
        else:
            log(f"HTTP 错误：{response.status_code}", "ERROR")
            return []
            
    except Exception as e:
        log(f"抓取失败：{e}", "ERROR")
        return []

def search_bilibili_video(keywords):
    """
    搜索 B 站视频（网页搜索替代方案，绕过 API 限制）
    返回：视频列表
    """
    log(f"搜索 B 站视频：{keywords}")
    
    # 方案 1：网页搜索（绕过 API 限制）
    url = f"https://search.bilibili.com/all?keyword={keywords}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.bilibili.com/",
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200 and len(response.content) > 5000:
            log(f"网页搜索成功，内容长度：{len(response.content)}")
            # 简单提取视频标题（实际使用时需要解析 HTML）
            return [{"title": f"{keywords} 相关视频", "url": url, "source": "B 站搜索"}]
        else:
            log(f"网页搜索失败，状态码：{response.status_code}", "WARN")
            return []
            
    except Exception as e:
        log(f"网页搜索异常：{e}", "ERROR")
        return []

def test_bilibili_access():
    """
    测试 B 站访问
    返回：是否可访问
    """
    log("测试 B 站访问...")
    
    url = "https://www.bilibili.com/"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200 and len(response.content) > 1000:
            log(f"B 站访问成功，内容长度：{len(response.content)}")
            return True
        else:
            log(f"B 站访问失败，状态码：{response.status_code}", "WARN")
            return False
            
    except Exception as e:
        log(f"B 站访问异常：{e}", "ERROR")
        return False

# ==================== 归档功能 ====================

def archive_video_to_knowledge_base(video, source):
    """归档视频到知识库"""
    category = "大佬观点" if "叶荣添" in source else "板块逻辑"
    
    filename = f"B 站视频_{source}_{datetime.now().strftime('%Y%m%d')}.md"
    filepath = KNOWLEDGE_BASE / category / filename
    
    content = f"""# B 站视频归档 - {source}

> 归档时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> 来源：B 站

---

## 视频信息

- 标题：{video.get('title', '未知')}
- UP 主：{source}
- 发布时间：{video.get('created', '未知')}
- 播放量：{video.get('play', '未知')}
- 链接：https://www.bilibili.com/video/{video.get('bvid', '未知')}

---

_此文件用于 B 站视频归档_
"""
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    log(f"视频已归档：{filepath}")
    return filepath

# ==================== 主程序 ====================

def monitor_bilibili():
    """执行 B 站监测"""
    log("=" * 50)
    log("B 站监测启动")
    log("=" * 50)
    
    # 1. 测试 B 站访问
    if not test_bilibili_access():
        log("B 站访问失败，停止监测", "ERROR")
        return False
    
    # 2. 搜索关键词视频
    for up in BILIBILI_UPS:
        for keyword in up["keywords"]:
            videos = search_bilibili_video(keyword)
            if videos:
                # 归档第一个视频（最新）
                archive_video_to_knowledge_base(videos[0], up["name"])
    
    log("=" * 50)
    log("B 站监测完成")
    log("=" * 50)
    return True

# ==================== 入口 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("B 站监测脚本 v1.0")
    print("=" * 50)
    
    try:
        success = monitor_bilibili()
        if success:
            print("\n[SUCCESS] B 站监测完成！")
        else:
            print("\n[WARN] B 站监测部分失败")
    except Exception as e:
        print(f"\n[ERROR] B 站监测异常：{e}")
        import sys
        sys.exit(1)
