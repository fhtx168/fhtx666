#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B 站投资类 UP 主监测脚本
监控财经、投资、股市分析类 UP 主视频更新

数据源：B 站 API（无需登录，公开数据）
"""

import requests
import json
import os
from datetime import datetime

# ============ 配置区 ============
CONFIG = {
    # 监控的 UP 主列表（财经投资类）
    "uplords": [
        # 叶荣添相关
        {"name": "叶荣添", "uid": ""},  # 待补充 UID
        
        # 财经大 V（示例）
        {"name": "财经十一人", "uid": "123456"},
        {"name": "巫师财经", "uid": "123457"},
    ],
    
    # 监控关键词（用于搜索）
    "keywords": [
        "A 股分析",
        "大盘研判",
        "板块轮动",
        "投资策略",
        "股市复盘",
    ],
    
    # 输出目录
    "output_dir": "../../portfolio/research-knowledge-base/bilibili",
}

# ============ 核心函数 ============

def get_up_videos(uid, page_size=10):
    """
    获取 UP 主最新视频列表
    API: https://api.bilibili.com/x/space/arc/search
    """
    if not uid:
        print(f"[SKIP] UP 主 UID 为空，跳过")
        return []
    
    url = "https://api.bilibili.com/x/space/arc/search"
    params = {
        "mid": uid,
        "ps": page_size,
        "tid": 0,
        "pn": 1,
        "keyword": "",
        "order": "pubdate",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("code") == 0:
            videos = []
            for v in data["data"]["list"]["vlist"]:
                videos.append({
                    "title": v.get("title", ""),
                    "url": f"https://www.bilibili.com/video/av{v.get('aid', '')}",
                    "pub_date": datetime.fromtimestamp(v.get("created", 0)).strftime("%Y-%m-%d %H:%M"),
                    "duration": v.get("length", ""),
                    "view_count": v.get("play", 0),
                    "danmaku_count": v.get("video_review", 0),
                    "up_name": v.get("author", ""),
                    "up_uid": uid,
                })
            return videos
        else:
            print(f"[ERROR] API 返回错误：{data.get('message', '')}")
            return []
    
    except Exception as e:
        print(f"[ERROR] 获取 UP 主视频失败：{str(e)}")
        return []


def search_bilibili_videos(keyword, page=1):
    """
    搜索 B 站视频
    API: https://api.bilibili.com/x/web-interface/search/type
    """
    url = "https://api.bilibili.com/x/web-interface/search/type"
    params = {
        "search_type": "video",
        "keyword": keyword,
        "page": page,
        "order": "pubdate",  # 按发布时间排序
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("code") == 0:
            videos = []
            for v in data["data"]["result"]:
                videos.append({
                    "title": v.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", ""),
                    "url": f"https://www.bilibili.com/video/av{v.get('aid', '')}",
                    "pub_date": v.get("pubdate", ""),
                    "duration": v.get("duration", ""),
                    "view_count": v.get("play", 0),
                    "danmaku_count": v.get("video_review", 0),
                    "up_name": v.get("author", ""),
                    "up_uid": v.get("mid", 0),
                    "keyword": keyword,
                })
            return videos
        else:
            print(f"[ERROR] API 返回错误：{data.get('message', '')}")
            return []
    
    except Exception as e:
        print(f"[ERROR] 搜索视频失败：{str(e)}")
        return []


def save_to_knowledge_base(videos, category):
    """
    保存视频到知识库
    """
    output_dir = CONFIG["output_dir"]
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{category}_{datetime.now().strftime('%Y%m%d')}.json"
    filepath = os.path.join(output_dir, filename)
    
    # 如果文件已存在，合并旧数据
    existing = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    
    # 去重（基于 URL）
    existing_urls = {v.get("url") for v in existing}
    new_videos = [v for v in videos if v.get("url") not in existing_urls]
    
    # 合并并保存
    all_videos = existing + new_videos
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_videos, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 保存 {len(new_videos)} 个新视频到 {filepath}")
    return len(new_videos)


# ============ 主函数 ============

def main():
    print("=" * 60)
    print("B 站投资类 UP 主监测脚本")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    total_new = 0
    
    # 1. 监控指定 UP 主
    print("\n【1】监控 UP 主...")
    for up in CONFIG["uplords"]:
        print(f"  → UP 主：{up['name']} (UID: {up['uid']})")
        videos = get_up_videos(up["uid"])
        if videos:
            new_count = save_to_knowledge_base(videos, f"up_{up['name']}")
            total_new += new_count
            print(f"    找到 {len(videos)} 个，新增 {new_count} 个")
    
    # 2. 按关键词搜索
    print("\n【2】监控关键词...")
    for keyword in CONFIG["keywords"]:
        print(f"  → 搜索：{keyword}")
        videos = search_bilibili_videos(keyword)
        if videos:
            new_count = save_to_knowledge_base(videos, f"keyword_{keyword}")
            total_new += new_count
            print(f"    找到 {len(videos)} 个，新增 {new_count} 个")
    
    print("\n" + "=" * 60)
    print(f"[完成] 本次共新增 {total_new} 个视频")
    print("=" * 60)
    
    return total_new


if __name__ == "__main__":
    main()
