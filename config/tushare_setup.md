# Tushare Pro 配置指南

**重要性**: 🔴 P0 级 - 实时行情数据核心依赖  
**配置时间**: 2026-05-24  
**状态**: ⏳ 待配置

---

## 📌 为什么需要 Tushare

当前能力缺口：
- ❌ A 股/港股/美股实时股价查询
- ❌ Level-2 资金流数据
- ❌ 龙虎榜、北向资金、南向资金监控
- ❌ 财务指标快速查询

AKShare 虽然免费，但部分接口不稳定。Tushare Pro 提供更稳定的 API 服务。

---

## 🎯 注册步骤

### 1. 访问官网
https://tushare.pro

### 2. 注册账号
- 点击"注册"
- 填写手机号/邮箱
- 完成验证

### 3. 获取 API Token
- 登录后进入"个人中心"
- 点击"接口 TOKEN"
- 复制 TOKEN（格式：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

### 4. 积分说明
- 新用户注册送 **100 积分**
- 基础接口（股票列表、日线行情）：**免费**
- 高级接口（资金流、龙虎榜）：需要 **2000+ 积分**
- 积分获取方式：
  - 每日签到：+10 积分
  - 邀请好友：+200 积分/人
  - 充值：1 元 = 10 积分（可选）

**建议**: 先用免费额度，不够再考虑充值

---

## ⚙️ 配置步骤

### 方法 1: 环境变量（推荐）

```powershell
# 添加到系统环境变量
# 方式 A: 永久添加（推荐）
[System.Environment]::SetEnvironmentVariable("TUSHARE_TOKEN", "your-token-here", "User")

# 方式 B: 临时添加（当前会话有效）
$env:TUSHARE_TOKEN = "your-token-here"
```

### 方法 2: .env 文件

在 `C:\Users\Admin\opcclawai\project\.env` 中添加：
```
TUSHARE_TOKEN=your-token-here
```

### 验证配置

```powershell
# 检查环境变量
echo $env:TUSHARE_TOKEN

# 测试 Python 导入
python -c "import os; print(os.environ.get('TUSHARE_TOKEN', '未配置'))"
```

---

## 📦 安装依赖

```powershell
# 安装 Tushare 和 Pandas
pip install tushare pandas -U

# 验证安装
python -c "import tushare; print(tushare.__version__)"
```

---

## 🚀 快速开始

### 测试连接

```python
import tushare as ts

# 初始化
ts.set_token('your-token-here')
pro = ts.pro_api()

# 测试：获取股票列表
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
print(df.head())
```

### 常用接口

```python
import tushare as ts
ts.set_token('your-token-here')
pro = ts.pro_api()

# 1. 实时行情
df = ts.realtime_quote(ts_code='000001.SZ')

# 2. 日线行情
df = pro.daily(ts_code='000001.SZ', start_date='20260520', end_date='20260524')

# 3. 资金流向
df = pro.moneyflow(ts_code='000001.SZ', start_date='20260520', end_date='20260524')

# 4. 股票基本信息
df = pro.stock_basic(ts_code='000001.SZ')

# 5. 财务指标
df = pro.fina_indicator(ts_code='000001.SZ', start_date='20260101', end_date='20260524')
```

---

## 📊 集成到现有流程

### 晚间资讯推送增强

当前晚间推送使用 AKShare，可增加 Tushare 作为备用数据源：

```python
# 优先使用 AKShare
try:
    data = akshare_data()
except:
    # 降级到 Tushare
    data = tushare_data()
```

### 持仓更新增强

当前持仓更新可增加 Tushare 实时行情：

```python
# 批量获取持仓行情
ts_codes = ['002463.SZ', '300308.SZ', '300394.SZ', ...]  # 60 只持仓
for code in ts_codes:
    quote = ts.realtime_quote(ts_code=code)
    update_portfolio(quote)
```

---

## ⚠️ 常见问题

### Q1: Token 无效
- 检查是否复制完整（32 位）
- 检查是否有空格
- 重新登录官网获取新 Token

### Q2: 积分不足
- 基础接口（stock_basic, daily）：**免费**
- 资金流（moneyflow）：需要 **2000 积分**
- 龙虎榜（top_list）：需要 **3000 积分**

**解决方案**:
1. 先用免费接口
2. 每日签到攒积分
3. 考虑充值（建议 100 元 = 1000 积分起步）

### Q3: 接口调用频繁
- 普通用户：**100 次/分钟**
- 付费用户：**1000 次/分钟**

**解决方案**:
- 增加缓存（本地保存 5 分钟内数据）
- 批量查询（一次获取多只股票）

---

## 📋 配置检查清单

- [ ] 注册 Tushare 账号
- [ ] 获取 API Token
- [ ] 配置环境变量
- [ ] 安装 Python 依赖
- [ ] 测试连接成功
- [ ] 验证常用接口
- [ ] 集成到晚间推送
- [ ] 集成到持仓更新

---

## 🔗 参考链接

- 官网：https://tushare.pro
- 文档：https://tushare.pro/document/2
- 接口列表：https://tushare.pro/document/2?doc_id=25
- 积分规则：https://tushare.pro/document/2?doc_id=24

---

**配置完成后删除此文件，或移动到 `config/` 目录归档**
