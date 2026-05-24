#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日持仓更新脚本
获取实时行情，计算盈亏，更新持仓文件
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# 持仓数据（从 holdings.md 提取）
A_SHARES = [
    {"name": "深南电路", "code": "SZ002916", "shares": 1000, "cost": 326.20},
    {"name": "长电科技", "code": "SH600584", "shares": 2000, "cost": 56.70},
    {"name": "中际旭创", "code": "SZ300308", "shares": 300, "cost": 679.99},
    {"name": "飞凯材料", "code": "SZ300398", "shares": 6900, "cost": 38.796},
    {"name": "宝丰能源", "code": "SH600989", "shares": 7000, "cost": 29.279},
    {"name": "拓维信息", "code": "SZ002261", "shares": 11900, "cost": 37.506},
    {"name": "埃斯顿", "code": "SZ002747", "shares": 2500, "cost": 18.758},
    {"name": "德赛西威", "code": "SZ002920", "shares": 5000, "cost": 111.893},
    {"name": "比亚迪", "code": "SZ002594", "shares": 30600, "cost": 87.07},
    {"name": "沪电股份", "code": "SZ002463", "shares": 5100, "cost": 74.66},
    {"name": "拓普集团", "code": "SH601689", "shares": 10000, "cost": 64.413},
    {"name": "中科曙光", "code": "SH603019", "shares": 9800, "cost": 83.172},
    {"name": "锡业股份", "code": "SZ000960", "shares": 6000, "cost": 37.804},
    {"name": "兴业银锡", "code": "SZ000426", "shares": 6000, "cost": 52.454},
    {"name": "中芯国际", "code": "SH688981", "shares": 9200, "cost": 114.557},
    {"name": "金诚信", "code": "SH603979", "shares": 7100, "cost": 70.345},
    {"name": "沪硅产业", "code": "SH688126", "shares": 17882, "cost": 20.464},
    {"name": "华海诚科", "code": "SH688535", "shares": 4753.76, "cost": 90.784},
    {"name": "中国巨石", "code": "SH600176", "shares": 10000, "cost": 18.766},
    {"name": "东阳光", "code": "SH600673", "shares": 10000, "cost": 28.1},
    {"name": "中石科技", "code": "SZ300684", "shares": 9500, "cost": 58.913},
    {"name": "胜宏科技", "code": "SZ300476", "shares": 2800, "cost": 286.942},
    {"name": "云南锗业", "code": "SZ002428", "shares": 8000, "cost": 3.886},
    {"name": "光库科技", "code": "SZ300620", "shares": 3600, "cost": 131.997},
    {"name": "中国铀业", "code": "SZ001280", "shares": 15900, "cost": 87.026},
    {"name": "东微半导", "code": "SH688261", "shares": 4000, "cost": 85.622},
    {"name": "英维克", "code": "SZ002837", "shares": 9800, "cost": 101.627},
    {"name": "阳光电源", "code": "SZ300274", "shares": 10000, "cost": 136.142},
    {"name": "福晶科技", "code": "SZ002222", "shares": 6600, "cost": 70.841},
    {"name": "兴森科技", "code": "SZ002436", "shares": 12000, "cost": 23.808},
    {"name": "康龙化成", "code": "SZ300759", "shares": 10000, "cost": 29.359},
    {"name": "科华数据", "code": "SZ002335", "shares": 10900, "cost": 62.117},
    {"name": "中兴通讯", "code": "SZ000063", "shares": 11300, "cost": 35.334},
    {"name": "中科创达", "code": "SZ300496", "shares": 3100, "cost": 57.579},
    {"name": "国电南瑞", "code": "SH600406", "shares": 26000, "cost": 24.138},
    {"name": "海南华铁", "code": "SH603300", "shares": 31600, "cost": 7.545},
    {"name": "通富微电", "code": "SZ002156", "shares": 28200, "cost": 49.003},
    {"name": "西藏珠峰", "code": "SH600338", "shares": 7800, "cost": 12.444},
    {"name": "华虹公司", "code": "SH688347", "shares": 2800, "cost": 124.967},
    {"name": "洛阳钼业", "code": "SH603993", "shares": 28000, "cost": 18.974},
    {"name": "西藏矿业", "code": "SZ000762", "shares": 8300, "cost": 25.674},
    {"name": "雄韬股份", "code": "SZ002733", "shares": 10000, "cost": 21.372},
    {"name": "华工科技", "code": "SZ000988", "shares": 13000, "cost": 76.308},
    {"name": "中国船舶", "code": "SH600150", "shares": 80000, "cost": 43.687},
    {"name": "神州数码", "code": "SZ000034", "shares": 5000, "cost": 44.177},
    {"name": "石英股份", "code": "SH603688", "shares": 10000, "cost": 37.37},
]

HK_SHARES = [
    {"name": "阿里巴巴-W", "code": "09988", "shares": 1300, "cost": 148.54},
    {"name": "云顶新耀", "code": "01952", "shares": 11000, "cost": 38.627},
    {"name": "晶泰控股", "code": "02228", "shares": 7000, "cost": 10.122},
    {"name": "小米集团-W", "code": "01810", "shares": 11600, "cost": 42.931},
    {"name": "迈富时", "code": "02556", "shares": 7800, "cost": 40.754},
    {"name": "锦欣生殖", "code": "01951", "shares": 207500, "cost": 2.584},
    {"name": "福寿园", "code": "01448", "shares": 79000, "cost": 2.989},
    {"name": "药明生物", "code": "02269", "shares": 10000, "cost": 11.944},
    {"name": "中国电力", "code": "02380", "shares": 80000, "cost": 3.573},
]

def get_a_share_quote(code):
    """获取 A 股实时行情"""
    exchange = "sz" if code.startswith("SZ") else "ss"
    symbol = code[2:]
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={exchange}.{symbol}&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f116,f60,f45,f52,f50,f48,f167,f117,f71,f113,f30,f124,f107,f104,f105,f140,f141,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f49,f53,f54,f55,f56,f59,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100,f101,f102,f103,f106,f108,f109,f110,f111,f112,f114,f115,f118,f119,f120,f121,f122,f123,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("data"):
            d = data["data"]
            return {
                "price": d.get("f2", 0),
                "change": d.get("f3", 0),
                "change_pct": d.get("f170", 0),
                "high": d.get("f44", 0),
                "low": d.get("f45", 0),
                "open": d.get("f46", 0),
                "prev_close": d.get("f60", 0),
                "volume": d.get("f47", 0),
                "amount": d.get("f48", 0),
            }
    except Exception as e:
        print(f"Error fetching {code}: {e}")
    return None

def get_hk_quote(code):
    """获取港股实时行情"""
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid=110.{code}&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f116,f60,f45,f52,f50,f48,f167,f117,f71,f113,f30,f124,f107,f104,f105,f140,f141,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f49,f53,f54,f55,f56,f59,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100,f101,f102,f103,f106,f108,f109,f110,f111,f112,f114,f115,f118,f119,f120,f121,f122,f123,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("data"):
            d = data["data"]
            return {
                "price": d.get("f2", 0),
                "change": d.get("f3", 0),
                "change_pct": d.get("f170", 0),
            }
    except Exception as e:
        print(f"Error fetching HK {code}: {e}")
    return None

def fetch_all_quotes():
    """获取所有持仓的实时行情"""
    print("Fetching A-share quotes...")
    a_results = {}
    for stock in A_SHARES:
        quote = get_a_share_quote(stock["code"])
        if quote:
            a_results[stock["code"]] = quote
            print(f"  {stock['name']}: {quote['price']:.2f} ({quote['change_pct']:+.2f}%)")
    
    print("\nFetching HK quotes...")
    hk_results = {}
    for stock in HK_SHARES:
        quote = get_hk_quote(stock["code"])
        if quote:
            hk_results[stock["code"]] = quote
            print(f"  {stock['name']}: {quote['price']:.2f} ({quote['change_pct']:+.2f}%)")
    
    return a_results, hk_results

def calculate_portfolio(a_quotes, hk_quotes):
    """计算持仓组合数据"""
    a_holdings = []
    hk_holdings = []
    
    total_a_market_value = 0
    total_hk_market_value = 0
    total_a_float_pnl = 0
    total_hk_float_pnl = 0
    
    # 处理 A 股
    for stock in A_SHARES:
        code = stock["code"]
        quote = a_quotes.get(code, {})
        price = quote.get("price", 0)
        change_pct = quote.get("change_pct", 0)
        
        if price > 0:
            market_value = price * stock["shares"]
            cost_value = stock["cost"] * stock["shares"]
            float_pnl = market_value - cost_value
            float_pnl_pct = (float_pnl / cost_value) * 100 if cost_value > 0 else 0
            
            a_holdings.append({
                "name": stock["name"],
                "code": code,
                "price": price,
                "change_pct": change_pct,
                "shares": stock["shares"],
                "cost": stock["cost"],
                "market_value": market_value,
                "float_pnl": float_pnl,
                "float_pnl_pct": float_pnl_pct,
            })
            total_a_market_value += market_value
            total_a_float_pnl += float_pnl
    
    # 处理港股
    for stock in HK_SHARES:
        code = stock["code"]
        quote = hk_quotes.get(code, {})
        price = quote.get("price", 0)
        change_pct = quote.get("change_pct", 0)
        
        if price > 0:
            market_value = price * stock["shares"]
            cost_value = stock["cost"] * stock["shares"]
            float_pnl = market_value - cost_value
            float_pnl_pct = (float_pnl / cost_value) * 100 if cost_value > 0 else 0
            
            hk_holdings.append({
                "name": stock["name"],
                "code": code,
                "price": price,
                "change_pct": change_pct,
                "shares": stock["shares"],
                "cost": stock["cost"],
                "market_value": market_value,
                "float_pnl": float_pnl,
                "float_pnl_pct": float_pnl_pct,
            })
            total_hk_market_value += market_value
            total_hk_float_pnl += float_pnl
    
    return {
        "a_holdings": a_holdings,
        "hk_holdings": hk_holdings,
        "total_a_market_value": total_a_market_value,
        "total_hk_market_value": total_hk_market_value,
        "total_a_float_pnl": total_a_float_pnl,
        "total_hk_float_pnl": total_hk_float_pnl,
    }

def generate_daily_tracking(data, date_str):
    """生成每日跟踪报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 找出异动股票（涨跌幅>=5%）
    big_gainers = [h for h in data["a_holdings"] + data["hk_holdings"] if h["change_pct"] >= 5]
    big_losers = [h for h in data["a_holdings"] + data["hk_holdings"] if h["change_pct"] <= -5]
    
    # 按今日盈亏排序
    sorted_by_pnl = sorted(data["a_holdings"], key=lambda x: x["float_pnl"], reverse=True)
    top_gainers = sorted_by_pnl[:5]
    top_losers = sorted_by_pnl[-5:]
    
    total_market_value = data["total_a_market_value"] + data["total_hk_market_value"]
    total_float_pnl = data["total_a_float_pnl"] + data["total_hk_float_pnl"]
    principal = 3148.44 * 10000  # 本金 3148.44 万
    cash = -59.79 * 10000  # 现金 -59.79 万
    total_assets = total_market_value + cash
    
    md = f"""# 每日持仓跟踪

## {today}（周三）收盘

### 📊 大盘概览
- 上证指数：待更新
- 深证成指：待更新  
- 创业板指：待更新
- 恒指：待更新
- 两市合计成交：待更新

### 📈 持仓总览
- **总资产**：{total_assets/10000:.2f}万
- **总市值**：{total_market_value/10000:.2f}万
- **A 股市值**：{data["total_a_market_value"]/10000:.2f}万
- **港股市值**：{data["total_hk_market_value"]/10000:.2f}万 HKD
- **现金**：{cash/10000:.2f}万（已使用融资）
- **本金**：3148.44 万
- **浮动盈亏**：{total_float_pnl/10000:.2f}万（{total_float_pnl/principal*100:.2f}%）
- **累计盈亏**：待计算

### A 股汇总
- 市值：{data["total_a_market_value"]/10000:.2f}万
- 浮动盈亏：{data["total_a_float_pnl"]/10000:.2f}万（{data["total_a_float_pnl"]/principal*100:.2f}%）

### 港股汇总
- 市值：{data["total_hk_market_value"]/10000:.2f}万 HKD
- 浮动盈亏：{data["total_hk_float_pnl"]/10000:.2f}万 HKD（{data["total_hk_float_pnl"]/(9*10000)*100:.2f}%）

---

### 🔥 今日异动标的（|涨跌幅| >= 5%）

#### 涨停 / 大涨
"""
    
    if big_gainers:
        md += "| 标的 | 代码 | 现价 | 涨跌幅 | 持仓市值 | 盈亏影响 |\n"
        md += "|------|------|------|--------|----------|----------|\n"
        for h in sorted(big_gainers, key=lambda x: x["change_pct"], reverse=True):
            pnl_impact = h["change_pct"] / 100 * h["market_value"]
            md += f"| {h['name']} | {h['code']} | {h['price']:.2f} | **{h['change_pct']:+.2f}%** | {h['market_value']/10000:.2f}万 | {pnl_impact/10000:+.2f}万 |\n"
    else:
        md += "无涨跌幅>=5% 的标的\n"
    
    md += "\n#### 大跌\n"
    if big_losers:
        md += "| 标的 | 代码 | 现价 | 涨跌幅 | 持仓市值 | 盈亏影响 |\n"
        md += "|------|------|------|--------|----------|----------|\n"
        for h in sorted(big_losers, key=lambda x: x["change_pct"]):
            pnl_impact = h["change_pct"] / 100 * h["market_value"]
            md += f"| {h['name']} | {h['code']} | {h['price']:.2f} | **{h['change_pct']:+.2f}%** | {h['market_value']/10000:.2f}万 | {pnl_impact/10000:+.2f}万 |\n"
    else:
        md += "无涨跌幅<=-5% 的标的\n"
    
    md += f"""
---

### 💰 今日盈亏前五

#### 盈利贡献
| 标的 | 持仓 | 浮动盈亏 | 盈亏率 |
|------|------|----------|--------|
"""
    for h in top_gainers:
        md += f"| {h['name']} | {h['shares']:.0f}股 | {h['float_pnl']/10000:.2f}万 | {h['float_pnl_pct']:+.2f}% |\n"
    
    md += "\n#### 亏损贡献\n"
    md += "| 标的 | 持仓 | 浮动盈亏 | 盈亏率 |\n"
    md += "|------|------|----------|--------|\n"
    for h in sorted(top_losers, key=lambda x: x["float_pnl"])[:5]:
        md += f"| {h['name']} | {h['shares']:.0f}股 | {h['float_pnl']/10000:.2f}万 | {h['float_pnl_pct']:+.2f}% |\n"
    
    md += f"""
---

### 📊 持仓明细（A 股 Top20 按市值）

| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 市值 | 浮动盈亏 |
|------|------|------|------|------|------|----------|
"""
    sorted_by_mv = sorted(data["a_holdings"], key=lambda x: x["market_value"], reverse=True)[:20]
    for h in sorted_by_mv:
        md += f"| {h['name']} | {h['code']} | {h['price']:.2f} | {h['change_pct']:+.2f}% | {h['shares']:.0f} | {h['market_value']/10000:.2f}万 | {h['float_pnl']/10000:.2f}万 |\n"
    
    md += f"""
---

### 📝 备注

- 数据截止：{today} 16:30
- 下次更新：明日 16:30
- 监控状态：✅ 正常

---

## 历史跟踪记录

| 日期 | 总资产 | 浮动盈亏 | 累计盈亏 | 备注 |
|------|--------|----------|----------|------|
| {today} | {total_assets/10000:.2f}万 | {total_float_pnl/10000:.2f}万 | 待计算 | 收盘更新 |
"""
    
    return md

def generate_holdings_md(data, date_str):
    """生成 holdings.md 文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    total_market_value = data["total_a_market_value"] + data["total_hk_market_value"]
    total_float_pnl = data["total_a_float_pnl"] + data["total_hk_float_pnl"]
    principal = 3148.44 * 10000
    cash = -59.79 * 10000
    total_assets = total_market_value + cash
    
    md = f"""# 持仓明细库

> 最后更新：{today} 收盘
> 总计：55 只（A 股 46 只 + 港股 9 只）

## 总览

| 指标 | 数值 |
|------|------|
| 总资产 | {total_assets/10000:.2f}万 |
| 总市值 | {total_market_value/10000:.2f}万 |
| 现金 | {cash/10000:.2f}万（已使用融资）|
| 本金 | 3148.44 万 |
| 浮动盈亏 | {total_float_pnl/10000:.2f}万（{total_float_pnl/principal*100:.2f}%）|
| 累计盈亏 | 待计算 |

### A 股
- 市值：{data["total_a_market_value"]/10000:.2f}万
- 浮动盈亏：{data["total_a_float_pnl"]/10000:.2f}万（{data["total_a_float_pnl"]/principal*100:.2f}%）

### 港股
- 市值：{data["total_hk_market_value"]/10000:.2f}万 HKD
- 浮动盈亏：{data["total_hk_float_pnl"]/10000:.2f}万 HKD

---

## A 股（46 只）

| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 成本 | 浮动盈亏 | 市值 |
|------|------|------|------|------|------|---------|------|
"""
    
    for h in sorted(data["a_holdings"], key=lambda x: x["market_value"], reverse=True):
        md += f"| {h['name']} | {h['code']} | {h['price']:.2f} | {h['change_pct']:+.2f}% | {h['shares']:.0f} | {h['cost']:.2f} | {h['float_pnl']/10000:.2f}万 | {h['market_value']/10000:.2f}万 |\n"
    
    md += f"""
---

## 港股（9 只）

| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 成本 | 浮动盈亏 | 市值 |
|------|------|------|------|------|------|---------|------|
"""
    
    for h in data["hk_holdings"]:
        md += f"| {h['name']} | {h['code']} | {h['price']:.2f} | {h['change_pct']:+.2f}% | {h['shares']:.0f} | {h['cost']:.2f} | {h['float_pnl']/10000:.2f}万 | {h['market_value']/10000:.2f}万 |\n"
    
    md += f"""
---

## 今日重点

### 涨幅榜（Top5）
"""
    top_gainers = sorted(data["a_holdings"], key=lambda x: x["change_pct"], reverse=True)[:5]
    for h in top_gainers:
        md += f"- **{h['name']}**: {h['change_pct']:+.2f}%\n"
    
    md += "\n### 跌幅榜（Top5）\n"
    top_losers = sorted(data["a_holdings"], key=lambda x: x["change_pct"])[:5]
    for h in top_losers:
        md += f"- **{h['name']}**: {h['change_pct']:+.2f}%\n"
    
    return md

def main():
    print("=" * 50)
    print("每日持仓更新脚本")
    print("=" * 50)
    
    # 获取实时行情
    a_quotes, hk_quotes = fetch_all_quotes()
    
    if not a_quotes and not hk_quotes:
        print("ERROR: Failed to fetch any quotes!")
        return
    
    # 计算组合数据
    portfolio_data = calculate_portfolio(a_quotes, hk_quotes)
    
    print(f"\nA 股市值：{portfolio_data['total_a_market_value']/10000:.2f}万")
    print(f"港股市值：{portfolio_data['total_hk_market_value']/10000:.2f}万 HKD")
    print(f"A 股浮盈：{portfolio_data['total_a_float_pnl']/10000:.2f}万")
    print(f"港股浮盈：{portfolio_data['total_hk_float_pnl']/10000:.2f}万 HKD")
    
    # 生成文件
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 更新 daily-tracking.md
    tracking_md = generate_daily_tracking(portfolio_data, today)
    tracking_path = Path("portfolio/daily-tracking.md")
    tracking_path.parent.mkdir(parents=True, exist_ok=True)
    tracking_path.write_text(tracking_md, encoding="utf-8")
    print(f"\n✅ Updated: {tracking_path}")
    
    # 更新 holdings.md
    holdings_md = generate_holdings_md(portfolio_data, today)
    holdings_path = Path("portfolio/holdings.md")
    holdings_path.write_text(holdings_md, encoding="utf-8")
    print(f"✅ Updated: {holdings_path}")
    
    # 生成推送摘要
    summary = generate_push_summary(portfolio_data, today)
    print("\n" + "=" * 50)
    print("推送摘要:")
    print(summary)
    
    # 保存推送摘要
    summary_path = Path("portfolio/push-summary.md")
    summary_path.write_text(summary, encoding="utf-8")
    print(f"\n✅ Saved push summary to: {summary_path}")

def generate_push_summary(data, date_str):
    """生成推送摘要"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    total_market_value = data["total_a_market_value"] + data["total_hk_market_value"]
    total_float_pnl = data["total_a_float_pnl"] + data["total_hk_float_pnl"]
    principal = 3148.44 * 10000
    cash = -59.79 * 10000
    total_assets = total_market_value + cash
    
    # 找出异动股票
    all_holdings = data["a_holdings"] + data["hk_holdings"]
    big_gainers = [h for h in all_holdings if h["change_pct"] >= 5]
    big_losers = [h for h in all_holdings if h["change_pct"] <= -5]
    
    summary = f"""📊 **持仓日报** ({today} 收盘)

【总资产】{total_assets/10000:.2f}万
【总市值】{total_market_value/10000:.2f}万
【浮动盈亏】{total_float_pnl/10000:.2f}万 ({total_float_pnl/principal*100:.2f}%)

🔥 今日异动:
"""
    
    if big_gainers:
        summary += "【大涨】" + "、".join([f"{h['name']}+{h['change_pct']:.1f}%" for h in sorted(big_gainers, key=lambda x: x['change_pct'], reverse=True)[:5]]) + "\n"
    
    if big_losers:
        summary += "【大跌】" + "、".join([f"{h['name']}{h['change_pct']:.1f}%" for h in sorted(big_losers, key=lambda x: x['change_pct'])[:5]]) + "\n"
    
    # 按市值排序的前 5
    top5 = sorted(data["a_holdings"], key=lambda x: x["market_value"], reverse=True)[:5]
    summary += "\n💰 持仓 Top5:\n"
    for h in top5:
        summary += f"- {h['name']}: {h['market_value']/10000:.1f}万 ({h['change_pct']:+.1f}%)\n"
    
    summary += "\n📁 详细数据已更新至 portfolio/daily-tracking.md"
    
    return summary

if __name__ == "__main__":
    main()
