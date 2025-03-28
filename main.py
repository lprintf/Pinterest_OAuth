import os
import requests
from fastapi import FastAPI, HTTPException, Query, Request
import base64
import json

# Pinterest API 配置
CLIENT_ID = os.getenv("PINTEREST_CLIENT_ID")
CLIENT_SECRET = os.getenv("PINTEREST_CLIENT_SECRET")
REDIRECT_URI = os.getenv("PINTEREST_REDIRECT_URI")
OAUTH_URL = "https://www.pinterest.com/oauth/"
TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
HEADERS = {
    "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
    "Content-Type": "application/x-www-form-urlencoded",
}
OUTPUT_DIR = "output"

app = FastAPI()


# 生成 Pinterest 授权 URL，前端点击跳转
@app.get("/login")
def login():
    auth_url = (
        f"{OAUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        # f"&scope=boards:read,pins:read,user_accounts:read,ads:read"  # 请求的权限
        f"&scope=boards:read,boards:write,pins:read,pins:write,user_accounts:read,campaigns:read,campaigns:write,ad_groups:read,ad_groups:write,ads:read,ads:write,analytics:read,product_groups:read,product_groups:write,feeds:read,feeds:write"
    )
    return {"auth_url": auth_url}


# 处理 Pinterest 授权回调，获取 access_token
@app.get("/callback")
def callback(request: Request, code: str = Query(None)):
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")
    print("Authorization code received:", code)
    print("Request headers:", request.headers.items())

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "continuous_refresh": True,
    }

    print(data)
    response = requests.post(TOKEN_URL, data=data, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    token_data = response.json()
    print("token_data:", token_data)

    headers={
        "Authorization": f"Bearer {token_data.get('access_token')}",
    }
    response = requests.get(
        "https://api.pinterest.com/v5/user_account",
        headers=headers,
    )
    user_account = response.json()
    print("user_account:", user_account)
    business_name=user_account.get("business_name")

    response = requests.get(
        "https://api.pinterest.com/v5/ad_accounts",
        headers=headers,
    )
    ad_accounts = response.json()
    print("ad_accounts:", ad_accounts)
    first_ad_account_id = ad_accounts.get("items")[0].get("id")
    site_data={
        "token_data": token_data,
        "user_account": user_account,
        "ad_accounts": ad_accounts,
    }
    # save token_data to database or session for later use
    save_path=f"{OUTPUT_DIR}/{business_name}-{first_ad_account_id}.json"
    with open(save_path, "w") as f:
        json.dump(site_data, f)
    return {"site_data": site_data}


# 使用 access_token 访问 Pinterest API
@app.get("/user_info")
def get_user_info(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://api.pinterest.com/v5/user_account", headers=headers
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
