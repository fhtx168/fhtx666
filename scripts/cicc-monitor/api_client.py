#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中金点晴 API 调用脚本
提供研报、宏观、行业、公司、市场等数据查询

API 文档：参考飞书文档
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.opcclaw/.env'))

# ============ 配置区 ============
CONFIG = {
    # API 端点（根据实际文档调整）
    "base_url": "https://cicc-api.example.com",  # 待确认
    
    # 认证信息
    "app_id": os.getenv("CICC_APP_ID"),
    "app_secret": os.getenv("CICC_APP_SECRET"),
    
    # 缓存配置
    "cache_dir": "../../portfolio/research-knowledge-base/cicc-cache",
    "cache_ttl": {
        "macro": 24 * 3600,      # 宏观数据 24 小时
        "industry": 12 * 3600,   # 行业数据 12 小时
        "company": 6 * 3600,     # 公司数据 6 小时
        "market": 5 * 60,        # 行情数据 5 分钟
        "research": 7 * 24 * 3600,  # 研报 7 天
    },
    
    # 调用限制
    "rate_limit": {
        "daily_quota": 1000,     # 日配额（待确认）
        "concurrent": 5,         # 并发数
    },
}

# ============ 认证 ============

def get_access_token():
    """
    获取访问令牌
    返回：access_token, expires_in
    """
    if not CONFIG["app_id"] or not CONFIG["app_secret"]:
        print("[ERROR] 未配置 CICC API 密钥")
        return None, 0
    
    # 注意：以下是示例代码，实际 API 端点和参数需要根据文档调整
    url = f"{CONFIG['base_url']}/oauth/token"
    data = {
        "app_id": CONFIG["app_id"],
        "app_secret": CONFIG["app_secret"],
        "grant_type": "client_credentials",
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        access_token = result.get("access_token")
        expires_in = result.get("expires_in", 3600)
        
        print(f"[INFO] 获取 access_token 成功，有效期 {expires_in}秒")
        return access_token, expires_in
    
    except Exception as e:
        print(f"[ERROR] 获取 token 失败：{str(e)}")
        return None, 0


# ============ 数据查询 ============

def get_research_reports(keyword="", industry="", date_range=None, limit=20):
    """
    获取研报列表
    
    参数：
    - keyword: 关键词
    - industry: 行业
    - date_range: 日期范围 [(start_date, end_date)]
    - limit: 返回数量限制
    
    返回：研报列表
    """
    access_token, _ = get_access_token()
    if not access_token:
        return []
    
    # 示例 API 调用（实际参数需根据文档调整）
    url = f"{CONFIG['base_url']}/research/reports"
    params = {
        "keyword": keyword,
        "industry": industry,
        "limit": limit,
    }
    
    if date_range:
        params["start_date"] = date_range[0]
        params["end_date"] = date_range[1]
    
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        reports = result.get("data", [])
        
        print(f"[INFO] 获取研报 {len(reports)} 篇")
        return reports
    
    except Exception as e:
        print(f"[ERROR] 获取研报失败：{str(e)}")
        return []


def get_macro_data(indicator="", date_range=None):
    """
    获取宏观经济数据
    
    参数：
    - indicator: 经济指标（GDP、CPI、PPI 等）
    - date_range: 日期范围
    
    返回：宏观数据
    """
    access_token, _ = get_access_token()
    if not access_token:
        return {}
    
    url = f"{CONFIG['base_url']}/macro/data"
    params = {
        "indicator": indicator,
    }
    
    if date_range:
        params["start_date"] = date_range[0]
        params["end_date"] = date_range[1]
    
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        data = result.get("data", {})
        
        print(f"[INFO] 获取宏观数据：{indicator}")
        return data
    
    except Exception as e:
        print(f"[ERROR] 获取宏观数据失败：{str(e)}")
        return {}


def get_company_info(stock_code=""):
    """
    获取公司基本信息
    
    参数：
    - stock_code: 股票代码
    
    返回：公司信息
    """
    access_token, _ = get_access_token()
    if not access_token:
        return {}
    
    url = f"{CONFIG['base_url']}/company/info"
    params = {
        "stock_code": stock_code,
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        info = result.get("data", {})
        
        print(f"[INFO] 获取公司信息：{stock_code}")
        return info
    
    except Exception as e:
        print(f"[ERROR] 获取公司信息失败：{str(e)}")
        return {}


def get_market_data(stock_code="", market_type="A"):
    """
    获取市场数据（行情、资金流向等）
    
    参数：
    - stock_code: 股票代码
    - market_type: 市场类型（A/H/US）
    
    返回：市场数据
    """
    access_token, _ = get_access_token()
    if not access_token:
        return {}
    
    url = f"{CONFIG['base_url']}/market/data"
    params = {
        "stock_code": stock_code,
        "market_type": market_type,
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        data = result.get("data", {})
        
        print(f"[INFO] 获取市场数据：{stock_code}")
        return data
    
    except Exception as e:
        print(f"[ERROR] 获取市场数据失败：{str(e)}")
        return {}


# ============ 缓存管理 ============

def save_to_cache(data, cache_key, category="research"):
    """
    保存数据到缓存
    """
    cache_dir = CONFIG["cache_dir"]
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")
    
    cache_data = {
        "data": data,
        "cached_at": datetime.now().isoformat(),
        "category": category,
    }
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 缓存已保存：{cache_file}")


def load_from_cache(cache_key, category="research"):
    """
    从缓存加载数据
    返回：data, is_expired
    """
    cache_dir = CONFIG["cache_dir"]
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")
    
    if not os.path.exists(cache_file):
        return None, True
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        cached_at = datetime.fromisoformat(cache_data["cached_at"])
        ttl = CONFIG["cache_ttl"].get(category, 3600)
        age = (datetime.now() - cached_at).total_seconds()
        
        is_expired = age > ttl
        
        return cache_data["data"], is_expired
    
    except:
        return None, True


# ============ 主函数 ============

def main():
    print("=" * 60)
    print("中金点晴 API 测试脚本")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 测试 1：获取 token
    print("\n【测试 1】获取 access_token...")
    token, expires = get_access_token()
    if token:
        print(f"  ✅ Token 获取成功，有效期 {expires}秒")
    else:
        print(f"  ❌ Token 获取失败")
        return
    
    # 测试 2：获取研报（示例）
    print("\n【测试 2】获取研报列表...")
    reports = get_research_reports(keyword="A 股策略", limit=5)
    if reports:
        print(f"  ✅ 获取 {len(reports)} 篇研报")
        for r in reports[:3]:
            print(f"    - {r.get('title', '无标题')}")
    else:
        print(f"  ❌ 研报获取失败（可能是 API 端点未配置）")
    
    # 测试 3：获取宏观数据（示例）
    print("\n【测试 3】获取宏观数据...")
    macro = get_macro_data(indicator="CPI")
    if macro:
        print(f"  ✅ 获取宏观数据成功")
    else:
        print(f"  ❌ 宏观数据获取失败（可能是 API 端点未配置）")
    
    print("\n" + "=" * 60)
    print("[完成] 测试结束")
    print("=" * 60)
    
    print("\n[提示] 如 API 端点未配置，请参考飞书文档更新 CONFIG['base_url']")


if __name__ == "__main__":
    main()
