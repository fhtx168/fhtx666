#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三维投资评估引擎
基于宏观大势、产业逻辑、企业绩效的综合评分系统
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple

# 添加脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# 动态导入模块（处理连字符文件名）
import importlib.util

# 导入宏观大势监测模块
spec1 = importlib.util.spec_from_file_location("macro_trend_monitor", os.path.join(script_dir, "macro-trend-monitor.py"))
macro_trend_monitor = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(macro_trend_monitor)

# 导入产业逻辑分析模块  
spec2 = importlib.util.spec_from_file_location("industry_logic_analyzer", os.path.join(script_dir, "industry-logic-analyzer.py"))
industry_logic_analyzer = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(industry_logic_analyzer)

# 导入企业绩效评价模块
spec3 = importlib.util.spec_from_file_location("enterprise_performance_evaluator", os.path.join(script_dir, "enterprise-performance-evaluator.py"))
enterprise_performance_evaluator = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(enterprise_performance_evaluator)

class ThreeDimensionalEvaluator:
    """三维投资评估引擎"""
    
    def __init__(self):
        self.macro_monitor = macro_trend_monitor.MacroTrendMonitor()
        self.industry_analyzer = industry_logic_analyzer.IndustryLogicAnalyzer()
        self.enterprise_evaluator = enterprise_performance_evaluator.EnterprisePerformanceEvaluator()
        
        # 三维权重配置（中线投资导向）
        self.weights = {
            'macro_trend': 0.30,      # 宏观大势适配度
            'industry_logic': 0.40,   # 产业逻辑强度  
            'enterprise_performance': 0.30  # 企业执行质量
        }
    
    def evaluate_stock(self, stock_code: str, stock_name: str) -> Dict:
        """
        对单只股票进行三维评估
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            
        Returns:
            包含各维度评分和综合评分的字典
        """
        print(f"正在评估 {stock_name}({stock_code})...")
        
        # 1. 宏观大势适配度评估
        macro_score = self.macro_monitor.calculate_macro_score()['weighted_score']
        
        # 2. 产业逻辑强度评估  
        industry_result = self.industry_analyzer.calculate_industry_logic_score(stock_name, self._get_industry(stock_code))
        industry_score = industry_result['industry_logic_score']
        
        # 3. 企业执行质量评估
        enterprise_score = self.enterprise_evaluator.evaluate_enterprise_performance(stock_code, stock_name)
        
        # 4. 计算综合评分
        total_score = (
            macro_score * self.weights['macro_trend'] +
            industry_score * self.weights['industry_logic'] +
            enterprise_score * self.weights['enterprise_performance']
        )
        
        result = {
            'stock_code': stock_code,
            'stock_name': stock_name,
            'evaluation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scores': {
                'macro_trend': round(macro_score, 2),
                'industry_logic': round(industry_score, 2), 
                'enterprise_performance': round(enterprise_score, 2),
                'total_score': round(total_score, 2)
            },
            'weights': self.weights,
            'recommendation': self._generate_recommendation(total_score, macro_score, industry_score, enterprise_score)
        }
        
        return result
    
    def _generate_recommendation(self, total_score: float, macro_score: float, 
                               industry_score: float, enterprise_score: float) -> str:
        """生成调仓建议"""
        
        # 一票否决条件检查（在具体实现中会详细检查）
        if total_score <= 60:
            return "考虑减仓或清仓"
        elif total_score >= 85:
            return "核心持仓，可适度加仓"
        elif total_score >= 75:
            return "优质持仓，维持仓位"
        else:
            return "观察持仓，密切跟踪"
    
    def _get_industry(self, stock_code: str) -> str:
        """根据股票代码获取行业分类"""
        # 简化版本：基于股票代码前缀判断
        industry_map = {
            'SZ002594': '新能源汽车',
            'SZ002428': '半导体材料', 
            'SZ300620': '光通信',
            'SH688981': '半导体制造',
            'SZ002920': '汽车电子',
            'SH600989': '煤化工',
            'SZ000960': '有色金属',
            'SZ002460': '锂电池'
        }
        return industry_map.get(stock_code, '通用制造业')
    
    def batch_evaluate(self, holdings: List[Dict]) -> List[Dict]:
        """批量评估持仓股票"""
        results = []
        for holding in holdings:
            try:
                result = self.evaluate_stock(holding['code'], holding['name'])
                results.append(result)
            except Exception as e:
                print(f"评估 {holding['name']} 失败: {e}")
                continue
        return results

def load_holdings_from_file(file_path: str) -> List[Dict]:
    """从持仓文件加载股票列表"""
    # 这里需要解析 holdings.md 文件
    # 简化版本：返回示例数据
    return [
        {'name': '比亚迪', 'code': 'SZ002594'},
        {'name': '云南锗业', 'code': 'SZ002428'},
        {'name': '光库科技', 'code': 'SZ300620'}
    ]

if __name__ == "__main__":
    evaluator = ThreeDimensionalEvaluator()
    
    # 加载持仓数据
    holdings = load_holdings_from_file("portfolio/holdings.md")
    
    # 批量评估
    results = evaluator.batch_evaluate(holdings)
    
    # 保存结果
    output_file = f"portfolio/three-dimensional-evaluation-{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"三维评估完成！结果保存至: {output_file}")
    
    # 打印摘要
    print("\n=== 评估摘要 ===")
    for result in results[:5]:  # 只显示前5个
        print(f"{result['stock_name']}: {result['scores']['total_score']}分 - {result['recommendation']}")