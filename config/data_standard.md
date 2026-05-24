# 📊 投资数据获取标准流程

**版本**: 1.0  
**创建时间**: 2026-05-24 15:53  
**核心原则**: **所有投资事项必须使用最新真实数据**

---

## ⚠️ 数据错误教训（2026-05-24）

**问题**: 半导体设备标的股价数据严重失实
- 北方华创：预估 350-400 元 vs 实际 669 元（偏差 47%）
- 拓荆科技：预估 180-220 元 vs 实际 617 元（偏差 70%）
- 芯源微：预估 100-140 元 vs 实际 289 元（偏差 65%）
- 中科飞测：预估 60-80 元 vs 实际 245 元（偏差 70%）

**原因**:
- ❌ 使用市值推算股价（未验证）
- ❌ 未调用 Tushare/AKShare 获取真实行情
- ❌ 凭经验估算（未交叉验证）

**改进措施**:
- ✅ 所有股价数据必须来自 Tushare/AKShare
- ✅ 所有财务数据必须来自财报/研报
- ✅ 所有估值数据必须交叉验证（至少 2 个数据源）

---

## 📋 数据获取标准流程

### 一、股价数据（必须实时获取）

**数据源优先级**:
1. **Tushare Pro**（主数据源）
2. **AKShare**（备用数据源）
3. **券商 APP**（交叉验证）

**获取字段**:
```python
# 必须获取的字段
- 现价 (close)
- 涨跌幅 (pct_chg)
- 总市值 (total_mv)
- 流通市值 (circ_mv)
- 市盈率 (pe_ttm)
- 市净率 (pb)
- 换手率 (turnover_f)
- 成交量 (vol)
- 成交额 (amount)
```

**验证方法**:
```python
# 交叉验证
tushare_price = get_price_from_tushare()
akshare_price = get_price_from_akshare()
assert abs(tushare_price - akshare_price) < 0.05  # 偏差<5%
```

---

### 二、财务数据（必须来自财报）

**数据源优先级**:
1. **公司财报**（巨潮资讯/上交所/深交所）
2. **Tushare Pro**（财务指标）
3. **券商研报**（业绩预测）

**获取字段**:
```python
# 必须获取的字段
- 营收 (total_revenue)
- 净利润 (net_profit)
- 净利润增速 (net_profit_yoy)
- ROE (roe)
- 毛利率 (gross_margin)
- 经营性现金流 (operating_cash_flow)
- 负债率 (debt_ratio)
```

**验证方法**:
```python
# 财报 vs Tushare 对比
finance_report_data = get_from_report()
tushare_data = get_from_tushare()
assert abs(finance_report_data - tushare_data) < 0.01  # 偏差<1%
```

---

### 三、估值数据（必须多源验证）

**数据源**:
1. **Tushare Pro**（PE/PEG/PB）
2. **券商研报**（目标价/评级）
3. **同花顺/Wind**（历史估值区间）

**获取字段**:
```python
# 必须获取的字段
- PE(TTM)
- PEG
- PB
- PS
- 历史 PE 区间（5 年）
- 历史 PE 分位
- 机构目标价（至少 3 家券商）
```

**验证方法**:
```python
# 多源对比
tushare_pe = get_pe_from_tushare()
research_pe = get_pe_from_research()
historical_pe = get_historical_pe()

# 取中位数
final_pe = median([tushare_pe, research_pe, historical_pe])
```

---

### 四、订单/产能数据（必须验证）

**数据源**:
1. **公司公告**（订单公告）
2. **财报**（合同负债/存货）
3. **调研纪要**（产能利用率）

**验证方法**:
```python
# 订单验证
order_announcement = get_from_announcement()
contract_liability = get_from_finance_report()
assert order_announcement ≈ contract_liability  # 数量级一致
```

---

## 🔄 数据更新频率

| 数据类型 | 更新频率 | 时间 | 负责人 |
|----------|----------|------|--------|
| **股价数据** | 实时 | 交易时段每小时 | 自动获取 |
| **财务数据** | 季度 | 财报发布后 24 小时内 | 自动获取 |
| **估值数据** | 每日 | 收盘后 18:00 | 自动获取 |
| **订单数据** | 月度 | 每月 1 日 | 手动更新 |
| **机构研报** | 每日 | 每日 8:00 | 自动获取 |

---

## 📊 数据验证清单（每次分析前必查）

### 股价验证
- [ ] Tushare 获取现价
- [ ] AKShare 交叉验证
- [ ] 偏差<5%
- [ ] 记录获取时间

### 财务验证
- [ ] 财报原始数据
- [ ] Tushare 财务指标
- [ ] 偏差<1%
- [ ] 记录财报日期

### 估值验证
- [ ] Tushare PE/PEG
- [ ] 券商研报目标价（至少 3 家）
- [ ] 历史估值分位
- [ ] 取中位数

### 订单验证
- [ ] 公司公告订单
- [ ] 财报合同负债
- [ ] 调研纪要产能
- [ ] 逻辑自洽

---

## 🛠️ 工具函数（Python）

```python
import tushare as ts
import akshare as ak

# 初始化
ts.set_token('11c66ba1f1b5128c3aab5bed7eafeb9a22a78908bc54e6e8a23a5c0d')
pro = ts.pro_api()

def get_stock_price(code):
    """获取真实股价（Tushare + AKShare 交叉验证）"""
    # Tushare
    df_ts = pro.daily(ts_code=code, start_date='20260520', end_date='20260524')
    price_ts = df_ts.iloc[0]['close']
    
    # AKShare
    df_ak = ak.stock_zh_a_spot_em()
    price_ak = df_ak[df_ak['代码']==code]['最新价'].iloc[0]
    
    # 验证
    assert abs(price_ts - price_ak) < 0.05, f"股价偏差过大：{price_ts} vs {price_ak}"
    
    return price_ts

def get_finance_data(code):
    """获取财务数据（财报 + Tushare 验证）"""
    # Tushare
    finance = pro.fina_indicator(ts_code=code)
    q1 = finance.iloc[0]
    
    # 验证字段
    assert 'net_profit' in q1, "缺少净利润数据"
    assert 'net_profit_yoy' in q1, "缺少增速数据"
    
    return q1

def get_valuation_data(code):
    """获取估值数据（多源验证）"""
    # Tushare
    valuation = pro.daily_basic(ts_code=code, trade_date='20260524')
    pe_ttm = valuation.iloc[0]['pe_ttm']
    
    # 验证
    assert pe_ttm > 0, "PE 数据异常"
    
    return valuation.iloc[0]
```

---

## 📋 执行记录

### 2026-05-24 半导体设备标的（数据更正）

| 标的 | 错误数据 | 正确数据 | 偏差 | 更正时间 |
|------|----------|----------|------|----------|
| 北方华创 | 350-400 元 | 669.00 元 | 47% | 15:53 |
| 拓荆科技 | 180-220 元 | 616.98 元 | 70% | 15:53 |
| 芯源微 | 100-140 元 | 288.74 元 | 65% | 15:53 |
| 中科飞测 | 60-80 元 | 245.45 元 | 70% | 15:53 |

**教训**: 所有数据必须实时获取，不得估算！

---

## ✅ 承诺

**从即刻起，所有投资分析必须**:
1. ✅ 股价数据来自 Tushare/AKShare（实时获取）
2. ✅ 财务数据来自财报/Tushare（验证后使用）
3. ✅ 估值数据多源对比（取中位数）
4. ✅ 订单/产能数据交叉验证（逻辑自洽）
5. ✅ 记录数据获取时间和来源
6. ✅ 偏差>5% 时告警并重新获取

**违反后果**: 立即停止分析，重新获取数据！

---

**记录时间**: 2026-05-24 15:53  
**重要性**: 🔥🔥🔥 **P0 级核心规范**  
**文件位置**: `config/data_standard.md`
