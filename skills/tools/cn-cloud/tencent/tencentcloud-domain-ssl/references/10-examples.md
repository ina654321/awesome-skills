# Examples

## 10.1 DNSPod API配置

```python
from tencentcloud.common import credential
from tencentcloud.dnspod.v20210323 import dnspod_client

cred = credential.Credential("SecretId", "SecretKey")
client = dnspod_client.DnspodClient(cred, "")

# 添加A记录
params = {
    "Domain": "yourdomain.com",
    "RecordType": "A",
    "RecordLine": "默认",
    "Value": "1.2.3.4",
    "SubDomain": "www",
    "TTL": 600
}
response = client.CreateRecord(params)
print(f"记录ID: {response.Response.RecordId}")

# 添加MX记录
params = {
    "Domain": "yourdomain.com",
    "RecordType": "MX",
    "RecordLine": "默认",
    "Value": "10 mail.yourdomain.com",
    "SubDomain": "@",
    "TTL": 600
}
response = client.CreateRecord(params)
```

## 10.2 SSL证书申请

```python
from tencentcloud.ssl.v20191205 import ssl_client

client = ssl_client.SslClient(cred, "ap-guangzhou")

# 申请免费证书
params = {
    "Domain": "yourdomain.com",
    "Method": "DNS",
    "CertificateType": "SVR"
}
response = client.ApplyCertificate(params)
print(f"证书ID: {response.Response.CertificateId}")

# 查询证书状态
describe_params = {
    "CertificateId": "CertificateId"
}
response = client.DescribeCertificateDetail(describe_params)
print(f"状态: {response.Response.Status}")
```

## 10.3 泛解析配置

```python
# 添加泛解析(*.yourdomain.com)
params = {
    "Domain": "yourdomain.com",
    "RecordType": "A",
    "RecordLine": "默认",
    "Value": "1.2.3.4",
    "SubDomain": "*"
}
client.CreateRecord(params)
```

## 10.4 HTTPS Nginx配置

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/yourdomain.com.crt;
    ssl_certificate_key /etc/nginx/ssl/yourdomain.com.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## 10.5 DNS failover配置

```python
# DNSPod不支持原生failover，但可配合其他服务实现:
# 1. 使用CLB健康检查
# 2. 配合腾讯云API网关实现流量切换
# 3. 使用DNSPod的SEO防护功能
```
