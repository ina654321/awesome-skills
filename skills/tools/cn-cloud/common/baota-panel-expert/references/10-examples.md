# Examples

## 10.1 宝塔LNMP环境安装

```bash
# 1. 安装宝塔
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh

# 2. 安装完成后，登录面板获取登录信息
# 访问: http://服务器IP:8888/随机码

# 3. 一键安装LNMP
# 宝塔面板 → 软件商店 → 运行环境
# 安装: Nginx 1.22, MySQL 5.7, PHP 7.4

# 4. 创建网站
# 宝塔面板 → 网站 → 添加站点
# 填写: 域名(可填写多个)、根目录、FTP(可选)、数据库
```

## 10.2 配置PHP

```bash
# 宝塔修改PHP配置
# 宝塔 → 软件商店 → PHP版本 → 设置 → 配置修改

# 常用配置项:
max_execution_time = 300
max_input_time = 300
memory_limit = 256M
post_max_size = 100M
upload_max_filesize = 100M

# 禁用危险函数
disable_functions = proc_exec,system,passthru,shell_exec

# 保存后重载配置
```

## 10.3 网站备份

```bash
# 宝塔计划任务配置
# 宝塔 → 计划任务 → 添加任务
# 任务类型: 备份网站 / 备份数据库
# 执行周期: 每天/每周/每月
# 保留份数: 3-7份
# 备份位置: 本地/www/backup 或远程OSS

# 命令行备份示例
bt 1  # 查看备份列表
bt 3  # 备份数据库
bt 4  # 备份网站
```

## 10.4 配置SSL证书

```
# 方式1: Let's Encrypt免费证书(推荐)
# 宝塔 → 网站 → 点击网站 → 设置 → SSL → Let's Encrypt
# 填写域名 → 申请(自动DNS验证)

# 方式2: 手动上传证书
# 宝塔 → 网站 → 点击网站 → 设置 → SSL → 其他证书
# 上传: 证书文件(PEM)、密钥文件(KEY)
```

## 10.5 Node.js应用部署

```bash
# 1. 安装Node.js
# 宝塔 → 软件商店 → 运行环境 → 安装Node.js版本管理器

# 2. 安装Node.js
bt 7  # 选择Node版本

# 3. 创建Node项目
cd /www/wwwroot
npm init -y
npm install express

# 4. 配置反向代理
# 宝塔 → 网站 → 添加反向代理
# 代理名称: myapp
# 目标URL: http://127.0.0.1:3000
# 发送域名: $host
```
