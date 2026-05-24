import os
from docx import Document

# 找到文件
desktop = 'C:/Users/Admin/Desktop'
files = [f for f in os.listdir(desktop) if f.startswith('5') and f.endswith('.doc')]
if not files:
    print("未找到文件")
    exit()

filename = files[0]
filepath = os.path.join(desktop, filename)
print(f"找到文件：{filename}")

try:
    doc = Document(filepath)
    text_parts = []
    for para in doc.paragraphs:
        if para.text.strip():
            text_parts.append(para.text)
    
    full_text = '\n'.join(text_parts)
    print(f"\n提取完成，共 {len(full_text)} 字符")
    print(f"\n前 2000 字符预览:")
    print("=" * 50)
    print(full_text[:2000])
    print("=" * 50)
    
    # 保存到项目目录
    output_path = r'C:\Users\Admin\opcclawai\project\yrt_monitoring\live-2026-05-17-transcript.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print(f"\n已保存到：{output_path}")
    
except Exception as e:
    print(f"错误：{e}")
    # 尝试直接读取 XML
    import zipfile
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            doc_xml = z.read('word/document.xml').decode('utf-8')
            # 提取文本（简单方式）
            import re
            text = re.sub(r'<[^>]+>', ' ', doc_xml)
            text = ' '.join(text.split())
            print(f"\nXML 方式提取成功，共 {len(text)} 字符")
            print(f"\n前 2000 字符预览:")
            print("=" * 50)
            print(text[:2000])
            print("=" * 50)
    except Exception as e2:
        print(f"XML 方式也失败：{e2}")
