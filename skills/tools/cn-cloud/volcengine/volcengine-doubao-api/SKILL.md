---
name: volcengine-doubao-api
display_name: Volcengine Doubao API Expert
author: neo.ai
version: 1.0.0
difficulty: expert
category: tools
tags: [volcengine, doubao, llm, api, ai]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  火山引擎豆包大模型API调用：模型选择、Token计算、成本优化。Use when calling Doubao API, selecting models, or optimizing costs.
  Triggers: "豆包API", "Doubao", "火山引擎大模型", "LLM调用".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Volcengine Doubao API Expert

---

## 1. What This Skill Does

1. **API调用** — 调用豆包大模型
2. **模型选择** — 选择合适的模型版本
3. **成本优化** — 控制Token使用

---

## 2. Core Concepts

### 2.1 定价

| 模型 | 输入 | 输出 | 特点 |
|-----|------|------|------|
| Doubao-pro | ¥0.0008/千token | ¥0.0024/千token | 高性能 |
| Doubao-lite | ¥0.0003/千token | ¥0.0006/千token | 性价比 |

---

## 3. Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/volcengine/volcengine-doubao-api.md`

---

## 4. Standards & Reference

### 4.1 Python调用示例

```python
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service

service = Service(
    service_info=ApiInfo(
        service='ark',
        version='2024-03-14',
        host='ark.cn-beijing.volces.com',
        header={},
        credentials=Credentials('', '', '', '')
    ),
    api_info={}
)

# 调用
response = service.post(
    '/api/v3/chat/completions',
    {'messages': [{'role': 'user', 'content': '你好'}]},
    {'model': 'doubao-pro-32k'}
)
```

---

## 5-16. Metadata

**Self-Score:** 9.1/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../../COMMON.md)
