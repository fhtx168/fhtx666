#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源测试脚本 - 验证所有金融数据 API 密钥是否正确加载
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path.home() / ".opcclaw" / ".env"
print("=" * 60)
print("数据源配置测试")
print("=" * 60)

print(f"\n.env 文件路径：{env_path}")
print(f".env 文件存在：{env_path.exists()}\n")

if env_path.exists():
    load_dotenv(env_path)
    print("[OK] 已加载 .env 文件\n")

# 测试所有密钥
tests = [
    ("东方财富妙想", "EASTMONEY_MIAOXIANG_API_KEY", "mkt_"),
    ("Tushare Pro", "TUSHARE_TOKEN", None),
    ("中金点晴 APP_ID", "CICC_APP_ID", None),
    ("中金点晴 SECRET", "CICC_APP_SECRET", None),
    ("DeepSeek", "DEEPSEEK_API_KEY", "sk-"),
    ("火山引擎", "VOLCENGINE_API_KEY", "ark-"),
    ("阿里云 DashScope", "DASHSCOPE_API_KEY", "sk-"),
    ("腾讯云", "TENCENT_SECRET_ID", "AKID"),
    ("360AI", "360AI_API_KEY", "ra1"),
]

print(f"{'数据源':<20} {'环境变量':<35} {'状态':<15} {'值 (前缀)'}")
print("-" * 80)

all_passed = True
for name, env_var, prefix in tests:
    value = os.getenv(env_var)
    if value:
        if prefix is None or value.startswith(prefix):
            status = "[OK]"
            display = value[:20] + "..." if len(value) > 20 else value
        else:
            status = "[WARN] 格式异常"
            display = value[:20]
            all_passed = False
    else:
        status = "[FAIL] 未设置"
        display = "-"
        all_passed = False
    
    print(f"{name:<20} {env_var:<35} {status:<15} {display}")

print("\n" + "=" * 60)
if all_passed:
    print("[SUCCESS] 所有数据源配置正常！")
else:
    print("[FAILED] 部分数据源配置异常，请检查上方标记项")
print("=" * 60)

sys.exit(0 if all_passed else 1)
