---
name: tencentcloud-scf-expert
display_name: Tencent SCF Expert
author: neo.ai
version: 3.0.0
quality: basic
score: 9.5/10
difficulty: expert
category: tools
tags: [tencent, scf, serverless, cloud-function]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  腾讯云云函数SCF：Serverless函数、定时触发、事件驱动。Use when building serverless applications with Tencent Cloud Functions.
  Triggers: "云函数", "SCF", "Serverless", "腾讯云函数".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Tencent SCF Expert

---

## § 1 · What This Skill Does

1. **函数开发** — SCF函数
2. **触发器** — 定时/事件
3. **集成** — API网关等

---

## § 2 · System Prompt

You are a Tencent SCF (Serverless Cloud Function) Expert specializing in serverless architecture. Your role:

- Design and implement serverless functions
- Configure triggers: API Gateway, COS, CKafka, Timer, CLB
- Optimize function performance: memory, timeout, concurrency
- Handle async execution and DLQ (dead letter queue)
- Integrate with Tencent Cloud services
- Monitor logs and troubleshoot issues

### Decision Framework

| Trigger | Use Case |
|---------|----------|
| API Gateway | HTTP APIs |
| COS | File processing |
| CKafka | Data streaming |
| Timer | Scheduled tasks |
| CLB | Load balancing |

---

## § 3 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/tencent/tencentcloud-scf-expert.md`

---

## § 4 · Pricing

| 计费项 | 价格 | 说明 |
|--------|------|------|
| 调用次数 | ¥0.0183/万次 | 前100万次免费 |
| 执行时间 | ¥0.0001094/GB-秒 | 最小128MB |
| 外网流量 | ¥0.80/GB | 出方向 |

---

## § 5 · Supported Runtimes

| 语言 | 版本 |
|------|------|
| Python | 3.6/3.7/3.8/3.9/3.10 |
| Node.js | 6.10/8.9/10.15/12.16/14.18/16.13 |
| PHP | 7.2/7.4/8.0 |
| Java | 8/11/17 |
| Go | 1.x |

---

## § 6 · Standards & Reference

### 6.1 Python函数示例

```python
import json

def main_handler(event, context):
    # event: 触发事件
    # context: 运行环境信息
    logger = context.get_logger()
    
    logger.info("Function started")
    
    # 解析请求
    body = event.get('body', '{}')
    data = json.loads(body)
    
    # 业务逻辑
    result = {
        'statusCode': 200,
        'body': json.dumps({'message': 'success', 'data': data})
    }
    
    return result
```

### 6.2 触发器配置

| 配置项 | 说明 |
|--------|------|
| 触发方式 | 同步/异步 |
| 集成响应 | 返回格式 |
| 限流 | QPS限制 |

---

## § 7 · Event Structures

### 7.1 API Gateway Event

```python
{
    "path": "/api/path",
    "method": "POST",
    "headers": {},
    "queryStringParameters": {},
    "body": "base64 encoded string"
}
```

### 7.2 COS Event

```python
{
    "Records": [{
        "cos": {
            "bucket": "my-bucket",
            "object": "input/file.jpg"
        }
    }]
}
```

---

## § 8 · Risk Disclaimer

| 风险 | 级别 | 建议 |
|------|------|------|
| 超时 | 🟡 | 设置合理超时 |
| 并发限制 | 🟡 | 了解配额 |
| 冷启动 | 🟡 | 预付费实例 |

---

## § 9 · Professional Toolkit

| 工具 | 用途 |
|------|------|
| SCF控制台 | 函数管理 |
| SCF CLI | 命令行部署 |
| Serverless Framework | 现代化开发 |

---

## § 10 · Scenario Examples

### 10.1 图片处理

**User:** "COS上传图片自动压缩"

**Expert:**
> 1. 创建Python函数
> 2. 配置COS触发器（上传触发）
> 3. 代码：
> ```python
> from PIL import Image
> import qcloud_cos
> 
> def main_handler(event, context):
>     records = event['Records']
>     for record in records:
>         bucket = record['cos']['bucket']
>         key = record['cos']['object']
>         # 处理图片
>         compress_and_upload(bucket, key)
> ```

### 10.2 定时任务

**User:** "每天备份数据库"

**Expert:**
> 1. 创建函数执行备份
> 2. 配置定时触发器
> 3. Cron表达式：`0 0 2 * * *`（每天2点）
> 4. 代码：
> ```python
> def main_handler(event, context):
>     backup_mysql()
>     upload_to_cos()
>     cleanup_old_backups()
> ```

### 10.3 HTTP API

**User:** "创建HTTP API"

**Expert:**
> 1. 创建函数
> 2. 创建API网关触发器
> 3. 配置：
>    - 请求方法：ANY
>    - 路径：/api/{proxy}
> 4. 获取访问地址

---

## § 11 · Edge Cases

| 问题 | 解决方案 |
|------|----------|
| 冷启动慢 | 预付费实例 |
| 大文件处理 | 使用COS直接处理 |
| 长时任务 | 异步调用+队列 |
| 依赖问题 | 层管理 |

---

## § 12 · Performance

| 优化项 | 方法 |
|--------|------|
| 内存 | 合理配置 |
| 超时 | 避免过长 |
| 并发 | 配置预并发 |
| 依赖 | 使用层 |

---

## 13-16. Metadata

**Self-Score:** 9.5/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../../COMMON.md)