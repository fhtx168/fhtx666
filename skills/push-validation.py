# 推送前验证脚本

> 用途：所有推送前必须执行此验证
> 创建时间：2026-05-04

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送前验证脚本
- 日期/假期验证
- 数据时效性验证
- 数据合理性检查
- 多数据源交叉验证
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
HOLIDAY_CALENDAR = WORKSPACE / "config" / "holiday-calendar.json"
DATA_QUALITY_CONFIG = WORKSPACE / "skills" / "data-quality-control.md"

# 数据合理性范围
DATA_RANGES = {
    '上证指数': {'min': 2000, 'max': 6000, 'max_daily_change': 0.10},
    '深证成指': {'min': 8000, 'max': 20000, 'max_daily_change': 0.10},
    '创业板指': {'min': 1500, 'max': 5000, 'max_daily_change': 0.20},
    '成交量': {'min': 500000000000, 'max': 5000000000000},  # 5000 亿 -5 万亿
}

# 数据最大允许延迟（小时）
MAX_DATA_AGE = {
    '大盘指数': 24,
    '持仓数据': 24,
    '个股行情': 1,
    '资讯新闻': 24,
}

# ==================== 假期日历验证 ====================

def load_holiday_calendar():
    """加载假期日历"""
    if not HOLIDAY_CALENDAR.exists():
        # 创建默认假期日历
        default_calendar = {
            "2026": {
                "2026-01-01": "元旦",
                "2026-02-18": "春节",
                "2026-02-19": "春节",
                "2026-02-20": "春节",
                "2026-02-21": "春节",
                "2026-02-22": "春节",
                "2026-02-23": "春节",
                "2026-02-24": "春节",
                "2026-04-05": "清明",
                "2026-04-06": "清明",
                "2026-05-01": "劳动节",
                "2026-05-02": "劳动节",
                "2026-05-03": "劳动节",
                "2026-05-04": "劳动节",
                "2026-05-05": "劳动节",
                "2026-06-19": "端午",
                "2026-06-20": "端午",
                "2026-06-21": "端午",
                "2026-09-25": "中秋",
                "2026-09-26": "中秋",
                "2026-09-27": "中秋",
                "2026-10-01": "国庆",
                "2026-10-02": "国庆",
                "2026-10-03": "国庆",
                "2026-10-04": "国庆",
                "2026-10-05": "国庆",
                "2026-10-06": "国庆",
                "2026-10-07": "国庆",
            }
        }
        HOLIDAY_CALENDAR.parent.mkdir(parents=True, exist_ok=True)
        with open(HOLIDAY_CALENDAR, 'w', encoding='utf-8') as f:
            json.dump(default_calendar, f, ensure_ascii=False, indent=2)
        return default_calendar["2026"]
    
    with open(HOLIDAY_CALENDAR, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("2026", {})

def is_trading_day(date=None):
    """
    验证是否为交易日
    
    Returns:
        (bool, str): (是否交易日，说明)
    """
    if date is None:
        date = datetime.now()
    
    # 1. 检查周末
    if date.weekday() >= 5:
        return False, f"周末休市（星期{date.weekday()+1}）"
    
    # 2. 检查法定节假日
    holidays = load_holiday_calendar()
    date_str = date.strftime("%Y-%m-%d")
    if date_str in holidays:
        return False, f"法定节假日：{holidays[date_str]}"
    
    # 3. 检查特殊休市（临时通知）
    # TODO: 从交易所 API 获取
    
    return True, "交易日"

# ==================== 数据时效性验证 ====================

def validate_data_freshness(data_time, max_age_hours=24):
    """
    验证数据时效性
    
    Args:
        data_time: 数据时间（datetime 或字符串）
        max_age_hours: 最大允许延迟（小时）
    
    Returns:
        (bool, str): (是否新鲜，说明)
    """
    if isinstance(data_time, str):
        data_time = datetime.fromisoformat(data_time)
    
    age = datetime.now() - data_time
    age_hours = age.total_seconds() / 3600
    
    if age_hours > max_age_hours:
        return False, f"数据已过期 {age_hours:.1f} 小时（最大允许{max_age_hours}小时）"
    
    return True, f"数据新鲜（{age_hours:.1f}小时前）"

# ==================== 数据合理性检查 ====================

def validate_data_range(data_type, value, last_value=None):
    """
    验证数据合理性
    
    Args:
        data_type: 数据类型（如'上证指数'）
        value: 当前值
        last_value: 上次值（用于计算变化率）
    
    Returns:
        (bool, str): (是否合理，说明)
    """
    if data_type not in DATA_RANGES:
        return True, f"未知数据类型 {data_type}，跳过合理性检查"
    
    config = DATA_RANGES[data_type]
    
    # 1. 范围检查
    if not (config['min'] <= value <= config['max']):
        return False, f"{data_type} 超出合理范围：{value}（合理范围：{config['min']}-{config['max']}）"
    
    # 2. 变化率检查
    if last_value and 'max_daily_change' in config:
        change_rate = abs(value - last_value) / last_value
        if change_rate > config['max_daily_change']:
            return False, f"{data_type} 波动过大：{change_rate*100:.1f}%（最大允许{config['max_daily_change']*100:.0f}%）"
    
    return True, f"{data_type} 数据合理：{value}"

# ==================== 多数据源交叉验证 ====================

def fetch_from_source(source_name, url, params=None):
    """
    从数据源获取数据
    
    Returns:
        (dict or None): 数据或 None
    """
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"数据源 {source_name} 失败：{e}")
        return None

def cross_validate(sources):
    """
    多数据源交叉验证
    
    Args:
        sources: 数据源列表 [{'name': str, 'url': str, 'params': dict}]
    
    Returns:
        (dict, list): (最佳数据，所有结果)
    """
    results = []
    
    for source in sources:
        data = fetch_from_source(source['name'], source['url'], source.get('params'))
        if data:
            results.append({
                'source': source['name'],
                'data': data,
                'timestamp': datetime.now()
            })
    
    if len(results) == 0:
        return None, []
    
    if len(results) == 1:
        return results[0]['data'], results
    
    # 比较各数据源结果
    values = [r['data'].get('value') for r in results if r['data'].get('value')]
    if len(values) >= 2:
        max_diff = max(values) - min(values)
        avg_value = sum(values) / len(values)
        if max_diff / avg_value > 0.05:  # 差异超过 5%
            print(f"⚠️ 数据源差异过大：{max_diff/avg_value*100:.1f}%")
            # TODO: 发送告警
    
    # 返回最新的数据
    results.sort(key=lambda x: x['timestamp'], reverse=True)
    return results[0]['data'], results

# ==================== 推送前完整验证 ====================

def pre_push_validation(push_type, data):
    """
    推送前完整验证
    
    Args:
        push_type: 推送类型（'早间速览'/'收盘复盘'/'晚间策略'）
        data: 推送数据
    
    Returns:
        (bool, list): (是否通过，错误列表)
    """
    errors = []
    warnings = []
    
    # 0. 持仓数据验证（P0 强制）
    holdings_path = Path(r"C:\Users\Admin\.opcclaw\workspace\portfolio\holdings.md")
    if not holdings_path.exists():
        errors.append("🔴 持仓文件缺失！")
    else:
        # 验证持仓文件是否可读
        try:
            with open(holdings_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '总计：' not in content or 'A 股市值' not in content:
                    errors.append("🔴 持仓文件格式错误！")
                else:
                    print(f"✅ 持仓数据验证通过：{holdings_path}")
        except Exception as e:
            errors.append(f"🔴 持仓文件读取失败：{e}")
    
    # 1. 日期/假期验证
    is_trading, msg = is_trading_day()
    if not is_trading and push_type in ['早间速览', '收盘复盘']:
        errors.append(f"日期错误：{msg}，不应发送{push_type}")
    
    # 2. 数据时效性验证
    if 'data_time' in data:
        fresh, msg = validate_data_freshness(data['data_time'])
        if not fresh:
            errors.append(f"数据时效：{msg}")
    
    # 3. 数据合理性检查
    if '上证指数' in data:
        valid, msg = validate_data_range('上证指数', data['上证指数'])
        if not valid:
            errors.append(f"数据合理：{msg}")
    
    # 4. 内容一致性检查
    if is_trading and '开盘策略' not in str(data):
        warnings.append("交易日推送应包含开盘策略")
    if not is_trading and '开盘策略' in str(data):
        errors.append("休市日不应包含开盘策略")
    
    # 输出结果
    print("=" * 50)
    print(f"推送前验证：{push_type}")
    print("=" * 50)
    
    if errors:
        print("❌ 错误：")
        for e in errors:
            print(f"  - {e}")
    
    if warnings:
        print("⚠️ 警告：")
        for w in warnings:
            print(f"  - {w}")
    
    if not errors and not warnings:
        print("✅ 验证通过")
    
    print("=" * 50)
    
    return len(errors) == 0, errors

# ==================== 主程序 ====================

if __name__ == "__main__":
    # 测试示例
    print("推送前验证脚本 - 测试模式")
    print()
    
    # 测试日期验证
    today = datetime.now()
    is_trading, msg = is_trading_day(today)
    print(f"今天（{today.strftime('%Y-%m-%d')}）：{msg}")
    
    # 测试数据合理性
    valid, msg = validate_data_range('上证指数', 4107.51, 4080.00)
    print(f"上证指数验证：{msg}")
    
    # 测试推送验证
    test_data = {
        'data_time': datetime.now() - timedelta(hours=1),
        '上证指数': 4107.51,
    }
    passed, errors = pre_push_validation('早间速览', test_data)
    print(f"推送验证：{'通过' if passed else '失败'}")

```

---

## 使用方法

### 1. 手动验证

```bash
python skills/push-validation.py
```

### 2. 推送前自动调用

```python
from push_validation import pre_push_validation

# 推送前验证
passed, errors = pre_push_validation('早间速览', data)
if not passed:
    alert("推送验证失败", errors)
    return
```

### 3. Cron 任务集成

在 cron 任务配置中添加验证步骤：

```json
{
  "preExecute": "python skills/push-validation.py",
  "onValidationFail": "abort_and_alert"
}
```

---

_创建时间：2026-05-04_
