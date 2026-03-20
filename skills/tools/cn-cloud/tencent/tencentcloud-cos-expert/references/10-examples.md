# Examples

## 10.1 Python SDK基础操作

```python
from qcloud_cos import CosConfig, CosS3Client

config = CosConfig(
    SecretId='AKIDxxxxxxxx',
    SecretKey='xxxxxxxx',
    Region='ap-beijing',
    Token=None
)
client = CosS3Client(config)
bucket = 'mybucket-1234567890'

# 上传文件
with open('local.jpg', 'rb') as f:
    client.put_object(Bucket=bucket, Body=f, Key='images/photo.jpg')

# 下载文件
response = client.get_object(Bucket=bucket, Key='images/photo.jpg')
response['Body'].get_stream_to_file('download.jpg')

# 列出文件
response = client.list_objects(Bucket=bucket, Prefix='images/')
for obj in response['Contents']:
    print(f"文件: {obj['Key']}, 大小: {obj['Size']}")

# 删除文件
client.delete_object(Bucket=bucket, Key='images/old.jpg')
```

## 10.2 生成预签名URL

```python
# 生成下载URL
download_url = client.generate_pre_signed_url(
    Bucket=bucket,
    Key='images/private.pdf',
    Expired=3600  # 1小时
)
print(f"下载链接: {download_url}")

# 生成上传URL(允许客户端直接上传)
upload_url = client.generate_pre_signed_url(
    Bucket=bucket,
    Key='uploads/new.jpg',
    Expired=7200,
    HttpMethod='PUT'
)
```

## 10.3 静态网站托管

```python
# 开启静态网站托管
client.put_bucket_website(
    Bucket=bucket,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'index.html'},
        'ErrorDocument': {'Key': 'error.html'},
        'RoutingRules': [
            {
                'RuleFilter': {},
                'Condition': {'KeyPrefixEquals': 'docs/'},
                'Redirect': {'ReplaceKeyWith': 'docs/index.html'}
            }
        ]
    }
)

# 设置公有读访问
client.put_bucket_acl(
    Bucket=bucket,
    ACL='public-read'
)
```

## 10.4 生命周期规则

```python
# 配置生命周期: 30天后转低频，180天后归档
client.put_bucket_lifecycle(
    Bucket=bucket,
    LifecycleConfiguration={
        'Rule': [
            {
                'ID': 'transition-rule',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'logs/'},
                'Transition': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 180, 'StorageClass': 'ARCHIVE'}
                ]
            },
            {
                'ID': 'delete-rule',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'temp/'},
                'Expiration': {'Days': 365}
            }
        ]
    }
)
```

## 10.5 CDN加速配置

```python
# 配置COS作为CDN源站
# 在CDN控制台添加COS域名作为源站
# 源站地址: mybucket-1234567890.cos.ap-beijing.myqcloud.com

# 或使用COS的CDN加速域名
response = client.get_bucket_domain_conf(Bucket=bucket)
print(response)
```
