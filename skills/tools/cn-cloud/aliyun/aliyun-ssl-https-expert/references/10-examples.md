# Examples

## 10.1 Nginx完整SSL配置

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # 证书配置
    ssl_certificate /etc/nginx/cert/yourdomain.com.pem;
    ssl_certificate_key /etc/nginx/cert/yourdomain.com.key;
    ssl_trusted_certificate /etc/nginx/cert/ca-bundle.crt;

    # SSL安全配置
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # TLS版本(禁用老旧版本)
    ssl_protocols TLSv1.2 TLSv1.3;

    # 加密套件
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 223.5.5.5 114.114.114.114 valid=300s;
    resolver_timeout 5s;

    # 安全头
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 网站目录
    location / {
        root /var/www/html;
        index index.html index.htm;
    }
}

# HTTP跳转HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}
```

## 10.2 Apache SSL配置

```apache
<VirtualHost *:443>
    ServerName yourdomain.com
    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile /etc/httpd/cert/yourdomain.com.crt
    SSLCertificateKeyFile /etc/httpd/cert/yourdomain.com.key
    SSLCertificateChainFile /etc/httpd/cert/ca-bundle.crt

    # TLS 1.2+
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    SSLHonorCipherOrder on

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

# HTTP跳转HTTPS
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>
```

## 10.3 Let's Encrypt自动续期

```bash
# 安装certbot
yum install certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 自动续期测试
certbot renew --dry-run

# 设置cron自动续期
crontab -e
# 添加: 0 0,12 * * * certbot renew --quiet
```

## 10.4 宝塔面板配置SSL

```
1. 宝塔面板 → 网站 → 点击目标网站 → 设置 → SSL
2. 选择证书类型:
   - Let's Encrypt: 免费自动申请(推荐)
   - 其他证书: 手动上传
3. 如果Let's Encrypt申请失败:
   - 确认域名已解析到服务器IP
   - 关闭其他SSL服务(如CDN)
   - 尝试手动验证方式
4. 开启"强制HTTPS"
5. 证书续期: 宝塔自动处理
```

## 10.5 检查SSL配置安全性

```bash
# 使用SSL Labs检查
# 访问: https://www.ssllabs.com/ssltest/
# 输入域名，获取详细安全评分

# 命令行检查
openssl s_client -connect yourdomain.com:443 -brief

# 检查证书链
openssl s_client -connect yourdomain.com:443 -showcerts

# 检查支持的TLS版本
openssl s_client -tls1_2 -connect yourdomain.com:443
openssl s_client -tls1_3 -connect yourdomain.com:443
```
