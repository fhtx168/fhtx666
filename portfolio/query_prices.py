#!/usr/bin/env python3
"""Batch query stock prices using mx-data API directly."""
import json
import subprocess
import sys
import os
import time

os.environ["MX_APIKEY"] = "mkt_edXkhUWKFpgt_Sh21ZY4KqmCCY_lAHQs14iRauDZKWo"

MX_DATA_DIR = "/home/nami/.openclaw/skills/mx-data"
OUTPUT_DIR = "/home/nami/.openclaw/workspace/mx_data/output"

# A股51只 (stock name, code)
A_STOCKS = [
    ("比亚迪", "002594"), ("德赛西威", "002920"), ("中科曙光", "603019"),
    ("中芯国际", "688981"), ("沪硅产业", "688126"), ("华海诚科", "688535"),
    ("东微半导", "688261"), ("沪电股份", "002463"), ("兴森科技", "002436"),
    ("胜宏科技", "300476"), ("光库科技", "300620"), ("中石科技", "300684"),
    ("英维克", "002837"), ("通富微电", "002156"), ("华虹公司", "688347"),
    ("神州数码", "000034"), ("中科创达", "300496"), ("拓普集团", "601689"),
    ("华工科技", "000988"), ("中兴通讯", "000063"), ("埃斯顿", "002747"),
    ("斯莱克", "300382"), ("拓维信息", "002261"), ("云南锗业", "002428"),
    ("锡业股份", "000960"), ("兴业银锡", "000426"), ("中国铀业", "001280"),
    ("金诚信", "603979"), ("洛阳钼业", "603993"), ("西藏珠峰", "600338"),
    ("赣锋锂业", "002460"), ("西藏矿业", "000762"), ("中国巨石", "600176"),
    ("石英股份", "603688"), ("东阳光", "600673"), ("宝丰能源", "600989"),
    ("隆基绿能", "601012"), ("通威股份", "600438"), ("阳光电源", "300274"),
    ("科华数据", "002335"), ("雄韬股份", "002733"), ("国电南瑞", "600406"),
    ("迈瑞医疗", "300760"), ("康龙化成", "300759"), ("华大基因", "300676"),
    ("中国船舶", "600150"), ("中直股份", "600038"), ("军工龙头ETF", "512710"),
    ("福晶科技", "002222"), ("海德股份", "000567"), ("海南华铁", "603300"),
]

# 港股9只
HK_STOCKS = [
    ("阿里巴巴", "09988"), ("云顶新耀", "01952"), ("晶泰控股", "02228"),
    ("小米集团", "01810"), ("迈富时", "02556"), ("锦欣生殖", "01951"),
    ("福寿园", "01448"), ("药明生物", "02269"), ("中国电力", "02380"),
]

def query_stock(name):
    """Query a single stock's price, change%, and market cap."""
    query = f"{name} 最新价 涨跌幅 总市值"
    result = subprocess.run(
        ["python3", "./mx_data.py", query, OUTPUT_DIR],
        cwd=MX_DATA_DIR, capture_output=True, text=True, timeout=30
    )
    # Find the latest raw JSON file
    import glob
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "mx_data_*_raw.json")), key=os.path.getmtime, reverse=True)
    if not files:
        return None
    
    for f in files[:3]:  # check latest 3 files
        try:
            with open(f) as fp:
                data = json.load(fp)
            dtl = data.get('data', {}).get('data', {}).get('searchDataResultDTO', {}).get('dataTableDTOList', [])
            for item in dtl:
                etag = item.get('entityTagDTO', {})
                sec_name = etag.get('fullName', '')
                secu_code = etag.get('secuCode', '')
                market = etag.get('marketChar', '')
                table = item.get('table', {})
                
                # Check if this matches our stock
                if secu_code == code_map.get(name, ''):
                    vals = {}
                    for k, v in table.items():
                        if isinstance(v, list) and v:
                            vals[k] = v[0]
                        else:
                            vals[k] = v
                    return {
                        'name': sec_name,
                        'code': f"{secu_code}.{market}",
                        'price': vals.get('f2', vals.get('325898', 'N/A')),
                        'change': vals.get('f3', vals.get('326865', 'N/A')),
                        'mcap': vals.get('f20', vals.get('326809', 'N/A')),
                    }
        except:
            continue
    return None

# Build code map
code_map = {name: code for name, code in A_STOCKS + HK_STOCKS}

results = {}
total = len(A_STOCKS) + len(HK_STOCKS)
count = 0

print(f"Starting batch query for {total} stocks...", file=sys.stderr)

# Query in batches of 3 to balance speed and accuracy
def query_batch(names):
    query = " ".join(f"{n}" for n in names) + " 最新价 涨跌幅 总市值"
    result = subprocess.run(
        ["python3", "./mx_data.py", query, OUTPUT_DIR],
        cwd=MX_DATA_DIR, capture_output=True, text=True, timeout=45
    )
    
    # Find the latest raw JSON
    import glob
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "mx_data_*_raw.json")), key=os.path.getmtime, reverse=True)
    
    if not files:
        return
    
    for f in files[:1]:
        try:
            with open(f) as fp:
                data = json.load(fp)
            dtl = data.get('data', {}).get('data', {}).get('searchDataResultDTO', {}).get('dataTableDTOList', [])
            
            for item in dtl:
                etag = item.get('entityTagDTO', {})
                sec_name = etag.get('fullName', '')
                secu_code = etag.get('secuCode', '')
                market = etag.get('marketChar', '')
                sec_type = etag.get('entityTypeName', '')
                table = item.get('table', {})
                headName = table.get('headName', [''])[0] if isinstance(table.get('headName'), list) else table.get('headName', '')
                
                vals = {}
                for k, v in table.items():
                    if isinstance(v, list) and v:
                        vals[k] = v[0]
                    else:
                        vals[k] = v
                
                # Extract price, change, mcap
                price = vals.get('f2', vals.get('325898', ''))
                change = vals.get('f3', vals.get('326865', ''))
                mcap = vals.get('f20', vals.get('326809', ''))
                
                # Only use the f2/f3/f20 format (standard quotes) not the daily format
                if price and change:
                    # Clean up units
                    price_str = str(price).replace('元', '').replace(' ', '')
                    change_str = str(change)
                    mcap_str = str(mcap)
                    
                    # Check date - only use today's data
                    if '2026-04-29' in str(headName) or '.' in str(headName):
                        key = f"{secu_code}.{market}"
                        results[key] = {
                            'name': sec_name,
                            'code': key,
                            'price': price_str,
                            'change': change_str,
                            'mcap': mcap_str,
                        }
        except Exception as e:
            print(f"Error parsing {f}: {e}", file=sys.stderr)

# Process A股 in batches of 5
for i in range(0, len(A_STOCKS), 5):
    batch = A_STOCKS[i:i+5]
    batch_names = [n for n, c in batch]
    query_batch(batch_names)
    count += len(batch)
    print(f"Progress: {count}/{total}", file=sys.stderr)
    time.sleep(0.5)

# Process 港股 in batches of 3
for i in range(0, len(HK_STOCKS), 3):
    batch = HK_STOCKS[i:i+3]
    batch_names = [n for n, c in batch]
    query_batch(batch_names)
    count += len(batch)
    print(f"Progress: {count}/{total}", file=sys.stderr)
    time.sleep(0.5)

# Output results as JSON
print(json.dumps(results, ensure_ascii=False, indent=2))
print(f"\nResolved: {len(results)}/{total} stocks", file=sys.stderr)
