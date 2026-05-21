import json
import re
from datetime import datetime

# Load fetched prices
with open('portfolio/temp_prices.json', 'r', encoding='utf-8') as f:
    prices_data = json.load(f)

# Create price lookup by code
price_map = {}
for p in prices_data:
    price_map[p['code']] = p

# Read holdings line by line
holdings = []
with open('portfolio/holdings.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_a_section = False
in_hk_section = False

for line in lines:
    line = line.strip()
    
    # Detect section
    if '## A 股' in line:
        in_a_section = True
        in_hk_section = False
        continue
    elif '## 港股' in line:
        in_a_section = False
        in_hk_section = True
        continue
    elif line.startswith('## '):
        in_a_section = False
        in_hk_section = False
        continue
    
    # Skip non-data rows
    if not line.startswith('|') or '名称' in line or '---' in line:
        continue
    
    # Parse row
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 9:
        continue
    
    try:
        name = parts[0]
        code_full = parts[1]
        
        # Parse code (format: 300308.SZ or 09988.HK)
        if '.HK' in code_full:
            code = code_full.replace('.HK', '')  # Keep leading zero for HK
            exchange = 'HK'
            stock_type = 'HK'
        elif '.SZ' in code_full:
            code = code_full.replace('.SZ', '')
            exchange = 'SZ'
            stock_type = 'A'
        elif '.SH' in code_full:
            code = code_full.replace('.SH', '')
            exchange = 'SH'
            stock_type = 'A'
        else:
            continue
        
        # Get price from fetched data
        if code not in price_map:
            print(f'Warning: No price for {name} ({code_full})')
            continue
        
        p = price_map[code]
        price = p['price']
        change_pct = p['change_pct']
        
        # Parse other fields
        position = int(parts[4])
        cost = float(parts[5])
        
        # Parse floating P&L (format: +1.88 万 or -1.92 万)
        floating_pl_str = parts[6].replace('万', '').strip()
        floating_pl = float(floating_pl_str)
        
        # Parse total P&L
        total_pl_str = parts[7].replace('万', '').strip()
        total_pl = float(total_pl_str)
        
        # Calculate market value
        if stock_type == 'HK':
            market_value = round(price * position / 10000, 2)  # HKD
        else:
            market_value = round(price * position / 10000, 2)  # CNY
        
        holdings.append({
            'name': name,
            'code': code,
            'code_full': code_full,
            'exchange': exchange,
            'type': stock_type,
            'price': price,
            'change_pct': change_pct,
            'position': position,
            'cost': cost,
            'floating_pl': floating_pl,
            'total_pl': total_pl,
            'market_value': market_value
        })
        
    except Exception as e:
        print(f'Error parsing line: {line} - {e}')
        continue

print(f'Processed {len(holdings)} holdings ({sum(1 for h in holdings if h["type"]=="A")} A-shares, {sum(1 for h in holdings if h["type"]=="HK")} HK)')

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
today_pl_a = sum(h['market_value'] * h['change_pct'] / 100 for h in a_holdings)
today_pl_hk = sum(h['market_value'] * h['change_pct'] / 100 for h in hk_holdings)
today_pl = today_pl_a + today_pl_hk

# Find top gainers/losers
top_gainers = sorted([h for h in holdings if h['change_pct'] > 0], key=lambda x: x['change_pct'], reverse=True)[:5]
top_losers = sorted([h for h in holdings if h['change_pct'] < 0], key=lambda x: x['change_pct'])[:5]

# Top P&L contributors
top_profit = sorted(holdings, key=lambda x: x['floating_pl'], reverse=True)[:5]
top_loss = sorted(holdings, key=lambda x: x['floating_pl'])[:5]

# Generate report
today = datetime.now().strftime('%Y-%m-%d')
weekday = datetime.now().strftime('%A')
weekday_cn = {'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三', 'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'}[weekday]

report = f"""# 每日持仓跟踪

## {today}（{weekday_cn}）收盘

### 📊 大盘概览
- 上证指数：待更新
- 深证成指：待更新
- 创业板指：待更新
- 恒指：待更新
- 两市合计成交：待更新

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
- 今日盈亏：{today_pl_a:.2f}万
- 浮动盈亏：{sum(h['floating_pl'] for h in a_holdings):.2f}万

### 港股汇总
- 市值：{hk_market_value:.2f}万 HKD
- 今日盈亏：{today_pl_hk:.2f}万 HKD
- 浮动盈亏：{sum(h['floating_pl'] for h in hk_holdings):.2f}万 HKD

---

### 🔥 今日异动标的（|涨跌幅| >= 5%）

#### 涨停 / 大涨
| 标的 | 代码 | 现价 | 涨跌幅 | 持仓市值 | 盈亏影响 |
|------|------|------|--------|----------|----------|
"""

for h in sorted([x for x in holdings if x['change_pct'] >= 5], key=lambda x: x['change_pct'], reverse=True):
    pl_impact = h['market_value'] * h['change_pct'] / 100
    report += f"| {h['name']} | {h['code_full']} | {h['price']:.2f} | **{h['change_pct']:+.2f}%** | {h['market_value']:.2f}万 | {pl_impact:+.2f}万 |\n"

if not [x for x in holdings if x['change_pct'] >= 5]:
    report += "| 无 | - | - | - | - | - |\n"

report += """
#### 大跌
| 标的 | 代码 | 现价 | 涨跌幅 | 持仓市值 | 盈亏影响 |
|------|------|------|--------|----------|----------|
"""

for h in sorted([x for x in holdings if x['change_pct'] <= -5], key=lambda x: x['change_pct']):
    pl_impact = h['market_value'] * h['change_pct'] / 100
    report += f"| {h['name']} | {h['code_full']} | {h['price']:.2f} | **{h['change_pct']:+.2f}%** | {h['market_value']:.2f}万 | {pl_impact:+.2f}万 |\n"

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

### 📊 持仓明细（全部 A 股）

| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 市值 | 浮动盈亏 |
|------|------|------|------|------|------|----------|
"""

# All A-shares sorted by market value
a_sorted = sorted(a_holdings, key=lambda x: x['market_value'], reverse=True)
for h in a_sorted:
    report += f"| {h['name']} | {h['code_full']} | {h['price']:.2f} | {h['change_pct']:+.2f}% | {h['position']} | {h['market_value']:.2f}万 | {h['floating_pl']:+.2f}万 |\n"

report += f"""
---

### 📊 港股持仓

| 名称 | 代码 | 现价 | 涨跌 | 持仓 | 市值 | 浮动盈亏 |
|------|------|------|------|------|------|----------|
"""

# All HK stocks
hk_sorted = sorted(hk_holdings, key=lambda x: x['market_value'], reverse=True)
for h in hk_sorted:
    report += f"| {h['name']} | {h['code_full']} | {h['price']:.2f} | {h['change_pct']:+.2f}% | {h['position']} | {h['market_value']:.2f}万 | {h['floating_pl']:+.2f}万 |\n"

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

print(f'\nReport saved to portfolio/daily-tracking.md')
print(f'Total assets: {total_assets:.2f}万')
print(f'Today P&L: {today_pl:.2f}万')
print(f'Floating P&L: {total_floating_pl:.2f}万 ({total_floating_pl/principal*100:.2f}%)')
