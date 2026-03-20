# Examples

## 10.1 生成推流/播放地址

```python
import hashlib
import time

def generate_push_url(domain, stream_name, key, expire_time):
    """生成推流地址"""
    if key:
        tail = f"{stream_name}-{expire_time}"
        md5 = hashlib.md5(tail.encode()).hexdigest()
        auth_key = f"{md5}{expire_time}"
        return f"rtmp://{domain}/live/{stream_name}?auth_key={auth_key}"
    else:
        return f"rtmp://{domain}/live/{stream_name}"

def generate_play_url(domain, stream_name, key=None, expire_time=None):
    """生成播放地址"""
    rtmp = f"rtmp://{domain}/live/{stream_name}"
    flv = f"http://{domain}/live/{stream_name}.flv"
    hls = f"http://{domain}/live/{stream_name}.m3u8"
    
    if key and expire_time:
        tail = f"{stream_name}-{expire_time}"
        md5 = hashlib.md5(tail.encode()).hexdigest()
        auth_key = f"{md5}{expire_time}"
        return {
            'rtmp': f"{rtmp}?auth_key={auth_key}",
            'flv': f"{flv}?auth_key={auth_key}",
            'hls': f"{hls}?auth_key={auth_key}"
        }
    return {'rtmp': rtmp, 'flv': flv, 'hls': hls}

# 使用示例
push_url = generate_push_url("push.yourdomain.com", "stream001", "secret_key", int(time.time()) + 7200)
play_urls = generate_play_url("pull.yourdomain.com", "stream001", "secret_key", int(time.time()) + 7200)
```

## 10.2 OBS推流配置

```
推流服务器: rtmp://push.yourdomain.com/live
推流密钥: stream001

编码设置:
- 视频编码器: x264 (或硬件编码器)
- 分辨率: 1920x1080
- 码率控制: CBR
- 视频码率: 3000 kbps
- 帧率: 20 fps
- 关键帧间隔: 2秒

音频编码器: AAC
- 采样率: 48kHz
- 音频码率: 128 kbps
```

## 10.3 Python录制管理

```python
from tencentcloud.live.v20180801 import live_client
from tencentcloud.common import credential

client = live_client.LiveClient(cred, "ap-guangzhou")

# 创建录制模板
params = {
    "TemplateName": "record_template",
    "RecordType": ["HLS", "MP4"],
    "HlsParam": {
        "RecordInterval": 3600,
        "StorageTime": 86400
    },
    "Mp4Param": {
        "RecordInterval": 3600000,
        "StorageTime": 604800
    }
}
response = client.CreateLiveRecordTemplate(params)

# 绑定录制规则到推流域名
params = {
    "DomainName": "push.yourdomain.com",
    "TemplateId": response.Response.TemplateId
}
client.BindLiveDomainWithRecordTemplate(params)
```

## 10.4 直播回调配置

```python
# 配置回调地址
params = {
    "CallbackUrl": "https://yourserver.com/live_callback",
    "EventType": [
        "0",  # 推流
        "1",  # 断流
        "100" # 录制回调
    ]
}
response = client.CreateLiveCallbackRule(params)
```

## 10.5 Web播放器集成

```html
<script src="https://qcloud.lvbu.qq.com/channel-player/player/liveplayer.js"></script>

<div id="player-container"></div>

<script>
    var player = new LivePlayer('player-container', {
        appId: 'your_app_id',
        fileId: 'your_file_id',
        streamId: 'stream001',
        liveUrl: 'rtmp://pull.yourdomain.com/live/stream001',
        autoplay: true
    });
    player.startPlay();
</script>
```
