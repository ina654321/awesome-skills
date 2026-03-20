# Examples

## 10.1 创建客服机器人

```
步骤1: 访问 coze.cn → 登录/注册
步骤2: 点击"创建Bot" → 填写名称和描述
步骤3: 配置Bot提示词:
  "你是[公司名]的智能客服，你的职责是...
   - 只回答与[产品/服务]相关的问题
   - 如果无法回答，请转人工服务"
步骤4: 添加知识库:
  - 上传产品文档、FAQ等
  - 配置召回参数
步骤5: 配置开场白:
  "您好！我是[公司名]智能客服，请问有什么可以帮您？"
步骤6: 发布到目标平台
```

## 10.2 Python API调用

```python
import requests

url = "https://api.coze.com/v1/chat"

headers = {
    "Authorization": "Bearer pat-xxxxx",
    "Content-Type": "application/json"
}

payload = {
    "bot_id": "7xxxxx",
    "user_id": "user_123",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [],
    "messages": [
        {
            "role": "user",
            "content": "你们的产品价格是多少？"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()
print(result)

# 解析响应
if result['code'] == 0:
    chat_id = result['data']['chat_id']
    conversation_id = result['data']['conversation_id']
    print(f"对话ID: {chat_id}")
```

## 10.3 流式输出

```python
import requests
import json

payload["stream"] = True

response = requests.post(url, json=payload, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        data = line.decode('utf-8').replace('data:', '')
        if data:
            try:
                event = json.loads(data)
                if event.get('event') == 'message':
                    content = event['data']['content']
                    print(content, end='', flush=True)
            except:
                pass
```

## 10.4 工作流创建

```
工作流节点示例 - 新闻摘要生成:

节点1: 大模型(输入)
  - 输入: 用户发送的新闻链接

节点2: HTTP请求(获取新闻)
  - 调用: 爬虫API或RSS获取新闻内容

节点3: 大模型(摘要)
  - 输入: 新闻内容
  - 提示词: "请将以下新闻内容精简为200字摘要: {content}"

节点4: 结束
  - 输出: 摘要结果
```

## 10.5 知识库配置

```
知识库创建步骤:

1. 创建知识库
   - 名称: 产品文档库
   - 描述: 存储所有产品相关文档

2. 上传文档
   - 支持: TXT, PDF, DOCX, HTML, Markdown
   - 单文件最大: 15MB
   - 建议: 先预处理文档，删除无关内容

3. 配置召回
   - 分段方式: 智能分段(推荐)
   - 分段长度: 500-800字符
   - 召回数量: 3-5

4. 关联到Bot
   - 在Bot配置中添加知识库
   - 设置召回参数
```
