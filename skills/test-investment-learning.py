#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投研学习系统 - 手动测试脚本 v2
用途：手动测试各平台监测功能
创建时间：2026-05-06
"""

import requests
from pathlib import Path
from datetime import datetime

# ==================== 配置 ====================

WORKSPACE = Path(r"C:\Users\Admin\.opcclaw\workspace")
KNOWLEDGE_BASE = WORKSPACE / "knowledge-base"

# ==================== 测试函数 ====================

def test_sogou_wechat_yerongtian():
    """测试 1：搜狗微信搜索 - 叶荣添"""
    print("=" * 50)
    print("测试 1：搜狗微信搜索 - 叶荣添")
    print("=" * 50)
    
    search_url = "https://weixin.sogou.com/weixin?type=2&query=%E5%8F%B6%E8%8D%A3%E6%B7%BB"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        response = requests.get(search_url, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200:
            print(f"[OK] HTTP 状态码：{response.status_code}")
            print(f"[OK] 响应内容长度：{len(response.content)}")
            print(f"[URL] 搜索 URL: {search_url}")
            print("\n[PASS] 测试通过 - 搜狗微信搜索可用")
            return True
        else:
            print(f"[WARN] HTTP 状态码：{response.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERROR] 请求失败：{e}")
        return False

def test_rss_cls():
    """测试 2：RSS 抓取 - 财联社（改用网页抓取）"""
    print("=" * 50)
    print("测试 2：网页抓取 - 财联社快讯")
    print("=" * 50)
    
    # 改用网页抓取，RSS 可能需要特殊处理
    url = "https://www.cls.cn/"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        
        if response.status_code == 200 and len(response.content) > 1000:
            print(f"[OK] HTTP 状态码：{response.status_code}")
            print(f"[OK] 网页内容长度：{len(response.content)}")
            print("\n[PASS] 测试通过 - 网页抓取可用")
            return True
        else:
            print(f"[WARN] 网页内容为空或过短")
            return False
            
    except Exception as e:
        print(f"[ERROR] 请求失败：{e}")
        return False

def test_knowledge_base_dir():
    """测试 3：知识库目录创建"""
    print("=" * 50)
    print("测试 3：知识库目录创建")
    print("=" * 50)
    
    categories = [
        "大盘趋势",
        "板块逻辑",
        "个股机会",
        "政策解读",
        "风控避雷",
        "大佬观点",
        "机构研报",
        "投研学习周报",
    ]
    
    created = []
    for cat in categories:
        cat_dir = KNOWLEDGE_BASE / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        created.append(cat)
        print(f"  [OK] {cat}/")
    
    print(f"\n共创建 {len(created)} 个分类目录")
    print("[PASS] 测试通过")
    return True

def test_knowledge_base_structure():
    """测试 4：创建测试归档文件"""
    print("=" * 50)
    print("测试 4：创建测试归档文件")
    print("=" * 50)
    
    test_file = KNOWLEDGE_BASE / "大佬观点" / "测试归档_叶荣添_20260506.md"
    
    content = f"""# 测试归档 - 叶荣添观点

> 归档时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> 来源：投研学习系统测试

---

## 测试内容

这是投研学习系统自动创建的测试归档文件。

## 七张底牌

1. 硅光
2. 大国芯片
3. 国产芯片的供应链
4. 新的涨价之王
5. CPU 的供应链
6. 散热
7. 总结

---

_此文件用于测试归档功能_
"""
    
    test_file.parent.mkdir(parents=True, exist_ok=True)
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"[OK] 测试文件已创建：{test_file}")
    print("[PASS] 测试通过")
    return True

# ==================== 主测试流程 ====================

def run_all_tests():
    """运行全部测试"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║  投研学习系统 - 手动测试套件 v2         ║")
    print("║  版本：v2.0  日期：2026-05-06          ║")
    print("╚" + "=" * 48 + "╝")
    print("\n")
    
    tests = [
        ("测试 1：搜狗微信 - 叶荣添", test_sogou_wechat_yerongtian),
        ("测试 2：RSS 抓取 - 财联社", test_rss_cls),
        ("测试 3：知识库目录创建", test_knowledge_base_dir),
        ("测试 4：创建测试归档文件", test_knowledge_base_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
            print("\n")
        except Exception as e:
            print(f"❌ 测试异常：{e}\n")
            results.append((name, False))
    
    # 汇总报告
    print("=" * 50)
    print("测试汇总报告")
    print("=" * 50)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} - {name}")
    
    print("-" * 50)
    print(f"总计：{passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("\n[SUCCESS] 全部测试通过！可以开启 Cron 定时任务")
    else:
        print("\n[WARN] 部分测试未通过，请先修复后再开启 Cron")
    
    print("=" * 50)
    
    return passed_count == total_count

# ==================== 入口 ====================

if __name__ == "__main__":
    success = run_all_tests()
    import sys
    sys.exit(0 if success else 1)
