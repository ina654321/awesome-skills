# Examples

## 10.1 Python函数处理COS事件

```python
import json
from qcloud_cos import CosConfig, CosS3Client

def main_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    # 获取COS事件信息
    records = event.get('Records', [])
    for record in records:
        cos_info = record['cos']
        bucket = cos_info['cosBucket']['name']
        key = cos_info['cosObject']['key']
        
        print(f"处理文件: {bucket}/{key}")
        
        # 处理逻辑
        # ...
    
    return {"statusCode": 200, "body": "Processed"}
```

## 10.2 定时触发器

```python
def main_handler(event, context):
    import datetime
    print(f"定时任务执行: {datetime.datetime.now()}")
    
    # 执行定时任务逻辑
    # 例如: 清理过期数据、发送报表等
    
    return {"statusCode": 200}
```

```json
// 触发器配置
{
  "TriggerName": "daily-trigger",
  "Type": "Timer",
  "Config": "0 0 2 * * * *"
}
```

## 10.3 HTTP API函数

```python
def main_handler(event, context):
    # HTTP事件
    if 'httpMethod' in event:
        method = event['httpMethod']
        path = event['path']
        query = event.get('queryStringParameters', {})
        
        if path == '/api/users':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'users': []})
            }
    
    return {"statusCode": 400, "body": "Bad Request"}
```

## 10.4 层(Layer)配置

```python
# layer.py - 打包成zip上传到SCF
# 使用方式: 在函数配置中添加层

# 常用Python包打包
pip install requests pandas -t ./python/lib/python3.9/site-packages/
zip -r layer.zip python/
```

## 10.5 SCF CLI部署

```bash
# 安装SCF CLI
pip install scf

# 部署函数
scf deploy --region ap-guangzhou --function-name myFunction --code-dir ./function_code

# 触发函数
scf invoke --region ap-guangzhou --function-name myFunction --event '{"key": "value"}'

# 查看日志
scf logs --region ap-guangzhou --function-name myFunction --tail
```
