#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场数据每日获取脚本 - 增强版
获取 A 股全部收盘数据、指数、板块排行、资金流向、涨跌停统计
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import os
import sys
import time

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 设置显示选项
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 100)

def get_date_str():
    """获取日期字符串"""
    return datetime.now().strftime("%Y%m%d")

def get_date_cn():
    """获取中文日期"""
    return datetime.now().strftime("%Y 年 %m 月 %d 日")

def retry_request(func, max_retries=3, delay=2):
    """重试机制"""
    for i in range(max_retries):
        try:
            result = func()
            return result
        except Exception as e:
            if i < max_retries - 1:
                print(f"   重试 {i+1}/{max_retries}... ({e})")
                time.sleep(delay)
            else:
                raise e

def get_all_stocks_data():
    """获取全部 A 股收盘数据"""
    print("获取全部 A 股收盘数据...")
    try:
        # 使用东方财富接口获取 A 股实时行情
        df = retry_request(lambda: ak.stock_zh_a_spot_em())
        print(f"   成功：获取 {len(df)} 只股票数据")
        return df
    except Exception as e:
        print(f"   失败：{e}")
        return None

def get_major_indices():
    """获取主要指数数据"""
    print("获取主要指数数据...")
    indices_data = []
    
    # 使用 ak.index_zh_a_hist 获取指数数据
    index_codes = {
        "上证指数": "000001",
        "深证成指": "399001", 
        "创业板指": "399006",
        "科创 50": "000688"
    }
    
    for name, code in index_codes.items():
        try:
            # 获取指数历史行情
            df = retry_request(lambda c=code: ak.index_zh_a_hist(symbol=c, period="daily", start_date="20260501", end_date="20260522"))
            if len(df) > 0:
                latest = df.iloc[-1]
                prev_close = df.iloc[-2]['收盘'] if len(df) > 1 else latest['收盘']
                change_pct = ((latest['收盘'] / prev_close) - 1) * 100
                
                indices_data.append({
                    "指数名称": name,
                    "指数代码": code,
                    "收盘价": round(float(latest['收盘']), 2),
                    "涨跌幅": round(change_pct, 2),
                    "成交量": int(float(latest['成交量'])),
                    "成交额": int(float(latest['成交额']))
                })
                print(f"   {name}: {round(float(latest['收盘']), 2)} ({change_pct:+.2f}%)")
        except Exception as e:
            print(f"   {name} 获取失败：{e}")
    
    return pd.DataFrame(indices_data)

def get_industry_ranking():
    """获取行业板块涨跌排行"""
    print("获取行业板块排行...")
    try:
        df = retry_request(lambda: ak.stock_board_industry_name_em())
        df = df.sort_values("涨跌幅", ascending=False)
        print(f"   成功：获取 {len(df)} 个行业板块")
        return df.head(20)
    except Exception as e:
        print(f"   失败：{e}")
        return None

def get_concept_ranking():
    """获取概念板块涨跌排行"""
    print("获取概念板块排行...")
    try:
        df = retry_request(lambda: ak.stock_board_concept_name_em())
        df = df.sort_values("涨跌幅", ascending=False)
        print(f"   成功：获取 {len(df)} 个概念板块")
        return df.head(20)
    except Exception as e:
        print(f"   失败：{e}")
        return None

def get_money_flow():
    """获取资金流向数据"""
    print("获取资金流向数据...")
    try:
        df = retry_request(lambda: ak.stock_individual_fund_flow_rank(indicator="今日"))
        print(f"   成功：获取资金流向排行")
        return df.head(20)
    except Exception as e:
        print(f"   失败：{e}")
        return None

def get_limit_stats():
    """获取涨跌停统计"""
    print("获取涨跌停统计...")
    date_str = get_date_str()
    
    try:
        # 涨停池
        df_zt = retry_request(lambda: ak.stock_zt_pool_em(date=date_str))
        zt_count = len(df_zt) if df_zt is not None else 0
        print(f"   涨停家数：{zt_count}")
    except:
        zt_count = 0
        print("   涨停数据获取失败")
    
    try:
        # 跌停池
        df_dt = retry_request(lambda: ak.stock_zt_pool_dtgc_em(date=date_str))
        dt_count = len(df_dt) if df_dt is not None else 0
        print(f"   跌停家数：{dt_count}")
    except:
        dt_count = 0
        print("   跌停数据获取失败")
    
    return zt_count, dt_count

def save_to_csv(df, filename):
    """保存数据到 CSV"""
    filepath = os.path.join("portfolio", filename)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"   已保存：{filepath}")
    return filepath

def update_daily_tracking(indices, industry_top5, concept_top5, zt_count, dt_count):
    """更新 daily-tracking.md 的大盘概览部分"""
    print("更新 daily-tracking.md...")
    
    date_str = get_date_str()
    date_cn = get_date_cn()
    
    # 生成大盘概览
    indices_text = ""
    for _, row in indices.iterrows():
        if row['涨跌幅'] > 0:
            symbol = "🟢"
        elif row['涨跌幅'] < 0:
            symbol = "🔴"
        else:
            symbol = "⚪"
        indices_text += f"- {row['指数名称']}: {row['收盘价']} ({symbol} {row['涨跌幅']:+.2f}%)\n"
    
    # 生成行业板块前五
    industry_text = ""
    for i, (_, row) in enumerate(industry_top5.iterrows(), 1):
        symbol = "🟢" if row['涨跌幅'] > 0 else "🔴"
        industry_text += f"{i}. {row['板块名称']} {symbol} {row['涨跌幅']:+.2f}%\n"
    
    # 生成概念板块前五
    concept_text = ""
    for i, (_, row) in enumerate(concept_top5.iterrows(), 1):
        symbol = "🟢" if row['涨跌幅'] > 0 else "🔴"
        concept_text += f"{i}. {row['板块名称']} {symbol} {row['涨跌幅']:+.2f}%\n"
    
    # 读取现有文件
    filepath = os.path.join("portfolio", "daily-tracking.md")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        content = "# 全域投研每日巡检\n\n"
    
    # 生成新的概览部分
    new_section = f"""## {date_cn} 收盘概览（15:00 更新）

### 主要指数
{indices_text}
### 行业板块涨幅前五
{industry_text}
### 概念板块涨幅前五
{concept_text}
### 市场情绪
- 涨停家数：{zt_count}
- 跌停家数：{dt_count}
- 涨跌比：{zt_count}:{dt_count}

---

"""
    
    # 插入到文件开头（在标题之后）
    if "# 全域投研每日巡检\n\n" in content:
        content = content.replace("# 全域投研每日巡检\n\n", "# 全域投研每日巡检\n\n" + new_section)
    else:
        content = new_section + content
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   已更新：{filepath}")

def main():
    """主函数"""
    print("=" * 60)
    print(f"市场数据每日获取 ({get_date_str()})")
    print("=" * 60)
    
    # 1. 获取全部 A 股数据
    all_stocks = get_all_stocks_data()
    if all_stocks is not None:
        save_to_csv(all_stocks, f"market_data_{get_date_str()}.csv")
    
    # 2. 获取主要指数
    indices = get_major_indices()
    
    # 3. 获取行业板块排行
    industry = get_industry_ranking()
    industry_top5 = industry.head(5) if industry is not None and len(industry) > 0 else pd.DataFrame()
    
    # 4. 获取概念板块排行
    concept = get_concept_ranking()
    concept_top5 = concept.head(5) if concept is not None and len(concept) > 0 else pd.DataFrame()
    
    # 5. 获取资金流向
    money_flow = get_money_flow()
    if money_flow is not None:
        save_to_csv(money_flow, f"money_flow_{get_date_str()}.csv")
    
    # 6. 获取涨跌停统计
    zt_count, dt_count = get_limit_stats()
    
    # 7. 更新 daily-tracking.md
    if len(indices) > 0:
        update_daily_tracking(indices, industry_top5, concept_top5, zt_count, dt_count)
    
    print("=" * 60)
    print("市场数据获取完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
