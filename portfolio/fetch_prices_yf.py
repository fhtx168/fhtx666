#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fetch real-time stock prices using yfinance and akshare fallback
"""
import yfinance as yf
import pandas as pd
from datetime import datetime

# Holdings data
holdings = {
    # A 股 (Yahoo Finance uses .SS for Shanghai, .SZ for Shenzhen)
    '万华化学': {'code': '600309.SS', 'shares': -1500, 'cost': 77.69, 'market': 'A'},
    '中际旭创': {'code': '300308.SZ', 'shares': 800, 'cost': 1023.80, 'market': 'A'},
    '长电科技': {'code': '600584.SS', 'shares': 2000, 'cost': 56.81, 'market': 'A'},
    '深南电路': {'code': '002916.SZ', 'shares': 1800, 'cost': 327.65, 'market': 'A'},
    '盛美上海': {'code': '688082.SS', 'shares': 2000, 'cost': 180.36, 'market': 'A'},
    '中微公司': {'code': '688012.SS', 'shares': 1200, 'cost': 457.27, 'market': 'A'},
    '飞凯材料': {'code': '300398.SZ', 'shares': 6900, 'cost': 38.79, 'market': 'A'},
    '宝丰能源': {'code': '600989.SS', 'shares': 7000, 'cost': 30.33, 'market': 'A'},
    '拓维信息': {'code': '002261.SZ', 'shares': 13500, 'cost': 36.89, 'market': 'A'},
    '埃斯顿': {'code': '002747.SZ', 'shares': 2500, 'cost': 20.68, 'market': 'A'},
    '德赛西威': {'code': '002920.SZ', 'shares': 5000, 'cost': 112.64, 'market': 'A'},
    '比亚迪': {'code': '002594.SZ', 'shares': 30600, 'cost': 99.97, 'market': 'A'},
    '沪电股份': {'code': '002463.SZ', 'shares': 6600, 'cost': 83.87, 'market': 'A'},
    '拓普集团': {'code': '601689.SS', 'shares': 10000, 'cost': 64.41, 'market': 'A'},
    '中科曙光': {'code': '603019.SS', 'shares': 9800, 'cost': 87.95, 'market': 'A'},
    '锡业股份': {'code': '000960.SZ', 'shares': 6000, 'cost': 38.05, 'market': 'A'},
    '中芯国际': {'code': '688981.SS', 'shares': 9200, 'cost': 115.56, 'market': 'A'},
    '金诚信': {'code': '603979.SS', 'shares': 7100, 'cost': 70.35, 'market': 'A'},
    '沪硅产业': {'code': '688126.SS', 'shares': 17882, 'cost': 20.46, 'market': 'A'},
    '华海诚科': {'code': '688535.SS', 'shares': 4753.76, 'cost': 90.85, 'market': 'A'},
    '中国巨石': {'code': '600176.SS', 'shares': 10000, 'cost': 24.28, 'market': 'A'},
    '东阳光': {'code': '600673.SS', 'shares': 10000, 'cost': 31.38, 'market': 'A'},
    '中石科技': {'code': '300684.SZ', 'shares': 9500, 'cost': 58.89, 'market': 'A'},
    '胜宏科技': {'code': '300476.SZ', 'shares': 3600, 'cost': 314.43, 'market': 'A'},
    '云南锗业': {'code': '002428.SZ', 'shares': 8800, 'cost': 49.23, 'market': 'A'},
    '光库科技': {'code': '300620.SZ', 'shares': 3600, 'cost': 209.67, 'market': 'A'},
    '中国铀业': {'code': '001280.SZ', 'shares': 17200, 'cost': 86.12, 'market': 'A'},
    '东微半导': {'code': '688261.SS', 'shares': 4000, 'cost': 85.62, 'market': 'A'},
    '英维克': {'code': '002837.SZ', 'shares': 9800, 'cost': 101.63, 'market': 'A'},
    '阳光电源': {'code': '300274.SZ', 'shares': 10000, 'cost': 136.83, 'market': 'A'},
    '福晶科技': {'code': '002222.SZ', 'shares': 6600, 'cost': 70.84, 'market': 'A'},
    '兴森科技': {'code': '002436.SZ', 'shares': 12000, 'cost': 23.81, 'market': 'A'},
    '科华数据': {'code': '002335.SZ', 'shares': 10900, 'cost': 62.12, 'market': 'A'},
    '中兴通讯': {'code': '000063.SZ', 'shares': 11300, 'cost': 39.11, 'market': 'A'},
    '中科创达': {'code': '300496.SZ', 'shares': 3100, 'cost': 68.06, 'market': 'A'},
    '国电南瑞': {'code': '600406.SS', 'shares': 26000, 'cost': 24.14, 'market': 'A'},
    '海南华铁': {'code': '603300.SS', 'shares': 31600, 'cost': 7.55, 'market': 'A'},
    '通富微电': {'code': '002156.SZ', 'shares': 28200, 'cost': 49.00, 'market': 'A'},
    '西藏珠峰': {'code': '600338.SS', 'shares': 7800, 'cost': 14.03, 'market': 'A'},
    '华虹公司': {'code': '688347.SS', 'shares': 2800, 'cost': 124.97, 'market': 'A'},
    '洛阳钼业': {'code': '603993.SS', 'shares': 28000, 'cost': 18.97, 'market': 'A'},
    '西藏矿业': {'code': '000762.SZ', 'shares': 8300, 'cost': 25.67, 'market': 'A'},
    '雄韬股份': {'code': '002733.SZ', 'shares': 10000, 'cost': 22.04, 'market': 'A'},
    '华工科技': {'code': '000988.SZ', 'shares': 13000, 'cost': 87.00, 'market': 'A'},
    '中国船舶': {'code': '600150.SS', 'shares': 80000, 'cost': 43.69, 'market': 'A'},
    '神州数码': {'code': '000034.SZ', 'shares': 7000, 'cost': 31.56, 'market': 'A'},
    '石英股份': {'code': '603688.SS', 'shares': 10000, 'cost': 37.37, 'market': 'A'},
    # 港股 (Yahoo Finance uses .HK)
    '阿里巴巴-W': {'code': '9988.HK', 'shares': 2000, 'cost': 132.48, 'market': 'HK'},
    '云顶新耀': {'code': '1952.HK', 'shares': 11000, 'cost': 38.63, 'market': 'HK'},
    '晶泰控股': {'code': '2228.HK', 'shares': 7000, 'cost': 10.12, 'market': 'HK'},
    '小米集团-W': {'code': '1810.HK', 'shares': 11600, 'cost': 42.93, 'market': 'HK'},
    '迈富时': {'code': '2556.HK', 'shares': 7800, 'cost': 40.75, 'market': 'HK'},
    '锦欣生殖': {'code': '1951.HK', 'shares': 207500, 'cost': 2.58, 'market': 'HK'},
    '福寿园': {'code': '1448.HK', 'shares': 79000, 'cost': 3.23, 'market': 'HK'},
    '药明生物': {'code': '2269.HK', 'shares': 10000, 'cost': 11.94, 'market': 'HK'},
    '中国电力': {'code': '2380.HK', 'shares': 80000, 'cost': 3.79, 'market': 'HK'},
}

def main():
    print("Fetching real-time stock prices via yfinance...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    errors = []
    
    for name, data in holdings.items():
        try:
            ticker = yf.Ticker(data['code'])
            info = ticker.fast_info
            price = info['lastPrice']
            
            # Get previous close for change calculation
            hist = ticker.history(period='2d')
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
            else:
                prev_close = info['previousClose']
            
            change = price - prev_close
            change_pct = (change / prev_close) * 100
            
            market_value = price * data['shares']
            cost_basis = data['cost'] * data['shares']
            float_pnl = market_value - cost_basis
            
            results.append({
                'name': name,
                'code': data['code'],
                'price': price,
                'change': change,
                'change_pct': change_pct,
                'shares': data['shares'],
                'cost': data['cost'],
                'market_value': market_value,
                'float_pnl': float_pnl,
                'market': data['market']
            })
            print(f"{data['market']} {name} ({data['code']}): {price:.2f} ({change:+.2f}, {change_pct:+.2f}%) 市值:{market_value/10000:.2f}万 盈亏:{float_pnl/10000:.2f}万")
        except Exception as e:
            errors.append((name, str(e)))
            print(f"ERROR {name} ({data['code']}): {e}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully fetched: {len(results)}")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nFailed stocks:")
        for name, err in errors:
            print(f"  - {name}: {err}")
    
    # Calculate totals
    total_market_value_a = sum(r['market_value'] for r in results if r['market'] == 'A')
    total_market_value_hk = sum(r['market_value'] for r in results if r['market'] == 'HK')
    total_float_pnl_a = sum(r['float_pnl'] for r in results if r['market'] == 'A')
    total_float_pnl_hk = sum(r['float_pnl'] for r in results if r['market'] == 'HK')
    
    print(f"\n=== Portfolio Summary ===")
    print(f"A 股市值：{total_market_value_a/10000:.2f}万")
    print(f"港股市值：{total_market_value_hk/10000:.2f}万 HKD")
    print(f"A 股浮动盈亏：{total_float_pnl_a/10000:.2f}万")
    print(f"港股浮动盈亏：{total_float_pnl_hk/10000:.2f}万 HKD")
    print(f"总市值：{(total_market_value_a + total_market_value_hk)/10000:.2f}万")

if __name__ == '__main__':
    main()
