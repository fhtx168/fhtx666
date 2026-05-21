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

# Read holdings file
with open('portfolio/holdings.md', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Update the summary section with new totals
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Update date line
    if line.startswith('> 最后更新：'):
        new_lines.append(f'> 最后更新：{datetime.now().strftime("%Y-%m-%d")} 收盘')
        i += 1
        continue
    
    # Update total market value in summary table
    if '| 总市值 |' in line and '万' in line:
        # Will recalculate later
        pass
    
    # Parse and update stock rows
    if line.strip().startswith('|') and not '名称' in line and not '---' in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 10:
            name = parts[1].strip()
            code_full = parts[2].strip()
            
            # Extract code
            if '.HK' in code_full:
                code = code_full.replace('.HK', '')
            elif '.SZ' in code_full:
                code = code_full.replace('.SZ', '')
            elif '.SH' in code_full:
                code = code_full.replace('.SH', '')
            else:
                new_lines.append(line)
                i += 1
                continue
            
            # Get new price
            if code in price_map:
                p = price_map[code]
                new_price = p['price']
                new_change = p['change_pct']
                
                # Get position from existing row
                try:
                    position = int(parts[5].strip())
                    cost = float(parts[6].strip())
                    
                    # Calculate new market value
                    new_market_value = round(new_price * position / 10000, 2)
                    
                    # Keep existing floating P&L and total P&L (parts[7] and parts[8])
                    # These would need proper recalculation but keeping for now
                    floating_pl = parts[7].strip()
                    total_pl = parts[8].strip()
                    
                    # Rebuild row
                    new_row = f"| {name} | {code_full} | {new_price:.2f} | {new_change:+.2f}% | {position} | {cost:.2f} | {floating_pl} | {total_pl} | {new_market_value:.2f}万 |"
                    new_lines.append(new_row)
                    i += 1
                    continue
                except:
                    pass
    
    new_lines.append(line)
    i += 1

# Now recalculate totals
updated_content = '\n'.join(new_lines)

# Re-read to calculate totals
a_market_value = 0
hk_market_value = 0
a_floating_pl = 0
hk_floating_pl = 0
a_total_pl = 0
hk_total_pl = 0

for line in updated_content.split('\n'):
    if line.strip().startswith('|') and not '名称' in line and not '---' in line and not '指标' in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 10:
            try:
                code_full = parts[2].strip()
                market_value_str = parts[9].strip().replace('万', '')
                floating_pl_str = parts[7].strip().replace('万', '')
                total_pl_str = parts[8].strip().replace('万', '')
                
                market_value = float(market_value_str)
                floating_pl = float(floating_pl_str)
                total_pl = float(total_pl_str)
                
                if '.HK' in code_full:
                    hk_market_value += market_value
                    hk_floating_pl += floating_pl
                    hk_total_pl += total_pl
                else:
                    a_market_value += market_value
                    a_floating_pl += floating_pl
                    a_total_pl += total_pl
            except:
                continue

total_market_value = a_market_value + hk_market_value
total_assets = total_market_value - 135.25  # cash
total_floating_pl = a_floating_pl + hk_floating_pl
total_pl = a_total_pl + hk_total_pl
principal = 3148.44

# Update summary section
today = datetime.now().strftime('%Y-%m-%d')
summary_update = f"""
## 总览

| 指标 | 数值 |
|------|------|
| 总资产 | {total_assets:.2f}万 |
| 总市值 | {total_market_value:.2f}万 |
| 现金 | -135.25 万（已使用融资）|
| 本金 | {principal}万 |
| 浮动盈亏 | {total_floating_pl:+.2f}万（{total_floating_pl/principal*100:.2f}%）|
| 累计盈亏 | {total_pl:+.2f}万（{total_pl/principal*100:.2f}%）|

### A 股
- 市值：{a_market_value:.2f}万
- 浮动盈亏：{a_floating_pl:+.2f}万（{a_floating_pl/principal*100:.2f}%）
- 累计盈亏：{a_total_pl:+.2f}万

### 港股
- 市值：{hk_market_value:.2f}万 HKD
- 浮动盈亏：{hk_floating_pl:+.2f}万 HKD
- 累计盈亏：{hk_total_pl:+.2f}万 HKD
"""

# Find and replace the summary section
content_lines = updated_content.split('\n')
new_content_lines = []
in_summary = False
skip_until_section = False

for line in content_lines:
    if line.strip() == '## 总览':
        in_summary = True
        continue
    if in_summary and line.strip().startswith('## ') and '总览' not in line:
        in_summary = False
        new_content_lines.append(summary_update.strip())
        new_content_lines.append('')
        new_content_lines.append(line)
        continue
    if not in_summary:
        new_content_lines.append(line)

# If we never exited summary section, append at the end
if in_summary:
    new_content_lines.append(summary_update.strip())

final_content = '\n'.join(new_content_lines)

# Update today's P&L in summary
# Calculate today's P&L from price changes
today_pl = 0
for line in final_content.split('\n'):
    if line.strip().startswith('|') and not '名称' in line and not '---' in line and not '指标' in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            try:
                change_str = parts[3].strip().replace('%', '')
                market_value_str = parts[9].strip().replace('万', '') if len(parts) > 9 else '0'
                change_pct = float(change_str)
                market_value = float(market_value_str)
                today_pl += market_value * change_pct / 100
            except:
                continue

# Add today's P&L to summary
final_content = final_content.replace(
    '| 累计盈亏 |',
    f'| 今日盈亏 | {today_pl:+.2f}万（{today_pl/total_assets*100:.2f}%）|\n| 累计盈亏 |'
)

# Save
with open('portfolio/holdings.md', 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f'holdings.md updated')
print(f'Total assets: {total_assets:.2f}万')
print(f'Today P&L: {today_pl:.2f}万')
print(f'Floating P&L: {total_floating_pl:+.2f}万')
