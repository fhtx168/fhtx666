#!/usr/bin/env python3
"""
PDF 文本提取工具
从 PDF 文件中提取所有文本内容
"""
import sys
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    从 PDF 文件中提取所有文本
    
    Args:
        pdf_path: PDF 文件路径
        
    Returns:
        提取的文本内容
    """
    try:
        reader = PdfReader(pdf_path)
        text_content = []
        
        # 遍历所有页面
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text.strip():
                text_content.append(f"=== 第 {page_num} 页 ===\n{page_text}\n")
        
        return "\n".join(text_content)
    
    except Exception as e:
        return f"错误：无法提取 PDF 文本 - {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_text.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    text = extract_text_from_pdf(pdf_file)
    print(text)
