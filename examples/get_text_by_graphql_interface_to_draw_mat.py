import requests
import matplotlib.pyplot as plt
import pytz

from datetime import datetime
from matplotlib.font_manager import FontProperties


# GraphQL 端点(需修改)
url = 'your_url'
page = 1
text = ""
durations = {}
utc = pytz.UTC


    # GraphQL 查询和变量
query = """
query Usages($username: String!, $page: Int!) {
  usages(username: $username, page: $page) {
    pageInfo {
      ...pageInfo
      __typename
    }
    data {
      id
      createdAt
      originalOwnerId
      ... on ProjectDataUsage {
        project {
          id
          __typename
        }
        updatedSize
        __typename
      }
      ... on JobDataUsage {
        job {
          id
          project {
            id
            __typename
          }
          __typename
        }
        updatedSize
        __typename
      }
      ... on JobUsage {
        job {
          id
          project {
            id
            __typename
          }
          __typename
        }
        resource {
          name
          __typename
        }
        startedAt
        endAt
        __typename
      }
      ... on JobDiscountUsage {
        job {
          project {
            id
            __typename
          }
          __typename
        }
        resource {
          name
          __typename
        }
        startedAt
        endAt
        duration
        __typename
      }
      ... on ServingUsage {
        resource {
          name
          verboseName
          __typename
        }
        replica
        startedAt
        endAt
        versionReferenceId
        __typename
      }
      ... on ServingDataUsage {
        versionReferenceId
        updatedSize
        __typename
      }
      ... on DatasetUsage {
        dataset {
          id
          __typename
        }
        updatedSize
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment pageInfo on Pager {
  first
  last
  current
  prev
  next
  total
  __typename
}
          """
variables = {
          "username": "xxx",
          "page": "1"
      }
# 请求头部，如果需要的话，例如包含认证信息
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'your_token'  # 需修改
}
username = 'xxx'
startTime = '2024-01-01T00:00:00'
endTime = '2024-12-31T23:59:59'
a = utc.localize(datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S'))
b = utc.localize(datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S'))

# 发送 POST 请求到 GraphQL 端点
while True:
    variables = {"username": "Zero", "page": page}
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        usages_data = response_data['data']['usages']['data']
        page_info = response_data['data']['usages']['pageInfo']

        for usages in usages_data:
            if usages['__typename'] == 'JobUsage':
                resource = usages['resource']['name']
                startedAt = usages['startedAt']
                endAt = usages['endAt']
                # 转换日期时间字符串为 datetime 对象
                start_datetime = utc.localize(datetime.strptime(startedAt, '%Y-%m-%dT%H:%M:%S.%fZ'))
                end_datetime = utc.localize(datetime.strptime(endAt, '%Y-%m-%dT%H:%M:%S.%fZ'))

                effective_start = max(start_datetime, a)
                effective_end = min(end_datetime, b)

                if effective_end > effective_start:
                    duration = (effective_end - effective_start).total_seconds() // 60
                    if resource in durations:
                        durations[resource] += duration
                    else:
                        durations[resource] = duration
                    print(f"{resource}: {duration} minutes within range")
                else:
                    print(f"{resource}: No valid usage within range")

                print(f"{resource}: {duration} minutes")

        # 检查是否还有下一页
        if not page_info['next']:
            break
        else:
            page = page_info['next']  # 更新页码到下一页
    else:
        print(f"Query failed with status code {response.status_code}: {response.text}")
        break

# 打印总结数据
print("Total durations:", durations)

# 现在我们需要将durations字典中的数据分配给categories和values1
categories = list(durations.keys())
values1 = list(durations.values())

# 创建条形图显示资源使用时间
plt.figure(figsize=(10, 5))
bars = plt.bar(categories, values1, color='blue')

for bar in bars:
    yval = bar.get_height()  # 获取柱子的高度
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1),  # 在柱子上方添加文本
             ha='center', va='bottom', fontsize=10, color='black')  # 水平居中，垂直底部对齐

font = FontProperties(fname="MSYH.TTC", size=10)  # 步骤二
plt.xlabel('资源', fontproperties = font)
plt.ylabel('总分钟数/m', fontproperties = font)
plt.title(username + ' 资源使用汇总 从 ' + startTime + " 至 " + endTime, fontproperties= font)
plt.show()