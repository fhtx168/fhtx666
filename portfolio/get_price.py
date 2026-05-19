import requests
import json

# 东方财富实时行情 API
stocks = {
    "1.600584": "长电科技",
    "0.300308": "中际旭创",
    "0.002916": "深南电路",
}

print("| 标的 | 现价 | 涨跌额 | 涨跌幅 |")
print("|------|------|--------|--------|")

for secid, name in stocks.items():
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f191,f192"
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        data = r.json()
        if data.get('data'):
            d = data['data']
            price = d['f46']/100
            change = d['f191']
            pct = d['f192']
            print(f"| {name} | {price:.2f}元 | {change} | {pct}% |")
    except Exception as e:
        print(f"| {name} | 获取失败 | - | - |")
