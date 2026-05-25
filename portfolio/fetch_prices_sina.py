#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fetch stock prices from Sina Finance API (free, no rate limit for basic quotes)
"""
import requests
import re
from datetime import datetime

# Holdings data
holdings = {
    # A 股
    '万华化学': {'code': 'sh600309', 'shares': -1500, 'cost': 77.69, 'market': 'A'},
    '中际旭创': {'code': 'sz300308', 'shares': 800, 'cost': 1023.80, 'market': 'A'},
    '长电科技': {'code': 'sh600584', 'shares': 2000, 'cost': 56.81, 'market': 'A'},
    '深南电路': {'code': 'sz002916', 'shares': 1800, 'cost': 327.65, 'market': 'A'},
    '盛美上海': {'code': 'sh688082', 'shares': 2000, 'cost': 180.36, 'market': 'A'},
    '中微公司': {'code': 'sh688012', 'shares': 1200, 'cost': 457.27, 'market': 'A'},
    '飞凯材料': {'code': 'sz300398', 'shares': 6900, 'cost': 38.79, 'market': 'A'},
    '宝丰能源': {'code': 'sh600989', 'shares': 7000, 'cost': 30.33, 'market': 'A'},
    '拓维信息': {'code': 'sz002261', 'shares': 13500, 'cost': 36.89, 'market': 'A'},
    '埃斯顿': {'code': 'sz002747', 'shares': 2500, 'cost': 20.68, 'market': 'A'},
    '德赛西威': {'code': 'sz002920', 'shares': 5000, 'cost': 112.64, 'market': 'A'},
    '比亚迪': {'code': 'sz002594', 'shares': 30600, 'cost': 99.97, 'market': 'A'},
    '沪电股份': {'code': 'sz002463', 'shares': 6600, 'cost': 83.87, 'market': 'A'},
    '拓普集团': {'code': 'sh601689', 'shares': 10000, 'cost': 64.41, 'market': 'A'},
    '中科曙光': {'code': 'sh603019', 'shares': 9800, 'cost': 87.95, 'market': 'A'},
    '锡业股份': {'code': 'sz000960', 'shares': 6000, 'cost': 38.05, 'market': 'A'},
    '中芯国际': {'code': 'sh688981', 'shares': 9200, 'cost': 115.56, 'market': 'A'},
    '金诚信': {'code': 'sh603979', 'shares': 7100, 'cost': 70.35, 'market': 'A'},
    '沪硅产业': {'code': 'sh688126', 'shares': 17882, 'cost': 20.46, 'market': 'A'},
    '华海诚科': {'code': 'sh688535', 'shares': 4753.76, 'cost': 90.85, 'market': 'A'},
    '中国巨石': {'code': 'sh600176', 'shares': 10000, 'cost': 24.28, 'market': 'A'},
    '东阳光': {'code': 'sh600673', 'shares': 10000, 'cost': 31.38, 'market': 'A'},
    '中石科技': {'code': 'sz300684', 'shares': 9500, 'cost': 58.89, 'market': 'A'},
    '胜宏科技': {'code': 'sz300476', 'shares': 3600, 'cost': 314.43, 'market': 'A'},
    '云南锗业': {'code': 'sz002428', 'shares': 8800, 'cost': 49.23, 'market': 'A'},
    '光库科技': {'code': 'sz300620', 'shares': 3600, 'cost': 209.67, 'market': 'A'},
    '中国铀业': {'code': 'sz001280', 'shares': 17200, 'cost': 86.12, 'market': 'A'},
    '东微半导': {'code': 'sh688261', 'shares': 4000, 'cost': 85.62, 'market': 'A'},
    '英维克': {'code': 'sz002837', 'shares': 9800, 'cost': 101.63, 'market': 'A'},
    '阳光电源': {'code': 'sz300274', 'shares': 10000, 'cost': 136.83, 'market': 'A'},
    '福晶科技': {'code': 'sz002222', 'shares': 6600, 'cost': 70.84, 'market': 'A'},
    '兴森科技': {'code': 'sz002436', 'shares': 12000, 'cost': 23.81, 'market': 'A'},
    '科华数据': {'code': 'sz002335', 'shares': 10900, 'cost': 62.12, 'market': 'A'},
    '中兴通讯': {'code': 'sz000063', 'shares': 11300, 'cost': 39.11, 'market': 'A'},
    '中科创达': {'code': 'sz300496', 'shares': 3100, 'cost': 68.06, 'market': 'A'},
    '国电南瑞': {'code': 'sh600406', 'shares': 26000, 'cost': 24.14, 'market': 'A'},
    '海南华铁': {'code': 'sh603300', 'shares': 31600, 'cost': 7.55, 'market': 'A'},
    '通富微电': {'code': 'sz002156', 'shares': 28200, 'cost': 49.00, 'market': 'A'},
    '西藏珠峰': {'code': 'sh600338', 'shares': 7800, 'cost': 14.03, 'market': 'A'},
    '华虹公司': {'code': 'sh688347', 'shares': 2800, 'cost': 124.97, 'market': 'A'},
    '洛阳钼业': {'code': 'sh603993', 'shares': 28000, 'cost': 18.97, 'market': 'A'},
    '西藏矿业': {'code': 'sz000762', 'shares': 8300, 'cost': 25.67, 'market': 'A'},
    '雄韬股份': {'code': 'sz002733', 'shares': 10000, 'cost': 22.04, 'market': 'A'},
    '华工科技': {'code': 'sz000988', 'shares': 13000, 'cost': 87.00, 'market': 'A'},
    '中国船舶': {'code': 'sh600150', 'shares': 80000, 'cost': 43.69, 'market': 'A'},
    '神州数码': {'code': 'sz000034', 'shares': 7000, 'cost': 31.56, 'market': 'A'},
    '石英股份': {'code': 'sh603688', 'shares': 10000, 'cost': 37.37, 'market': 'A'},
    # 港股 (Sina uses hk for HK stocks)
    '阿里巴巴-W': {'code': 'hk09988', 'shares': 2000, 'cost': 132.48, 'market': 'HK'},
    '云顶新耀': {'code': 'hk01952', 'shares': 11000, 'cost': 38.63, 'market': 'HK'},
    '晶泰控股': {'code': 'hk02228', 'shares': 7000, 'cost': 10.12, 'market': 'HK'},
    '小米集团-W': {'code': 'hk01810', 'shares': 11600, 'cost': 42.93, 'market': 'HK'},
    '迈富时': {'code': 'hk02556', 'shares': 7800, 'cost': 40.75, 'market': 'HK'},
    '锦欣生殖': {'code': 'hk01951', 'shares': 207500, 'cost': 2.58, 'market': 'HK'},
    '福寿园': {'code': 'hk01448', 'shares': 79000, 'cost': 3.23, 'market': 'HK'},
    '药明生物': {'code': 'hk02269', 'shares': 10000, 'cost': 11.94, 'market': 'HK'},
    '中国电力': {'code': 'hk02380', 'shares': 80000, 'cost': 3.79, 'market': 'HK'},
}

def fetch_sina_quote(code):
    """Fetch single stock quote from Sina Finance API"""
    url = f"http://hq.sinajs.cn/?_={int(datetime.now().timestamp()*1000)}&symbol={code}"
    headers = {
        'Referer': 'http://finance.sina.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.encoding = 'gbk'
        text = resp.text.strip()
        # Parse: var hq_str_sh600309="万华化学，77.99,..."
        match = re.search(r'="([^"]+)"', text)
        if match:
            parts = match.group(1).split(',')
            if len(parts) >= 32:
                name = parts[0]
                prev_close = float(parts[2]) if parts[2] else 0
                price = float(parts[3]) if parts[3] else 0
                high = float(parts[4]) if parts[4] else 0
                low = float(parts[5]) if parts[5] else 0
                volume = int(parts[8]) if parts[8] else 0
                return {
                    'name': name,
                    'price': price,
                    'prev_close': prev_close,
                    'change': price - prev_close,
                    'change_pct': ((price - prev_close) / prev_close * 100) if prev_close else 0,
                }
    except Exception as e:
        return None
    return None

def main():
    print("Fetching stock prices from Sina Finance API...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    errors = []
    
    # Batch fetch (Sina allows multiple symbols in one request)
    all_codes = list(holdings.keys())
    
    for name, data in holdings.items():
        quote = fetch_sina_quote(data['code'])
        if quote and quote['price'] > 0:
            price = quote['price']
            change = quote['change']
            change_pct = quote['change_pct']
            
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
        else:
            errors.append(name)
            print(f"ERROR {name} ({data['code']}): Failed to fetch")
    
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
    
    print(f"\n=== Portfolio Summary ===")
    print(f"A 股市值：{total_market_value_a/10000:.2f}万")
    print(f"港股市值：{total_market_value_hk/10000:.2f}万 HKD")
    print(f"A 股浮动盈亏：{total_float_pnl_a/10000:.2f}万")
    print(f"港股浮动盈亏：{total_float_pnl_hk/10000:.2f}万 HKD")
    print(f"总市值：{(total_market_value_a + total_market_value_hk)/10000:.2f}万")

if __name__ == '__main__':
    main()
