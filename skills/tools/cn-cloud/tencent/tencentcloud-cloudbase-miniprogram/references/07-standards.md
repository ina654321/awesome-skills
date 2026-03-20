# Standards & Reference

## 7.1 Official Documentation

- [云开发CloudBase](https://cloud.tencent.com/product/tcb)
- [CloudBase开发文档](https://docs.cloud.tencent.com/document/product/876)
- [微信小程序云开发](https://developers.weixin.qq.com/miniprogram/dev/wxcloud/basis/getting-started.html)
- [CloudBase CLI](https://docs.cloud.tencent.com/tcb/cli/)

## 7.2 服务架构

### 7.2.1 核心服务

| 服务 | 说明 | 用途 |
|------|------|------|
| 云数据库 | JSON NoSQL数据库 | 数据存储 |
| 云存储 | 文件存储(图片/音视频) | 文件管理 |
| 云函数 | Serverless函数 | 服务端逻辑 |
| 静态网站托管 | 前端页面托管 | 静态站点 |
| 身份认证 | 微信/短信认证 | 用户登录 |

### 7.2.2 计费套餐

| 套餐 | 价格 | 资源限制 |
|------|------|---------|
| 开发版 | 免费 | 100并发，500云函数调用/天 |
| 个人版 | ¥9.9/月 | 1000并发，10万函数调用/天 |
| 基础版1 | ¥49/月 | 3000并发，50万函数调用/天 |
| 企业版 | ¥99/月起 | 按量付费 |

## 7.3 环境配置

### 7.3.1 环境ID

```
环境ID格式: cloud1-xxxxxx
环境名称: 可自定义
地域: ap-shanghai / ap-beijing / ap-guangzhou
```

### 7.3.2 数据库集合

```javascript
// 数据库集合示例: users
{
    "_id": "xxxxx",
    "name": "张三",
    "email": "zhangsan@yourdomain.com",
    "age": 28,
    "createTime": "2024-01-01"
}
```

## 7.4 SDK使用

### 7.4.1 小程序端初始化

```javascript
// app.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

// 使用云数据库
const db = cloud.database()

// 查询
db.collection('users').where({ name: '张三' }).get()

// 插入
db.collection('users').add({
    data: {
        name: '李四',
        age: 25
    }
})
```

### 7.4.2 云函数示例

```javascript
// 云函数入口: index.js
const cloud = require('wx-server-sdk')
cloud.init()

exports.main = async (event, context) => {
    const db = cloud.database()
    
    switch (event.action) {
        case 'getUser':
            const user = await db.collection('users')
                .doc(event.userId)
                .get()
            return { success: true, data: user.data }
        default:
            return { success: false, error: 'unknown action' }
    }
}
```

## 7.5 安全规则

| 规则类型 | 配置位置 | 说明 |
|---------|---------|------|
| 数据库权限 | 控制台/安全规则 | 基于用户身份的读写控制 |
| 存储权限 | 控制台/权限设置 | 文件访问控制 |
| 云函数调用 | 环境设置 | 允许的调用来源 |
