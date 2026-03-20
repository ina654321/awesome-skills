# Examples

## 10.1 Python SDK调用

```python
from tencentcloud.common import credential
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

cred = credential.Credential("SecretId", "SecretKey")
client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou")

req = models.ChatCompletionsRequest()
req.Model = "hunyuan-standard"
req.Messages = [
    {"Role": "user", "Content": "你好"}
]

resp = client.ChatCompletions(req)
print(resp.Choices[0].Message.Content)
```

## 10.2 多轮对话

```python
messages = [
    {"Role": "system", "Content": "你是专业的Python导师"}
]

def chat(question):
    messages.append({"Role": "user", "Content": question})
    
    req = models.ChatCompletionsRequest()
    req.Model = "hunyuan-standard"
    req.Messages = messages
    
    resp = client.ChatCompletions(req)
    answer = resp.Choices[0].Message.Content
    messages.append({"Role": "assistant", "Content": answer})
    return answer

print(chat("什么是装饰器?"))
print(chat("给个例子"))
```

## 10.3 流式输出

```python
req = models.ChatCompletionsRequest()
req.Model = "hunyuan-standard"
req.Messages = [{"Role": "user", "Content": "写一首诗"}]
req.Stream = True

resp = client.ChatCompletions(req)

for event in resp:
    if hasattr(event, 'Choices'):
        delta = event.Choices[0].Delta.Content
        print(delta, end="", flush=True)
```

## 10.4 OpenAI兼容调用

```python
import openai

openai.api_key = "SecretId:SecretKey"
openai.base_url = "https://hunyuan.cloud.tencent.com/"

response = openai.ChatCompletion.create(
    model="hunyuan-standard",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

## 10.5 多模态理解

```python
req = models.ChatCompletionsRequest()
req.Model = "hunyuan-vision"
req.Messages = [
    {
        "Role": "user",
        "Content": [
            {"type": "text", "text": "描述这张图片"},
            {"type": "image_url", "image_url": {"url": "https://yourbucket-1234567890.cos.ap-guangzhou.myqcloud.com/demo.jpg"}}
        ]
    }
]

resp = client.ChatCompletions(req)
print(resp.Choices[0].Message.Content)
```
