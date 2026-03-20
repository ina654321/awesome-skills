# Examples

## 10.1 Python SDK调用通义千问

```python
import os
from dashscope import Generation

os.environ["DASHSCOPE_API_KEY"] = "sk-xxxxxxxx"

# 基础对话
response = Generation.call(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "你是一个专业的技术顾问"},
        {"role": "user", "content": "解释一下什么是RAG"}
    ],
    temperature=0.7
)

print(response.output.choices[0].message.content)
```

## 10.2 构建RAG知识库问答

```python
from dashscope import TextEmbedding, Generation
import dashscope

dashscope.base_api_key = "sk-xxxxxxxx"

# Step 1: 文档向量化
def embed_text(text):
    response = TextEmbedding.call(
        model=TextEmbedding.models.text_embedding_v3,
        input=text
    )
    return response.output['embeddings'][0]['embedding']

# Step 2: 检索相关文档(伪代码)
def search_knowledge(query, knowledge_base):
    query_vector = embed_text(query)
    # 在向量数据库中做相似度搜索
    results = vector_db.search(query_vector, top_k=3)
    return [r.content for r in results]

# Step 3: RAG问答
def rag_answer(question):
    docs = search_knowledge(question, knowledge_base)
    context = "\n".join(docs)
    
    response = Generation.call(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": f"基于以下资料回答问题，\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.output.choices[0].message.content
```

## 10.3 使用OpenAI SDK调用百炼

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxxxxxxx",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "用Python写一个快速排序"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

## 10.4 流式输出

```python
from dashscope import Generation

responses = Generation.call(
    model="qwen-plus",
    messages=[{"role": "user", "content": "讲一个关于AI的短故事"}],
    stream=True,
    incremental_output=True
)

for response in responses:
    if response.status_code == 200:
        content = response.output.choices[0].message.content
        print(content, end="", flush=True)
```

## 10.5 多模态理解

```python
from dashscope import MultiModalConversation

response = MultiModalConversation.call(
    model="qwen-vl-plus",
    messages=[{
        "role": "user",
        "content": [
            {"image": "https://yourbucket.oss-cn-beijing.aliyuncs.com/demo.jpg"},
            {"text": "描述这张图片的内容"}
        ]
    }]
)
print(response.output.choices[0].message.content)
```
