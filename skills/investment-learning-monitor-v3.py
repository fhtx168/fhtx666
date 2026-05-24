#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投研学习监测脚本 v3.0 - 简化搜索摘要版
用途：全网巡检（稳定第一，仅搜索摘要）
创建时间：2026-05-06 22:35
"""

import requests
from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
KNOWLEDGE_BASE = WORKSPACE / "knowledge-base"
LOG_FILE = WORKSPACE / "logs" / "investment-learning-v3.log"

# 监测平台（仅搜索摘要，稳定第一，不重试）
MONITOR_PLATFORMS = [
    # 核心层
    {"name": "微博 - 叶荣添", "search_url": "https://s.weibo.com/weibo/{keyword}", "keywords": ["叶荣添", "预见"]},
    {"name": "搜狗微信 - 叶荣添", "search_url": "https://weixin.sogou.com/weixin?type=2&query={keyword}", "keywords": ["叶荣添", "预见"]},
    # 优质层
    {"name": "B 站 - 叶荣添", "search_url": "https://search.bilibili.com/all?keyword={keyword}", "keywords": ["叶荣添"]},
    {"name": "今日头条 - 叶荣添", "search_url": "https://www.toutiao.com/search/?keyword={keyword}", "keywords": ["叶荣添"]},
    # 扩展层
    {"name": "抖音 - 叶荣添", "search_url": "https://www.douyin.com/search/{keyword}", "keywords": ["叶荣添"]},
    {"name": "知乎 - 叶荣添", "search_url": "https://www.zhihu.com/search?q={keyword}", "keywords": ["叶荣添"], "headers": {"Referer": "https://www.zhihu.com/"}},
]

# 严格限制：不重试，不强行抓取全文
MAX_RETRIES = 0  # 不重试
FETCH_FULL_TEXT = False  # 不强行 fetch 全文

# 算力监控配置
DAILY_EXEC_LIMIT = 50  # 单日执行上限
AUTO_THROTTLE_THRESHOLD = 0.5  # 失败率超 50% 自动降频

# ==================== 日志 ====================

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

# ==================== 搜索抓取 ====================

def search_platform(platform):
    """搜索平台，返回摘要"""
    name = platform["name"]
    search_url = platform["search_url"]
    keywords = platform["keywords"]
    
    results = []
    
    for keyword in keywords:
        url = search_url.format(keyword=keyword)
        log(f"搜索：{name} - {keyword}")
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
            # 添加平台特定 headers
            if platform.get("headers"):
                headers.update(platform["headers"])
            
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            
            if response.status_code == 200 and len(response.content) > 1000:
                log(f"  OK 成功，内容长度：{len(response.content)}")
                results.append({
                    "platform": name,
                    "keyword": keyword,
                    "url": url,
                    "content_length": len(response.content),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                log(f"  FAIL 失败，状态码：{response.status_code}", "WARN")
                
        except Exception as e:
            log(f"  ERROR 异常：{e}", "ERROR")
    
    return results

# ==================== 归档 ====================

def archive_search_result(result):
    """归档搜索结果到知识库"""
    category = "大佬观点" if "叶荣添" in result["platform"] else "板块逻辑"
    filename = f"search_{result['platform'].replace(' - ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = KNOWLEDGE_BASE / category / filename
    
    content = f"""# 搜索结果归档 - {result['platform']}

> 归档时间：{result['timestamp']}
> 关键词：{result['keyword']}
> 搜索 URL: {result['url']}
> 内容长度：{result['content_length']} 字节

---

## 说明

此文件为搜索结果摘要归档，详细内容请访问搜索 URL。

---

_投研学习系统 v3.0 - 稳定第一_
"""
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    log(f"  → 已归档：{filepath}")
    return filepath

# ==================== 主程序 ====================

def run_monitor():
    """执行监测"""
    log("=" * 60)
    log("投研学习监测脚本 v3.0 - 启动")
    log("=" * 60)
    
    all_results = []
    
    for platform in MONITOR_PLATFORMS:
        log("-" * 50)
        log(f"平台：{platform['name']}")
        log("-" * 50)
        
        results = search_platform(platform)
        for result in results:
            archive_search_result(result)
        all_results.extend(results)
    
    log("=" * 60)
    log(f"监测完成，共 {len(all_results)} 条结果")
    log("=" * 60)
    
    return all_results

# ==================== 入口 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("投研学习监测脚本 v3.0 - 简化搜索摘要版")
    print("=" * 60)
    
    try:
        results = run_monitor()
        print(f"\n[SUCCESS] 监测完成！共 {len(results)} 条结果")
    except Exception as e:
        print(f"\n[ERROR] 监测异常：{e}")
        import sys
        sys.exit(1)
