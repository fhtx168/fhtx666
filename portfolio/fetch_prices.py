import requests
import json
import re
import time
from datetime import datetime

# Read holdings
stocks = []
with open('portfolio/holdings.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Parse A-shares (SZ/SH prefix)
a_share_pattern = r'\|\s*(.*?)\s*\|\s*(SZ|SH)(\d+)\s*\|\s*([\d\.]+)\s*\|\s*([+-]?\d\.?\d*)%'
for match in re.finditer(a_share_pattern, content):
    name = match.group(1).strip()
    code = match.group(2) + match.group(3)
    stocks.append({'name': name, 'code': code, 'type': 'A'})

# Parse HK stocks
hk_pattern = r'\|\s*(.*?)\s*\|\s*0(\d{5})\s*\|\s*([\d\.]+)\s*\|\s*([+-]?\d\.?\d*)%'
for match in re.finditer(hk_pattern, content):
    name = match.group(1).strip()
    code = match.group(2)
    stocks.append({'name': name, 'code': code, 'type': 'HK'})

print(f'Found {len(stocks)} stocks')

# Fetch prices from Sina Finance API (more reliable)
results = []
for i, stock in enumerate(stocks):
    try:
        if stock['type'] == 'A':
            # Sina API for A-shares
            if stock['code'].startswith('SZ'):
                symbol = f'sz{stock["code"][2:]}'
            else:
                symbol = f'sh{stock["code"][2:]}'
        else:
            # HK stocks use different symbol format
            symbol = f'hk{stock["code"]}'
        
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
                        'type': stock['type'],
                        'price': price,
                        'change_pct': round(change_pct, 2)
                    })
                    print(f'{i+1}/{len(stocks)} {stock["code"]}: {price} ({change_pct:+.2f}%)')
        time.sleep(0.1)  # Rate limiting
    except Exception as e:
        print(f'Error fetching {stock["code"]}: {e}')

print(f'\nSuccessfully fetched {len(results)} prices')

# Save to temp file
with open('portfolio/temp_prices.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('Prices saved to temp_prices.json')
