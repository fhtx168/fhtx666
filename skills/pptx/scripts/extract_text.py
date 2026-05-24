#!/usr/bin/env python3
"""
PPTX 文本提取工具
从 PPTX 文件中提取所有文本内容
"""
import sys
import zipfile
from xml.etree import ElementTree as ET


def extract_text_from_pptx(pptx_path: str) -> str:
    """
    从 PPTX 文件中提取所有文本
    
    Args:
        pptx_path: PPTX 文件路径
        
    Returns:
        提取的文本内容
    """
    try:
        text_content = []
        
        # PPTX 文件是一个 ZIP 压缩包
        with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
            # 获取所有幻灯片文件
            slide_files = [f for f in zip_ref.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            slide_files.sort()  # 按顺序排序
            
            # 定义 XML 命名空间
            namespaces = {
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
            }
            
            # 遍历每个幻灯片
            for slide_num, slide_file in enumerate(slide_files, start=1):
                slide_text = []
                
                # 读取幻灯片 XML
                with zip_ref.open(slide_file) as xml_file:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    # 提取所有文本节点 (a:t 标签)
                    for text_elem in root.findall('.//a:t', namespaces):
                        if text_elem.text:
                            slide_text.append(text_elem.text)
                
                # 如果幻灯片有文本，添加到结果中
                if slide_text:
                    text_content.append(f"=== 幻灯片 {slide_num} ===\n" + "\n".join(slide_text) + "\n")
        
        return "\n".join(text_content) if text_content else "未找到文本内容"
    
    except Exception as e:
        return f"错误：无法提取 PPTX 文本 - {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_text.py <pptx_file>")
        sys.exit(1)
    
    pptx_file = sys.argv[1]
    text = extract_text_from_pptx(pptx_file)
    print(text)
