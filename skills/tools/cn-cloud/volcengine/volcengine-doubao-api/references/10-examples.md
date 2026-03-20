# Examples

## 10.1 Python SDK调用

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
        credentials=Credentials(
            service='ark',
            region='cn-beijing',
            secret_id='AKIDxxxxxxxx',
            secret_key='xxxxxxxx'
        )
    ),
    api_info={}
)

response = service.post(
    '/api/v3/chat/completions',
    {
        'model': 'doubao-pro-32k',
        'messages': [
            {"role": "user", "content": "你好"}
        ]
    },
    {}
)

result = response.json()
print(result['choices'][0]['message']['content'])
```

## 10.2 多轮对话

```python
messages = [
    {"role": "system", "content": "你是一个专业的Python导师"}
]

def chat(question):
    messages.append({"role": "user", "content": question})
    
    response = service.post(
        '/api/v3/chat/completions',
        {
            'model': 'doubao-pro-32k',
            'messages': messages
        },
        {}
    )
    
    result = response.json()
    answer = result['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": answer})
    return answer

print(chat("什么是装饰器?"))
print(chat("给个例子"))
```

## 10.3 OpenAI兼容调用

```python
from openai import OpenAI

client = OpenAI(
    api_key="your_access_key:your_secret_key",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

response = client.chat.completions.create(
    model="doubao-pro-32k",
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)
```

## 10.4 流式输出

```python
response = service.post(
    '/api/v3/chat/completions',
    {
        'model': 'doubao-pro-32k',
        'messages': [{"role": "user", "content": "写一首诗"}],
        'stream': True
    },
    {}
)

for line in response.iter_lines():
    if line:
        data = line.decode('utf-8').replace('data: ', '')
        if data and data != '[DONE]':
            try:
                event = json.loads(data)
                if event.get('choices'):
                    delta = event['choices'][0]['delta'].get('content', '')
                    print(delta, end='', flush=True)
            except:
                pass
```

## 10.5 Token计算

```python
def estimate_tokens(text):
    """估算中英文混合文本的Token数"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_chars = len(text) - chinese_chars
    
    # 中文约1-2字符/Token，英文约4字符/Token
    estimated = chinese_chars * 1.5 + english_chars * 0.25
    return int(estimated)

text = "这是一个测试文本 Hello World"
print(f"估算Token数: {estimate_tokens(text)}")
```
