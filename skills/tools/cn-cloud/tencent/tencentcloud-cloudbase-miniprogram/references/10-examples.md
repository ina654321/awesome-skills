# Examples

## 10.1 小程序云数据库操作

```javascript
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

// 查询数据
async function getUser(userId) {
    return await db.collection('users')
        .where({ _id: userId })
        .get()
}

// 添加数据
async function addUser(userData) {
    return await db.collection('users')
        .add({ data: userData })
}

// 更新数据
async function updateUser(userId, updateData) {
    return await db.collection('users')
        .doc(userId)
        .update({ data: updateData })
}

// 删除数据
async function deleteUser(userId) {
    return await db.collection('users')
        .doc(userId)
        .remove()
}

// 聚合查询
async function getUserStats() {
    return await db.collection('orders')
        .aggregate()
        .match({ status: 'completed' })
        .group({ _id: '$userId', total: $.sum('$amount') })
        .end()
}
```

## 10.2 云函数示例

```javascript
// 云函数入口
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()

exports.main = async (event, context) => {
    const { action, data } = event
    
    switch (action) {
        case 'login':
            // 获取用户信息
            const user = await db.collection('users')
                .where({ openid: cloud.getWXContext().OPENID })
                .get()
            
            if (user.data.length === 0) {
                // 创建新用户
                await db.collection('users').add({
                    data: {
                        openid: cloud.getWXContext().OPENID,
                        createTime: new Date()
                    }
                })
            }
            return { success: true, openid: cloud.getWXContext().OPENID }
            
        case 'query':
            // 查询数据
            return await db.collection('products').get()
            
        default:
            return { error: 'unknown action' }
    }
}
```

## 10.3 云存储上传下载

```javascript
// 小程序端上传文件
wx.cloud.uploadFile({
    cloudPath: 'avatars/' + openid + '.jpg',
    filePath: tempFilePath,
    success: res => {
        console.log('上传成功', res.fileID)
    }
})

// 下载文件
wx.cloud.downloadFile({
    fileID: 'cloud://xxx/xxx.jpg',
    success: res => {
        console.log('临时路径', res.tempFilePath)
    }
})
```

## 10.4 数据库实时监听

```javascript
// 监听数据变化
const watcher = db.collection('messages')
    .where({ roomId: 'room123' })
    .orderBy('createTime', 'asc')
    .watch({
        onChange: snapshot => {
            console.log('数据变化', snapshot.docs)
        },
        onError: err => {
            console.error('监听错误', err)
        }
    })

// 停止监听
watcher.close()
```

## 10.5 云开发CLI部署

```bash
# 安装CLI
npm install -g @cloudbase/cli

# 登录
tcb login

# 部署云函数
tcb fn deploy myFunction --dir ./functions/myFunction

# 查看函数日志
tcb fn log myFunction

# 触发函数
tcb fn invoke myFunction --params '{"action":"test"}'
```
