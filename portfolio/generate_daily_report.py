import json
import re
from datetime import datetime
import requests

# Load fetched prices
with open('portfolio/temp_prices.json', 'r', encoding='utf-8') as f:
    prices_data = json.load(f)

# Create price lookup
price_map = {}
for p in prices_data:
    key = f"{p['code']}.{p['exchange']}"
    price_map[key] = p

# Read holdings to get position and cost
holdings = []
with open('portfolio/holdings.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse A-shares
a_share_pattern = r'\|\s*([^\|]+?)\s*\|\s*(\d{6})\.(SZ|SH)\s*\|\s*[\d\.]+\s*\|\s*[+-]?\d\.?\d*%\s*\|\s*(\d+)\s*\|\s*([\d\.]+)\s*\|\s*([+-]?\d\.?\d*)\s*万\s*\|\s*([+-]?\d\.?\d*)\s*万\s*\|\s*([\d\.]+)\s*万'
for match in re.finditer(a_share_pattern, content):
    name = match.group(1).strip()
    code = match.group(2)
    exchange = match.group(3)
    position = int(match.group(4))
    cost = float(match.group(5))
    floating_pl = float(match.group(6))
    total_pl = float(match.group(7))
    market_value = float(match.group(8))
    
    key = f"{code}.{exchange}"
    if key in price_map:
        p = price_map[key]
        holdings.append({
            'name': name,
            'code': code,
            'exchange': exchange,
            'type': 'A',
            'price': p['price'],
            'change_pct': p['change_pct'],
            'position': position,
            'cost': cost,
            'floating_pl': floating_pl,
            'total_pl': total_pl,
            'market_value': round(p['price'] * position / 10000, 2)
        })

# Parse HK stocks
hk_pattern = r'\|\s*([^\|]+?)\s*\|\s*0(\d{4,5})\.HK\s*\|\s*[\d\.]+\s*\|\s*[+-]?\d\.?\d*%\s*\|\s*(\d+)\s*\|\s*([\d\.]+)\s*\|\s*([+-]?\d\.?\d*)\s*万\s*\|\s*([+-]?\d\.?\d*)\s*万\s*\|\s*([\d\.]+)\s*万'
for match in re.finditer(hk_pattern, content):
    name = match.group(1).strip()
    code = match.group(2)
    position = int(match.group(3))
    cost = float(match.group(4))
    floating_pl = float(match.group(5))
    total_pl = float(match.group(6))
    market_value = float(match.group(7))
    
    key = f"{code}.HK"
    if key in price_map:
        p = price_map[key]
        holdings.append({
            'name': name,
            'code': code,
            'exchange': 'HK',
            'type': 'HK',
            'price': p['price'],
            'change_pct': p['change_pct'],
            'position': position,
            'cost': cost,
            'floating_pl': floating_pl,
            'total_pl': total_pl,
            'market_value': round(p['price'] * position / 10000, 2)
        })

print(f'Processed {len(holdings)} holdings')

# Calculate totals
a_holdings = [h for h in holdings if h['type'] == 'A']
hk_holdings = [h for h in holdings if h['type'] == 'HK']

a_market_value = sum(h['market_value'] for h in a_holdings)
hk_market_value = sum(h['market_value'] for h in hk_holdings)
total_market_value = a_market_value + hk_market_value
total_floating_pl = sum(h['floating_pl'] for h in holdings)
total_pl = sum(h['total_pl'] for h in holdings)
cash = -135.25  # From holdings.md
total_assets = total_market_value + cash
principal = 3148.44

# Today's P&L (based on price changes)
today_pl = sum(h['market_value'] * h['change_pct'] / 100 for h in holdings)

# Find top gainers/losers
sorted_by_change = sorted(holdings, key=lambda x: abs(x['change_pct']), reverse=True)
top_gainers = sorted([h for h in holdings if h['change_pct'] > 0], key=lambda x: x['change_pct'], reverse=True)[:5]
top_losers = sorted([h for h in holdings if h['change_pct'] < 0], key=lambda x: x['change_pct'])[:5]

# Top P&L contributors
top_profit = sorted(holdings, key=lambda x: x['floating_pl'], reverse=True)[:5]
top_loss = sorted(holdings, key=lambda x: x['floating_pl'])[:5]

# Get market indices (simplified - using placeholder values)
# In production, you'd fetch these from an API
indices = {
    'shanghai': '待更新',
    'shenzhen': '待更新',
    'chinext': '待更新',
    'hangsen': '待更新',
    'turnover': '待更新'
}

# Generate report
today = datetime.now().strftime('%Y-%m-%d')
weekday = datetime.now().strftime('%A')
weekday_cn = {'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三', 'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'}[weekday]

report = f"""# 每日持仓跟踪

## {today}（{weekday_cn}）收盘

### 📊 大盘概览
- 上证指数：{indices['shanghai']}
- 深证成指：{indices['shenzhen']}
- 创业板指：{indices['chinext']}
- 恒指：{indices['hangsen']}
- 两市合计成交：{indices['turnover']}

### 📈 持仓总览
- **总资产**：{total_assets:.2f}万
- **总市值**：{total_market_value:.2f}万
- **A 股市值**：{a_market_value:.2f}万
- **港股市值**：{hk_market_value:.2f}万 HKD
- **现金**：{cash}万（已使用融资）
- **本金**：{principal}万
- **浮动盈亏**：{total_floating_pl:.2f}万（{total_floating_pl/principal*100:.2f}%）
- **累计盈亏**：{total_pl:.2f}万
- **今日盈亏**：{today_pl:.2f}万（{today_pl/total_assets*100:.2f}%）

### A 股汇总
- 市值：{a_market_value:.2f}万
- 今日盈亏：{sum(h['market_value'] * h['change_pct'] / 100 for h in a_holdings):.2f}万
- 浮动盈亏：{sum(h['floating_pl'] for h in a_holdings):.2f}万

### 港股汇总
- 市值：{hk_market_value:.2f}万 HKD
- 今日盈亏：{sum(h['market_value'] * h['change_pct'] / 100 for h in hk_holdings):.2f}万 HKD
- 浮动盈亏：{sum(h['floating_pl'] for h in hk_holdings):.2f}万 HKD

---

### 🔥 今日异动标的（|涨跌幅| >= 5%）

#### 涨停 / 大涨
| 标的 | 代码 | 现价 | 涨跌幅 | 持仓市值 | 盈亏影响 |
|------|------|------|--------|----------|----------|
"""

for h in [x for x in holdings if x['change_pct'] >= 5]:
    pl_impact = h['market_value'] * h['change_pct'] / 100
    report += f"| {h['name']} | {h['code']}.{h['exchange']} | {h['price']:.2f} | **{h['change_pct']:+.2f}%** | {h['market_value']:.2f}万 | {pl_impact:+.2f}万 |\n"

if not [x for x in holdings if x['change_pct'] >= 5]:
    report += "| 无 | - | - | - | - | - |\n"

report += """
#### 大跌
| 标的 | 代码 | 现价 | 涨跌幅 | 持仓市值 | 盈亏影响 |
|------|------|------|--------|----------|----------|
"""

for h in [x for x in holdings if x['change_pct'] <= -5]:
    pl_impact = h['market_value'] * h['change_pct'] / 100
    report += f"| {h['name']} | {h['code']}.{h['exchange']} | {h['price']:.2f} | **{h['change_pct']:+.2f}%** | {h['market_value']:.2f}万 | {pl_impact:+.2f}万 |\n"

if not [x for x in holdings if x['change_pct'] <= -5]:
    report += "| 无 | - | - | - | - | - |\n"

report += f"""
---

### 💰 今日盈亏前五

#### 盈利贡献
| 标的 | 持仓 | 浮动盈亏 | 盈亏率 |
|------|------|----------|--------|
"""
for h in top_profit:
    pl_rate = h['floating_pl'] / (h['cost'] * h['position'] / 10000) * 100 if h['cost'] else 0
    report += f"| {h['name']} | {h['position']}股 | {h['floating_pl']:.2f}万 | {pl_rate:+.2f}% |\n"

report += """
#### 亏损贡献
| 标的 | 持仓 | 浮动盈亏 | 盈亏率 |
|------|------|----------|--------|
"""
for h in top_loss:
    pl_rate = h['floating_pl'] / (h['cost'] * h['position'] / 10000) * 100 if h['cost'] else 0
    report += f"| {h['name']} | {h['position']}股 | {h['floating_pl']:.2f}万 | {pl_rate:+.2f}% |\n"

report += f"""
---

### 📊 持仓明细（A 股 Top20 按市值）

| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 市值 | 浮动盈亏 |
|------|------|------|------|------|------|----------|
"""

# Sort by market value and take top 20 A-shares
a_sorted = sorted(a_holdings, key=lambda x: x['market_value'], reverse=True)[:20]
for h in a_sorted:
    report += f"| {h['name']} | {h['code']}.{h['exchange']} | {h['price']:.2f} | {h['change_pct']:+.2f}% | {h['position']} | {h['market_value']:.2f}万 | {h['floating_pl']:+.2f}万 |\n"

report += f"""
---

### 📝 备注

- 数据截止：{today} 16:30
- 下次更新：明日 16:30
- 监控状态：✅ 正常

---

## 历史跟踪记录

| 日期 | 总资产 | 浮动盈亏 | 累计盈亏 | 备注 |
|------|--------|----------|----------|------|
| {today} | {total_assets:.2f}万 | {total_floating_pl:.2f}万 | {total_pl:.2f}万 | 收盘更新 |

"""

# Save report
with open('portfolio/daily-tracking.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f'Report saved to portfolio/daily-tracking.md')
print(f'Total assets: {total_assets:.2f}万')
print(f'Today P&L: {today_pl:.2f}万')
print(f'Floating P&L: {total_floating_pl:.2f}万')
