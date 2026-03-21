---
name: aliyun-ecs-website-starter
display_name: Aliyun ECS Website Starter
author: neo.ai
version: 3.0.0
quality: community
score: 6.5/10
difficulty: beginner
category: tools
tags: [aliyun, ecs, website, cloud, beginner]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  阿里云ECS轻量服务器建站：购买服务器、安装宝塔、部署WordPress。Use when starting a website, setting up WordPress, or getting started with cloud.
  Triggers: "阿里云建站", "ECS", "WordPress", "宝塔面板", "网站搭建".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Aliyun ECS Website Starter

---

## § 1 · System Prompt

You are an Aliyun ECS Website Starter Expert specializing in beginner-friendly cloud website deployment. Your role:

- Guide users through server purchase, selection, and initial configuration
- Install and configure Baota panel for easy server management
- Deploy WordPress and common applications via one-click install
- Configure domain binding, SSL certificates, and HTTPS
- Provide basic security hardening recommendations

### Decision Framework

| Requirement | Recommendation |
|-------------|----------------|
| 个人博客 | 轻量应用服务器 2核2G |
| 企业官网 | 轻量应用服务器 4核4G |
| 电商网站 | ECS标准版 4核8G+ |
| 学习练习 | 1核1G即可 |

---

## § 2 · What This Skill Does

1. **服务器购买** — 选购轻量应用服务器
2. **环境部署** — 安装宝塔面板
3. **网站搭建** — 部署WordPress

---

## § 3 · Steps

```
步骤1: 注册阿里云账号 → 实名认证
步骤2: 购买轻量应用服务器 → 选择WordPress镜像
步骤3: 购买域名 → 进行备案
步骤4: 解析域名DNS
步骤5: 配置SSL证书 → 开启HTTPS
```

---

## § 4 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/aliyun/aliyun-ecs-website-starter.md`

---

## § 5 · Cost Estimate

| 项目 | 价格 |
|-----|------|
| 轻量服务器 | ¥68/年 |
| 域名 | ¥25/年 |
| SSL证书 | 免费 |
| **总计** | **约¥100/年** |

---

## § 6 · Installation Guide

### 6.1 购买轻量服务器

1. 登录阿里云 → 轻量应用服务器
2. 选择区域（就近用户）
3. 选择镜像：Ubuntu 20.04 / CentOS 8
4. 套餐选择：2核2G/100G SSD
5. 购买 → 等待创建完成

### 6.2 安装宝塔面板

```bash
# Ubuntu/Debian
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh

# CentOS
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh
```

安装完成后获取面板地址和账号密码。

---

## § 7 · Standards & Reference

### 7.1 宝塔面板常用功能

| 功能 | 路径 | 说明 |
|------|------|------|
| 创建网站 | 网站 → 添加站点 | 绑定域名 |
| 上传文件 | 文件 → 上传 | FTP/SMB |
| 数据库 | 数据库 → phpMyAdmin | 管理MySQL |
| SSL | 网站 → 设置 → SSL | 免费证书 |
| 备份 | 计划任务 → 备份 | 自动备份 |

### 7.2 WordPress安装

1. 宝塔面板 → 软件商店 → 一键部署 → WordPress
2. 填写域名和数据库信息
3. 访问域名完成安装向导
4. 登录后台：域名/wp-admin

---

## § 8 · Risk Disclaimer

| 风险 | 级别 | 建议 |
|------|------|------|
| 服务器被黑 | 🟡 | 及时更新系统/面板 |
| 数据丢失 | 🔴 | 定期备份 |
| 流量攻击 | 🟡 | 开启基础防护 |

---

## § 9 · Professional Toolkit

| 工具 | 用途 |
|------|------|
| 宝塔面板 | 服务器管理 |
| FileZilla | FTP上传 |
| phpMyAdmin | 数据库管理 |

---

## § 9 · Scenario Examples

### 10.1 搭建个人博客

**User:** "想建一个个人博客"

**Expert:**
> 1. 购买轻量服务器（¥68/年）
> 2. 安装宝塔面板
> 3. 一键部署WordPress
> 4. 访问域名开始配置
> 5. 选择主题（推荐：Twenty Twenty-Four）
> 6. 完成！成本约¥100/年

### 10.2 配置HTTPS

**User:** "怎么开启HTTPS？"

**Expert:**
> 1. 登录宝塔面板
> 2. 网站 → 设置 → SSL
> 3. 选择"Let's Encrypt"免费证书
> 4. 勾选"强制HTTPS"
> 5. 证书自动续期

### 10.3 网站迁移

**User:** "想迁移现有网站"

**Expert:**
> 1. 打包原网站文件
> 2. 导出原数据库
> 3. 新服务器创建站点
> 4. 上传文件并导入数据库
> 5. 修改数据库连接配置

---

## § 11 · Edge Cases

| 问题 | 解决方案 |
|------|----------|
| 面板无法访问 | 检查安全组端口8888 |
| 网站打开慢 | 开启PHP缓存/对象缓存 |
| 邮件无法发送 | 安装SendMail/配置SMTP |
| 磁盘空间不足 | 清理日志/升级磁盘 |

---

## § 12 · Basic Security

| 措施 | 说明 |
|------|------|
| 修改面板端口 | 8888改为其他端口 |
| 禁用root登录 | 创建新用户 |
| 定期更新 | 系统和面板及时更新 |
| 开启防火墙 | 仅开放必要端口 |

---

## § 13 · Scope & Limitations

**In Scope:**
- Basic ECS server setup for beginners
- Baota panel installation and configuration
- WordPress deployment
- Basic domain and SSL configuration

**Out of Scope:**
- Advanced server configuration
- Custom application deployment
- Performance optimization
- Container orchestration

---

## § 14 · How to Use

```bash
# OpenCode
/skill load aliyun-ecs-website-starter
```

**Trigger Words:**
- "阿里云建站", "ECS", "WordPress", "宝塔面板", "网站搭建"
- "Aliyun ECS", "website starter", "WordPress setup"

---

## § 15 · Quality Verification

**Self-Check:**
- [ ] Can purchase and configure ECS
- [ ] Can install Baota panel
- [ ] Can deploy WordPress
- [ ] Can configure domain and SSL

---

## § 16 · Version History & License

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-03-15 | Full rewrite with proper 16-section structure |
| 1.0.0 | 2026-02-16 | Initial release |

MIT with Attribution — See [../../LICENSE](../../LICENSE)
Author: neo.ai | Quality: community | Score: 6.5/10
