---
name: 360browser_shopping_compare
description: 根据用户输入的商品名称，用浏览器打开京东、淘宝，搜索此商品，读取各平台商品的优惠策略，包括优惠券等信息，综合测算后在多个电商平台进行比价。当用户提供商品名称，希望查看不同平台的价格信息、优惠信息，从而找到最划算的购买选项时使用。当用户输入提及某款商品的价格、哪个平台更便宜、购买、优惠、划算等关键词时，优先调用。常见的输入示例"<商品名称>怎么买最划算"，"<商品名称>价格"，"<商品名称>值得买吗"
cn-name: 购物比价助手
allowed-tools: Bash(360browser_shopping_compare:*)
timeout: 300
---

# Shopping Price Comparison Skill

## When to use

- **User's intent is to query/compare commodity prices**: The user says they want to check the price of a specific commodity, or compare prices across multiple platforms, and expects the system to help them get price information from different e-commerce platforms and find the most cost-effective option.

Call this skill whenever the user's clear intent is to **query/compare the price of a specific commodity**, and they provide the **name** of the commodity. For example:

- "Help me check the price of this commodity"
- "Compare the prices of this mobile phone on major platforms"
- "I want to see which platform sells <commodity name> cheaper"

## Quick start

```bash
node scripts/360browser_shopping_compare.mjs shop 'commodity_name'  # Get price info of this commodity across multiple e-commerce platforms
```

## Notes

- **Extended timeout**: This skill requires extended execution time (300 seconds) due to:
  - Browser startup and page loading
  - Login detection and authentication processes
  - Multi-platform search and data extraction
  - Network latency and page rendering delays
