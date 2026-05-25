import akshare as ak
import pandas as pd
from datetime import datetime

print("=== 2026-05-25 市场数据 ===\n")

# 获取指数数据
indices = {
    '上证指数': 'sh000001',
    '深证成指': 'sz399001', 
    '创业板指': 'sz399006',
    '科创 50': 'sh000688'
}

print("【主要指数】")
for name, code in indices.items():
    try:
        df = ak.stock_zh_index_daily(symbol=code)
        close = round(df.iloc[-1]['close'], 2)
        change = round((df.iloc[-1]['close'] - df.iloc[-2]['close']) / df.iloc[-2]['close'] * 100, 2)
        print(f"{name}: {close}点 ({change:+.2f}%)")
    except Exception as e:
        print(f"{name}: 获取失败")

# 获取涨跌停家数
print("\n【涨跌停统计】")
try:
    today = datetime.now().strftime('%Y%m%d')
    zt_df = ak.stock_zt_pool_em(date=today)
    dt_df = ak.stock_zt_pool_dtgc_em(date=today)
    print(f"涨停家数：{len(zt_df)}家")
    print(f"跌停家数：{len(dt_df)}家")
except Exception as e:
    print(f"获取失败：{e}")

# 获取行业板块
print("\n【行业涨幅前五】")
try:
    industry = ak.stock_board_industry_name_em()
    for _, row in industry.nlargest(5, '涨跌幅').iterrows():
        print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
    print("\n【行业跌幅前五】")
    for _, row in industry.nsmallest(5, '涨跌幅').iterrows():
        print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
except Exception as e:
    print(f"获取失败：{e}")

# 获取概念板块
print("\n【概念涨幅前五】")
try:
    concept = ak.stock_board_concept_name_em()
    for _, row in concept.nlargest(5, '涨跌幅').iterrows():
        print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
except Exception as e:
    print(f"获取失败：{e}")

# 获取资金流向
print("\n【主力资金净流入前五】")
try:
    fund = ak.stock_individual_fund_flow_rank(indicator='今日')
    for _, row in fund.head(5).iterrows():
        print(f"  {row['名称']}: {row['主力净流入']}万元")
except Exception as e:
    print(f"获取失败：{e}")

# 获取市场涨跌分布
print("\n【涨跌分布】")
try:
    sentiment = ak.stock_market_activity_legu()
    print(f"上涨家数：{sentiment.get('上涨家数', 'N/A')}")
    print(f"下跌家数：{sentiment.get('下跌家数', 'N/A')}")
except Exception as e:
    print(f"获取失败：{e}")
