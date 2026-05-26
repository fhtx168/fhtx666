# -*- coding: utf-8 -*-
"""
A 股 6 只股票深度分析报告
使用 AKShare 获取实时数据
"""
import akshare as ak
import pandas as pd
from datetime import datetime

# 6 只股票代码
stocks = [
    {"code": "688008", "name": "澜起科技"},
    {"code": "300620", "name": "光库科技"},
    {"code": "002222", "name": "福晶科技"},
    {"code": "300684", "name": "中石科技"},
    {"code": "002335", "name": "科华数据"},
    {"code": "688037", "name": "芯源微"},
]

def get_stock_realtime(code):
    """获取 A 股实时行情"""
    try:
        # 东方财富实时行情
        df = ak.stock_zh_a_spot_em()
        stock_data = df[df['代码'] == code]
        if len(stock_data) > 0:
            return stock_data.iloc[0]
        return None
    except Exception as e:
        print(f"获取{code}实时行情失败：{e}")
        return None

def get_stock_kline(code, period="daily"):
    """获取 K 线数据用于技术分析"""
    try:
        df = ak.stock_zh_kline(symbol=code, period=period, adjust="qfq")
        return df
    except Exception as e:
        print(f"获取{code}K 线数据失败：{e}")
        return None

def get_stock_fundamental(code):
    """获取基本面数据"""
    try:
        # 市盈率、市净率等
        df = ak.stock_value_em(symbol=code)
        return df
    except Exception as e:
        print(f"获取{code}基本面数据失败：{e}")
        return None

def get_financial_indicators(code):
    """获取财务指标"""
    try:
        # 利润表
        df = ak.stock_financial_report_sina(symbol=code, report_type="利润表")
        return df
    except Exception as e:
        print(f"获取{code}财务数据失败：{e}")
        return None

def calculate_rsi(close_prices, period=14):
    """计算 RSI 指标"""
    if len(close_prices) < period + 1:
        return None
    
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def analyze_stock(stock_info):
    """分析单只股票"""
    code = stock_info["code"]
    name = stock_info["name"]
    
    print(f"\n{'='*60}")
    print(f"【{name} ({code})】深度分析报告")
    print(f"{'='*60}\n")
    
    # 1. 实时行情
    realtime = get_stock_realtime(code)
    if realtime is not None:
        print("📊 一、实时市场数据")
        print(f"   当前价格：¥{realtime.get('最新价', 'N/A')}")
        print(f"   涨跌幅：{realtime.get('涨跌幅', 'N/A')}%")
        print(f"   涨跌额：¥{realtime.get('涨跌额', 'N/A')}")
        print(f"   成交量：{realtime.get('成交量', 'N/A')} 手")
        print(f"   成交额：{realtime.get('成交额', 'N/A')} 元")
        print(f"   总市值：{realtime.get('总市值', 'N/A')} 元")
        print(f"   流通市值：{realtime.get('流通市值', 'N/A')} 元")
        print()
    
    # 2. 估值指标
    try:
        df_pe = ak.stock_value_em(symbol=code)
        if len(df_pe) > 0:
            latest_pe = df_pe.iloc[-1]
            print("📈 二、估值指标")
            print(f"   市盈率 (PE-TTM): {latest_pe.get('PE', 'N/A')}")
            print(f"   市净率 (PB): {latest_pe.get('PB', 'N/A')}")
            print(f"   市销率 (PS): {latest_pe.get('PS', 'N/A')}")
            print()
    except Exception as e:
        print(f"   估值数据获取失败：{e}")
        print()
    
    # 3. K 线与技术分析
    kline = get_stock_kline(code)
    if kline is not None and len(kline) > 0:
        print("📉 三、技术面分析")
        
        # 近期涨跌幅
        if len(kline) >= 20:
            latest_close = kline['close'].iloc[-1]
            close_5 = kline['close'].iloc[-5] if len(kline) >= 5 else latest_close
            close_10 = kline['close'].iloc[-10] if len(kline) >= 10 else latest_close
            close_20 = kline['close'].iloc[-20] if len(kline) >= 20 else latest_close
            
            change_5d = ((latest_close / close_5) - 1) * 100
            change_10d = ((latest_close / close_10) - 1) * 100
            change_20d = ((latest_close / close_20) - 1) * 100
            
            print(f"   5 日涨跌幅：{change_5d:.2f}%")
            print(f"   10 日涨跌幅：{change_10d:.2f}%")
            print(f"   20 日涨跌幅：{change_20d:.2f}%")
        
        # RSI 指标
        rsi = calculate_rsi(kline['close'])
        if rsi:
            print(f"   RSI(14): {rsi:.2f}")
            if rsi > 70:
                print(f"   RSI 状态：超买区")
            elif rsi < 30:
                print(f"   RSI 状态：超卖区")
            else:
                print(f"   RSI 状态：中性区")
        
        # MACD (简化版)
        if len(kline) >= 26:
            close = kline['close']
            ema12 = close.ewm(span=12, adjust=False).mean()
            ema26 = close.ewm(span=26, adjust=False).mean()
            macd_line = ema12 - ema26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            macd_hist = macd_line - signal_line
            
            latest_macd = macd_line.iloc[-1]
            latest_signal = signal_line.iloc[-1]
            latest_hist = macd_hist.iloc[-1]
            
            print(f"   MACD 柱状图：{latest_hist:.2f}")
            if latest_hist > 0:
                print(f"   MACD 状态：多头")
            else:
                print(f"   MACD 状态：空头")
        
        print()
    
    # 4. 基本面数据
    try:
        # 尝试获取财务指标
        df_indicator = ak.stock_financial_analysis_indicator(symbol=code)
        if len(df_indicator) > 0:
            latest_indicator = df_indicator.iloc[-1]
            print("💰 四、基本面数据")
            print(f"   ROE(净资产收益率): {latest_indicator.get('净资产收益率', 'N/A')}%")
            print(f"   毛利率：{latest_indicator.get('销售毛利率', 'N/A')}%")
            print(f"   营收增速：{latest_indicator.get('营业收入增长率', 'N/A')}%")
            print(f"   净利增速：{latest_indicator.get('净利润增长率', 'N/A')}%")
            print()
    except Exception as e:
        print(f"   基本面数据获取失败：{e}")
        print()
    
    # 5. 资金流向
    try:
        df_flow = ak.stock_individual_fund_flow(symbol=code, market="sh" if code.startswith('6') else "sz")
        if len(df_flow) > 0:
            print("💹 五、资金流向")
            latest_flow = df_flow.iloc[-1]
            print(f"   主力净流入：{latest_flow.get('主力净流入-净额', 'N/A')} 万元")
            print(f"   大单净流入：{latest_flow.get('大单净流入-净额', 'N/A')} 万元")
            print(f"   中单净流入：{latest_flow.get('中单净流入-净额', 'N/A')} 万元")
            print(f"   小单净流入：{latest_flow.get('小单净流入-净额', 'N/A')} 万元")
            print()
    except Exception as e:
        print(f"   资金流向数据获取失败：{e}")
        print()
    
    # 6. 风险评估
    print("⚠️  六、风险评估")
    try:
        # 股东减持
        df_holder = ak.stock_holder_rank_em(symbol=code)
        if len(df_holder) > 0:
            print(f"   股东人数：{df_holder['股东人数'].iloc[-1]}")
            print(f"   户均持股：{df_holder['户均持股'].iloc[-1]}")
    except Exception as e:
        print(f"   股东数据获取失败：{e}")
    
    try:
        # 股权质押
        df_pledge = ak.stock_gpzy_profile_em(symbol=code)
        if len(df_pledge) > 0:
            latest_pledge = df_pledge.iloc[-1]
            print(f"   股权质押比例：{latest_pledge.get('质押比例', 'N/A')}%")
    except Exception as e:
        print(f"   股权质押数据获取失败：{e}")
    
    print(f"   商誉风险：需查阅最新财报")
    print(f"   减持风险：需关注公告")
    print()
    
    # 7. 综合评级
    print("🎯 七、综合投资评级")
    print(f"   说明：基于以上数据的综合评估")
    print(f"   建议：请结合个人风险偏好和投资策略决策")
    print()

def main():
    print("="*60)
    print("A 股 6 只股票深度分析报告")
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    for stock in stocks:
        try:
            analyze_stock(stock)
        except Exception as e:
            print(f"\n分析{stock['name']}时出错：{e}\n")
    
    print("\n" + "="*60)
    print("报告生成完毕")
    print("="*60)

if __name__ == "__main__":
    main()
