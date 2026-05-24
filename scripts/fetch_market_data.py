# -*- coding: utf-8 -*-
"""
2026-05-22 市场数据抓取脚本
"""
import akshare as ak
import pandas as pd
from datetime import datetime
import json

def fetch_market_data():
    result = {
        'date': '2026-05-22',
        'indices': {},
        'market_stats': {},
        'industries': {'top_gainers': [], 'top_losers': []},
        'concepts': {'top_gainers': [], 'top_losers': []},
        'fund_flow': [],
        'limit_up_down': {}
    }
    
    print('=== 2026-05-22 市场数据抓取 ===\n')
    
    # 1. 主要指数
    print('【1. 主要指数】')
    try:
        # 上证指数
        index_sh = ak.stock_zh_index_daily(symbol='sh000001')
        # 深证成指
        index_sz = ak.stock_zh_index_daily(symbol='sz399001')
        # 创业板指
        index_cyb = ak.stock_zh_index_daily(symbol='sz399006')
        # 科创 50
        index_kc50 = ak.stock_zh_index_daily(symbol='sh000688')
        
        result['indices'] = {
            '上证指数': {'close': float(index_sh.iloc[-1]['close']), 'change': float(index_sh.iloc[-1]['change'])},
            '深证成指': {'close': float(index_sz.iloc[-1]['close']), 'change': float(index_sz.iloc[-1]['change'])},
            '创业板指': {'close': float(index_cyb.iloc[-1]['close']), 'change': float(index_cyb.iloc[-1]['change'])},
            '科创 50': {'close': float(index_kc50.iloc[-1]['close']), 'change': float(index_kc50.iloc[-1]['change'])}
        }
        
        print(f"上证指数：{result['indices']['上证指数']['close']:.2f} ({result['indices']['上证指数']['change']:.2f}%)")
        print(f"深证成指：{result['indices']['深证成指']['close']:.2f} ({result['indices']['深证成指']['change']:.2f}%)")
        print(f"创业板指：{result['indices']['创业板指']['close']:.2f} ({result['indices']['创业板指']['change']:.2f}%)")
        print(f"科创 50: {result['indices']['科创 50']['close']:.2f} ({result['indices']['科创 50']['change']:.2f}%)")
    except Exception as e:
        print(f'指数数据获取失败：{e}')
        result['indices_error'] = str(e)
    
    print()
    
    # 2. 市场涨跌分布
    print('【2. 市场涨跌分布】')
    try:
        market_activity = ak.stock_market_activity_legu()
        # 解析涨跌分布数据
        if isinstance(market_activity, pd.DataFrame) and len(market_activity) > 0:
            print(market_activity)
            result['market_stats'] = market_activity.to_dict('records')
    except Exception as e:
        print(f'涨跌分布获取失败：{e}')
        # 尝试备用方法
        try:
            # 获取实时行情
            realtime = ak.stock_zh_a_spot_em()
            up_count = len(realtime[realtime['涨跌幅'] > 0])
            down_count = len(realtime[realtime['涨跌幅'] < 0])
            flat_count = len(realtime[realtime['涨跌幅'] == 0])
            result['market_stats'] = {
                '上涨家数': up_count,
                '下跌家数': down_count,
                '平盘家数': flat_count,
                '总家数': len(realtime)
            }
            print(f"上涨：{up_count}家，下跌：{down_count}家，平盘：{flat_count}家")
        except Exception as e2:
            print(f'备用方法也失败：{e2}')
            result['market_stats_error'] = str(e2)
    
    print()
    
    # 3. 行业板块
    print('【3. 行业板块涨跌幅】')
    try:
        industry = ak.stock_board_industry_name_em()
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
    except Exception as e:
        print(f'行业板块获取失败：{e}')
        result['industries_error'] = str(e)
    
    print()
    
    # 4. 概念板块
    print('【4. 概念板块涨跌幅】')
    try:
        concept = ak.stock_board_concept_name_em()
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
    
    # 5. 资金流向
    print('【5. 主力资金净流入前五】')
    try:
        flow = ak.stock_individual_fund_flow_rank(indicator='今日')
        if isinstance(flow, pd.DataFrame) and len(flow) > 0:
            top_flow = flow.head(5)
            result['fund_flow'] = top_flow.to_dict('records')
            
            for _, row in top_flow.iterrows():
                print(f"  {row.get('名称', row.get('股票', 'N/A'))}: {row.get('今日主力净流入', 'N/A')}万元")
    except Exception as e:
        print(f'资金流向获取失败：{e}')
        result['fund_flow_error'] = str(e)
    
    print()
    
    # 6. 涨跌停家数
    print('【6. 涨跌停家数】')
    try:
        # 涨停
        zt_df = ak.stock_zt_pool_em(date='20260522')
        zt_count = len(zt_df) if isinstance(zt_df, pd.DataFrame) else 0
        
        # 跌停
        dt_df = ak.stock_dt_pool_em(date='20260522')
        dt_count = len(dt_df) if isinstance(dt_df, pd.DataFrame) else 0
        
        result['limit_up_down'] = {
            '涨停家数': zt_count,
            '跌停家数': dt_count
        }
        
        print(f"涨停：{zt_count}家，跌停：{dt_count}家")
    except Exception as e:
        print(f'涨跌停获取失败：{e}')
        result['limit_up_down_error'] = str(e)
    
    print()
    print('=== 数据抓取完成 ===')
    
    # 保存为 JSON
    with open('C:/Users/Admin/opcclawai/project/scripts/market_data_20260522.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f'数据已保存至：market_data_20260522.json')
    
    return result

if __name__ == '__main__':
    fetch_market_data()
