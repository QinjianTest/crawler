import requests
import re
import json
from datetime import datetime, timedelta

# 目标URL
url = 'https://www.investing.com/holiday-calendar/Service/getCalendarFilteredData'

# 请求头
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.investing.com',
    'referer': 'https://www.investing.com/holiday-calendar/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

# 获取当前日期
start_date = datetime.now()

# 进行10次循环
for i in range(10):
    # 计算当前循环的日期
    current_date = start_date + timedelta(days=i)
    formatted_date = current_date.strftime('%Y-%m-%d')

    # POST请求的参数
    payload = {
        'dateFrom': formatted_date,
        'dateTo': formatted_date,
        'currentTab': 'custom',
        'limit_from': 0,
        'country': ''
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        try:
            # 解析JSON数据
            json_data = json.loads(response.text)

            # 提取"data"字段中的HTML内容
            html_content = json_data.get('data', '')

            # 使用正则表达式提取国家名称和事件名称
            countries = re.findall(r'<a href=".*?">(.*?)<\/a>', html_content)
            events = re.findall(r'<td class="last">(.*?)<\/td>', html_content)

            # 打印所有国家和事件名称
            for country, event in zip(countries, events):
                print(f"Date: {formatted_date}, Country: {country}, Event: {event}")
        except json.JSONDecodeError:
            print("Failed to parse JSON. Please check the response format.")
    else:
        print(f"Failed to retrieve the data for {formatted_date}. Status code: {response.status_code}")
