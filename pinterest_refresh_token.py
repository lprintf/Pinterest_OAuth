import requests
import base64
import os

# Pinterest API 配置
CLIENT_ID = os.getenv("PINTEREST_CLIENT_ID")
CLIENT_SECRET = os.getenv("PINTEREST_CLIENT_SECRET")
OAUTH_URL = "https://www.pinterest.com/oauth/"
TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
HEADERS = {
    "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
    "Content-Type": "application/x-www-form-urlencoded",
}
OUTPUT_DIR = "output"
def refresh_pinterest_token(client_id, client_secret, refresh_token):
    # 生成 base64 编码的字符串
    credentials = f"{client_id}:{client_secret}"
    base64_encoded = base64.b64encode(credentials.encode()).decode()

    # 定义请求的 URL 和数据
    url = "https://api.pinterest.com/v5/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "boards:read"
    }

    # 定义请求的头部
    headers = {
        "Authorization": f"Basic {base64_encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=data)
        # 检查响应状态码
        response.raise_for_status()
        print("请求成功")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except Exception as err:
        print(f"其他错误发生: {err}")
    return None

if __name__ == "__main__":
    pass