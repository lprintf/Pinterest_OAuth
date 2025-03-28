# Pinterest OAuth 认证项目

本项目是一个基于 FastAPI 的 Pinterest OAuth 认证示例。用户可以通过此项目登录 Pinterest 并授权应用访问其 Pinterest 数据。

## 功能

- 生成 Pinterest 授权 URL
- 处理 Pinterest 授权回调并获取 access_token
- 使用 access_token 获取用户账户信息和广告账户信息
- 将获取的信息保存到本地文件

## 环境变量

请在环境变量中设置以下值：

- `PINTEREST_REDIRECT_URI`：Pinterest 授权回调的 URL
- `CLIENT_ID`：你的 Pinterest 应用的客户端 ID
- `CLIENT_SECRET`：你的 Pinterest 应用的客户端密钥

## API 端点

### GET /login

生成 Pinterest 授权 URL，前端页面可以通过访问此端点获取 URL 并进行跳转。

返回：

```json
{
    "auth_url": "https://www.pinterest.com/oauth/?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=..."
}
```

### GET /callback

处理 Pinterest 授权回调，获取 access_token。此端点应设置为 Pinterest 应用的授权回调 URL。

请求参数：

- `code`： Pinterest 授权回调时传递的授权码

返回：

```json
{
    "site_data": {
        "token_data": {
            "access_token": "YOUR_ACCESS_TOKEN",
            ...
        },
        "user_account": {
            "business_name": "YOUR_BUSINESS_NAME",
            ...
        },
        "ad_accounts": {
            "items": [
                {
                    "id": "YOUR_AD_ACCOUNT_ID",
                    ...
                },
                ...
            ]
        }
    }
}
```

## 使用方法

1. 确保已经设置了所有需要的环境变量。
2. 运行 FastAPI 应用。
3. 访问 `/login` 端点获取授权 URL 并进行跳转。
4. 授权成功后，Pinterest 会重定向到你设置的 `REDIRECT_URI`，并携带授权码。
5. 在回调端点 `/callback` 中处理授权码，获取 access_token 和用户信息。

## 注意事项

- 请确保你的 Pinterest 应用已经正确设置了 `redirect_uri`，并且与你在环境变量中设置的 `PINTEREST_REDIRECT_URI` 一致。
- 本项目仅用于演示 Pinterest OAuth 认证流程，请勿在生产环境中使用。