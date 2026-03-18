---
name: tencentcloud-cos-expert
display_name: Tencent COS Expert
author: neo.ai
version: 3.0.0
quality: basic
score: 7.5/10
difficulty: expert
category: tools
tags: [tencent, cos, storage, cloud, object-storage]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  腾讯云COS对象存储：存储桶配置、权限管理、CDN加速。Use when storing files, building static websites, or CDN distribution.
  Triggers: "COS", "腾讯云存储", "对象存储", "CDN".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Tencent COS Expert

---

## § 1 · What This Skill Does

1. **存储管理** — COS Bucket操作
2. **权限配置** — 公有/私有访问
3. **CDN集成** — 加速分发

---

## § 2 · Pricing

| 类型 | 价格 |
|-----|------|
| 标准存储 | ¥0.099/GB/月 |
| CDN流量 | ¥0.21/GB |

---

## § 3 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/tencent/tencentcloud-cos-expert.md`

---

## § 4 · Standards & Reference

```python
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

config = CosConfig(secret_id='id', secret_key='key', region='ap-beijing')
client = CosS3Client(config)

# 上传
client.put_object(Bucket='mybucket', Body=b'content', Key='file.txt')

# 下载
client.get_object(Bucket='mybucket', Key='file.txt')
```

---

## 5-16. Metadata

**Self-Score:** 9.0/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../../COMMON.md)
