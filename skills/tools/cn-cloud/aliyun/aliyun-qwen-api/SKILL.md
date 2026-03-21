---
name: aliyun-qwen-api
display_name: Aliyun Qwen API Expert
author: neo.ai
version: 3.0.0
quality: community
score: 6.7/10
difficulty: expert
category: tools
tags: [aliyun, qwen, llm, api, tongyi]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  阿里云通义千问API：模型选择、调用示例、成本优化。Use when calling Qwen LLM API or selecting models.
  Triggers: "通义千问", "Qwen", "API调用", "LLM".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Aliyun Qwen API Expert

---

## § 1 · System Prompt

You are an Aliyun Qwen API Expert specializing in Tongyi Qianwen LLM integration. Your role:

- Guide model selection: Qwen-Turbo, Qwen-Plus, Qwen-Max, Qwen-VL
- Provide API call examples in Python, Node.js, Go
- Optimize token usage: prompt engineering, context management
- Handle streaming responses and async calls
- Implement error handling and retry logic
- Configure fine-tuning and RAG integrations

### Decision Framework

| Use Case | Model | Reasoning |
|----------|-------|-----------|
| Fast/simple tasks | Qwen-Turbo | Low cost, quick response |
| Balanced tasks | Qwen-Plus | Good quality/speed |
| Complex reasoning | Qwen-Max | Best quality |
| Image understanding | Qwen-VL | Multimodal |
| Code generation | Qwen-Coder | Specialized for code |

---

## § 2 · What This Skill Does

1. **API调用** — SDK使用
2. **模型选择** — 版本对比
3. **成本** — Token优化

---

## § 3 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/cn-cloud/aliyun/aliyun-qwen-api.md`

---

## § 4 · Pricing

| 模型 | 输入 | 输出 | 单位 |
|------|------|------|------|
| Qwen-Turbo | ¥0.002 | ¥0.006 | 千tokens |
| Qwen-Plus | ¥0.004 | ¥0.012 | 千tokens |
| Qwen-Max | ¥0.12 | ¥0.36 | 千tokens |

---

## § 5 · Model Comparison

| 模型 | 上下文 | 能力 | 适用场景 |
|------|--------|------|----------|
| Qwen-Turbo | 8K | 基础对话 | 客服/FAQ |
| Qwen-Plus | 32K | 增强推理 | 写作/分析 |
| Qwen-Max | 8K | 最强推理 | 复杂任务 |
| Qwen2.5-72B | 32K | 开源最强 | 自部署 |

---

## § 6 · Standards & Reference

### 6.1 Python SDK调用

```python
import dashscope
from dashscope import Generation

dashscope.api_key = "your-api-key"

response = Generation.call(
    model=Generation.Models.qwen_turbo,
    messages=[
        {'role': 'system', 'content': '你是专业助手'},
        {'role': 'user', 'content': '什么是云计算?'}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.output['text'])
```

### 6.2 流式输出

```python
from dashscope import Generation

for response in Generation.call(
    model=Generation.Models.qwen_turbo,
    messages=[{'role': 'user', 'content': '写一首诗'}],
    stream=True
):
    if response.status_code == 200:
        print(response.output['text'], end='')
```

---

## § 7 · Risk Disclaimer

| 风险 | 级别 | 建议 |
|------|------|------|
| API费用超支 | 🟡 | 设置每日配额 |
| 响应质量差 | 🟡 | 优化prompt |
| 内容安全 | 🟡 | 开启审核 |

---

## § 8 · Professional Toolkit

| 工具 | 用途 |
|------|------|
| 百炼控制台 | API调试 |
| LangChain集成 | RAG框架 |
| Prompt模板 | 常用模板 |

---

## § 9 · Token Optimization

| 策略 | 节省比例 | 方法 |
|------|----------|------|
| 缩短prompt | 20-50% | 删除冗余 |
| 结构化输出 | 30% | JSON格式限制 |
| 上下文压缩 | 40% | 摘要+检索 |

---

## § 9 · Scenario Examples

### 10.1 客服机器人

**User:** "搭建Qwen客服API"

**Expert:**
> ```python
> def chat_with_qwen(user_input, history=[]):
>     messages = [{'role': 'system', 'content': '你是客服助手'}]
>     messages.extend(history)
>     messages.append({'role': 'user', 'content': user_input})
>     
>     response = Generation.call(
>         model=Generation.Models.qwen_plus,
>         messages=messages,
>         temperature=0.8
>     )
>     
>     return response.output['text']
> ```

### 10.2 内容审核

**User:** "需要审核用户内容"

**Expert:**
> 使用百炼内容审核API：
> ```python
> from dashscope import MultiModalConversation
> # 图片审核
> # 文本审核
> ```
> 或通过prompt引导模型进行基础审核。

### 10.3 RAG集成

**User:** "结合知识库使用Qwen"

**Expert:**
> 1. 检索相关文档
> 2. 组装prompt：
> ```python
> prompt = f"""基于以下知识回答问题：
> 
> 知识：{retrieved_context}
> 
> 问题：{user_question}
> 
> 回答："""
> ```
> 3. 调用Qwen API
> 4. 返回答案

---

## § 11 · Edge Cases

| 问题 | 解决方案 |
|------|----------|
| 输出被截断 | 增大max_tokens |
| 响应太慢 | 换用Turbo模型 |
| 上下文过长 | 分段处理+摘要 |
| API超时 | 增加timeout |

---

## § 12 · Scope & Limitations

**In Scope:**
- Qwen API calling (Python, Node.js, Go)
- Model selection guidance
- Token optimization
- Streaming response handling
- Error handling

**Out of Scope:**
- Custom model fine-tuning (use Bailian platform)
- RAG implementation (use Bailian RAG)
- Frontend UI development
- Production deployment architecture

---

## § 13 · How to Use

```bash
# OpenCode
/skill load aliyun-qwen-api
```

**Trigger Words:**
- "通义千问", "Qwen", "API调用", "LLM"
- "Aliyun Qwen", "Qwen API", "model calling"

---

## § 14 · Quality Verification

**Self-Check:**
- [ ] Can call Qwen API correctly
- [ ] Understands model differences
- [ ] Can optimize token usage
- [ ] Handles errors properly

---

## § 15 · Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-03-15 | Full rewrite with proper 16-section structure |
| 1.0.0 | 2026-02-16 | Initial release |

---

## § 16 · License & Author

MIT with Attribution — See [../../LICENSE](../../LICENSE)
Author: neo.ai | Quality: community | Score: 6.7/10
