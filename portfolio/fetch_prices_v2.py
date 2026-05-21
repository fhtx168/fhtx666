import requests
import json
import re
import time
from datetime import datetime

# Read holdings
stocks = []
with open('portfolio/holdings.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse A-shares (format: 300308.SZ or 600584.SH)
a_share_pattern = r'\|\s*([^\|]+?)\s*\|\s*(\d{6})\.(SZ|SH)\s*\|'
for match in re.finditer(a_share_pattern, content):
    name = match.group(1).strip()
    code = match.group(2)
    exchange = match.group(3)
    # Skip header row
    if name == '名称':
        continue
    stocks.append({'name': name, 'code': code, 'exchange': exchange, 'type': 'A'})

# Parse HK stocks (format: 09988.HK)
hk_pattern = r'\|\s*([^\|]+?)\s*\|\s*0(\d{4,5})\.HK\s*\|'
for match in re.finditer(hk_pattern, content):
    name = match.group(1).strip()
    code = match.group(2)
    # Skip header row
    if name == '名称':
        continue
    stocks.append({'name': name, 'code': code, 'exchange': 'HK', 'type': 'HK'})

print(f'Found {len(stocks)} stocks ({sum(1 for s in stocks if s["type"]=="A")} A-shares, {sum(1 for s in stocks if s["type"]=="HK")} HK)')

# Fetch prices from Sina Finance API
results = []
for i, stock in enumerate(stocks):
    try:
        if stock['type'] == 'A':
            # Sina API for A-shares: sh600584 or sz000001
            symbol = f"{stock['exchange'].lower()}{stock['code']}"
        else:
            # HK stocks: hk09988
            symbol = f"hk{stock['code']}"
        
        url = f'http://hq.sinajs.cn/rn={int(time.time()*1000)}&list={symbol}'
        headers = {'Referer': 'http://finance.sina.com.cn/'}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200 and symbol in resp.text:
            # Parse Sina response: var hq_str_sz000001="name,price,..."
            parts = resp.text.split('"')
            if len(parts) > 1:
                data = parts[1].split(',')
                if len(data) >= 4:
                    name = data[0]
                    price = float(data[3]) if data[3] else 0
                    # Yesterday close is at index 2
                    yesterday = float(data[2]) if data[2] else price
                    change_pct = ((price - yesterday) / yesterday * 100) if yesterday else 0
                    
                    results.append({
                        'name': name,
                        'code': stock['code'],
                        'exchange': stock['exchange'],
                        'type': stock['type'],
                        'price': price,
                        'change_pct': round(change_pct, 2)
                    })
                    print(f'{i+1}/{len(stocks)} {symbol}: {price} ({change_pct:+.2f}%)')
        time.sleep(0.05)  # Rate limiting
    except Exception as e:
        print(f'Error fetching {stock["code"]}: {e}')

print(f'\nSuccessfully fetched {len(results)} prices')

# Save to temp file
with open('portfolio/temp_prices.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('Prices saved to temp_prices.json')
