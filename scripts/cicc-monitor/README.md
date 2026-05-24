# 中金点晴 API 集成指南

## ✅ 密钥已配置

**存储位置**：`C:\Users\Admin\.opcclaw\.env`

```bash
CICC_APP_ID=17781430846340957@765063
CICC_APP_SECRET=lYthZdt8w2zxzBF24zks8XpGxvbhE6tI
```

---

## 📁 文件结构

```
scripts/
└── cicc-monitor/
    ├── api_client.py          # API 调用客户端
    ├── test_api.py            # 测试脚本（待创建）
    └── README.md              # 本文档
```

---

## 🧪 测试步骤

### 第一步：确认 API 端点

**需要补充的信息**（请查看飞书文档）：

1. **API Base URL**：`_________________________`
2. **获取 Token 的端点**：`_________________________`
3. **研报查询端点**：`_________________________`
4. **宏观数据端点**：`_________________________`
5. **公司数据端点**：`_________________________`
6. **市场数据端点**：`_________________________`

### 第二步：更新配置

编辑 [`api_client.py`](file:///C:/Users/Admin/opcclawai/project/scripts/cicc-monitor/api_client.py)，更新 `CONFIG` 中的 `base_url`：

```python
CONFIG = {
    "base_url": "https://你的 API 端点",  # ← 修改这里
    ...
}
```

### 第三步：运行测试

```bash
cd scripts/cicc-monitor
python api_client.py
```

---

## 📊 调用场景配置

### 场景 1：早盘准备（08:00）

**调用内容**：
- 隔夜外盘数据
- 宏观新闻汇总
- 晨会纪要

**代码示例**：
```python
from api_client import get_research_reports, get_macro_data

# 获取晨会纪要
reports = get_research_reports(keyword="晨会纪要", limit=5)

# 获取宏观新闻
macro = get_macro_data(indicator="全部")
```

### 场景 2：盘中监控（交易时段）

**调用内容**：
- 持仓股相关研报
- 行业快讯
- 资金流向

**代码示例**：
```python
from api_client import get_company_info, get_market_data

# 获取持仓股信息
for stock in holdings:
    info = get_company_info(stock_code=stock)
    data = get_market_data(stock_code=stock)
```

### 场景 3：收盘复盘（15:30）

**调用内容**：
- 收盘点评
- 龙虎榜数据
- 当日研报汇总

### 场景 4：晚间推送（21:00）

**调用内容**：
- 晚间研报
- 明日策略
- 外围市场

---

## 🔧 与现有系统集成

### 集成到投研知识库

```python
# 保存中金研报到知识库
from api_client import get_research_reports, save_to_cache

reports = get_research_reports(keyword="A 股策略")
save_to_cache(reports, "daily_reports", category="research")
```

### 集成到晚间推送

```python
# 在晚间资讯推送中加入中金观点
from api_client import get_research_reports

evening_reports = get_research_reports(
    keyword="收盘复盘",
    date_range=["2026-05-07", "2026-05-07"]
)
```

---

## ⚠️ 注意事项

### 1. API 配额管理

- 查询剩余额度：`GET /quota/query`
- 配额预警：剩余 20% 时降级为 P0 only
- 配额重置时间：每日 00:00

### 2. 错误处理

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 401 | 认证失败 | 重新获取 token |
| 403 | 权限不足 | 检查配额 |
| 429 | 请求超限 | 指数退避 |
| 500 | 服务器错误 | 重试或降级 |

### 3. 缓存策略

| 数据类型 | 缓存时间 | 说明 |
|---------|---------|------|
| 宏观数据 | 24 小时 | 变化较慢 |
| 行业数据 | 12 小时 | 中等频率 |
| 公司数据 | 6 小时 | 较快变化 |
| 行情数据 | 5 分钟 | 实时性高 |
| 研报内容 | 7 天 | 静态内容 |

---

## 📝 待确认事项

- [ ] API Base URL
- [ ] 各功能端点路径
- [ ] 日调用配额
- [ ] 并发限制
- [ ] 数据范围权限
- [ ] 特殊字段说明

---

## 🚀 下一步

1. **补充 API 端点信息**（查看飞书文档）
2. **更新 api_client.py 配置**
3. **运行测试脚本**
4. **验证数据质量**
5. **集成到现有系统**

---

**最后更新**：2026-05-07  
**状态**：密钥已配置，待补充 API 端点
