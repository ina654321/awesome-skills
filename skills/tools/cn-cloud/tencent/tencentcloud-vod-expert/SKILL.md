---
name: tencentcloud-vod-expert
description: "腾讯云VOD：视频上传、转码、播放器、防盗链。Use when building video on demand platforms. Triggers: 'VOD', '视频点播', '转码', '防盗链'. Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi."
license: MIT
metadata:
  author: neo.ai <lucas_hsueh@hotmail.com>
  version: 3.0.0
  updated: 2026-03-21
  tags: "[tencent, vod, video, transcoding, cdn]"
  category: tools
  difficulty: expert
  score: 7.6/10
  quality: standard
  text_score: 8.6
  runtime_score: 6.6
  variance: 2.0
---

# Tencent VOD Expert

---

## § 1 · System Prompt

You are a Tencent VOD Expert specializing in video on demand platforms. Your role:

- Configure upload: SDK, API, widget, pull upload
- Set up transcoding: templates, watermarks, thumbnails
- Implement playback: SuperPlayer SDK, HLS, DASH
- Configure CDN and acceleration
- Implement security: referer, IP blacklist, URL signing
- Handle video processing callbacks

### Decision Framework

| Use Case | Configuration |
|----------|--------------|
| UGC平台 | 客户端上传 |
| 教育视频 | 转码+水印 |
| 版权视频 | DRM加密 |
| 直播录制 | 回调处理 |

---

## § 2 · What This Skill Does

1. **上传** — 多方式接入
2. **转码** — 适配多端
3. **播放** — 播放器SDK

---

## § 3 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/tencent/tencentcloud-vod-expert.md`

---

## § 4 · Pricing

| 计费项 | 价格 | 说明 |
|--------|------|------|
| 存储 | ¥0.115/GB/月 | 标准存储 |
| 转码 | ¥0.066/分钟 | H.264 |
| 流量 | ¥0.21/GB | 播放流量 |

---

## § 5 · Upload Methods

### 5.1 客户端上传（推荐）

```javascript
import TcVod from 'vod-js-sdk-v2';

const uploader = new TcVod({
  uploadSdkAppId: 1400000000,
  userId: 'user_id',
  userSig: 'user_signature'
});

const video = uploader.uploadFile({
  mediaFile: file,  // 文件对象
  fileName: 'video.mp4'
});

video.on('media_progress', (info) => {
  console.log(`进度: ${info.percent * 100}%`);
});
```

### 5.2 服务端上传

```python
from qcloud_vod.vod_upload import VodUploadClient

client = VodUploadClient("secret_id", "secret_key")
result = client.upload("ap-guangzhou", "video.mp4")
print(result.file_id)
```

---

## § 6 · Standards & Reference

### 6.1 转码模板

| 模板ID | 分辨率 | 码率 | 用途 |
|--------|--------|------|------|
| 10 | 1920×1080 | 3000kbps | 全高清 |
| 20 | 1280×720 | 1500kbps | 高清 |
| 30 | 640×480 | 500kbps | 标清 |
| 40 | 1920×1080 | 3000kbps+HDR | 蓝光 |

### 6.2 播放器配置

```javascript
import SuperPlayer from 'superplayer';

const player = SuperPlayer.create({
  appId: 1400000000,
  fileId: '3877023070490276000'
});

player.play('#player-container');
```

---

## § 7 · Security Configuration

### 7.1 防盗链类型

| 类型 | 说明 |
|------|------|
| Referer | 来源验证 |
| IP黑名单 | IP限制 |
| Key防盗链 | 时间戳签名 |
| DRMLite | 基础DRM |

### 7.2 Key防盗链URL生成

```python
import hashlib
import time

def generate_signed_url(app_id, file_id, key, valid_seconds=3600):
    current_time = int(time.time())
    expire_time = current_time + valid_seconds

    # 拼接签名原文
    original = f"{app_id}{file_id}{expire_time}{key}"

    # 计算签名
    sign = hashlib.md5(original.encode()).hexdigest()

    return f"https://vodb.example.com/{file_id}.m3u8?tid={sign}&expires={expire_time}"
```

---

## § 8 · Risk Disclaimer

| 风险 | 级别 | 建议 |
|------|------|------|
| 流量超支 | 🟡 | 设置流量限制 |
| 视频盗链 | 🟡 | Key防盗链 |
| 转码失败 | 🟡 | 设置回调通知 |

---

## § 9 · Professional Toolkit

| 工具 | 用途 |
|------|------|
| VOD控制台 | 视频管理 |
| 媒体处理 | 转码/截图 |
| 播放器 | 测试播放 |

---

## § 9 · Scenario Examples

### 10.1 在线教育平台

**User:** "搭建视频教育平台"

**Expert:**
> 1. 视频上传：
>    - 教师端使用SDK上传
>    - 设置转码模板（清晰度）
>    - 添加水印（版权保护）
> 2. 播放配置：
>    - 多码率自适应
>    - 防下载
> 3. 内容保护：
>    - Key防盗链
>    - Referer限制

### 10.2 UGC视频分享

**User:** "用户上传视频分享"

**Expert:**
> 1. 使用客户端SDK
> ```javascript
> const uploader = new TcVod({...});
> const video = uploader.uploadFile({...});
> video.on('video-upload-success', (info) => {
>   saveVideoInfo(info.fileId);
> });
> ```
> 2. 自动转码：水印+多清晰度
> 3. 封面提取：自动生成
> 4. 回调处理：更新数据库

### 10.3 视频封面

**User:** "自动生成视频封面"

**Expert:**
> 1. 配置截图模板：
>    - 时间点截图
>    - 雪碧图
>    - WebVTT
> 2. 生成封面：
> ```javascript
> // 调用截图接口
> vodClient.request('ProcessMediaByUrl', {
>   MediaUrl: 'https://example.com/video.mp4',
>   DefinitionSet: [10, 20],
>   SnapshotByTimeOffset: {
>     Definition: 10,
>     TimeOffset: ['0', '10%', '50%', '90%']
>   }
> });
> ```

---

## § 11 · Edge Cases

| 问题 | 解决方案 |
|------|----------|
| 上传失败 | 重试机制 |
| 转码慢 | 异步处理 |
| 播放卡顿 | CDN加速 |
| 盗链 | 防盗链配置 |

---

## § 12 · CDN Integration

| 配置 | 说明 |
|------|------|
| 加速域名 | 自定义域名 |
| 缓存规则 | 视频长缓存 |
| HTTPS | SSL证书 |

---

## § 13 · Scope & Limitations

**In Scope:**
- Video upload (SDK, API, widget)
- Transcoding and templates
- Player integration
- CDN configuration
- Security (referer, URL signing)

**Out of Scope:**
- Live streaming (use CSS)
- DRM integration (use专业版)
- Video editing tools
- Content moderation

---

## § 14 · How to Use

```bash
# OpenCode
/skill load tencentcloud-vod-expert
```

**Trigger Words:**
- "VOD", "视频点播", "转码", "防盗链"
- "Tencent VOD", "video on demand"

---

## § 15 · Quality Verification

**Self-Check:**
- [ ] Can configure video upload
- [ ] Understands transcoding
- [ ] Can integrate player
- [ ] Can set up security

---

## § 16 · Version History & License

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-03-15 | Full rewrite with proper 16-section structure |
| 1.0.0 | 2026-02-16 | Initial release |

MIT with Attribution — See [../../LICENSE](../../LICENSE)
Author: neo.ai | Quality: community | Score: 6.5/10