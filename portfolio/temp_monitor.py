# -*- coding: utf-8 -*-
# 盘中异动监控脚本

holdings = [
    {'name': '埃斯顿', 'code': 'SZ002747', 'price': 25.43, 'change': 7.12, 'market_cap': 6.36},
    {'name': '拓普集团', 'code': 'SH601689', 'price': 69.93, 'change': 7.45, 'market_cap': 69.93},
    {'name': '华海诚科', 'code': 'SH688535', 'price': 133.77, 'change': 15.49, 'market_cap': 63.59},
    {'name': '阳光电源', 'code': 'SZ300274', 'price': 152.95, 'change': 13.27, 'market_cap': 152.95},
    {'name': '锡业股份', 'code': 'SZ000960', 'price': 36.52, 'change': -6.17, 'market_cap': 21.91},
    {'name': '兴业银锡', 'code': 'SZ000426', 'price': 44.14, 'change': -8.37, 'market_cap': 26.48},
    {'name': '金诚信', 'code': 'SH603979', 'price': 62.95, 'change': -5.34, 'market_cap': 44.69},
    {'name': '中国巨石', 'code': 'SH600176', 'price': 33.86, 'change': -9.99, 'market_cap': 33.86},
    {'name': '云南锗业', 'code': 'SZ002428', 'price': 90.33, 'change': -7.07, 'market_cap': 72.26},
    {'name': '光库科技', 'code': 'SZ300620', 'price': 272.02, 'change': -5.10, 'market_cap': 97.93},
    {'name': '东微半导', 'code': 'SH688261', 'price': 83.26, 'change': -6.44, 'market_cap': 33.30},
    {'name': '福晶科技', 'code': 'SZ002222', 'price': 105.82, 'change': -6.98, 'market_cap': 69.84},
    {'name': '洛阳钼业', 'code': 'SH603993', 'price': 18.88, 'change': -5.84, 'market_cap': 52.86},
]

# 筛选异动
p0 = [s for s in holdings if s['change'] <= -9.5 or s['change'] >= 9.5]
p1_up = [s for s in holdings if s['change'] >= 5 and s['change'] < 9.5]
p1_down = [s for s in holdings if s['change'] <= -5 and s['change'] > -9.5]

print('=== P0 紧急异动 ===')
if p0:
    for s in p0:
        status = '[跌停]' if s['change'] < 0 else '[涨停]'
        print(f"{status} {s['name']}({s['code']}): {s['change']:+.2f}% 现价{s['price']}元 市值{s['market_cap']}万")
else:
    print('无')

print()
print('=== P1 重要异动（上涨）===')
if p1_up:
    for s in sorted(p1_up, key=lambda x: x['change'], reverse=True):
        print(f"[大涨] {s['name']}({s['code']}): {s['change']:+.2f}% 现价{s['price']}元 市值{s['market_cap']}万")
else:
    print('无')

print()
print('=== P1 重要异动（下跌）===')
if p1_down:
    for s in sorted(p1_down, key=lambda x: x['change']):
        print(f"[大跌] {s['name']}({s['code']}): {s['change']:+.2f}% 现价{s['price']}元 市值{s['market_cap']}万")
else:
    print('无')

print()
print(f"统计：P0 {len(p0)}只 | P1 上涨{len(p1_up)}只 | P1 下跌{len(p1_down)}只 | 合计{len(p0)+len(p1_up)+len(p1_down)}只")
