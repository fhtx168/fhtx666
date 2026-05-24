"""
百度 OCR 识别体检报告
需要百度智能云 API Key 和 Secret Key
免费额度：500 次/月
"""

import requests
import base64
import json

# 百度 OCR API 配置
# 需要申请：https://console.bce.baidu.com/ai/
API_KEY = "你的 API Key"
SECRET_KEY = "你的 Secret Key"

def get_access_token():
    """获取 access token"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    response = requests.post(url)
    return response.json().get('access_token')

def ocr_medical_report(image_path):
    """识别体检报告图片"""
    # 读取图片并转 base64
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # 调用百度 OCR 通用文字识别（高精度版）
    access_token = get_access_token()
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={access_token}"
    
    payload = {
        "image": img_base64,
        "detect_direction": "true",
        "detect_language": "true",
        "paragraph": "true",
        "probability": "true"
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    result = response.json()
    
    # 提取文字
    if 'words_result' in result:
        text = '\n'.join([item['words'] for item in result['words_result']])
        return text
    else:
        print(f"OCR 识别失败：{result}")
        return None

def ocr_medical_table(image_path):
    """识别体检报告表格（专用接口）"""
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    access_token = get_access_token()
    # 使用表格文字识别接口
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/table?access_token={access_token}"
    
    payload = {
        "image": img_base64,
        "recognize_granularity": "big"
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    result = response.json()
    
    if 'words_result' in result:
        table_data = result['words_result']
        return table_data
    else:
        print(f"表格识别失败：{result}")
        return None

if __name__ == "__main__":
    # 测试
    image_path = "temp_page1.png"
    print(f"开始识别：{image_path}")
    text = ocr_medical_report(image_path)
    if text:
        print("=" * 50)
        print("识别结果:")
        print("=" * 50)
        print(text)
        # 保存到文件
        with open('ocr_result.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print("\n识别结果已保存到 ocr_result.txt")
