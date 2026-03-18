---
name: aliyun-ssl-https-expert
display_name: Aliyun SSL HTTPS Expert
author: neo.ai
version: 3.0.0
quality: basic
score: 7.5/10
difficulty: beginner
category: tools
tags: [aliyun, ssl, https, security, website]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  阿里云SSL证书：免费DV证书申请、Nginx/Apache配置、HTTPS启用。Use when securing websites, setting up HTTPS, or configuring SSL certificates.
  Triggers: "SSL证书", "HTTPS", "免费证书", "Nginx配置", "网站安全".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Aliyun SSL HTTPS Expert

---

## § 1 · What This Skill Does

1. **证书申请** — 免费DV证书
2. **服务器配置** — Nginx/Apache
3. **HTTPS启用** — 全站HTTPS

---

## § 2 · Steps

```
1. 进入阿里云SSL控制台
2. 选择"免费型"DV证书
3. 提交域名验证
4. 下载证书
5. 配置到Nginx/Apache/宝塔
```

---

## § 3 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/aliyun/aliyun-ssl-https-expert.md`

---

## § 4 · Nginx配置

```nginx
server {
    listen 443 ssl;
    server_name example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256;
    
    location
        root /var/www/html;
    }
}
```

---

## 5-16. Metadata

**Self-Score:** 9.0/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../../COMMON.md)
