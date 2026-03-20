# Examples

## 10.1 Python函数处理OSS上传

```python
import oss2

def handler(event, context):
    # event是OSS事件
    evt = json.loads(event)
    
    bucket_name = evt['events'][0]['oss']['bucket']['name']
    object_key = evt['events'][0]['oss']['object']['key']
    
    # 获取临时凭证
    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    
    # 处理文件(如生成缩略图)
    bucket = oss2.Bucket(auth, 'oss-cn-hangzhou-internal.aliyuncs.com', bucket_name)
    
    # 下载原图
    bucket.get_object(object_key, '/tmp/original.jpg')
    
    # ... 图片处理逻辑 ...
    
    return {'statusCode': 200, 'body': 'Processed'}
```

## 10.2 定时任务

```python
import base64
import json

def handler(event, context):
    # 每天凌晨清理过期日志
    from datetime import datetime, timedelta
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    
    # 清理OSS中的日志
    # ... 清理逻辑 ...
    
    print(f"清理完成: {yesterday}")
    return {'statusCode': 200}
```

```json
// 定时触发器配置
{
  "triggerName": "daily-cleanup",
  "triggerType": "timer",
  "triggerConfig": {
    "cronExpression": "0 0 2 * * *",
    "enable": true
  }
}
```

## 10.3 HTTP API服务

```python
import json

def handler(event, context):
    # 处理HTTP请求
    if 'requestContext' in event:
        method = event['httpMethod']
        path = event['path']
        query = event.get('queryStringParameters', {})
        
        if path == '/api/users' and method == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'users': []})
            }
        
        return {'statusCode': 404, 'body': 'Not Found'}
    
    return {'statusCode': 400, 'body': 'Bad Request'}
```

## 10.4 层(Layer)配置

```yaml
# serverless.yaml
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'

Services:
  MyService:
    Functions:
      MyFunction:
        Handler: index.handler
        Runtime: python3.9
        Layers:
          - acs:log:cn-hangzhou:*
            /layer:log-python-1.0
```

## 10.5 异步调用

```python
def handler(event, context):
    # 返回异步调用响应
    return {
        'statusCode': 202,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'requestId': context.request_id,
            'message': 'Request accepted'
        })
    }
```
