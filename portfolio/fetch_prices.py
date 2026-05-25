#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fetch real-time stock prices for portfolio holdings
"""
import akshare as ak
import pandas as pd
from datetime import datetime

# Holdings data from holdings.md
holdings = {
    # A 股：名称，代码，持仓数量，成本价
    '万华化学': {'code': '600309', 'shares': -1500, 'cost': 77.69, 'market': 'A'},
    '中际旭创': {'code': '300308', 'shares': 800, 'cost': 1023.80, 'market': 'A'},
    '长电科技': {'code': '600584', 'shares': 2000, 'cost': 56.81, 'market': 'A'},
    '深南电路': {'code': '002916', 'shares': 1800, 'cost': 327.65, 'market': 'A'},
    '盛美上海': {'code': '688082', 'shares': 2000, 'cost': 180.36, 'market': 'A'},
    '中微公司': {'code': '688012', 'shares': 1200, 'cost': 457.27, 'market': 'A'},
    '飞凯材料': {'code': '300398', 'shares': 6900, 'cost': 38.79, 'market': 'A'},
    '宝丰能源': {'code': '600989', 'shares': 7000, 'cost': 30.33, 'market': 'A'},
    '拓维信息': {'code': '002261', 'shares': 13500, 'cost': 36.89, 'market': 'A'},
    '埃斯顿': {'code': '002747', 'shares': 2500, 'cost': 20.68, 'market': 'A'},
    '德赛西威': {'code': '002920', 'shares': 5000, 'cost': 112.64, 'market': 'A'},
    '比亚迪': {'code': '002594', 'shares': 30600, 'cost': 99.97, 'market': 'A'},
    '沪电股份': {'code': '002463', 'shares': 6600, 'cost': 83.87, 'market': 'A'},
    '拓普集团': {'code': '601689', 'shares': 10000, 'cost': 64.41, 'market': 'A'},
    '中科曙光': {'code': '603019', 'shares': 9800, 'cost': 87.95, 'market': 'A'},
    '锡业股份': {'code': '000960', 'shares': 6000, 'cost': 38.05, 'market': 'A'},
    '中芯国际': {'code': '688981', 'shares': 9200, 'cost': 115.56, 'market': 'A'},
    '金诚信': {'code': '603979', 'shares': 7100, 'cost': 70.35, 'market': 'A'},
    '沪硅产业': {'code': '688126', 'shares': 17882, 'cost': 20.46, 'market': 'A'},
    '华海诚科': {'code': '688535', 'shares': 4753.76, 'cost': 90.85, 'market': 'A'},
    '中国巨石': {'code': '600176', 'shares': 10000, 'cost': 24.28, 'market': 'A'},
    '东阳光': {'code': '600673', 'shares': 10000, 'cost': 31.38, 'market': 'A'},
    '中石科技': {'code': '300684', 'shares': 9500, 'cost': 58.89, 'market': 'A'},
    '胜宏科技': {'code': '300476', 'shares': 3600, 'cost': 314.43, 'market': 'A'},
    '云南锗业': {'code': '002428', 'shares': 8800, 'cost': 49.23, 'market': 'A'},
    '光库科技': {'code': '300620', 'shares': 3600, 'cost': 209.67, 'market': 'A'},
    '中国铀业': {'code': '001280', 'shares': 17200, 'cost': 86.12, 'market': 'A'},
    '东微半导': {'code': '688261', 'shares': 4000, 'cost': 85.62, 'market': 'A'},
    '英维克': {'code': '002837', 'shares': 9800, 'cost': 101.63, 'market': 'A'},
    '阳光电源': {'code': '300274', 'shares': 10000, 'cost': 136.83, 'market': 'A'},
    '福晶科技': {'code': '002222', 'shares': 6600, 'cost': 70.84, 'market': 'A'},
    '兴森科技': {'code': '002436', 'shares': 12000, 'cost': 23.81, 'market': 'A'},
    '科华数据': {'code': '002335', 'shares': 10900, 'cost': 62.12, 'market': 'A'},
    '中兴通讯': {'code': '000063', 'shares': 11300, 'cost': 39.11, 'market': 'A'},
    '中科创达': {'code': '300496', 'shares': 3100, 'cost': 68.06, 'market': 'A'},
    '国电南瑞': {'code': '600406', 'shares': 26000, 'cost': 24.14, 'market': 'A'},
    '海南华铁': {'code': '603300', 'shares': 31600, 'cost': 7.55, 'market': 'A'},
    '通富微电': {'code': '002156', 'shares': 28200, 'cost': 49.00, 'market': 'A'},
    '西藏珠峰': {'code': '600338', 'shares': 7800, 'cost': 14.03, 'market': 'A'},
    '华虹公司': {'code': '688347', 'shares': 2800, 'cost': 124.97, 'market': 'A'},
    '洛阳钼业': {'code': '603993', 'shares': 28000, 'cost': 18.97, 'market': 'A'},
    '西藏矿业': {'code': '000762', 'shares': 8300, 'cost': 25.67, 'market': 'A'},
    '雄韬股份': {'code': '002733', 'shares': 10000, 'cost': 22.04, 'market': 'A'},
    '华工科技': {'code': '000988', 'shares': 13000, 'cost': 87.00, 'market': 'A'},
    '中国船舶': {'code': '600150', 'shares': 80000, 'cost': 43.69, 'market': 'A'},
    '神州数码': {'code': '000034', 'shares': 7000, 'cost': 31.56, 'market': 'A'},
    '石英股份': {'code': '603688', 'shares': 10000, 'cost': 37.37, 'market': 'A'},
    # 港股
    '阿里巴巴-W': {'code': '09988', 'shares': 2000, 'cost': 132.48, 'market': 'HK'},
    '云顶新耀': {'code': '01952', 'shares': 11000, 'cost': 38.63, 'market': 'HK'},
    '晶泰控股': {'code': '02228', 'shares': 7000, 'cost': 10.12, 'market': 'HK'},
    '小米集团-W': {'code': '01810', 'shares': 11600, 'cost': 42.93, 'market': 'HK'},
    '迈富时': {'code': '02556', 'shares': 7800, 'cost': 40.75, 'market': 'HK'},
    '锦欣生殖': {'code': '01951', 'shares': 207500, 'cost': 2.58, 'market': 'HK'},
    '福寿园': {'code': '01448', 'shares': 79000, 'cost': 3.23, 'market': 'HK'},
    '药明生物': {'code': '02269', 'shares': 10000, 'cost': 11.94, 'market': 'HK'},
    '中国电力': {'code': '02380', 'shares': 80000, 'cost': 3.79, 'market': 'HK'},
}

def fetch_a_shares():
    """Fetch A-share real-time quotes"""
    try:
        df = ak.stock_zh_a_spot_em()
        return df
    except Exception as e:
        print(f"Error fetching A-shares: {e}")
        return None

def fetch_hk_stocks():
    """Fetch HK stock real-time quotes"""
    try:
        df = ak.stock_hk_spot_em()
        return df
    except Exception as e:
        print(f"Error fetching HK stocks: {e}")
        return None

def main():
    print("Fetching real-time stock prices...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Fetch data
    a_df = fetch_a_shares()
    hk_df = fetch_hk_stocks()
    
    if a_df is None or hk_df is None:
        print("Failed to fetch market data")
        return
    
    results = []
    
    # Process A-shares
    for name, data in holdings.items():
        if data['market'] == 'A':
            code = data['code']
            match = a_df[a_df['代码'] == code]
            if not match.empty:
                row = match.iloc[0]
                price = float(row['最新价'])
                change_pct = float(row['涨跌幅'])
                prev_close = float(row['昨收'])
                change = price - prev_close
                
                market_value = price * data['shares']
                cost_basis = data['cost'] * data['shares']
                float_pnl = market_value - cost_basis
                
                results.append({
                    'name': name,
                    'code': code,
                    'price': price,
                    'change': change,
                    'change_pct': change_pct,
                    'shares': data['shares'],
                    'cost': data['cost'],
                    'market_value': market_value,
                    'float_pnl': float_pnl,
                    'market': 'A'
                })
                print(f"A {name} ({code}): {price:.2f} ({change:+.2f}, {change_pct:+.2f}%) 市值:{market_value/10000:.2f}万 盈亏:{float_pnl/10000:.2f}万")
    
    # Process HK stocks
    for name, data in holdings.items():
        if data['market'] == 'HK':
            code = data['code']
            match = hk_df[hk_df['代码'] == code]
            if not match.empty:
                row = match.iloc[0]
                price = float(row['最新价'])
                change_pct = float(row['涨跌幅'])
                prev_close = float(row['昨收'])
                change = price - prev_close
                
                market_value = price * data['shares']
                cost_basis = data['cost'] * data['shares']
                float_pnl = market_value - cost_basis
                
                results.append({
                    'name': name,
                    'code': code,
                    'price': price,
                    'change': change,
                    'change_pct': change_pct,
                    'shares': data['shares'],
                    'cost': data['cost'],
                    'market_value': market_value,
                    'float_pnl': float_pnl,
                    'market': 'HK'
                })
                print(f"HK {name} ({code}): {price:.2f} ({change:+.2f}, {change_pct:+.2f}%) 市值:{market_value/10000:.2f}万 盈亏:{float_pnl/10000:.2f}万")
    
    # Save results
    print(f"\nTotal stocks fetched: {len(results)}")
    
    # Output as markdown table
    print("\n=== A 股持仓明细 ===")
    print("| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 成本 | 市值 | 浮动盈亏 |")
    print("|------|------|------|------|------|------|------|----------|")
    for r in [x for x in results if x['market'] == 'A']:
        print(f"| {r['name']} | {r['code']} | {r['price']:.2f} | {r['change_pct']:+.2f}% | {r['shares']} | {r['cost']:.2f} | {r['market_value']/10000:.2f}万 | {r['float_pnl']/10000:+.2f}万 |")
    
    print("\n=== 港股持仓明细 ===")
    print("| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 成本 | 市值 | 浮动盈亏 |")
    print("|------|------|------|------|------|------|------|----------|")
    for r in [x for x in results if x['market'] == 'HK']:
        print(f"| {r['name']} | {r['code']} | {r['price']:.2f} | {r['change_pct']:+.2f}% | {r['shares']} | {r['cost']:.2f} | {r['market_value']/10000:.2f}万 | {r['float_pnl']/10000:+.2f}万 |")
    
    # Calculate totals
    total_market_value_a = sum(r['market_value'] for r in results if r['market'] == 'A')
    total_market_value_hk = sum(r['market_value'] for r in results if r['market'] == 'HK')
    total_float_pnl_a = sum(r['float_pnl'] for r in results if r['market'] == 'A')
    total_float_pnl_hk = sum(r['float_pnl'] for r in results if r['market'] == 'HK')
    
    print(f"\n=== 总览 ===")
    print(f"A 股市值：{total_market_value_a/10000:.2f}万")
    print(f"港股市值：{total_market_value_hk/10000:.2f}万 HKD")
    print(f"A 股浮动盈亏：{total_float_pnl_a/10000:.2f}万")
    print(f"港股浮动盈亏：{total_float_pnl_hk/10000:.2f}万 HKD")
    print(f"总市值：{(total_market_value_a + total_market_value_hk)/10000:.2f}万")

if __name__ == '__main__':
    main()
