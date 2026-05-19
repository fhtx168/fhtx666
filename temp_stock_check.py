import requests

# 使用东方财富 API 获取实时行情
stocks = [
    ('沪电股份', '002463'),
    ('阳光电源', '300274'),
    ('中芯国际', '688981'),
    ('通富微电', '002156'),
]

headers = {
    'User-Agent': 'Mozilla/5.0'
}

for name, code in stocks:
    try:
        secid = '1' if code.startswith('6') else '0'
        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}.{code}&fields=f43,f44,f46,f170'
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get('data'):
            price = data['data']['f46']  # 最新价
            change_pct = data['data']['f170']  # 涨跌幅
            print(f'{name} ({code}): {price:.2f} | {change_pct:.2f}%')
        else:
            print(f'{name} ({code}): No data')
    except Exception as e:
        print(f'{name} ({code}): ERROR - {str(e)}')
