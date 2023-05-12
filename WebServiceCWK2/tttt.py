import requests

# 设置请求的 URL 和参数
# url = 'http://localhost:8000/paymentservice/register/'
# data = {'Name': '2d', 'Email':'sss@qq.com','Password': 'password'}
#
# # 发起 POST 请求
# response = requests.post(url, json=data)
# # 输出响应的内容和状态码
# print(response.content)
# print(response.status_code)
url = 'http://localhost:8000/paymentservice/login/'
data = {'PaymentId':'1'}

# 发起 POST 请求
session = requests.session()
response = session.post(url, json=data)
# # 输出响应的内容和状态码
print(response.content)
print(response.status_code)
# url = 'http://localhost:8000/paymentservice/order/'
# data = {'MerchantOrderId': '60', 'Price': '20'}

## 发起 POST 请求
# response = session.post(url, json=data)
# # 输出响应的内容和状态码
# print(response.content)
# print(response.status_code)
# url = 'http://localhost:8000/paymentservice/deposit/'
# data = {'Price': '20'}

# # 发起 POST 请求
# response = session.post(url, json=data)
# # 输出响应的内容和状态码
# print(response.content)
# print(response.status_code)
url = 'http://localhost:8000/paymentservice/refund/'
data = {'PaymentId': 6,'Price':5}

# 发起 POST 请求
response = session.post(url, json=data)
# 输出响应的内容和状态码
print(response.content)
print(response.status_code)