# -*- coding: utf-8 -*-
"""
市场数据每日抓取脚本 - 2026-05-25 更新版
用于 cron 定时任务获取 A 股收盘数据
"""
import akshare as ak
import pandas as pd
from datetime import datetime
import json
import sys
import os

def fetch_market_data(target_date='2026-05-25'):
    """获取市场数据并保存"""
    
    date_str = target_date.replace('-', '')
    output_dir = 'C:/Users/Admin/opcclawai/project/portfolio'
    os.makedirs(output_dir, exist_ok=True)
    
    result = {
        'date': target_date,
        'indices': {},
        'market_stats': {},
        'industries': {'top_gainers': [], 'top_losers': []},
        'concepts': {'top_gainers': [], 'top_losers': []},
        'fund_flow': [],
        'limit_up_down': {},
        'all_stocks': []
    }
    
    print(f'=== {target_date} 市场数据抓取 ===\n')
    
    # 1. 主要指数 - 使用指数实时行情
    print('【1. 主要指数】')
    try:
        # 获取全部指数行情
        index_df = ak.stock_zh_index_spot_em()
        
        indices_map = {
            '上证指数': 'sh000001',
            '深证成指': 'sz399001', 
            '创业板指': 'sz399006',
            '科创 50': 'sh000688'
        }
        
        for name, symbol in indices_map.items():
            try:
                row = index_df[index_df['代码'] == symbol].iloc[0]
                result['indices'][name] = {
                    'close': float(row.get('最新价', 0)),
                    'change': float(row.get('涨跌幅', 0))
                }
                print(f"{name}: {result['indices'][name]['close']:.2f} ({result['indices'][name]['change']:.2f}%)")
            except Exception as e:
                print(f"  {name}获取失败：{e}")
                continue
                
    except Exception as e:
        print(f'指数数据获取失败：{e}')
        result['indices_error'] = str(e)
    
    print()
    
    # 2. 市场涨跌分布 - 使用 A 股实时行情（带重试）
    print('【2. 市场涨跌分布】')
    for attempt in range(3):
        try:
            realtime = ak.stock_zh_a_spot_em()
            if len(realtime) > 0:
                up_count = len(realtime[realtime['涨跌幅'] > 0])
                down_count = len(realtime[realtime['涨跌幅'] < 0])
                flat_count = len(realtime[realtime['涨跌幅'] == 0])
                
                result['market_stats'] = {
                    '上涨家数': int(up_count),
                    '下跌家数': int(down_count),
                    '平盘家数': int(flat_count),
                    '总家数': len(realtime)
                }
                print(f"上涨：{up_count}家，下跌：{down_count}家，平盘：{flat_count}家，总计：{len(realtime)}家")
                
                # 保存全部股票数据
                result['all_stocks'] = realtime.to_dict('records')
                break
        except Exception as e:
            print(f'涨跌分布获取失败 (尝试{attempt+1}/3): {e}')
            if attempt < 2:
                import time
                time.sleep(2)
            else:
                result['market_stats_error'] = str(e)
    
    print()
    
    # 3. 行业板块 - 带重试
    print('【3. 行业板块涨跌幅】')
    for attempt in range(3):
        try:
            industry = ak.stock_board_industry_name_em()
            if len(industry) > 0:
                industry_sorted = industry.sort_values('涨跌幅', ascending=False)
                
                top_gainers = industry_sorted.head(5)
                top_losers = industry_sorted.tail(5)
                
                result['industries']['top_gainers'] = top_gainers[['板块名称', '涨跌幅']].to_dict('records')
                result['industries']['top_losers'] = top_losers[['板块名称', '涨跌幅']].to_dict('records')
                
                print('涨幅前五:')
                for _, row in top_gainers.iterrows():
                    print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
                print('跌幅前五:')
                for _, row in top_losers.iterrows():
                    print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
                break
        except Exception as e:
            print(f'行业板块获取失败 (尝试{attempt+1}/3): {e}')
            if attempt < 2:
                import time
                time.sleep(2)
            else:
                result['industries_error'] = str(e)
    
    print()
    
    # 4. 概念板块
    print('【4. 概念板块涨跌幅】')
    try:
        concept = ak.stock_board_concept_name_em()
        if len(concept) > 0:
            concept_sorted = concept.sort_values('涨跌幅', ascending=False)
            
            result['concepts']['top_gainers'] = concept_sorted.head(5)[['板块名称', '涨跌幅']].to_dict('records')
            result['concepts']['top_losers'] = concept_sorted.tail(5)[['板块名称', '涨跌幅']].to_dict('records')
            
            print('概念涨幅前五:')
            for _, row in concept_sorted.head(5).iterrows():
                print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
    except Exception as e:
        print(f'概念板块获取失败：{e}')
        result['concepts_error'] = str(e)
    
    print()
    
    # 5. 资金流向 - 带重试
    print('【5. 主力资金净流入前五】')
    for attempt in range(3):
        try:
            flow = ak.stock_individual_fund_flow_rank(indicator='今日')
            if len(flow) > 0:
                top_flow = flow.head(5)
                result['fund_flow'] = top_flow.to_dict('records')
                
                for _, row in top_flow.iterrows():
                    name = row.get('名称', row.get('股票', 'N/A'))
                    flow_val = row.get('今日主力净流入', 'N/A')
                    print(f"  {name}: {flow_val}万元")
                break
        except Exception as e:
            print(f'资金流向获取失败 (尝试{attempt+1}/3): {e}')
            if attempt < 2:
                import time
                time.sleep(2)
            else:
                result['fund_flow_error'] = str(e)
    
    print()
    
    # 6. 涨跌停家数
    print('【6. 涨跌停家数】')
    try:
        zt_df = ak.stock_zt_pool_em(date=date_str)
        zt_count = len(zt_df) if isinstance(zt_df, pd.DataFrame) else 0
        
        # 跌停池 - 使用正确的 API
        try:
            dt_df = ak.stock_zt_pool_dtgc_em(date=date_str)
            dt_count = len(dt_df) if isinstance(dt_df, pd.DataFrame) else 0
        except:
            dt_count = 0
        
        result['limit_up_down'] = {
            '涨停家数': int(zt_count),
            '跌停家数': int(dt_count)
        }
        
        print(f"涨停：{zt_count}家，跌停：{dt_count}家")
    except Exception as e:
        print(f'涨跌停获取失败：{e}')
        result['limit_up_down_error'] = str(e)
    
    print()
    print('=== 数据抓取完成 ===')
    
    # 保存为 JSON（完整数据）
    json_path = f'{output_dir}/market_data_{date_str}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'完整数据已保存：{json_path}')
    
    # 保存为 CSV（仅股票数据）
    if result['all_stocks']:
        df_stocks = pd.DataFrame(result['all_stocks'])
        csv_path = f'{output_dir}/market_data_{date_str}.csv'
        df_stocks.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f'股票数据已保存：{csv_path}')
    
    # 更新 daily-tracking.md
    update_daily_tracking(result, target_date)
    
    return result

def update_daily_tracking(data, date_str):
    """更新 daily-tracking.md 的大盘概览"""
    tracking_path = 'C:/Users/Admin/opcclawai/project/portfolio/daily-tracking.md'
    
    # 生成概览文本
    overview = f"""
## {date_str} 市场概览

### 主要指数
| 指数 | 收盘价 | 涨跌幅 |
|------|--------|--------|
"""
    for name, vals in data.get('indices', {}).items():
        overview += f"| {name} | {vals.get('close', 'N/A'):.2f} | {vals.get('change', 'N/A'):.2f}% |\n"
    
    stats = data.get('market_stats', {})
    overview += f"""
### 涨跌分布
- 上涨：{stats.get('上涨家数', 'N/A')}家
- 下跌：{stats.get('下跌家数', 'N/A')}家
- 平盘：{stats.get('平盘家数', 'N/A')}家

### 涨跌停
- 涨停：{data.get('limit_up_down', {}).get('涨停家数', 'N/A')}家
- 跌停：{data.get('limit_up_down', {}).get('跌停家数', 'N/A')}家

### 行业涨幅前五
"""
    for item in data.get('industries', {}).get('top_gainers', [])[:5]:
        overview += f"- {item.get('板块名称', 'N/A')}: {item.get('涨跌幅', 'N/A'):.2f}%\n"

    overview += "\n### 概念涨幅前五\n"
    for item in data.get('concepts', {}).get('top_gainers', [])[:5]:
        overview += f"- {item.get('板块名称', 'N/A')}: {item.get('涨跌幅', 'N/A'):.2f}%\n"
    
    overview += "\n### 主力资金净流入前五\n"
    for item in data.get('fund_flow', [])[:5]:
        name = item.get('名称', item.get('股票', 'N/A'))
        flow = item.get('今日主力净流入', 'N/A')
        overview += f"- {name}: {flow}万元\n"
    
    overview += "\n---\n"
    
    # 读取现有文件
    try:
        with open(tracking_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有今日数据
        if f'## {date_str} 市场概览' in content:
            print(f'{date_str} 数据已存在，跳过更新')
            return
        
        # 添加到文件开头
        new_content = f"# 每日市场跟踪\n{overview}\n{content.split('# 每日市场跟踪')[1] if '# 每日市场跟踪' in content else ''}"
        
        with open(tracking_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'已更新：{tracking_path}')
        
    except Exception as e:
        print(f'更新 daily-tracking 失败：{e}')
        # 创建新文件
        with open(tracking_path, 'w', encoding='utf-8') as f:
            f.write(f"# 每日市场跟踪\n{overview}")
        print(f'已创建：{tracking_path}')

if __name__ == '__main__':
    date_arg = sys.argv[1] if len(sys.argv) > 1 else '2026-05-25'
    fetch_market_data(date_arg)
