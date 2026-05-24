#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三维投资评估引擎 - 简化版
"""

import json
from datetime import datetime

def evaluate_stock_simple(stock_name, stock_code):
    """简化版评估函数"""
    # 模拟评分（实际会调用各模块）
    macro_score = 85.0
    industry_score = 90.0
    enterprise_score = 80.0
    
    total_score = (macro_score * 0.3 + industry_score * 0.4 + enterprise_score * 0.3)
    
    if total_score >= 85:
        recommendation = "核心持仓，可适度加仓"
    elif total_score >= 75:
        recommendation = "优质持仓，维持仓位"
    elif total_score >= 60:
        recommendation = "观察持仓，密切跟踪"
    else:
        recommendation = "考虑减仓或清仓"
    
    return {
        'stock_code': stock_code,
        'stock_name': stock_name,
        'scores': {
            'macro_trend': round(macro_score, 2),
            'industry_logic': round(industry_score, 2),
            'enterprise_performance': round(enterprise_score, 2),
            'total_score': round(total_score, 2)
        },
        'recommendation': recommendation
    }

def main():
    # 测试股票列表
    test_stocks = [
        {'name': '比亚迪', 'code': 'SZ002594'},
        {'name': '云南锗业', 'code': 'SZ002428'},
        {'name': '光库科技', 'code': 'SZ300620'}
    ]
    
    results = []
    for stock in test_stocks:
        result = evaluate_stock_simple(stock['name'], stock['code'])
        results.append(result)
        print(f"{result['stock_name']}: {result['scores']['total_score']}分 - {result['recommendation']}")
    
    # 保存结果
    output_file = f"../portfolio/three-dimensional-evaluation-{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n评估完成！结果保存至: {output_file}")

if __name__ == "__main__":
    main()