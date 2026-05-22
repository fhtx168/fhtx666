# -*- coding: utf-8 -*-
"""每日持仓更新脚本 - 获取全部持仓股实时行情"""
import akshare as ak
import pandas as pd
from datetime import datetime

# A 股持仓代码列表（46 只）
a_stocks = [
    "300308.SZ", "600584.SH", "002916.SZ", "688082.SH", "688012.SH",
    "300398.SZ", "600989.SH", "002261.SZ", "002747.SZ", "002920.SZ",
    "002594.SZ", "002463.SZ", "601689.SH", "603019.SH", "000960.SZ",
    "000426.SZ", "688981.SH", "603979.SH", "688126.SH", "688535.SH",
    "600176.SH", "600673.SH", "300684.SZ", "300476.SZ", "002428.SZ",
    "300620.SZ", "001280.SZ", "688261.SH", "002837.SZ", "300274.SZ",
    "002222.SZ", "002436.SZ", "002335.SZ", "000063.SZ", "300496.SZ",
    "600406.SH", "603300.SH", "002156.SZ", "600338.SH", "688347.SH",
    "603993.SH", "000762.SZ", "002733.SZ", "000988.SZ", "600150.SH",
    "000034.SZ"
]

# 港股持仓代码列表（9 只）
hk_stocks = [
    "09988.HK", "01952.HK", "02228.HK", "01810.HK", "02556.HK",
    "01951.HK", "01448.HK", "02269.HK", "02380.HK"
]

def get_a_stock_price(code):
    """获取 A 股实时行情"""
    try:
        # 移除.SZ/.SH 后缀
        symbol = code.replace(".SZ", "").replace(".SH", "")
        df = ak.stock_zh_a_spot_em()
        match = df[df['代码'] == symbol]
        if len(match) > 0:
            row = match.iloc[0]
            return {
                'name': row['名称'],
                'price': row['最新价'],
                'change_pct': row['涨跌幅'],
                'change': row['涨跌额']
            }
    except Exception as e:
        print(f"Error fetching {code}: {e}")
    return None

def get_hk_stock_price(code):
    """获取港股实时行情"""
    try:
        # 移除.HK 后缀
        symbol = code.replace(".HK", "")
        df = ak.stock_hk_spot()
        match = df[df['代码'] == int(symbol)]
        if len(match) > 0:
            row = match.iloc[0]
            return {
                'name': row['名称'],
                'price': row['最新价'],
                'change_pct': row['涨跌幅'],
                'change': row['涨跌额']
            }
    except Exception as e:
        print(f"Error fetching {code}: {e}")
    return None

def get_index_data():
    """获取大盘指数"""
    try:
        df = ak.index_zh_a_spot_em()
        indices = {}
        for _, row in df.iterrows():
            if '上证指数' in row['名称']:
                indices['shanghai'] = {'price': row['最新价'], 'change_pct': row['涨跌幅']}
            elif '深证成指' in row['名称']:
                indices['shenzhen'] = {'price': row['最新价'], 'change_pct': row['涨跌幅']}
            elif '创业板指' in row['名称']:
                indices['chiext'] = {'price': row['最新价'], 'change_pct': row['涨跌幅']}
        return indices
    except:
        return {}

if __name__ == "__main__":
    print(f"开始获取行情数据... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取 A 股行情
    print("获取 A 股行情...")
    a_results = {}
    for code in a_stocks:
        data = get_a_stock_price(code)
        if data:
            a_results[code] = data
            print(f"  {code}: {data['name']} = {data['price']} ({data['change_pct']}%)")
    
    # 获取港股行情
    print("\n获取港股行情...")
    hk_results = {}
    for code in hk_stocks:
        data = get_hk_stock_price(code)
        if data:
            hk_results[code] = data
            print(f"  {code}: {data['name']} = {data['price']} ({data['change_pct']}%)")
    
    # 获取大盘指数
    print("\n获取大盘指数...")
    indices = get_index_data()
    
    # 输出结果
    print("\n" + "="*60)
    print("行情数据获取完成")
    print(f"A 股成功：{len(a_results)}/{len(a_stocks)}")
    print(f"港股成功：{len(hk_results)}/{len(hk_stocks)}")
    
    # 保存为 JSON 供后续使用
    import json
    output = {
        'timestamp': datetime.now().isoformat(),
        'indices': indices,
        'a_stocks': a_results,
        'hk_stocks': hk_results
    }
    
    with open('portfolio/market_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到 portfolio/market_data.json")
