import requests
import time

def fetch_price(symbol, name):
    url = f'http://hq.sinajs.cn/rn={int(time.time()*1000)}&list={symbol}'
    headers = {'Referer': 'http://finance.sina.com.cn/'}
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code == 200 and symbol in resp.text:
        parts = resp.text.split('"')
        if len(parts) > 1:
            data = parts[1].split(',')
            if len(data) >= 4:
                price = float(data[3]) if data[3] else 0
                yesterday = float(data[2]) if data[2] else price
                change_pct = ((price - yesterday) / yesterday * 100) if yesterday else 0
                print(f'{name}: {price} ({change_pct:+.2f}%)')
                return price, change_pct
    return None, None

# Missing A-shares
fetch_price('sh688535', '华海诚科')
fetch_price('sz300274', '阳光电源')

# HK stocks
hk_stocks = [
    ('hk09988', '阿里巴巴-W'),
    ('hk01952', '云顶新耀'),
    ('hk02228', '晶泰控股'),
    ('hk01810', '小米集团-W'),
    ('hk02556', '迈富时'),
    ('hk01951', '锦欣生殖'),
    ('hk01448', '福寿园'),
    ('hk02269', '药明生物'),
    ('hk02380', '中国电力'),
]

for symbol, name in hk_stocks:
    fetch_price(symbol, name)
