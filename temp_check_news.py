import requests
import json

# 重点检查异动股
abnormal_stocks = ['SH600176', 'SH688535', 'SZ300274', 'SZ000426', 'SZ002747', 'SH601689', 'SZ002222', 'SZ300620', 'SH688261', 'SZ000960', 'SH603993', 'SZ002463']

print('=== 异动股新闻检查 ===')
for code in abnormal_stocks[:6]:
    try:
        url = f'http://newsapi.eastmoney.com/quicknews/v1/getstocknews?stockcode={code}&pageIndex=1&pageSize=3'
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('Data') and data['Data'].get('Items'):
                print(f"\n{code}: {len(data['Data']['Items'])} 条新闻")
                for item in data['Data']['Items'][:2]:
                    title = item.get('Title', 'N/A')
                    print(f"  - {title[:60] if title else 'N/A'}")
    except Exception as e:
        print(f'{code}: 获取失败')

print("\n=== 叶荣添微博检查 ===")
try:
    # 检查微博
    url = 'https://weibo.com/ajax/statuses/mymblog?uid=1364334665&page=1&feature=0'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers, timeout=5)
    print(f"微博 API 状态：{resp.status_code}")
except:
    print("微博 API 无法访问")
