# Examples

## 10.1 MySQL连接

```python
import pymysql

# Python连接RDS
connection = pymysql.connect(
    host='rm-xxxxx.mysql.rds.aliyuncs.com',
    port=3306,
    user='myuser',
    password='mypassword',
    database='mydb',
    charset='utf8mb4',
    ssl={'ca': '/path/to/ca.pem'}  # SSL连接
)

try:
    with connection.cursor() as cursor:
        # 查询
        sql = "SELECT * FROM users WHERE id = %s"
        cursor.execute(sql, (1,))
        result = cursor.fetchone()
        
        # 插入
        sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(sql, ('张三', 'zhangsan@yourdomain.com'))
        connection.commit()
finally:
    connection.close()
```

## 10.2 Django配置RDS

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'rm-xxxxx.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

## 10.3 备份与恢复

```bash
# 使用mysqldump备份
mysqldump -h rm-xxxxx.mysql.rds.aliyuncs.com \
  -u myuser -p \
  --single-transaction \
  --routines --triggers \
  mydb > backup.sql

# 恢复数据
mysql -h rm-xxxxx.mysql.rds.aliyuncs.com \
  -u myuser -p mydb < backup.sql

# 恢复指定时间点
# 控制台 → 数据库恢复 → 选择时间点
```

## 10.4 读写分离配置

```python
# 配置主从读写分离
import pymysql

# 主库写入
def write_db(sql, params):
    connection = pymysql.connect(
        host='rm-master.mysql.rds.aliyuncs.com', ...)
    # 执行写入操作
    connection.close()

# 从库读取
def read_db(sql, params):
    connection = pymysql.connect(
        host='rm-slave.mysql.rds.aliyuncs.com', ...)
    # 执行读取操作
    connection.close()

# 或使用连接池 + 自动路由
from dbutils.pooled_db import PooledDB
pool = PooledDB(creator=pymysql, maxconnections=10, host='rm-rw.mysql.rds.aliyuncs.com', ...)
```

## 10.5 性能监控

```python
# 查询RDS性能指标
from aliyunsdkrds.request.v20140815 import DescribeDBInstancePerformanceRequest

client = CommonACNClient('cn-hangzhou')

req = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
req.set_DBInstanceId('rm-xxxxx')
req.set['StartTime']('2024-01-01T00:00:00Z')
req.set['EndTime']('2024-01-01T23:59:59Z')
req.set['Category']('MySQL_Network_IO')

response = client.do_action_with_exception(req)
print(response)
```
