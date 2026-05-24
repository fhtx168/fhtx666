#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音财经类博主监测脚本
监控财经、投资、股市分析类博主视频更新

注意：抖音反爬较严，建议配合手动导入使用
"""

import requests
import json
import os
from datetime import datetime

# ============ 配置区 ============
CONFIG = {
    # 监控的博主列表（财经投资类）
    "creators": [
        # 示例格式（需要实际 sec_uid）
        # {"name": "叶荣添", "sec_uid": "MS4wLjABAAAA..."},
    ],
    
    # 监控关键词（用于搜索）
    "keywords": [
        "A 股分析",
        "大盘走势",
        "板块机会",
        "投资策略",
        "股市直播",
    ],
    
    # 输出目录
    "output_dir": "../../portfolio/research-knowledge-base/douyin",
    
    # 手动导入文件（兜底方案）
    "manual_import_file": "manual_import.json",
}

# ============ 核心函数 ============

def search_douyin_videos(keyword, count=10):
    """
    搜索抖音视频
    
    注意：抖音搜索需要登录 cookie，否则可能受限
    如无 cookie，返回空列表并提示手动导入
    """
    # 抖音搜索 API（需要登录态）
    url = "https://www.douyin.com/aweme/v1/web/general/search/single/"
    params = {
        "keyword": keyword,
        "count": count,
        "offset": 0,
        "search_channel": "aweme",
        "sort_type": "0",  # 综合排序
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.douyin.com",
        # 需要 cookie 才能正常访问
        # "Cookie": "your_cookie_here",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        # 检查是否需要登录
        if response.status_code == 403 or "登录" in response.text:
            print(f"[WARN] 需要登录 cookie，跳过自动搜索")
            print(f"  → 请使用手动导入方式（见下方说明）")
            return []
        
        data = response.json()
        
        videos = []
        # 根据实际 API 返回结构调整
        for v in data.get("data", []):
            videos.append({
                "title": v.get("desc", ""),
                "url": f"https://www.douyin.com/video/{v.get('aweme_id', '')}",
                "pub_date": datetime.fromtimestamp(v.get("create_time", 0)).strftime("%Y-%m-%d %H:%M"),
                "author": v.get("author", {}).get("nickname", ""),
                "like_count": v.get("statistics", {}).get("digg_count", 0),
                "comment_count": v.get("statistics", {}).get("comment_count", 0),
                "share_count": v.get("statistics", {}).get("share_count", 0),
                "keyword": keyword,
            })
        
        return videos
    
    except Exception as e:
        print(f"[WARN] 抖音搜索失败：{str(e)}")
        print(f"  → 建议使用手动导入方式")
        return []


def manual_import_videos():
    """
    手动导入视频（兜底方案）
    用户可以将抖音链接保存到 manual_import.json
    """
    filepath = os.path.join(CONFIG["output_dir"], CONFIG["manual_import_file"])
    
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            videos = json.load(f)
        print(f"[INFO] 手动导入 {len(videos)} 个视频")
        return videos
    except:
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
    print("抖音财经类博主监测脚本")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    total_new = 0
    
    # 1. 自动搜索（可能需要 cookie）
    print("\n【1】关键词搜索...")
    for keyword in CONFIG["keywords"]:
        print(f"  → 搜索：{keyword}")
        videos = search_douyin_videos(keyword)
        if videos:
            new_count = save_to_knowledge_base(videos, f"keyword_{keyword}")
            total_new += new_count
            print(f"    找到 {len(videos)} 个，新增 {new_count} 个")
    
    # 2. 手动导入（兜底）
    print("\n【2】手动导入...")
    manual_videos = manual_import_videos()
    if manual_videos:
        new_count = save_to_knowledge_base(manual_videos, "manual_import")
        total_new += new_count
        print(f"    导入 {len(manual_videos)} 个，新增 {new_count} 个")
    
    print("\n" + "=" * 60)
    print(f"[完成] 本次共新增 {total_new} 个视频")
    print("=" * 60)
    
    # 提示
    if total_new == 0:
        print("\n[提示] 自动搜索未获取到数据，建议使用手动导入方式")
        print(f"  手动导入文件：{os.path.join(CONFIG['output_dir'], CONFIG['manual_import_file'])}")
        print(f"  格式：[{{\"title\": \"标题\", \"url\": \"抖音链接\", \"author\": \"作者\"}}]")
    
    return total_new


if __name__ == "__main__":
    main()
