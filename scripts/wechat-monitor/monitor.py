#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号监测脚本 - 搜狗微信搜索替代方案
无需官方 API，无需企业认证，直接可用

监控模式：关键词 + 公众号名称双监控
数据源：搜狗微信搜索 (weixin.sogou.com)
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# ============ 配置区 ============
CONFIG = {
    # 监控的公众号列表（财经大V）
    "accounts": [
        "叶荣添",
        "预见未来",
        "杨宁",
        "喜哥说财经", 
        "李大霄",
        "小小辛巴"
    ],
    
    # 监控关键词（投资相关）
    "keywords": [
        "A 股",
        "大盘研判", 
        "板块逻辑",
        "选股思路",
        "仓位策略",
        "杨宁观点",
        "喜哥分析",
        "李大霄策略",
        "小小辛巴价值投资"
    ],
    
    # 输出目录
    "output_dir": "../../portfolio/research-knowledge-base/wechat",
    
    # 是否启用代理（反爬用）
    "use_proxy": False,
}

# ============ 核心函数 ============

def search_wechat_articles(keyword, page=1):
    """
    搜狗微信搜索文章
    返回：文章列表 [{title, url, pub_date, account, summary}]
    
    注意：搜狗微信搜索反爬较严，可能需要验证码
    """
    url = "https://weixin.sogou.com/weixin"
    params = {
        "type": "2",  # 文章
        "query": keyword,
        "page": page,
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    
    try:
        print(f"    正在搜索：{keyword} ...")
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        # 检查是否触发反爬
        if response.status_code == 403:
            print(f"    [WARN] 触发反爬（403），需要验证码")
            return []
        
        if "验证码" in response.text or "antispider" in response.text:
            print(f"    [WARN] 触发验证码，请稍后重试或使用代理")
            return []
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # 尝试多种选择器
        for item in soup.select(".wx-rb2, .result-box-com"):
            title_elem = item.select_one(".wx-rb3 a, .title a")
            summary_elem = item.select_one(".txt-info, .summary")
            date_elem = item.select_one(".s2, .time")
            
            if title_elem:
                articles.append({
                    "title": title_elem.get_text(strip=True),
                    "url": title_elem.get("href", ""),
                    "summary": summary_elem.get_text(strip=True) if summary_elem else "",
                    "pub_date": date_elem.get_text(strip=True) if date_elem else "",
                    "keyword": keyword,
                })
        
        if not articles:
            print(f"    [WARN] 未解析到文章，可能页面结构变化")
        
        return articles
    
    except requests.exceptions.Timeout:
        print(f"    [ERROR] 请求超时，请稍后重试")
        return []
    except requests.exceptions.RequestException as e:
        print(f"    [ERROR] 网络错误：{str(e)}")
        return []
    except Exception as e:
        print(f"    [ERROR] 解析失败：{str(e)}")
        return []


def fetch_article_content(url):
    """
    抓取文章全文内容
    返回：{title, content, pub_date, author}
    """
    if not url:
        return None
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title = soup.select_one("#activity-name")
        title = title.get_text(strip=True) if title else "无标题"
        
        # 提取正文
        content_div = soup.select_one("#js_content")
        content = content_div.get_text(strip=True) if content_div else ""
        
        # 提取发布时间
        pub_date = soup.select_one("#publish_time")
        pub_date = pub_date.get_text(strip=True) if pub_date else ""
        
        # 提取作者
        author = soup.select_one("#js_name")
        author = author.get_text(strip=True) if author else ""
        
        return {
            "title": title,
            "content": content,
            "pub_date": pub_date,
            "author": author,
            "url": url,
        }
    
    except Exception as e:
        print(f"[ERROR] 抓取文章失败：{url} - {str(e)}")
        return None


def save_to_knowledge_base(articles, keyword):
    """
    保存文章到知识库
    """
    output_dir = CONFIG["output_dir"]
    os.makedirs(output_dir, exist_ok=True)
    
    # 按关键词分类保存
    filename = f"{keyword}_{datetime.now().strftime('%Y%m%d')}.json"
    filepath = os.path.join(output_dir, filename)
    
    # 如果文件已存在，合并旧数据
    existing = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    
    # 去重（基于 URL）
    existing_urls = {a.get("url") for a in existing}
    new_articles = [a for a in articles if a.get("url") not in existing_urls]
    
    # 合并并保存
    all_articles = existing + new_articles
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 保存 {len(new_articles)} 篇新文章到 {filepath}")
    return len(new_articles)


# ============ 主函数 ============

def main():
    print("=" * 60)
    print("微信公众号监测脚本 - 搜狗微信搜索")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    total_new = 0
    
    # 1. 按公众号名称搜索
    print("\n【1】监控公众号...")
    for account in CONFIG["accounts"]:
        print(f"  → 搜索：{account}")
        articles = search_wechat_articles(account)
        if articles:
            new_count = save_to_knowledge_base(articles, f"account_{account}")
            total_new += new_count
            print(f"    找到 {len(articles)} 篇，新增 {new_count} 篇")
    
    # 2. 按关键词搜索
    print("\n【2】监控关键词...")
    for keyword in CONFIG["keywords"]:
        print(f"  → 搜索：{keyword}")
        articles = search_wechat_articles(keyword)
        if articles:
            new_count = save_to_knowledge_base(articles, f"keyword_{keyword}")
            total_new += new_count
            print(f"    找到 {len(articles)} 篇，新增 {new_count} 篇")
    
    print("\n" + "=" * 60)
    print(f"[完成] 本次共新增 {total_new} 篇文章")
    print("=" * 60)
    
    return total_new


if __name__ == "__main__":
    main()
