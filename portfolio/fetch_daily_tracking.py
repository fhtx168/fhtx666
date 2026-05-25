#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fetch stock prices from East Money API and generate daily tracking report
"""
import requests
import json
from datetime import datetime

# Holdings data with East Money secid format (1=Shanghai, 0=Shenzhen, hk=Hong Kong)
holdings = {
    # A 股 - Shanghai (1.)
    '万华化学': {'secid': '1.600309', 'shares': -1500, 'cost': 77.69, 'market': 'A'},
    '长电科技': {'secid': '1.600584', 'shares': 2000, 'cost': 56.81, 'market': 'A'},
    '盛美上海': {'secid': '1.688082', 'shares': 2000, 'cost': 180.36, 'market': 'A'},
    '中微公司': {'secid': '1.688012', 'shares': 1200, 'cost': 457.27, 'market': 'A'},
    '宝丰能源': {'secid': '1.600989', 'shares': 7000, 'cost': 30.33, 'market': 'A'},
    '拓普集团': {'secid': '1.601689', 'shares': 10000, 'cost': 64.41, 'market': 'A'},
    '中科曙光': {'secid': '1.603019', 'shares': 9800, 'cost': 87.95, 'market': 'A'},
    '中芯国际': {'secid': '1.688981', 'shares': 9200, 'cost': 115.56, 'market': 'A'},
    '金诚信': {'secid': '1.603979', 'shares': 7100, 'cost': 70.35, 'market': 'A'},
    '沪硅产业': {'secid': '1.688126', 'shares': 17882, 'cost': 20.46, 'market': 'A'},
    '华海诚科': {'secid': '1.688535', 'shares': 4753.76, 'cost': 90.85, 'market': 'A'},
    '中国巨石': {'secid': '1.600176', 'shares': 10000, 'cost': 24.28, 'market': 'A'},
    '东阳光': {'secid': '1.600673', 'shares': 10000, 'cost': 31.38, 'market': 'A'},
    '东微半导': {'secid': '1.688261', 'shares': 4000, 'cost': 85.62, 'market': 'A'},
    '国电南瑞': {'secid': '1.600406', 'shares': 26000, 'cost': 24.14, 'market': 'A'},
    '海南华铁': {'secid': '1.603300', 'shares': 31600, 'cost': 7.55, 'market': 'A'},
    '西藏珠峰': {'secid': '1.600338', 'shares': 7800, 'cost': 14.03, 'market': 'A'},
    '华虹公司': {'secid': '1.688347', 'shares': 2800, 'cost': 124.97, 'market': 'A'},
    '洛阳钼业': {'secid': '1.603993', 'shares': 28000, 'cost': 18.97, 'market': 'A'},
    '中国船舶': {'secid': '1.600150', 'shares': 80000, 'cost': 43.69, 'market': 'A'},
    '石英股份': {'secid': '1.603688', 'shares': 10000, 'cost': 37.37, 'market': 'A'},
    # A 股 - Shenzhen (0.)
    '中际旭创': {'secid': '0.300308', 'shares': 800, 'cost': 1023.80, 'market': 'A'},
    '深南电路': {'secid': '0.002916', 'shares': 1800, 'cost': 327.65, 'market': 'A'},
    '飞凯材料': {'secid': '0.300398', 'shares': 6900, 'cost': 38.79, 'market': 'A'},
    '拓维信息': {'secid': '0.002261', 'shares': 13500, 'cost': 36.89, 'market': 'A'},
    '埃斯顿': {'secid': '0.002747', 'shares': 2500, 'cost': 20.68, 'market': 'A'},
    '德赛西威': {'secid': '0.002920', 'shares': 5000, 'cost': 112.64, 'market': 'A'},
    '比亚迪': {'secid': '0.002594', 'shares': 30600, 'cost': 99.97, 'market': 'A'},
    '沪电股份': {'secid': '0.002463', 'shares': 6600, 'cost': 83.87, 'market': 'A'},
    '锡业股份': {'secid': '0.000960', 'shares': 6000, 'cost': 38.05, 'market': 'A'},
    '中石科技': {'secid': '0.300684', 'shares': 9500, 'cost': 58.89, 'market': 'A'},
    '胜宏科技': {'secid': '0.300476', 'shares': 3600, 'cost': 314.43, 'market': 'A'},
    '云南锗业': {'secid': '0.002428', 'shares': 8800, 'cost': 49.23, 'market': 'A'},
    '光库科技': {'secid': '0.300620', 'shares': 3600, 'cost': 209.67, 'market': 'A'},
    '中国铀业': {'secid': '0.001280', 'shares': 17200, 'cost': 86.12, 'market': 'A'},
    '英维克': {'secid': '0.002837', 'shares': 9800, 'cost': 101.63, 'market': 'A'},
    '阳光电源': {'secid': '0.300274', 'shares': 10000, 'cost': 136.83, 'market': 'A'},
    '福晶科技': {'secid': '0.002222', 'shares': 6600, 'cost': 70.84, 'market': 'A'},
    '兴森科技': {'secid': '0.002436', 'shares': 12000, 'cost': 23.81, 'market': 'A'},
    '科华数据': {'secid': '0.002335', 'shares': 10900, 'cost': 62.12, 'market': 'A'},
    '中兴通讯': {'secid': '0.000063', 'shares': 11300, 'cost': 39.11, 'market': 'A'},
    '中科创达': {'secid': '0.300496', 'shares': 3100, 'cost': 68.06, 'market': 'A'},
    '通富微电': {'secid': '0.002156', 'shares': 28200, 'cost': 49.00, 'market': 'A'},
    '西藏矿业': {'secid': '0.000762', 'shares': 8300, 'cost': 25.67, 'market': 'A'},
    '雄韬股份': {'secid': '0.002733', 'shares': 10000, 'cost': 22.04, 'market': 'A'},
    '华工科技': {'secid': '0.000988', 'shares': 13000, 'cost': 87.00, 'market': 'A'},
    '神州数码': {'secid': '0.000034', 'shares': 7000, 'cost': 31.56, 'market': 'A'},
    # 港股 (hk.)
    '阿里巴巴-W': {'secid': 'hk.09988', 'shares': 2000, 'cost': 132.48, 'market': 'HK'},
    '云顶新耀': {'secid': 'hk.01952', 'shares': 11000, 'cost': 38.63, 'market': 'HK'},
    '晶泰控股': {'secid': 'hk.02228', 'shares': 7000, 'cost': 10.12, 'market': 'HK'},
    '小米集团-W': {'secid': 'hk.01810', 'shares': 11600, 'cost': 42.93, 'market': 'HK'},
    '迈富时': {'secid': 'hk.02556', 'shares': 7800, 'cost': 40.75, 'market': 'HK'},
    '锦欣生殖': {'secid': 'hk.01951', 'shares': 207500, 'cost': 2.58, 'market': 'HK'},
    '福寿园': {'secid': 'hk.01448', 'shares': 79000, 'cost': 3.23, 'market': 'HK'},
    '药明生物': {'secid': 'hk.02269', 'shares': 10000, 'cost': 11.94, 'market': 'HK'},
    '中国电力': {'secid': 'hk.02380', 'shares': 80000, 'cost': 3.79, 'market': 'HK'},
}

def fetch_quote(secid):
    """Fetch single stock quote from East Money API"""
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f169,f170,f57,f58,f167,f168"
    headers = {
        'Referer': 'https://quote.eastmoney.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if data.get('rc') == 0 and data.get('data'):
            d = data['data']
            return {
                'price': d.get('f43', 0) / 100,  # Current price
                'high': d.get('f44', 0) / 100,
                'low': d.get('f45', 0) / 100,
                'open': d.get('f46', 0) / 100,
                'volume': d.get('f47', 0),
                'change': d.get('f169', 0) / 100,
                'change_pct': d.get('f170', 0) / 100,
                'pe': d.get('f167', 0) / 100,
                'pb': d.get('f168', 0) / 100,
            }
    except Exception as e:
        print(f"Error fetching {secid}: {e}")
    return None

def main():
    print("Fetching stock prices from East Money API...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    errors = []
    
    for name, data in holdings.items():
        quote = fetch_quote(data['secid'])
        if quote and quote['price'] > 0:
            price = quote['price']
            change = quote['change']
            change_pct = quote['change_pct']
            
            market_value = price * data['shares']
            cost_basis = data['cost'] * data['shares']
            float_pnl = market_value - cost_basis
            
            results.append({
                'name': name,
                'secid': data['secid'],
                'price': price,
                'change': change,
                'change_pct': change_pct,
                'shares': data['shares'],
                'cost': data['cost'],
                'market_value': market_value,
                'float_pnl': float_pnl,
                'market': data['market']
            })
            print(f"{data['market']} {name} ({data['secid']}): {price:.2f} ({change:+.2f}, {change_pct:+.2f}%) 市值:{market_value/10000:.2f}万 盈亏:{float_pnl/10000:.2f}万")
        else:
            errors.append(name)
            print(f"ERROR {name} ({data['secid']}): Failed to fetch")
    
    print(f"\n=== Summary ===")
    print(f"Successfully fetched: {len(results)}")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print(f"\nFailed stocks: {', '.join(errors)}")
    
    # Calculate totals
    total_market_value_a = sum(r['market_value'] for r in results if r['market'] == 'A')
    total_market_value_hk = sum(r['market_value'] for r in results if r['market'] == 'HK')
    total_float_pnl_a = sum(r['float_pnl'] for r in results if r['market'] == 'A')
    total_float_pnl_hk = sum(r['float_pnl'] for r in results if r['market'] == 'HK')
    total_cost_a = sum(r['cost'] * r['shares'] for r in results if r['market'] == 'A')
    total_cost_hk = sum(r['cost'] * r['shares'] for r in results if r['market'] == 'HK')
    
    print(f"\n=== Portfolio Summary ===")
    print(f"A 股市值：{total_market_value_a/10000:.2f}万")
    print(f"港股市值：{total_market_value_hk/10000:.2f}万 HKD")
    print(f"A 股浮动盈亏：{total_float_pnl_a/10000:.2f}万")
    print(f"港股浮动盈亏：{total_float_pnl_hk/10000:.2f}万 HKD")
    print(f"总市值：{(total_market_value_a + total_market_value_hk)/10000:.2f}万")
    
    # Generate markdown report
    date_str = datetime.now().strftime('%Y-%m-%d')
    report = f"""# 每日持仓跟踪 - {date_str}

> **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **数据来源**: 东方财富网  
> **市场状态**: 已收盘

## 总览

| 指标 | 数值 |
|------|------|
| **总市值** | **{(total_market_value_a + total_market_value_hk)/10000:.2f}万** |
| **A 股市值** | **{total_market_value_a/10000:.2f}万** |
| **港股市值** | **{total_market_value_hk/10000:.2f}万 HKD** |
| **A 股浮动盈亏** | **{total_float_pnl_a/10000:+.2f}万** |
| **港股浮动盈亏** | **{total_float_pnl_hk/10000:+.2f}万 HKD** |
| **持仓数量** | **{len(results)}只** |

---

## A 股持仓明细

| 名称 | 代码 | 现价 | 涨跌 | 涨跌幅 | 持仓 | 成本 | 市值 | 浮动盈亏 |
|------|------|------|------|--------|------|------|------|----------|
"""
    
    for r in sorted([x for x in results if x['market'] == 'A'], key=lambda x: x['change_pct'], reverse=True):
        code = r['secid'].split('.')[1]
        report += f"| {r['name']} | {code} | {r['price']:.2f} | {r['change']:+.2f} | {r['change_pct']:+.2f}% | {r['shares']} | {r['cost']:.2f} | {r['market_value']/10000:.2f}万 | {r['float_pnl']/10000:+.2f}万 |\n"
    
    report += f"""
---

## 港股持仓明细

| 名称 | 代码 | 现价 | 涨跌 | 涨跌幅 | 持仓 | 成本 | 市值 | 浮动盈亏 |
|------|------|------|------|--------|------|------|------|----------|
"""
    
    for r in sorted([x for x in results if x['market'] == 'HK'], key=lambda x: x['change_pct'], reverse=True):
        code = r['secid'].split('.')[1]
        report += f"| {r['name']} | {code} | {r['price']:.2f} | {r['change']:+.2f} | {r['change_pct']:+.2f}% | {r['shares']} | {r['cost']:.2f} | {r['market_value']/10000:.2f}万 | {r['float_pnl']/10000:+.2f}万 |\n"
    
    # Save report
    with open('daily-tracking.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved to daily-tracking.md")

if __name__ == '__main__':
    main()
