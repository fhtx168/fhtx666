import akshare as ak
import pandas as pd
from datetime import datetime
import time

print("=== 补充数据 ===\n")

# 重试获取行业数据
for i in range(3):
    try:
        time.sleep(1)
        industry = ak.stock_board_industry_name_em()
        print("【行业涨幅前五】")
        for _, row in industry.nlargest(5, '涨跌幅').iterrows():
            print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
        print("\n【行业跌幅前五】")
        for _, row in industry.nsmallest(5, '涨跌幅').iterrows():
            print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
        break
    except Exception as e:
        if i == 2:
            print(f"行业数据获取失败")
        continue

# 重试获取概念数据
for i in range(3):
    try:
        time.sleep(1)
        concept = ak.stock_board_concept_name_em()
        print("\n【概念涨幅前五】")
        for _, row in concept.nlargest(5, '涨跌幅').iterrows():
            print(f"  {row['板块名称']}: {row['涨跌幅']:.2f}%")
        break
    except Exception as e:
        if i == 2:
            print(f"概念数据获取失败")
        continue

# 重试获取资金流向
for i in range(3):
    try:
        time.sleep(1)
        fund = ak.stock_individual_fund_flow_rank(indicator='今日')
        print("\n【主力资金净流入前五】")
        for _, row in fund.head(5).iterrows():
            print(f"  {row['名称']}: {row['主力净流入']}万元")
        break
    except Exception as e:
        if i == 2:
            print(f"资金流向获取失败")
        continue

# 获取市场成交额
print("\n【市场成交】")
try:
    # 获取市场总成交额（亿元）
    sh_vol = ak.stock_zh_index_daily(symbol='sh000001')
    sz_vol = ak.stock_zh_index_daily(symbol='sz399001')
    latest_sh = sh_vol.iloc[-1]
    latest_sz = sz_vol.iloc[-1]
    # 估算成交额（单位：亿元）
    total_vol = round((latest_sh['volume'] + latest_sz['volume']) / 100000000, 2)
    print(f"两市成交额：约{total_vol}亿元")
except Exception as e:
    print(f"成交额获取失败")
