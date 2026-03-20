# Examples

## 10.1 服务端上传

```python
from vod.vod_upload import VodUploadClient

client = VodUploadClient("SecretId", "SecretKey")

# 上传本地视频
result = client.upload("ap-guangzhou", "video.mp4")
print(f"FileId: {result['FileId']}")
print(f"URL: {result['MediaUrl']}")

# 监听上传进度
class ProgressListener(VodUploadListener):
    def on_progress(self, upload_size, total_size):
        progress = int(upload_size * 100 / total_size)
        print(f"上传进度: {progress}%")

client.upload("ap-guangzhou", "video.mp4", ProgressListener())
```

## 10.2 客户端上传签名

```python
import hashlib
import json
import base64
import time

def generate_upload_signature(app_id, file_name, file_size, user_id):
    """生成客户端上传签名"""
    current = int(time.time())
    # 签名有效期7天
    expire = current + 7 * 24 * 3600
    
    # 构建签名原文
    original = {
        "appId": app_id,
        "fileName": file_name,
        "fileSize": file_size,
        "userId": user_id,
        "time": expire
    }
    
    # 简化版: 实际生产请使用HMAC-SHA256
    signature = base64.b64encode(
        json.dumps(original).encode()
    ).decode()
    
    return {
        "signature": signature,
        "expiredTime": expire
    }
```

## 10.3 Web播放器

```html
<!DOCTYPE html>
<html>
<head>
    <title>VOD播放</title>
    <script src="https://sdkplayer.vod2.myqcloud.com/player/js/tcplayer.min.js"></script>
</head>
<body>
    <video id="player-container" width="640" height="360"></video>
    
    <script>
        var player = TCPlayer('player-container', {
            appID: 'your_app_id',
            fileID: 'your_file_id',
            // 使用防盗链URL时
            sources: [{
                src: 'https://your_vod_url?sign=xxx',
                type: 'video/mp4'
            }]
        });
        
        player.play();
    </script>
</body>
</html>
```

## 10.4 触发转码任务

```python
from tencentcloud.vod.v20180717 import vod_client
from tencentcloud.vod.v20180717 import models as vod_models

client = vod_client.VodClient(cred, "ap-guangzhou")

# 提交转码任务
req = vod_models.ProcessMediaRequest()
req.FileId = "387702307230696220"
req.MediaProcessTask = {
    "TranscodeTaskSet": [
        {
            "Definition": 10  # 使用模板ID
        }
    ]
}

resp = client.ProcessMedia(req)
print(f"任务ID: {resp.TaskId}")
```

## 10.5 生成防盗链播放URL

```python
import hashlib
import time
import urllib.parse

def generate_signed_url(app_id, file_id, current_time, key):
    """生成防盗链URL"""
    # 原始播放域名
    original_url = f"https://vodb.vod2.myqcloud.com/{app_id}/{file_id}/v.f30.m3u8"
    
    # 过期时间(当前时间+1小时)
    expire = int(time.time()) + 3600
    
    # 签名: md5(key + fileId + expire)
    sign_str = f"{key}{file_id}{expire}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    
    # 拼接URL
    signed_url = f"{original_url}?t={expire}&sign={sign}"
    return signed_url
```
