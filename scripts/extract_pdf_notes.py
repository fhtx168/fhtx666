import fitz

pdf_path = r'C:\Users\Admin\Desktop\5 月 17 日_笔记.pdf'
output_path = r'C:\Users\Admin\opcclawai\project\yrt_monitoring\live-2026-05-17-notes.txt'

doc = fitz.open(pdf_path)
text = ''
for page in doc:
    text += page.get_text()

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'PDF 共{len(doc)}页，提取{len(text)}字符')
print('\n前 2000 字符:')
print('=' * 50)
print(text[:2000] if text else '无内容')
print('=' * 50)
