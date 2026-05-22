# -*- coding: utf-8 -*-
"""每日持仓更新脚本 - 使用新浪接口"""
import requests
import json
from datetime import datetime

print("Starting price update via Sina API...")

# 持仓代码
holdings_a = [
    ("中际旭创", "sz300308"), ("长电科技", "sh600584"), ("深南电路", "sz002916"),
    ("盛美上海", "sh688082"), ("中微公司", "sh688012"), ("飞凯材料", "sz300398"),
    ("宝丰能源", "sh600989"), ("拓维信息", "sz002261"), ("埃斯顿", "sz002747"),
    ("德赛西威", "sz002920"), ("比亚迪", "sz002594"), ("沪电股份", "sz002463"),
    ("拓普集团", "sh601689"), ("中科曙光", "sh603019"), ("锡业股份", "sz000960"),
    ("兴业银锡", "sz000426"), ("中芯国际", "sh688981"), ("金诚信", "sh603979"),
    ("沪硅产业", "sh688126"), ("华海诚科", "sh688535"), ("中国巨石", "sh600176"),
    ("东阳光", "sh600673"), ("中石科技", "sz300684"), ("胜宏科技", "sz300476"),
    ("云南锗业", "sz002428"), ("光库科技", "sz300620"), ("中国铀业", "sz001280"),
    ("东微半导", "sh688261"), ("英维克", "sz002837"), ("阳光电源", "sz300274"),
    ("福晶科技", "sz002222"), ("兴森科技", "sz002436"), ("科华数据", "sz002335"),
    ("中兴通讯", "sz000063"), ("中科创达", "sz300496"), ("国电南瑞", "sh600406"),
    ("海南华铁", "sh603300"), ("通富微电", "sz002156"), ("西藏珠峰", "sh600338"),
    ("华虹公司", "sh688347"), ("洛阳钼业", "sh603993"), ("西藏矿业", "sz000762"),
    ("雄韬股份", "sz002733"), ("华工科技", "sz000988"), ("中国船舶", "sh600150"),
    ("神州数码", "sz000034")
]

holdings_hk = [
    ("阿里巴巴-W", "hk09988"), ("云顶新耀", "hk01952"), ("晶泰控股", "hk02228"),
    ("小米集团-W", "hk01810"), ("迈富时", "hk02556"), ("锦欣生殖", "hk01951"),
    ("福寿园", "hk01448"), ("药明生物", "hk02269"), ("中国电力", "hk02380")
]

results = {'a_stocks': {}, 'hk_stocks': {}, 'timestamp': datetime.now().isoformat()}

# 构建新浪 API 请求
symbols_a = ','.join([code for _, code in holdings_a])
symbols_hk = ','.join([code for _, code in holdings_hk])

# 获取 A 股
print("Fetching A-shares from Sina...")
try:
    url_a = f"http://hq.sinajs.cn/list={symbols_a}"
    resp = requests.get(url_a, timeout=10)
    lines = resp.text.strip().split('\n')
    
    for i, (name, code) in enumerate(holdings_a):
        if i < len(lines):
            line = lines[i]
            parts = line.split('"')
            if len(parts) > 1:
                data = parts[1].split(',')
                if len(data) > 3:
                    price = float(data[3])  # 当前价
                    change_pct = float(data[2]) * 100  # 涨跌幅
                    change = price - float(data[2])  # 涨跌额
                    results['a_stocks'][code.replace('sh', '').replace('sz', '')] = {
                        'name': name,
                        'price': price,
                        'change_pct': change_pct,
                        'change': change
                    }
                    print(f"  {name}: {price} ({change_pct:+.2f}%)")
except Exception as e:
    print(f"A-share error: {e}")

# 获取港股
print("\nFetching HK stocks from Sina...")
try:
    url_hk = f"http://hq.sinajs.cn/list={symbols_hk}"
    resp = requests.get(url_hk, timeout=10)
    lines = resp.text.strip().split('\n')
    
    for i, (name, code) in enumerate(holdings_hk):
        if i < len(lines):
            line = lines[i]
            parts = line.split('"')
            if len(parts) > 1:
                data = parts[1].split(',')
                if len(data) > 3:
                    price = float(data[3])
                    change_pct = float(data[2]) * 100
                    change = price - float(data[2])
                    results['hk_stocks'][code.replace('hk', '')] = {
                        'name': name,
                        'price': price,
                        'change_pct': change_pct,
                        'change': change
                    }
                    print(f"  {name}: {price} ({change_pct:+.2f}%)")
except Exception as e:
    print(f"HK stock error: {e}")

# Save
with open('portfolio/market_data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nDone! A-shares: {len(results['a_stocks'])}, HK stocks: {len(results['hk_stocks'])}")
