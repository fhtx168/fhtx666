#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全盘市场数据获取脚本
获取 A 股、港股、美股、期货、外汇、大宗商品等全市场数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

def get_market_overview():
    """获取大盘概览"""
    print("=" * 80)
    print(f"市场概览 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # A 股主要指数
    indices = {
        "上证指数": "sh000001",
        "深证成指": "sz399001",
        "创业板指": "sz399006",
        "科创 50": "sh000688",
        "沪深 300": "sh000300",
        "上证 50": "sh000016",
        "中证 500": "sh000905",
    }
    
    print("\n【主要指数】")
    print("-" * 80)
    print(f"{'指数名称':<15} {'最新价':>12} {'涨跌幅':>10} {'涨跌额':>10}")
    print("-" * 80)
    
    for name, code in indices.items():
        try:
            df = ak.stock_zh_index_spot(symbol=code)
            if df is not None and len(df) > 0:
                price = df['close'].iloc[-1] if 'close' in df.columns else df['current_price'].iloc[0]
                change_pct = df['change_percent'].iloc[0] if 'change_percent' in df.columns else 0
                change = df['change'].iloc[0] if 'change' in df.columns else 0
                
                print(f"{name:<15} {price:>12.2f} {change_pct:>9.2f}% {change:>10.2f}")
        except Exception as e:
            print(f"{name:<15} 数据获取失败")
    
    print("-" * 80)

def get_a_market_summary():
    """获取 A 股市场全貌"""
    print("\n【A 股市场全貌】")
    print("=" * 80)
    
    try:
        # 全部 A 股行情
        df = ak.stock_zh_a_spot_em()
        
        total = len(df)
        up = len(df[df['涨跌幅'] > 0])
        down = len(df[df['涨跌幅'] < 0])
        limit_up = len(df[df['涨跌幅'] >= 9.8])
        limit_down = len(df[df['涨跌幅'] <= -9.8])
        
        avg_change = df['涨跌幅'].mean()
        median_change = df['涨跌幅'].median()
        total_volume = df['成交量'].sum()
        total_amount = df['成交额'].sum() / 1e8  # 亿
        
        print(f"上市公司总数：{total} 家")
        print(f"上涨家数：{up} 家 ({up/total*100:.1f}%)")
        print(f"下跌家数：{down} 家 ({down/total*100:.1f}%)")
        print(f"涨停家数：{limit_up} 家")
        print(f"跌停家数：{limit_down} 家")
        print(f"平均涨跌幅：{avg_change:.2f}%")
        print(f"中位数涨跌幅：{median_change:.2f}%")
        print(f"总成交量：{total_volume:,.0f} 手")
        print(f"总成交额：{total_amount:,.2f} 亿元")
        
        # 涨跌分布
        print("\n【涨跌分布】")
        print("-" * 80)
        ranges = [
            (9, 100, "涨停"),
            (5, 9, "+5%~+9%"),
            (3, 5, "+3%~+5%"),
            (0, 3, "0~+3%"),
            (-3, 0, "-3%~0"),
            (-5, -3, "-5%~-3%"),
            (-9, -5, "-9%~-5%"),
            (-100, -9, "跌停")
        ]
        
        for low, high, label in ranges:
            count = len(df[(df['涨跌幅'] >= low) & (df['涨跌幅'] < high)])
            pct = count / total * 100
            bar = "#" * int(pct / 2)
            print(f"{label:>12}: {count:>5} 家 ({pct:>5.1f}%) {bar}")
        
        # 行业板块
        print("\n【行业板块涨跌前五】")
        print("-" * 80)
        
        try:
            industry_df = ak.stock_board_industry_name_em()
            if industry_df is not None and len(industry_df) > 0:
                top5 = industry_df.nlargest(5, '涨跌幅')
                bottom5 = industry_df.nsmallest(5, '涨跌幅')
                
                print("涨幅前五：")
                for _, row in top5.iterrows():
                    print(f"  {row['板块名称']:<20} {row['涨跌幅']:>7.2f}%")
                
                print("\n跌幅前五：")
                for _, row in bottom5.iterrows():
                    print(f"  {row['板块名称']:<20} {row['涨跌幅']:>7.2f}%")
        except:
            pass
            
    except Exception as e:
        print(f"获取 A 股数据失败：{e}")

def get_hot_concepts():
    """获取热门概念板块"""
    print("\n【热门概念板块】")
    print("=" * 80)
    
    try:
        concept_df = ak.stock_board_concept_name_em()
        if concept_df is not None and len(concept_df) > 0:
            top10 = concept_df.nlargest(10, '涨跌幅')
            
            print(f"{'排名':<5} {'概念名称':<25} {'涨跌幅':>10} {'领涨股':<15}")
            print("-" * 80)
            
            for idx, (_, row) in enumerate(top10.iterrows(), 1):
                print(f"{idx:<5} {row['板块名称']:<25} {row['涨跌幅']:>9.2f}% {row.get('领涨股', 'N/A'):<15}")
    except Exception as e:
        print(f"获取概念数据失败：{e}")

def get_active_stocks():
    """获取活跃个股（涨跌幅前 20）"""
    print("\n【活跃个股 Top20】")
    print("=" * 80)
    
    try:
        df = ak.stock_zh_a_spot_em()
        
        # 涨幅前 10
        top10 = df.nlargest(10, '涨跌幅')
        print("【涨幅前十】")
        print(f"{'代码':<12} {'名称':<15} {'最新价':>10} {'涨跌幅':>10} {'成交额 (亿)':>12}")
        print("-" * 80)
        for _, row in top10.iterrows():
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            price = row.get('最新价', 0)
            change = row.get('涨跌幅', 0)
            amount = row.get('成交额', 0) / 1e8
            print(f"{code:<12} {name:<15} {price:>10.2f} {change:>9.2f}% {amount:>12.2f}")
        
        # 跌幅前 10
        bottom10 = df.nsmallest(10, '涨跌幅')
        print("\n【跌幅前十】")
        print(f"{'代码':<12} {'名称':<15} {'最新价':>10} {'涨跌幅':>10} {'成交额 (亿)':>12}")
        print("-" * 80)
        for _, row in bottom10.iterrows():
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            price = row.get('最新价', 0)
            change = row.get('涨跌幅', 0)
            amount = row.get('成交额', 0) / 1e8
            print(f"{code:<12} {name:<15} {price:>10.2f} {change:>9.2f}% {amount:>12.2f}")
            
    except Exception as e:
        print(f"获取个股数据失败：{e}")

def get_funds_flow():
    """获取资金流向"""
    print("\n【资金流向】")
    print("=" * 80)
    
    try:
        # 个股资金流
        fund_df = ak.stock_individual_fund_flow_rank(indicator="今日")
        if fund_df is not None and len(fund_df) > 0:
            top5 = fund_df.head(5)
            
            print("【个股资金净流入前五】")
            print(f"{'代码':<12} {'名称':<15} {'主力净流入 (万)':>15} {'超大单':>12} {'大单':>12}")
            print("-" * 80)
            
            for _, row in top5.iterrows():
                code = row.get('代码', 'N/A')
                name = row.get('名称', 'N/A')
                main_in = row.get('主力净流入 - 万元', 0)
                super_large = row.get('超大单 - 万元', 0)
                large = row.get('大单 - 万元', 0)
                print(f"{code:<12} {name:<15} {main_in:>15.2f} {super_large:>12.2f} {large:>12.2f}")
    except Exception as e:
        print(f"获取资金流数据失败：{e}")

def get_market_emotion():
    """获取市场情绪指标"""
    print("\n【市场情绪】")
    print("=" * 80)
    
    try:
        # 涨跌停比
        df = ak.stock_zh_a_spot_em()
        limit_up = len(df[df['涨跌幅'] >= 9.8])
        limit_down = len(df[df['涨跌幅'] <= -9.8])
        
        if limit_down > 0:
            ratio = limit_up / limit_down
        else:
            ratio = limit_up if limit_up > 0 else 0
        
        print(f"涨停家数：{limit_up} 家")
        print(f"跌停家数：{limit_down} 家")
        print(f"涨跌停比：{ratio:.2f}")
        
        if ratio > 3:
            emotion = "火热"
        elif ratio > 1:
            emotion = "乐观"
        elif ratio > 0.5:
            emotion = "中性"
        else:
            emotion = "恐慌"
        
        print(f"情绪判断：{emotion}")
        
    except Exception as e:
        print(f"获取情绪数据失败：{e}")

def save_to_file():
    """保存数据到文件"""
    print("\n【保存数据】")
    print("=" * 80)
    
    try:
        # A 股全量数据
        df = ak.stock_zh_a_spot_em()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"C:/Users/Admin/opcclawai/project/portfolio/market_data_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"数据已保存到：{filename}")
        print(f"   共 {len(df)} 只股票，{len(df.columns)} 个字段")
    except Exception as e:
        print(f"保存失败：{e}")

def main():
    """主函数"""
    print("\n" + "=" * 40)
    print("  全盘市场数据获取系统 ")
    print("=" * 40 + "\n")
    
    get_market_overview()
    get_a_market_summary()
    get_hot_concepts()
    get_active_stocks()
    get_funds_flow()
    get_market_emotion()
    save_to_file()
    
    print("\n" + "=" * 80)
    print("数据获取完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()
