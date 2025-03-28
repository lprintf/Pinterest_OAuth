import os
import requests
from fastapi import FastAPI, HTTPException, Query
import base64

# Pinterest API 配置
CLIENT_ID = os.getenv("PINTEREST_CLIENT_ID")
CLIENT_SECRET = os.getenv("PINTEREST_CLIENT_SECRET")
REDIRECT_URI = os.getenv("PINTEREST_REDIRECT_URI")
OAUTH_URL = "https://www.pinterest.com/oauth/"
TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
headers = {
    "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
    "Content-Type": "application/x-www-form-urlencoded",
    }

app = FastAPI()

# 生成 Pinterest 授权 URL，前端点击跳转
@app.get("/login")
def login():
    auth_url = (
        f"{OAUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=boards:read,pins:read,user_accounts:read,ads:read"  # 请求的权限
    )
    return {"auth_url": auth_url}

# 处理 Pinterest 授权回调，获取 access_token
@app.get("/callback")
def callback(code: str = Query(None)):
    print(code)
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        # "client_id": CLIENT_ID,
        # "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "continuous_refresh": False
    }
    
    print(data)
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    token_data = response.json()
    # save token_data to database or session for later use
    print(token_data)
    return {"access_token": token_data.get("access_token")}

# 使用 access_token 访问 Pinterest API
@app.get("/user_info")
def get_user_info(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.pinterest.com/v5/user_account", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
