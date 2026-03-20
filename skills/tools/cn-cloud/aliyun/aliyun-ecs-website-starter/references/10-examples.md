# Examples

## 10.1 快速部署WordPress

```
步骤1: 购买轻量应用服务器，选择WordPress应用镜像
步骤2: 登录宝塔面板(batpanels.com:8888/随机端口)
步骤3: 一键部署WordPress
  - 宝塔 → 网站 → 一键部署 → 填入域名
步骤4: 配置固定链接
  - WordPress后台 → 设置 → 固定链接 → 选择"文章名"
  - 宝塔 → 网站 → 设置 → 伪静态 → 选择"wordpress"
步骤5: 配置SSL
  - 宝塔 → 网站 → 设置 → SSL → Let's Encrypt申请
```

## 10.2 手动部署LNMP + WordPress

```bash
# 1. 安装宝塔
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh

# 2. 安装软件(通过宝塔面板或命令行)
# 宝塔面板 → 软件商店 → 安装:
# - Nginx
# - MySQL 5.7+
# - PHP 7.4+

# 3. 创建网站
bt website add
# 输入: 域名、FTP选择"否"、数据库选择"MySQL"、数据库名和用户

# 4. 下载WordPress
cd /www/wwwroot/yourdomain.com
wget https://cn.wordpress.org/latest-zh_CN.tar.gz
tar -xzf latest-zh_CN.tar.gz
mv wordpress/* .
rm -rf wordpress latest-zh_CN.tar.gz

# 5. 设置权限
chown -R www:www /www/wwwroot/yourdomain.com

# 6. 访问域名完成安装向导
```

## 10.3 宝塔计划任务备份

```bash
# 宝塔面板 → 计划任务 → 添加备份任务
# 备份类型: 整站备份 / 数据库备份 / 文件备份
# 备份周期: 每天 / 每周 / 每月
# 保留份数: 3-7份
# 备份位置: /www/backup 或 OSS远程备份
```

## 10.4 配置多个PHP版本

```bash
# 宝塔支持多PHP版本共存
# 宝塔 → 软件商店 → PHP → 安装多个版本

# 网站绑定PHP版本:
# 宝塔 → 网站 → 点击网站 → 设置 → PHP版本

# PHP版本切换示例:
bt
# 选择: 1) 切换PHP版本
# 选择需要的版本
```

## 10.5 宝塔防火墙配置

```bash
# 宝塔防火墙规则设置
# 宝塔 → 安全 → 防火墙

# 推荐放行端口:
# 22 (SSH) - 仅限管理IP访问
# 80 (HTTP) - 0.0.0.0/0
# 443 (HTTPS) - 0.0.0.0/0
# 8888 (宝塔面板) - 仅内网或指定IP
# 3306 (MySQL) - 仅内网

# 命令行查看防火墙状态
systemctl status firewalld
systemctl status iptables

# 云服务器安全组同样需要放行以上端口
```
