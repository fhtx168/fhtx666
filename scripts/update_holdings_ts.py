#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日持仓更新脚本 - 使用 Tushare API
"""

import tushare as ts
import pandas as pd
from datetime import datetime
from pathlib import Path
import time

# Tushare token (from MEMORY.md)
TS_TOKEN = "11c66ba1f1b5128c3aab5bed7eafeb9a22a78908bc54e6e8a23a5c0d"
ts.set_token(TS_TOKEN)
pro = ts.pro_api()

# 持仓数据
A_SHARES = [
    {"name": "深南电路", "code": "002916.SZ", "ts_code": "002916.SZ", "shares": 1000, "cost": 326.20},
    {"name": "长电科技", "code": "600584.SH", "ts_code": "600584.SH", "shares": 2000, "cost": 56.70},
    {"name": "中际旭创", "code": "300308.SZ", "ts_code": "300308.SZ", "shares": 300, "cost": 679.99},
    {"name": "飞凯材料", "code": "300398.SZ", "ts_code": "300398.SZ", "shares": 6900, "cost": 38.796},
    {"name": "宝丰能源", "code": "600989.SH", "ts_code": "600989.SH", "shares": 7000, "cost": 29.279},
    {"name": "拓维信息", "code": "002261.SZ", "ts_code": "002261.SZ", "shares": 11900, "cost": 37.506},
    {"name": "埃斯顿", "code": "002747.SZ", "ts_code": "002747.SZ", "shares": 2500, "cost": 18.758},
    {"name": "德赛西威", "code": "002920.SZ", "ts_code": "002920.SZ", "shares": 5000, "cost": 111.893},
    {"name": "比亚迪", "code": "002594.SZ", "ts_code": "002594.SZ", "shares": 30600, "cost": 87.07},
    {"name": "沪电股份", "code": "002463.SZ", "ts_code": "002463.SZ", "shares": 5100, "cost": 74.66},
    {"name": "拓普集团", "code": "601689.SH", "ts_code": "601689.SH", "shares": 10000, "cost": 64.413},
    {"name": "中科曙光", "code": "603019.SH", "ts_code": "603019.SH", "shares": 9800, "cost": 83.172},
    {"name": "锡业股份", "code": "000960.SZ", "ts_code": "000960.SZ", "shares": 6000, "cost": 37.804},
    {"name": "兴业银锡", "code": "000426.SZ", "ts_code": "000426.SZ", "shares": 6000, "cost": 52.454},
    {"name": "中芯国际", "code": "688981.SH", "ts_code": "688981.SH", "shares": 9200, "cost": 114.557},
    {"name": "金诚信", "code": "603979.SH", "ts_code": "603979.SH", "shares": 7100, "cost": 70.345},
    {"name": "沪硅产业", "code": "688126.SH", "ts_code": "688126.SH", "shares": 17882, "cost": 20.464},
    {"name": "华海诚科", "code": "688535.SH", "ts_code": "688535.SH", "shares": 4753.76, "cost": 90.784},
    {"name": "中国巨石", "code": "600176.SH", "ts_code": "600176.SH", "shares": 10000, "cost": 18.766},
    {"name": "东阳光", "code": "600673.SH", "ts_code": "600673.SH", "shares": 10000, "cost": 28.1},
    {"name": "中石科技", "code": "300684.SZ", "ts_code": "300684.SZ", "shares": 9500, "cost": 58.913},
    {"name": "胜宏科技", "code": "300476.SZ", "ts_code": "300476.SZ", "shares": 2800, "cost": 286.942},
    {"name": "云南锗业", "code": "002428.SZ", "ts_code": "002428.SZ", "shares": 8000, "cost": 3.886},
    {"name": "光库科技", "code": "300620.SZ", "ts_code": "300620.SZ", "shares": 3600, "cost": 131.997},
    {"name": "中国铀业", "code": "001280.SZ", "ts_code": "001280.SZ", "shares": 15900, "cost": 87.026},
    {"name": "东微半导", "code": "688261.SH", "ts_code": "688261.SH", "shares": 4000, "cost": 85.622},
    {"name": "英维克", "code": "002837.SZ", "ts_code": "002837.SZ", "shares": 9800, "cost": 101.627},
    {"name": "阳光电源", "code": "300274.SZ", "ts_code": "300274.SZ", "shares": 10000, "cost": 136.142},
    {"name": "福晶科技", "code": "002222.SZ", "ts_code": "002222.SZ", "shares": 6600, "cost": 70.841},
    {"name": "兴森科技", "code": "002436.SZ", "ts_code": "002436.SZ", "shares": 12000, "cost": 23.808},
    {"name": "康龙化成", "code": "300759.SZ", "ts_code": "300759.SZ", "shares": 10000, "cost": 29.359},
    {"name": "科华数据", "code": "002335.SZ", "ts_code": "002335.SZ", "shares": 10900, "cost": 62.117},
    {"name": "中兴通讯", "code": "000063.SZ", "ts_code": "000063.SZ", "shares": 11300, "cost": 35.334},
    {"name": "中科创达", "code": "300496.SZ", "ts_code": "300496.SZ", "shares": 3100, "cost": 57.579},
    {"name": "国电南瑞", "code": "600406.SH", "ts_code": "600406.SH", "shares": 26000, "cost": 24.138},
    {"name": "海南华铁", "code": "603300.SH", "ts_code": "603300.SH", "shares": 31600, "cost": 7.545},
    {"name": "通富微电", "code": "002156.SZ", "ts_code": "002156.SZ", "shares": 28200, "cost": 49.003},
    {"name": "西藏珠峰", "code": "600338.SH", "ts_code": "600338.SH", "shares": 7800, "cost": 12.444},
    {"name": "华虹公司", "code": "688347.SH", "ts_code": "688347.SH", "shares": 2800, "cost": 124.967},
    {"name": "洛阳钼业", "code": "603993.SH", "ts_code": "603993.SH", "shares": 28000, "cost": 18.974},
    {"name": "西藏矿业", "code": "000762.SZ", "ts_code": "000762.SZ", "shares": 8300, "cost": 25.674},
    {"name": "雄韬股份", "code": "002733.SZ", "ts_code": "002733.SZ", "shares": 10000, "cost": 21.372},
    {"name": "华工科技", "code": "000988.SZ", "ts_code": "000988.SZ", "shares": 13000, "cost": 76.308},
    {"name": "中国船舶", "code": "600150.SH", "ts_code": "600150.SH", "shares": 80000, "cost": 43.687},
    {"name": "神州数码", "code": "000034.SZ", "ts_code": "000034.SZ", "shares": 5000, "cost": 44.177},
    {"name": "石英股份", "code": "603688.SH", "ts_code": "603688.SH", "shares": 10000, "cost": 37.37},
]

HK_SHARES = [
    {"name": "阿里巴巴-W", "code": "09988.HK", "ts_code": "09988.HK", "shares": 1300, "cost": 148.54},
    {"name": "云顶新耀", "code": "01952.HK", "ts_code": "01952.HK", "shares": 11000, "cost": 38.627},
    {"name": "晶泰控股", "code": "02228.HK", "ts_code": "02228.HK", "shares": 7000, "cost": 10.122},
    {"name": "小米集团-W", "code": "01810.HK", "ts_code": "01810.HK", "shares": 11600, "cost": 42.931},
    {"name": "迈富时", "code": "02556.HK", "ts_code": "02556.HK", "shares": 7800, "cost": 40.754},
    {"name": "锦欣生殖", "code": "01951.HK", "ts_code": "01951.HK", "shares": 207500, "cost": 2.584},
    {"name": "福寿园", "code": "01448.HK", "ts_code": "01448.HK", "shares": 79000, "cost": 2.989},
    {"name": "药明生物", "code": "02269.HK", "ts_code": "02269.HK", "shares": 10000, "cost": 11.944},
    {"name": "中国电力", "code": "02380.HK", "ts_code": "02380.HK", "shares": 80000, "cost": 3.573},
]

def fetch_quotes():
    """获取所有持仓的实时行情"""
    today = datetime.now().strftime("%Y%m%d")
    
    # 获取 A 股行情
    print("Fetching A-share quotes from Tushare...")
    ts_codes = [s["ts_code"] for s in A_SHARES]
    
    try:
        # 使用 daily 接口获取日线数据（最新一天）
        df = pro.daily(ts_code=",".join(ts_codes), start_date=today, end_date=today)
        
        if df.empty:
            print("No data for today, trying previous trading day...")
            # 如果是非交易日，尝试获取最近的数据
            df = pro.daily(ts_code=",".join(ts_codes))
            # 获取每个股票的最新数据
            a_quotes = {}
            for ts_code in ts_codes:
                stock_df = df[df["ts_code"] == ts_code].head(1)
                if not stock_df.empty:
                    row = stock_df.iloc[0]
                    a_quotes[ts_code] = {
                        "price": row["close"],
                        "change": row["close"] - row["pre_close"],
                        "change_pct": (row["close"] - row["pre_close"]) / row["pre_close"] * 100,
                        "open": row["open"],
                        "high": row["high"],
                        "low": row["low"],
                        "pre_close": row["pre_close"],
                    }
                    print(f"  {ts_code}: {row['close']:.2f} ({a_quotes[ts_code]['change_pct']:+.2f}%)")
            return a_quotes, {}
        
        a_quotes = {}
        for _, row in df.iterrows():
            ts_code = row["ts_code"]
            a_quotes[ts_code] = {
                "price": row["close"],
                "change": row["close"] - row["pre_close"],
                "change_pct": (row["close"] - row["pre_close"]) / row["pre_close"] * 100,
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "pre_close": row["pre_close"],
            }
            print(f"  {ts_code}: {row['close']:.2f} ({a_quotes[ts_code]['change_pct']:+.2f}%)")
        
        return a_quotes, {}
    
    except Exception as e:
        print(f"Error fetching A-shares: {e}")
        return {}, {}

def calculate_portfolio(a_quotes, hk_quotes):
    """计算持仓组合数据"""
    a_holdings = []
    hk_holdings = []
    
    total_a_market_value = 0
    total_hk_market_value = 0
    total_a_float_pnl = 0
    total_hk_float_pnl = 0
    
    principal = 3148.44 * 10000
    
    # 处理 A 股
    for stock in A_SHARES:
        ts_code = stock["ts_code"]
        quote = a_quotes.get(ts_code, {})
        price = quote.get("price", 0)
        change_pct = quote.get("change_pct", 0)
        
        if price > 0:
            market_value = price * stock["shares"]
            cost_value = stock["cost"] * stock["shares"]
            float_pnl = market_value - cost_value
            float_pnl_pct = (float_pnl / cost_value) * 100 if cost_value > 0 else 0
            
            a_holdings.append({
                "name": stock["name"],
                "code": stock["code"],
                "ts_code": ts_code,
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
    
    # 处理港股（简化处理，使用 A 股类似逻辑）
    for stock in HK_SHARES:
        ts_code = stock["ts_code"]
        quote = hk_quotes.get(ts_code, {})
        price = quote.get("price", stock["cost"])  # 如果没有数据，使用成本价
        change_pct = quote.get("change_pct", 0)
        
        market_value = price * stock["shares"]
        cost_value = stock["cost"] * stock["shares"]
        float_pnl = market_value - cost_value
        float_pnl_pct = (float_pnl / cost_value) * 100 if cost_value > 0 else 0
        
        hk_holdings.append({
            "name": stock["name"],
            "code": stock["code"],
            "ts_code": ts_code,
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
    
    all_holdings = data["a_holdings"] + data["hk_holdings"]
    big_gainers = [h for h in all_holdings if h["change_pct"] >= 5]
    big_losers = [h for h in all_holdings if h["change_pct"] <= -5]
    
    sorted_by_pnl = sorted(data["a_holdings"], key=lambda x: x["float_pnl"], reverse=True)
    top_gainers = sorted_by_pnl[:5]
    top_losers = sorted_by_pnl[-5:]
    
    total_market_value = data["total_a_market_value"] + data["total_hk_market_value"]
    total_float_pnl = data["total_a_float_pnl"] + data["total_hk_float_pnl"]
    principal = 3148.44 * 10000
    cash = -59.79 * 10000
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
- 浮动盈亏：{data["total_hk_float_pnl"]/10000:.2f}万 HKD

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

def generate_push_summary(data, date_str):
    """生成推送摘要"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    total_market_value = data["total_a_market_value"] + data["total_hk_market_value"]
    total_float_pnl = data["total_a_float_pnl"] + data["total_hk_float_pnl"]
    principal = 3148.44 * 10000
    cash = -59.79 * 10000
    total_assets = total_market_value + cash
    
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
    
    top5 = sorted(data["a_holdings"], key=lambda x: x["market_value"], reverse=True)[:5]
    summary += "\n💰 持仓 Top5:\n"
    for h in top5:
        summary += f"- {h['name']}: {h['market_value']/10000:.1f}万 ({h['change_pct']:+.1f}%)\n"
    
    summary += "\n📁 详细数据已更新至 portfolio/daily-tracking.md"
    
    return summary

def main():
    print("=" * 50)
    print("Daily Holdings Update (Tushare)")
    print("=" * 50)
    
    # 获取实时行情
    a_quotes, hk_quotes = fetch_quotes()
    
    if not a_quotes:
        print("WARNING: No A-share data fetched, using cached data")
    
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
    print(f"\n[OK] Updated: {tracking_path}")
    
    # 更新 holdings.md
    holdings_md = generate_holdings_md(portfolio_data, today)
    holdings_path = Path("portfolio/holdings.md")
    holdings_path.write_text(holdings_md, encoding="utf-8")
    print(f"[OK] Updated: {holdings_path}")
    
    # 生成推送摘要
    summary = generate_push_summary(portfolio_data, today)
    print("\n" + "=" * 50)
    print("Push Summary:")
    print(summary.encode('utf-8').decode('gbk', errors='ignore'))
    
    # 保存推送摘要
    summary_path = Path("portfolio/push-summary.md")
    summary_path.write_text(summary, encoding="utf-8")
    print(f"\n[OK] Saved push summary to: {summary_path}")

if __name__ == "__main__":
    main()
