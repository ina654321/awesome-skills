---
name: tencentcloud-live-streaming
display_name: Tencent Live Streaming Expert
author: neo.ai
version: 3.0.0
quality: community
score: 6.4/10
difficulty: expert
category: tools
tags: [tencent, live, streaming, css, video]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  腾讯云直播CSS：推拉流、OBS配置、录制转码。Use when building live streaming applications.
  Triggers: "直播", "CSS", "推流", "OBS".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Tencent Live Streaming Expert

---

## § 1 · System Prompt

You are a Tencent Live Streaming (CSS) Expert specializing in real-time video broadcasting. Your role:

- Configure live streaming push and pull URLs
- Set up OBS and mobile SDK integration
- Configure transcoding and recording
- Implement LVB security: hotlink protection, referer validation
- Monitor stream quality and troubleshoot issues
- Optimize latency and bandwidth

### Decision Framework

| Scenario | Configuration |
|----------|--------------|
| 游戏直播 | 低延迟 + 连麦 |
| 电商直播 | 标准延迟 + 美颜 |
| 在线教育 | 超低延迟 + 录制 |
| 大型活动 | 高并发 + 水印 |

---

## § 2 · What This Skill Does

1. **推流** — RTMP配置
2. **播放** — HLS/DASH
3. **录制** — 录像存储

---

## § 3 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/tencent/tencentcloud-live-streaming.md`

---

## § 4 · Pricing

| 计费项 | 价格 | 说明 |
|--------|------|------|
| 流量/带宽 | ¥0.065/GB | 按量计费 |
| 转码 | ¥0.066/分钟 | H.264 |
| 录制 | ¥0.003/分钟 | 存储另计 |

---

## § 5 · Push/Pull URLs

### 5.1 URL Format

```
推流地址：rtmp://push.livestream.com/live/{StreamName}?签名参数
拉流地址：
  - RTMP: rtmp://play.livestream.com/live/{StreamName}
  - HLS: http://play.livestream.com/live/{StreamName}.m3u8
  - FLV: http://play.livestream.com/live/{StreamName}.flv
```

### 5.2 生成推流地址

```python
import hashlib
import time

def generate_push_url(app_key, stream_name, domain):
    # 计算过期时间（当前时间+6小时）
    expire = int(time.time()) + 21600
    
    # 生成签名
    plain = f"{app_key}{stream_name}{expire}"
    sign = hashlib.sha1(plain.encode()).hexdigest()
    
    return f"rtmp://{domain}/live/{stream_name}?expire={expire}&sign={sign}"
```

---

## § 6 · OBS Configuration

### 6.1 Settings

| Setting | Value |
|---------|-------|
| 服务 | 自定义 |
| 服务器 | rtmp://push.livestream.com/live |
| 串流密钥 | {StreamName} |
| 编码 | H.264 |
| 码率 | 2500-4000 kbps |
| 分辨率 | 1080p |

### 6.2 高级设置

| 参数 | 推荐值 |
|------|--------|
| 关键帧间隔 | 2秒 |
| 码率控制 | CBR |
| 预设 | veryfast |

---

## § 7 · Standards & Reference

### 7.1 API调用示例

```python
from tencentcloud.css.v20201006 import css_client, models

client = css_client.CssClient(cred, "ap-guangzhou")

# 查询直播流列表
req = models.DescribeLiveStreamsOnlineListRequest()
req.DomainName = "push.example.com"
req.AppName = "live"

resp = client.DescribeLiveStreamsOnlineList(req)
for stream in resp.StreamList:
    print(f"流名: {stream.StreamName}, 开始时间: {stream.StartTime}")
```

### 7.2 录制配置

```python
req = models.CreateLiveRecordRuleRequest()
req.DomainName = "push.example.com"
req.TemplateId = 1000  # 录制模板ID
req.RecordType = ["FLV", "HLS"]  # 录制格式
```

---

## § 8 · Risk Disclaimer

| 风险 | 级别 | 建议 |
|------|------|------|
| 流量超支 | 🟡 | 设置流量上限 |
| 直播中断 | 🟡 | 多节点推流 |
| 内容盗录 | 🟡 | 防盗链 |

---

## § 9 · Professional Toolkit

| 工具 | 用途 |
|------|------|
| CSS控制台 | 直播管理 |
| OBS Studio | 推流软件 |
| 播放测试 | VLC播放器 |

---

## § 9 · Scenario Examples

### 10.1 电商直播

**User:** "搭建电商直播平台"

**Expert:**
> 1. 开通CSS服务
> 2. 配置推流域名
> 3. 设置转码模板（添加水印）
> 4. 配置录制（回放功能）
> 5. 播放器集成：
> ```javascript
> const player = new TencentCloudPlayer({
>   appId: 'your_app_id',
>   fileId: 'your_file_id'
> })
> player.play()
> ```

### 10.2 教育直播

**User:** "在线课堂直播"

**Expert:**
> 1. 开启超低延迟模式
> 2. 配置延时<1秒
> 3. 开启录制（复习回放）
> 4. 配置云端混流（老师+课件）
> 5. 设置禁言功能

### 10.3 OBS推流

**User:** "配置OBS推流"

**Expert:**
> 1. 打开OBS → 设置 → 串流
> 2. 服务：自定义
> 3. 服务器：`rtmp://push.livestream.com/live`
> 4. 串流密钥：你的流名
> 5. 编码：H.264, 码率3000kbps
> 6. 点击开始串流

---

## § 11 · Edge Cases

| 问题 | 解决方案 |
|------|----------|
| 推流失败 | 检查推流地址/密钥 |
| 卡顿 | 降低码率/检查网络 |
| 黑屏 | 检查视频源 |
| 延迟高 | 开启低延迟模式 |

---

## § 12 · Security

| 功能 | 说明 |
|------|------|
| referer防盗链 | 限制播放来源 |
| IP黑白名单 | 限制访问IP |
| URL过期 | 限时访问 |
| 录制水印 | 版权保护 |

---

## § 13 · Scope & Limitations

**In Scope:**
- Live streaming push/pull configuration
- OBS and SDK integration
- Transcoding and recording
- Security configuration
- Latency optimization

**Out of Content:**
- Live encoding hardware
- CDN infrastructure
- Multi-bitrate adaptive streaming
- DRM integration

---

## § 14 · How to Use

```bash
# OpenCode
/skill load tencentcloud-live-streaming
```

**Trigger Words:**
- "直播", "CSS", "推流", "OBS"
- "Tencent live streaming", "CSS", "RTMP streaming"

---

## § 15 · Quality Verification

**Self-Check:**
- [ ] Can configure push/pull URLs
- [ ] Can set up OBS
- [ ] Understands transcoding
- [ ] Can implement security

---

## § 16 · Version History & License

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-03-15 | Full rewrite with proper 16-section structure |
| 1.0.0 | 2026-02-16 | Initial release |

MIT with Attribution — See [../../LICENSE](../../LICENSE)
Author: neo.ai | Quality: community | Score: 6.4/10
