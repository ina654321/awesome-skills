# Examples

## 10.1 Python SDK常用操作

```python
import oss2
import os

auth = oss2.Auth('<AccessKeyId>', '<AccessKeySecret>')
bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'my-bucket')

# 上传文件
bucket.put_object_from_file('images/photo.jpg', '/local/photo.jpg')

# 下载文件
bucket.get_object_to_file('images/photo.jpg', '/local/download.jpg')

# 列出文件
for obj in oss2.ObjectIterator(bucket, prefix='images/'):
    print(f'文件: {obj.key}, 大小: {obj.size}')

# 删除文件
bucket.delete_object('images/old.jpg')

# 判断文件是否存在
exist = bucket.object_exists('images/photo.jpg')
print(f'文件存在: {exist}')
```

## 10.2 生成签名URL

```python
# 生成私有读文件的访问URL
url = bucket.sign_url('GET', 'private/doc.pdf', 3600)
print(f'访问链接(有效期1小时): {url}')

# 生成上传签名URL(让客户端直接上传到OSS)
policy = bucket.sign_url('PUT', 'uploads/file.jpg', 3600)
print(f'上传链接: {policy}')
```

## 10.3 图片处理

```python
# OSS图片处理服务
# 缩略图
style = 'image/resize,p_50'
url = bucket.sign_url('GET', 'images/photo.jpg', 3600, params={'x-oss-process': style})

# 水印
style = 'image/watermark,text_SGVsbG8gV29ybGQ'
url = bucket.sign_url('GET', 'images/photo.jpg', 3600, params={'x-oss-process': style})

# 格式转换
style = 'image/format,webp,quality,85'
url = bucket.sign_url('GET', 'images/photo.jpg', 3600, params={'x-oss-process': style})
```

## 10.4 跨域配置

```python
from oss2.models import BucketCors, CorsRule

# 配置CORS，允许前端网页直接访问OSS
cors_rule = CorsRule(
    allowed_origins=['https://yourdomain.com'],
    allowed_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allowed_headers=['*'],
    expose_headers=['ETag'],
    max_age_seconds=3600
)

bucket.put_bucket_cors(BucketCors([cors_rule]))
```

## 10.5 分片上传大文件

```python
import os
from oss2 import determine_part_size

file_path = '/large/video.mp4'
file_size = os.path.getsize(file_path)

# 初始化分片上传
upload_id = bucket.init_multipart_upload('videos/movie.mp4').upload_id
key = 'videos/movie.mp4'

# 计算每个分片大小
part_size = determine_part_size(file_size, preferred_size=1024 * 1024)

# 上传分片
parts = []
with open(file_path, 'rb') as f:
    part_number = 1
    offset = 0
    while offset < file_size:
        chunk_size = min(part_size, file_size - offset)
        result = bucket.upload_part(key, upload_id, part_number, f.read(chunk_size))
        parts.append(oss2.models.PartInfo(part_number, result.etag))
        offset += chunk_size
        part_number += 1

# 完成分片上传
bucket.complete_multipart_upload(key, upload_id, parts)
```
