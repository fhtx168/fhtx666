import akshare as ak
import pandas as pd
import os
import sys

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 创建目录
os.makedirs('research_reports/2026-05-15', exist_ok=True)

try:
    # 获取券商研报数据 - 最新研报
    print("正在获取最新券商研报数据...")
    df = ak.stock_report_disclosure()
    print("券商研报数据获取成功")
    print(df.head())
    df.to_csv('research_reports/2026-05-15/latest_reports.csv', index=False)
    
    # 获取个股研报（尝试几个科技股）
    tech_stocks = ["600519", "000858", "601318", "000333", "600036"]
    for stock in tech_stocks:
        try:
            stock_reports = ak.stock_research_report_em(symbol=stock)
            if not stock_reports.empty:
                stock_reports.to_csv(f'research_reports/2026-05-15/reports_{stock}.csv', index=False)
                print(f"个股{stock}研报获取成功")
        except Exception as e:
            print(f"个股{stock}研报获取失败: {e}")
            
except Exception as e:
    print(f"券商研报数据获取失败: {e}")
    import traceback
    traceback.print_exc()