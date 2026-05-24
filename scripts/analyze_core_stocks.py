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

# 核心标的池（叶荣添提到的 + 现有持仓）
stocks = {
    # 半导体设备五大方向
    '中微公司': '688012.SH',
    '北方华创': '002371.SZ',
    '长电科技': '600584.SH',
    '拓荆科技': '688072.SH',
    '盛美上海': '688082.SH',
    '芯源微': '688378.SH',
    '中科飞测': '688361.SH',
    '精测电子': '300567.SZ',
    
    # 光互联/DSP 链
    '尤讯股份': '688629.SH',  # 假设代码
    
    # 现有持仓 S 级
    '沪电股份': '002463.SZ',
    '中国铀业': '001280.SZ',
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
        # 1. 实时行情
        df_realtime = pro.quote(ts_code=code)
        
        # 2. 近期走势（5 日）
        df_5d = pro.daily(ts_code=code, start_date='20260512', end_date='20260518')
        
        # 3. 基本面数据
        df_basic = pro.stock_basic(ts_code=code, fields='ts_code,symbol,name,area,industry,market,list_date')
        
        # 4. 财务指标
        df_finance = pro.fina_indicator(ts_code=code, start_date='20251231', end_date='20260331')
        
        # 5. 资金流向（北向）
        df_money = pro.moneyflow(ts_code=code, start_date='20260512', end_date='20260518')
        
        # 整理数据
        result = {
            '名称': name,
            '代码': code,
            '现价': df_realtime['close'].iloc[0] if not df_realtime.empty else None,
            '涨跌幅': df_realtime['pct_chg'].iloc[0] if not df_realtime.empty else None,
            '市盈率 (TTM)': df_realtime['pe_ttm'].iloc[0] if not df_realtime.empty else None,
            '市净率': df_realtime['pb'].iloc[0] if not df_realtime.empty else None,
            '总市值': df_realtime['total_mv'].iloc[0] if not df_realtime.empty else None,
            '流通市值': df_realtime['circ_mv'].iloc[0] if not df_realtime.empty else None,
            '5 日涨跌幅': df_5d['pct_chg'].sum() if not df_5d.empty else None,
            '5 日主力净流入': df_money['buy_sm_amount'].sum() - df_money['sell_sm_amount'].sum() if not df_money.empty else None,
            '行业': df_basic['industry'].iloc[0] if not df_basic.empty else None,
            '上市日期': df_basic['list_date'].iloc[0] if not df_basic.empty else None,
        }
        
        # 财务数据（最新季度）
        if not df_finance.empty:
            latest = df_finance.iloc[0]
            result['ROE'] = latest.get('roe')
            result['毛利率'] = latest.get('gross_margin')
            result['净利率'] = latest.get('net_margin')
            result['营收增速'] = latest.get('rev_yoy')
            result['净利增速'] = latest.get('netprofit_yoy')
        
        results.append(result)
        print(f"  ✅ 现价：{result['现价']}, 涨跌幅：{result['涨跌幅']:.2f}%, 市盈率：{result['市盈率 (TTM)']:.2f}" if result['现价'] else "  ⚠️ 数据缺失")
        
    except Exception as e:
        print(f"  ❌ 错误：{e}")
        results.append({
            '名称': name,
            '代码': code,
            '现价': None,
            '涨跌幅': None,
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
print(f"\n✅ 数据已保存到：C:\\Users\\Admin\\opcclawai\\project\\analysis\\core-stocks-analysis-20260518.csv")

# 按涨跌幅排序
print("\n" + "=" * 80)
print("按 5 日涨跌幅排序")
print("=" * 80)
df_sorted = df_summary.dropna(subset=['5 日涨跌幅']).sort_values('5 日涨跌幅', ascending=False)
print(df_sorted[['名称', '现价', '涨跌幅', '5 日涨跌幅', '市盈率 (TTM)']].to_string(index=False))

# 按市盈率排序
print("\n" + "=" * 80)
print("按市盈率排序（从低到高）")
print("=" * 80)
df_pe = df_summary.dropna(subset=['市盈率 (TTM)']).sort_values('市盈率 (TTM)')
print(df_pe[['名称', '现价', '市盈率 (TTM)', '市净率', '总市值']].to_string(index=False))
