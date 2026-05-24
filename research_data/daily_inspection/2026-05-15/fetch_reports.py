#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import akshare as ak
import pandas as pd
import sys
import json
from datetime import datetime

# Target stocks with their codes
target_stocks = {
    "沪电股份": "002463",
    "中国铀业": "01164",  # HK stock, might be different
    "阳光电源": "300274", 
    "中芯国际": "688981",  # A share code
    "通富微电": "002156"
}

def fetch_research_reports():
    """Try to fetch research reports using AKShare"""
    results = {}
    
    # Try different AKShare functions that might provide research reports
    try:
        # Check if there's a research report function
        print("Checking available AKShare functions...")
        
        # Try stock_news_em - might contain analyst reports
        for stock_name, stock_code in target_stocks.items():
            print(f"\nFetching data for {stock_name} ({stock_code})")
            
            try:
                # Try to get stock info first
                stock_info = ak.stock_individual_info_em(symbol=stock_code)
                print(f"Stock info for {stock_name}:")
                print(stock_info.head())
                
                # Try to get recent news which might include research reports
                try:
                    news = ak.stock_news_em(symbol=stock_code)
                    if not news.empty:
                        print(f"Recent news for {stock_name}:")
                        print(news[['title', 'pub_date']].head(3))
                except Exception as e:
                    print(f"No news data for {stock_name}: {e}")
                    
            except Exception as e:
                print(f"Error fetching data for {stock_name}: {e}")
                
    except Exception as e:
        print(f"Error in main function: {e}")
        return None
        
    return results

if __name__ == "__main__":
    results = fetch_research_reports()
    if results:
        print("\nSuccessfully fetched some data")
    else:
        print("\nNo research report data found")