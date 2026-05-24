"""
使用免费 OCR 服务识别体检报告
方案：
1. 腾讯 OCR（免费 1000 次/月）
2. 有道 OCR（免费）
3. 在线 OCR 工具（无需 API）
"""

import requests
import base64
import json

def ocr_tencent(image_path, app_id, app_key):
    """腾讯 OCR 通用文字识别"""
    url = "https://aip-api.market.alicloudapi.com/ali-ocr/ali_ocr"
    
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "image": img_base64
    }
    
    headers = {
        "Authorization": f"APPCODE {app_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if 'data' in result and 'text' in result['data']:
        return result['data']['text']
    else:
        print(f"腾讯 OCR 失败：{result}")
        return None

def ocr_youdao(image_path):
    """有道 OCR（免费，无需 API）"""
    url = "https://ocr.youdao.com/ocrapi/server"
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {
            'langType': 'chn',
            'detectType': '10012',
            'imageType': '1',
            'octype': 'web'
        }
        response = requests.post(url, files=files, data=data)
        result = response.json()
        
        if 'Result' in result and 'regions' in result['Result']:
            text = ''
            for region in result['Result']['regions']:
                if 'lines' in region:
                    for line in region['lines']:
                        if 'text' in line:
                            text += line['text'] + '\n'
            return text
        else:
            print(f"有道 OCR 失败：{result}")
            return None

def ocr_online(image_path):
    """使用在线 OCR 工具（无需 API Key）"""
    # 方案 1: 使用 https://www.onlineocr.net/
    # 方案 2: 使用 https://ocr.space/
    # 方案 3: 使用 https://newocr.com/
    
    print("推荐使用以下在线 OCR 工具:")
    print("1. https://www.onlineocr.net/ (免费，支持中文)")
    print("2. https://ocr.space/ (免费 25000 次/月)")
    print("3. https://newocr.com/ (完全免费)")
    print("\n操作步骤:")
    print("1. 打开网站")
    print("2. 上传图片")
    print("3. 选择语言：中文简体")
    print("4. 点击识别")
    print("5. 复制结果")
    return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("python ocr_medical.py <图片路径> [API 类型]")
        print("API 类型：baidu|tencent|youdao|online")
        print("\n示例:")
        print("python ocr_medical.py temp_page1.png baidu")
        sys.exit(1)
    
    image_path = sys.argv[1]
    api_type = sys.argv[2] if len(sys.argv) > 2 else "online"
    
    print(f"开始 OCR 识别：{image_path}")
    print(f"使用 API: {api_type}")
    
    if api_type == "baidu":
        # 需要配置百度 API
        print("请配置百度 API Key 和 Secret Key")
    elif api_type == "tencent":
        # 需要配置腾讯 API
        print("请配置腾讯 API AppID 和 AppKey")
    elif api_type == "youdao":
        text = ocr_youdao(image_path)
        if text:
            print("=" * 50)
            print("识别结果:")
            print("=" * 50)
            print(text)
            with open('ocr_result.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            print("\n识别结果已保存到 ocr_result.txt")
    else:
        ocr_online(image_path)
