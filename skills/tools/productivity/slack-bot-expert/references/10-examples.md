# Examples

## 10.1 Slack Webhook Response

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def handle_event():
    # Verify request
    signature = request.headers.get("X-Slack-Signature")
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    
    # Handle URL verification
    if request.json.get("type") == "url_verification":
        return {"challenge": request.json.get("challenge")}
    
    # Handle message event
    event = request.json.get("event", {})
    if event.get("type") == "message":
        channel = event.get("channel")
        text = event.get("text")
        # Process message
    
    return "", 200
```

## 10.2 Send Message

```python
import requests

def send_message(token, channel, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"channel": channel, "text": text}
    return requests.post(url, headers=headers, json=data)
```

## 10.3 Interactive Component

```python
@app.route("/slack/action", methods=["POST"])
def handle_action():
    payload = request.form.get("payload")
    action_data = json.loads(payload)
    # Handle button click
    return "", 200
```