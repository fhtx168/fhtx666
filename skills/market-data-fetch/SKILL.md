# 市场数据获取技能

## 目标
获取 A 股全盘市场数据，用于投资分析和晚间资讯推送。

## 数据源
- **AKShare**: A 股实时行情、指数、行业、概念、资金流
- **Tushare**: 备用数据源
- **yfinance**: 港股、美股数据

## 核心数据清单

### 1. 大盘指数（必选）
```python
import akshare as ak

# 上证指数
sh = ak.stock_zh_index_spot(symbol="sh000001")
# 深证成指
sz = ak.stock_zh_index_spot(symbol="sz399001")
# 创业板指
cyb = ak.stock_zh_index_spot(symbol="sz399006")
# 科创 50
kc50 = ak.stock_zh_index_spot(symbol="sh000688")
```

### 2. 全市场统计（必选）
```python
# 全部 A 股行情
all_stocks = ak.stock_zh_a_spot_em()

# 关键指标
total = len(all_stocks)
up = len(all_stocks[all_stocks['涨跌幅'] > 0])
down = len(all_stocks[all_stocks['涨跌幅'] < 0])
limit_up = len(all_stocks[all_stocks['涨跌幅'] >= 9.8])
limit_down = len(all_stocks[all_stocks['涨跌幅'] <= -9.8])
avg_change = all_stocks['涨跌幅'].mean()
median_change = all_stocks['涨跌幅'].median()
total_amount = all_stocks['成交额'].sum() / 1e8  # 亿元
```

### 3. 行业板块（必选）
```python
# 行业涨跌排行
industry = ak.stock_board_industry_name_em()
top5_industry = industry.nlargest(5, '涨跌幅')
bottom5_industry = industry.nsmallest(5, '涨跌幅')
```

### 4. 概念板块（必选）
```python
# 概念涨跌排行
concept = ak.stock_board_concept_name_em()
top10_concept = concept.nlargest(10, '涨跌幅')
```

### 5. 资金流向（必选）
```python
# 个股资金流
fund_flow = ak.stock_individual_fund_flow_rank(indicator="今日")
top5_inflow = fund_flow.head(5)
top5_outflow = fund_flow.tail(5)
```

### 6. 涨跌停统计（必选）
```python
# 涨停股
limit_up_stocks = all_stocks[all_stocks['涨跌幅'] >= 9.8]
# 跌停股
limit_down_stocks = all_stocks[all_stocks['涨跌幅'] <= -9.8]
# 涨跌停比
ratio = len(limit_up_stocks) / len(limit_down_stocks) if len(limit_down_stocks) > 0 else len(limit_up_stocks)
```

### 7. 活跃个股（必选）
```python
# 涨幅前 10
top10_gainers = all_stocks.nlargest(10, '涨跌幅')
# 跌幅前 10
top10_losers = all_stocks.nsmallest(10, '涨跌幅')
# 成交额前 10
top10_volume = all_stocks.nlargest(10, '成交额')
```

## 数据保存

### CSV 格式
```python
timestamp = datetime.now().strftime('%Y%m%d')
filename = f"portfolio/market_data_{timestamp}.csv"
all_stocks.to_csv(filename, index=False, encoding='utf-8-sig')
```

### Markdown 摘要
```markdown
## 2026-05-21 市场概览

### 大盘指数
| 指数 | 收盘价 | 涨跌幅 |
|------|--------|--------|
| 上证指数 | XXXX.XX | +X.XX% |
| 深证成指 | XXXX.XX | +X.XX% |
| 创业板指 | XXXX.XX | +X.XX% |
| 科创 50 | XXXX.XX | +X.XX% |

### 市场全貌
- 上市公司：XXXX 家
- 上涨：XXX 家 (XX.X%)
- 下跌：XXX 家 (XX.X%)
- 涨停：XX 家
- 跌停：XX 家
- 成交额：XXXX.XX 亿元

### 行业前五
涨幅：XXX、XXX、XXX
跌幅：XXX、XXX、XXX
```

## 错误处理

### 网络异常
```python
import time

def fetch_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(2 ** i)  # 指数退避
            else:
                raise e
```

### 数据验证
```python
def validate_data(df, required_columns):
    if df is None or len(df) == 0:
        raise ValueError("数据为空")
    
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"缺少必要列：{col}")
    
    return True
```

## 执行时间
- **每个交易日 15:00**（收盘后）
- **晚间资讯推送前**（21:00 前）

## 输出文件
1. `portfolio/market_data_YYYYMMDD.csv` - 全量数据
2. `portfolio/daily-tracking.md` - 更新大盘概览
3. `memory/YYYY-MM-DD.md` - 记录市场特征

## 质量标准
- ✅ 数据完整性：全部 7 项核心数据
- ✅ 数据准确性：与东方财富网一致
- ✅ 时效性：收盘后 1 小时内完成
- ✅ 可用性：可直接用于投资报告

## 注意事项
1. 避免频繁请求（间隔至少 1 秒）
2. 使用 UTF-8-SIG 编码保存 CSV
3. 网络异常时重试最多 3 次
4. 数据异常时标记并告警
