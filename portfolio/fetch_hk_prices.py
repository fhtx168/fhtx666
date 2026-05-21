import requests
import json
import time

# HK stocks from holdings.md
hk_stocks = [
    {'name': '阿里巴巴-W', 'code': '09988'},
    {'name': '云顶新耀', 'code': '01952'},
    {'name': '晶泰控股', 'code': '02228'},
    {'name': '小米集团-W', 'code': '01810'},
    {'name': '迈富时', 'code': '02556'},
    {'name': '锦欣生殖', 'code': '01951'},
    {'name': '福寿园', 'code': '01448'},
    {'name': '药明生物', 'code': '02269'},
    {'name': '中国电力', 'code': '02380'},
]

print(f'Fetching {len(hk_stocks)} HK stocks...')

results = []
for i, stock in enumerate(hk_stocks):
    try:
        symbol = f"hk{stock['code']}"
        url = f'http://hq.sinajs.cn/rn={int(time.time()*1000)}&list={symbol}'
        headers = {'Referer': 'http://finance.sina.com.cn/'}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200 and symbol in resp.text:
            parts = resp.text.split('"')
            if len(parts) > 1:
                data = parts[1].split(',')
                if len(data) >= 4:
                    name = data[0]
                    price = float(data[3]) if data[3] else 0
                    yesterday = float(data[2]) if data[2] else price
                    change_pct = ((price - yesterday) / yesterday * 100) if yesterday else 0
                    
                    results.append({
                        'name': name,
                        'code': stock['code'],
                        'exchange': 'HK',
                        'type': 'HK',
                        'price': price,
                        'change_pct': round(change_pct, 2)
                    })
                    print(f'{i+1}/{len(hk_stocks)} {symbol}: {price} ({change_pct:+.2f}%)')
        time.sleep(0.1)
    except Exception as e:
        print(f'Error fetching {stock["code"]}: {e}')

print(f'\nSuccessfully fetched {len(results)} HK prices')

# Load existing A-share prices and merge
with open('portfolio/temp_prices.json', 'r', encoding='utf-8') as f:
    all_prices = json.load(f)

all_prices.extend(results)

# Save merged results
with open('portfolio/temp_prices.json', 'w', encoding='utf-8') as f:
    json.dump(all_prices, f, ensure_ascii=False, indent=2)

print(f'Total: {len(all_prices)} prices saved')
