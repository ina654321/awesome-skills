# Examples

## 10.1 Python对话调用

```python
from dashscope import Generation

response = Generation.call(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "你是一个专业的Python开发工程师"},
        {"role": "user", "content": "解释Python中的装饰器是什么"}
    ],
    temperature=0.7,
    max_tokens=2000
)

if response.status_code == 200:
    print(response.output.choices[0].message.content)
    print(f"Token使用: {response.usage}")
else:
    print(f"错误: {response.code}, {response.message}")
```

## 10.2 多轮对话

```python
messages = [
    {"role": "system", "content": "你是一个技术顾问"}
]

def chat(question):
    messages.append({"role": "user", "content": question})
    
    response = Generation.call(
        model="qwen-plus",
        messages=messages,
        temperature=0.7
    )
    
    answer = response.output.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    
    return answer

# 多轮对话
print(chat("Python是什么?"))
print(chat("它和Java有什么区别?"))
```

## 10.3 函数调用(Function Calling)

```python
from dashscope import Generation
import json

# 定义可用函数
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    }
]

response = Generation.call(
    model="qwen-max",
    messages=[{"role": "user", "content": "北京今天天气怎么样?"}],
    tools=functions
)

# 处理函数调用
if response.output.choices[0].finish_reason == 'tool_calls':
    tool_call = response.output.choices[0].message.tool_calls[0]
    print(f"调用函数: {tool_call.function.name}")
    print(f"参数: {tool_call.function.arguments}")
```

## 10.4 流式输出

```python
from dashscope import Generation

responses = Generation.call(
    model="qwen-plus",
    messages=[{"role": "user", "content": "写一首关于春天的诗"}],
    stream=True,
    incremental_output=True
)

full_content = ""
for resp in responses:
    if resp.status_code == 200:
        delta = resp.output.choices[0].delta.content
        print(delta, end="", flush=True)
        full_content += delta
```

## 10.5 文本嵌入

```python
from dashscope import TextEmbedding

response = TextEmbedding.call(
    model=TextEmbedding.models.text_embedding_v3,
    input="这是一个测试文本"
)

if response.status_code == 200:
    embedding = response.output['embeddings'][0]['embedding']
    print(f"向量维度: {len(embedding)}")
    print(f"向量前5个值: {embedding[:5]}")
```
