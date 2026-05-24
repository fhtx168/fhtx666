import fitz
import os
import glob

# 找到正确的文件名
desktop = r'C:\Users\Admin\Desktop'
pdf_files = glob.glob(os.path.join(desktop, '5*.pdf'))
print(f'找到 PDF 文件：{pdf_files}')

if not pdf_files:
    print('未找到 5 月 17 日笔记 PDF')
    exit()

pdf_path = pdf_files[0]
output_path = r'C:\Users\Admin\opcclawai\project\yrt_monitoring\live-2026-05-17-notes.txt'

print(f'使用文件：{pdf_path}')

try:
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f'\nPDF 共{len(doc)}页，提取{len(text)}字符')
    print('\n前 3000 字符:')
    print('=' * 50)
    print(text[:3000] if text else '无内容')
    print('=' * 50)
    
except Exception as e:
    print(f'错误：{e}')
