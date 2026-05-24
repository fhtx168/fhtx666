# API 签名说明

## 核心逻辑

使用 MD5 生成签名请求头，与前端 `getHeaders` 等价。

## 签名要素

| 字段 | 说明 |
|------|------|
| `device-platform` | 固定 `H5` |
| `timestamp` | ISO8601 格式（东八区） |
| `zm-ver` | 固定 `1.3` |
| `access-token` | UUID（自动生成） |
| `zm-token` | MD5 签名 |
| `zm-ua` | MD5(user-agent) |
| `zm-nonce` | 16位随机数字 |

## zm-token 计算

```
md5(H5 + timestamp + 1.3 + access-token + md5(user-agent))
```

## Cookie 处理

从 `~/.openclaw/workspace/config/.cookie.json` 读取：

```json
{
  "cookie": "xxx"
}
```

## 请求地址

- 基础地址：`https://www.n.cn/api/ai_agent_flow/chat`
- 上传地址：`https://nami.so.360.com/api/s3/upload`
