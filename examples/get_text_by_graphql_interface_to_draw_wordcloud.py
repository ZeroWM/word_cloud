#!/usr/bin/env python
"""
Minimal Example
===============

Generating a wordcloud from project names using default arguments.
"""

import requests
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from os import path
from wordcloud import WordCloud

# GraphQL 端点(需修改)
url = 'http://your_http_here'
page = 1
text = ""

    # GraphQL 查询和变量
query = """
query yourMethod {
  yourMethod(include: UNRESERVED, type: LIST) {
    __typename
    id
    name
    reserved
  }
}
          """

# 请求头部，如果需要的话，例如包含认证信息
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_token_here'  # 需修改
}

# 发送 POST 请求到 GraphQL 端点
response = requests.post(url, json={'query': query}, headers=headers)

# 检查响应状态码并解析数据
if response.status_code == 200:
    # 获取JSON响应体
    response_data = response.json()

    # 遍历数据，这里假设 'data' 字段存在于响应中
    for tag in response_data['data']['tags']:
        tag_name = tag['name']
        text += tag_name + ' '
else:
    print(f"Query failed with status code {response.status_code}: {response.text}")

# 在收集完所有数据后生成和显示词云

print(text)

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
mask = np.array(Image.open(path.join(d, "stormtrooper_mask.png")))
wordcloud = WordCloud(font_path='MSYH.TTC', mask=mask, width=800, height=800,background_color="white").generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
