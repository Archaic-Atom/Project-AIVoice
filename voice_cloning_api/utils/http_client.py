import requests

def post_request(url, data):
  """
  发送 POST 请求
  """
  response = requests.post(url, json=data)
  response.raise_for_status()  # 检查请求是否成功
  return response.json()