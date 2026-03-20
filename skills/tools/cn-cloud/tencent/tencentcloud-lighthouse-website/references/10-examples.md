# Examples

## 10.1 快速部署WordPress

```
步骤1: 购买轻量应用服务器，选择WordPress应用镜像
步骤2: 访问管理后台: http://服务器IP/admin
步骤3: 配置域名解析到服务器IP
步骤4: 申请SSL证书(控制台 → 域名 → 免费证书)
步骤5: 配置固定链接: WordPress后台 → 设置 → 固定链接 → 文章名
```

## 10.2 应用镜像安装宝塔

```bash
# SSH登录服务器
ssh root@服务器IP

# 安装宝塔
yum install -y wget && wget -O install.sh https://download.bt.cn/install/install_6.0.sh && sh install.sh

# 访问宝塔面板
# http://服务器IP:8888/随机码
```

## 10.3 防火墙配置

```bash
# 腾讯云控制台 → 轻量应用服务器 → 防火墙

# 放行常用端口:
# 22  - SSH
# 80  - HTTP
# 443 - HTTPS
# 8888 - 宝塔面板
```

## 10.4 Node.js应用部署

```bash
# 1. 安装Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# 2. 创建项目
mkdir /www/wwwroot/myapp
cd /www/wwwroot/myapp
npm init -y
npm install express

# 3. 配置反向代理
# 宝塔 → 网站 → 添加反向代理
# 代理名称: myapp
# 目标URL: http://127.0.0.1:3000

# 4. 使用PM2运行
npm install -g pm2
pm2 start app.js --name myapp
pm2 save
pm2 startup
```

## 10.5 配置HTTPS

```
1. 腾讯云控制台 → SSL证书 → 申请免费证书
2. 下载Nginx格式证书
3. 宝塔 → 网站 → 设置 → SSL → 上传证书
4. 开启"强制HTTPS"
```
