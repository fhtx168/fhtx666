import akshare as ak
import json

results = {}

# 1. 主要指数
indices = {
    '上证指数': 'sh000001',
    '深证成指': 'sz399001',
    '创业板指': 'sz399006',
    '科创 50': 'sh000688'
}

results['indices'] = {}
for name, symbol in indices.items():
    try:
        df = ak.stock_zh_index_daily(symbol=symbol)
        latest = df.iloc[-1]
        close = float(latest['close'])
        open_p = float(latest['open'])
        change = close - open_p
        pct = change / open_p * 100
        vol = float(latest['volume']) / 100000000
        results['indices'][name] = {
            'close': close,
            'change': f"{change:.2f} ({pct:.2f}%)",
            'volume': f"{vol:.2f}亿"
        }
    except Exception as e:
        results['indices'][name] = {'error': str(e)}

# 2. 涨停数据
try:
    df_zt = ak.stock_zt_pool_em(date='20260528')
    results['limit_up'] = len(df_zt)
except Exception as e:
    results['limit_up'] = f"Error: {e}"

# 3. 行业板块
try:
    df_ind = ak.stock_board_industry_name_em()
    df_sorted = df_ind.sort_values('涨跌幅', ascending=False)
    results['industry_top'] = []
    for _, row in df_sorted.head(5).iterrows():
        results['industry_top'].append({'name': row['板块名称'], 'change': row['涨跌幅']})
    results['industry_bottom'] = []
    for _, row in df_sorted.tail(5).iterrows():
        results['industry_bottom'].append({'name': row['板块名称'], 'change': row['涨跌幅']})
except Exception as e:
    results['industry'] = f"Error: {e}"

# 4. 资金流向
try:
    df_flow = ak.stock_individual_fund_flow_rank()
    results['capital_flow'] = []
    for _, row in df_flow.head(5).iterrows():
        results['capital_flow'].append({'name': row['名称'], 'inflow': row['主力净流入']})
except Exception as e:
    results['capital_flow'] = f"Error: {e}"

# 5. 概念板块
try:
    df_concept = ak.stock_board_concept_name_em()
    df_sorted = df_concept.sort_values('涨跌幅', ascending=False)
    results['concept_top'] = []
    for _, row in df_sorted.head(5).iterrows():
        results['concept_top'].append({'name': row['板块名称'], 'change': row['涨跌幅']})
except Exception as e:
    results['concept'] = f"Error: {e}"

print(json.dumps(results, ensure_ascii=False, indent=2))
