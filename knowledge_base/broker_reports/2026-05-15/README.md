# 券商研报抓取结果 - 2026-05-15

本目录包含今日抓取的叶荣添七张底牌相关领域的券商研报，已使用broker-report-parser技能解析为结构化JSON格式。

## 文件命名规则
`{领域}_{股票简称}_{券商}_{日期}.json`

## 抓取领域
- AI芯片 (AI Chip)
- 光模块 (Optical Module)  
- 先进封装 (Advanced Packaging)
- 液冷 (Liquid Cooling)
- PCB

## 数据结构
每个JSON文件包含以下字段：
- stock_name: 股票名称
- stock_code: 股票代码
- broker: 券商名称
- analyst: 分析师
- report_date: 发布日期
- rating: 评级
- target_price: 目标价
- current_price: 当前价
- upside: 预期涨幅%
- core_thesis: 核心投资逻辑
- financial_forecast: 财务预测
- key_catalysts: 关键催化剂
- risks: 风险提示
- sentiment: 市场情绪