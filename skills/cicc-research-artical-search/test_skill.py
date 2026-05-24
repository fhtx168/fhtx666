#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中金点晴技能测试脚本
"""

import asyncio
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.get_data import query_search_data

async def main():
    print("=" * 60)
    print("中金点晴研究文章搜索技能测试")
    print("=" * 60)
    
    # 从环境变量获取密钥
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    
    if not app_id or not app_secret:
        print("[错误] 未找到环境变量 APP_ID 或 APP_SECRET")
        print("请确认已在 C:\\Users\\Admin\\.opcclaw\\.env 中配置")
        return
    
    print(f"[信息] APP_ID: {app_id[:20]}...")
    print(f"[信息] APP_SECRET: {app_secret[:10]}...")
    print()
    
    # 测试查询
    query = "人工智能发展趋势"
    print(f"[测试] 查询关键词：{query}")
    print()
    
    result = await query_search_data(
        query=query,
        app_id=app_id,
        app_secret=app_secret,
        output_dir=None,
        save_to_file=False,
    )
    
    if result.get("error"):
        print(f"[错误] {result['error']}")
    else:
        print("[成功] 查询完成！")
        print()
        print("=" * 60)
        print("搜索结果：")
        print("=" * 60)
        print(result.get("content", "无内容"))
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
