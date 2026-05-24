#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业绩效评价模型
基于三十维 v2.0 框架，专注于企业执行质量维度评估
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnterprisePerformanceEvaluator:
    """企业绩效评价器"""
    
    def __init__(self):
        self.weights = {
            'financial_health': 0.35,      # 财务健康度 (10% of total)
            'management_capability': 0.27, # 管理层能力 (8% of total)  
            'innovation_efficiency': 0.23, # 创新投入产出 (7% of total)
            'governance_quality': 0.15     # 治理规范性 (5% of total)
        }
        
    def evaluate_financial_health(self, stock_code: str, financial_data: Dict) -> Dict:
        """
        评估财务健康度
        包含：现金流、负债率、ROE稳定性、盈利能力
        """
        score = 0
        details = {}
        
        # 现金流健康度 (30%)
        cash_flow_ratio = financial_data.get('operating_cash_flow', 0) / max(financial_data.get('net_profit', 1), 1)
        if cash_flow_ratio >= 1.0:
            cash_score = 100
        elif cash_flow_ratio >= 0.8:
            cash_score = 85
        elif cash_flow_ratio >= 0.6:
            cash_score = 70
        elif cash_flow_ratio >= 0.4:
            cash_score = 55
        else:
            cash_score = 40
        details['cash_flow_health'] = {'score': cash_score, 'ratio': cash_flow_ratio}
        score += cash_score * 0.3
        
        # 负债率合理性 (25%)
        debt_ratio = financial_data.get('total_liabilities', 0) / max(financial_data.get('total_assets', 1), 1)
        if debt_ratio <= 0.3:
            debt_score = 100
        elif debt_ratio <= 0.5:
            debt_score = 85
        elif debt_ratio <= 0.7:
            debt_score = 70
        elif debt_ratio <= 0.8:
            debt_score = 55
        else:
            debt_score = 40
        details['debt_ratio'] = {'score': debt_score, 'ratio': debt_ratio}
        score += debt_score * 0.25
        
        # ROE稳定性 (25%)
        roe_list = financial_data.get('roe_history', [])
        if len(roe_list) >= 3:
            avg_roe = sum(roe_list) / len(roe_list)
            roe_volatility = sum(abs(roe - avg_roe) for roe in roe_list) / len(roe_list)
            if avg_roe >= 15 and roe_volatility <= 5:
                roe_score = 100
            elif avg_roe >= 10 and roe_volatility <= 8:
                roe_score = 85
            elif avg_roe >= 8 and roe_volatility <= 12:
                roe_score = 70
            else:
                roe_score = 50
        else:
            roe_score = 60
        details['roe_stability'] = {'score': roe_score, 'avg_roe': sum(roe_list)/len(roe_list) if roe_list else 0}
        score += roe_score * 0.25
        
        # 盈利能力趋势 (20%)
        profit_trend = financial_data.get('profit_growth_trend', 0)
        if profit_trend > 0.2:
            profit_score = 100
        elif profit_trend > 0.1:
            profit_score = 85
        elif profit_trend > 0:
            profit_score = 70
        elif profit_trend > -0.1:
            profit_score = 55
        else:
            profit_score = 40
        details['profit_trend'] = {'score': profit_score, 'trend': profit_trend}
        score += profit_score * 0.2
        
        return {
            'dimension': 'financial_health',
            'score': round(score, 2),
            'weight': self.weights['financial_health'],
            'weighted_score': round(score * self.weights['financial_health'], 2),
            'details': details
        }
    
    def evaluate_management_capability(self, stock_code: str, management_data: Dict) -> Dict:
        """
        评估管理层能力
        包含：战略规划、执行效果、资本配置效率
        """
        score = 0
        details = {}
        
        # 战略清晰度 (40%)
        strategy_clarity = management_data.get('strategy_clarity_score', 0)
        if strategy_clarity >= 80:
            strategy_score = 100
        elif strategy_clarity >= 60:
            strategy_score = 85
        elif strategy_clarity >= 40:
            strategy_score = 70
        else:
            strategy_score = 50
        details['strategy_clarity'] = {'score': strategy_score, 'value': strategy_clarity}
        score += strategy_score * 0.4
        
        # 执行效果 (40%)
        execution_effectiveness = management_data.get('execution_score', 0)
        if execution_effectiveness >= 85:
            execution_score = 100
        elif execution_effectiveness >= 70:
            execution_score = 85
        elif execution_effectiveness >= 55:
            execution_score = 70
        else:
            execution_score = 50
        details['execution_effectiveness'] = {'score': execution_score, 'value': execution_effectiveness}
        score += execution_score * 0.4
        
        # 资本配置效率 (20%)
        capital_efficiency = management_data.get('capital_allocation_score', 0)
        if capital_efficiency >= 90:
            capital_score = 100
        elif capital_efficiency >= 75:
            capital_score = 85
        elif capital_efficiency >= 60:
            capital_score = 70
        else:
            capital_score = 50
        details['capital_efficiency'] = {'score': capital_score, 'value': capital_efficiency}
        score += capital_score * 0.2
        
        return {
            'dimension': 'management_capability',
            'score': round(score, 2),
            'weight': self.weights['management_capability'],
            'weighted_score': round(score * self.weights['management_capability'], 2),
            'details': details
        }
    
    def evaluate_innovation_efficiency(self, stock_code: str, innovation_data: Dict) -> Dict:
        """
        评估创新投入产出效率
        包含：研发投入占比、专利质量、技术转化能力
        """
        score = 0
        details = {}
        
        # 研发投入强度 (35%)
        rd_ratio = innovation_data.get('rd_expense_ratio', 0)
        if rd_ratio >= 0.15:
            rd_score = 100
        elif rd_ratio >= 0.1:
            rd_score = 85
        elif rd_ratio >= 0.07:
            rd_score = 70
        elif rd_ratio >= 0.05:
            rd_score = 55
        else:
            rd_score = 40
        details['rd_intensity'] = {'score': rd_score, 'ratio': rd_ratio}
        score += rd_score * 0.35
        
        # 专利质量 (35%)
        patent_quality = innovation_data.get('patent_quality_score', 0)
        if patent_quality >= 85:
            patent_score = 100
        elif patent_quality >= 70:
            patent_score = 85
        elif patent_quality >= 55:
            patent_score = 70
        else:
            patent_score = 50
        details['patent_quality'] = {'score': patent_score, 'value': patent_quality}
        score += patent_score * 0.35
        
        # 技术转化效率 (30%)
        tech_conversion = innovation_data.get('tech_conversion_rate', 0)
        if tech_conversion >= 0.3:
            conversion_score = 100
        elif tech_conversion >= 0.2:
            conversion_score = 85
        elif tech_conversion >= 0.15:
            conversion_score = 70
        elif tech_conversion >= 0.1:
            conversion_score = 55
        else:
            conversion_score = 40
        details['tech_conversion'] = {'score': conversion_score, 'rate': tech_conversion}
        score += conversion_score * 0.3
        
        return {
            'dimension': 'innovation_efficiency',
            'score': round(score, 2),
            'weight': self.weights['innovation_efficiency'],
            'weighted_score': round(score * self.weights['innovation_efficiency'], 2),
            'details': details
        }
    
    def evaluate_governance_quality(self, stock_code: str, governance_data: Dict) -> Dict:
        """
        评估治理规范性
        包含：ESG表现、股权结构、激励机制、合规记录
        """
        score = 0
        details = {}
        
        # ESG评级 (40%)
        esg_score = governance_data.get('esg_rating', 0)
        if esg_score >= 80:
            esg_eval = 100
        elif esg_score >= 65:
            esg_eval = 85
        elif esg_score >= 50:
            esg_eval = 70
        else:
            esg_eval = 50
        details['esg_rating'] = {'score': esg_eval, 'value': esg_score}
        score += esg_eval * 0.4
        
        # 股权结构合理性 (25%)
        ownership_structure = governance_data.get('ownership_structure_score', 0)
        if ownership_structure >= 85:
            ownership_score = 100
        elif ownership_structure >= 70:
            ownership_score = 85
        elif ownership_structure >= 55:
            ownership_score = 70
        else:
            ownership_score = 50
        details['ownership_structure'] = {'score': ownership_score, 'value': ownership_structure}
        score += ownership_score * 0.25
        
        # 激励机制有效性 (20%)
        incentive_effectiveness = governance_data.get('incentive_effectiveness', 0)
        if incentive_effectiveness >= 90:
            incentive_score = 100
        elif incentive_effectiveness >= 75:
            incentive_score = 85
        elif incentive_effectiveness >= 60:
            incentive_score = 70
        else:
            incentive_score = 50
        details['incentive_effectiveness'] = {'score': incentive_score, 'value': incentive_effectiveness}
        score += incentive_score * 0.2
        
        # 合规记录 (15%)
        compliance_record = governance_data.get('compliance_score', 0)
        if compliance_record >= 95:
            compliance_score = 100
        elif compliance_record >= 85:
            compliance_score = 85
        elif compliance_record >= 75:
            compliance_score = 70
        else:
            compliance_score = 50
        details['compliance_record'] = {'score': compliance_score, 'value': compliance_record}
        score += compliance_score * 0.15
        
        return {
            'dimension': 'governance_quality',
            'score': round(score, 2),
            'weight': self.weights['governance_quality'],
            'weighted_score': round(score * self.weights['governance_quality'], 2),
            'details': details
        }
    
    def evaluate_enterprise_performance(self, stock_code: str, data: Dict) -> Dict:
        """
        综合评估企业绩效
        """
        logger.info(f"评估企业绩效: {stock_code}")
        
        # 获取各维度数据
        financial_data = data.get('financial', {})
        management_data = data.get('management', {})
        innovation_data = data.get('innovation', {})
        governance_data = data.get('governance', {})
        
        # 评估各维度
        financial_result = self.evaluate_financial_health(stock_code, financial_data)
        management_result = self.evaluate_management_capability(stock_code, management_data)
        innovation_result = self.evaluate_innovation_efficiency(stock_code, innovation_data)
        governance_result = self.evaluate_governance_quality(stock_code, governance_data)
        
        # 计算总分
        total_weighted_score = (
            financial_result['weighted_score'] +
            management_result['weighted_score'] +
            innovation_result['weighted_score'] +
            governance_result['weighted_score']
        )
        
        # 标准化到100分制
        total_score = min(100, max(0, total_weighted_score * 100))
        
        return {
            'stock_code': stock_code,
            'evaluation_date': datetime.now().strftime('%Y-%m-%d'),
            'total_score': round(total_score, 2),
            'dimensions': [
                financial_result,
                management_result,
                innovation_result,
                governance_result
            ],
            'recommendation': self._generate_recommendation(total_score)
        }
    
    def _generate_recommendation(self, total_score: float) -> str:
        """生成建议"""
        if total_score >= 85:
            return "优秀 - 核心持仓，可适度加仓"
        elif total_score >= 70:
            return "良好 - 继续持有，关注改善机会"
        elif total_score >= 60:
            return "一般 - 密切监控，谨慎操作"
        else:
            return "较差 - 考虑调出，寻找替代标的"

def main():
    """测试函数"""
    evaluator = EnterprisePerformanceEvaluator()
    
    # 测试数据
    test_data = {
        'financial': {
            'operating_cash_flow': 1000000000,
            'net_profit': 800000000,
            'total_liabilities': 5000000000,
            'total_assets': 10000000000,
            'roe_history': [18, 20, 19],
            'profit_growth_trend': 0.15
        },
        'management': {
            'strategy_clarity_score': 85,
            'execution_score': 80,
            'capital_allocation_score': 75
        },
        'innovation': {
            'rd_expense_ratio': 0.12,
            'patent_quality_score': 80,
            'tech_conversion_rate': 0.25
        },
        'governance': {
            'esg_rating': 75,
            'ownership_structure_score': 80,
            'incentive_effectiveness': 85,
            'compliance_score': 90
        }
    }
    
    result = evaluator.evaluate_enterprise_performance("TEST001", test_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()