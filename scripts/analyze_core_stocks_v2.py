"""
叶荣添 5.17 直播核心标的全面分析
基本面 + 股价 + 资金流向
"""

import tushare as ts
import pandas as pd
from datetime import datetime

# 配置
ts.set_token('11c66ba1f1b5128c3aab5bed7eafeb9a22a78908bc54e6e8a23a5c0d')
pro = ts.pro_api()

# 核心标的池
stocks = {
    # 半导体设备五大方向
    '中微公司': '688012.SH',
    '北方华创': '002371.SZ',
    '长电科技': '600584.SH',
    '拓荆科技': '688072.SH',
    '盛美上海': '688082.SH',
    '芯源微': '688378.SH',
    
    # 现有持仓相关
    '沪电股份': '002463.SZ',
    '阳光电源': '300274.SZ',
    '中芯国际': '688981.SH',
    '通富微电': '002156.SZ',
    '华海诚科': '688535.SH',
    '兴森科技': '002436.SZ',
}

print("=" * 80)
print("叶荣添 5.17 直播核心标的全面分析")
print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 80)

results = []

for name, code in stocks.items():
    print(f"\n正在分析：{name} ({code})")
    
    try:
        # 1. 近期走势（5 日）
        df_5d = pro.daily(ts_code=code, start_date='20260512', end_date='20260518')
        
        # 2. 基本面数据
        df_basic = pro.stock_basic(ts_code=code, fields='ts_code,symbol,name,area,industry,market,list_date')
        
        # 3. 财务指标（最新季报）
        df_finance = pro.fina_indicator(ts_code=code, start_date='20251231', end_date='20260331')
        
        # 4. 资金流向
        df_money = pro.moneyflow(ts_code=code, start_date='20260512', end_date='20260518')
        
        # 获取最新行情（从 5 日数据中取最后一天）
        latest_price = df_5d['close'].iloc[-1] if not df_5d.empty else None
        latest_pct = df_5d['pct_chg'].iloc[-1] if not df_5d.empty else None
        
        # 整理数据
        result = {
            '名称': name,
            '代码': code,
            '现价': latest_price,
            '今日涨跌幅': latest_pct,
            '5 日涨跌幅': df_5d['pct_chg'].sum() if not df_5d.empty else None,
            '5 日主力净流入 (万)': ((df_money['buy_sm_amount'].sum() - df_money['sell_sm_amount'].sum()) / 10000) if not df_money.empty else None,
            '行业': df_basic['industry'].iloc[0] if not df_basic.empty else None,
            '总市值 (亿)': None,
            '市盈率': None,
            'ROE': None,
            '营收增速': None,
            '净利增速': None,
        }
        
        # 财务数据
        if not df_finance.empty:
            latest = df_finance.iloc[0]
            result['ROE'] = latest.get('roe')
            result['营收增速'] = latest.get('rev_yoy')
            result['净利增速'] = latest.get('netprofit_yoy')
        
        results.append(result)
        
        if latest_price:
            print(f"  现价：{latest_price:.2f}, 今日涨跌幅：{latest_pct:.2f}%, 5 日涨跌幅：{result['5 日涨跌幅']:.2f}%")
        else:
            print("  数据缺失")
        
    except Exception as e:
        print(f"  错误：{e}")
        results.append({
            '名称': name,
            '代码': code,
            '现价': None,
            '今日涨跌幅': None,
            '错误': str(e)
        })

# 生成汇总表格
print("\n" + "=" * 80)
print("核心标的汇总分析")
print("=" * 80)

df_summary = pd.DataFrame(results)
print(df_summary.to_string(index=False))

# 保存到文件
df_summary.to_csv(r'C:\Users\Admin\opcclawai\project\analysis\core-stocks-analysis-20260518.csv', index=False, encoding='utf-8-sig')
print(f"\n数据已保存到：analysis\\core-stocks-analysis-20260518.csv")

# 按 5 日涨跌幅排序
print("\n" + "=" * 80)
print("按 5 日涨跌幅排序")
print("=" * 80)
df_sorted = df_summary.dropna(subset=['5 日涨跌幅']).sort_values('5 日涨跌幅', ascending=False)
print(df_sorted[['名称', '现价', '今日涨跌幅', '5 日涨跌幅']].to_string(index=False))
