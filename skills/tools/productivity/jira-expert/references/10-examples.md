# Examples

## 10.1 Create Issue

```python
import requests
from requests.auth import HTTPBasicAuth

url = "https://your-domain.atlassian.net/rest/api/3/issue"
auth = HTTPBasicAuth("email@example.com", "API_TOKEN")

headers = {"Content-Type": "application/json"}
data = {
    "fields": {
        "project": {"key": "PROJ"},
        "summary": "My issue",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Description"}]}]
        },
        "issuetype": {"name": "Task"}
    }
}

response = requests.post(url, json=data, auth=auth, headers=headers)
print(response.json())
```

## 10.2 Search JQL

```python
url = "https://your-domain.atlassian.net/rest/api/3/search"
params = {"jql": "project = PROJ AND status = 'To Do' ORDER BY created DESC"}

response = requests.get(url, auth=auth, params=params)
issues = response.json()
for issue in issues["issues"]:
    print(f"{issue['key']}: {issue['fields']['summary']}")
```

## 10.3 Transition Issue

```python
issue_key = "PROJ-123"
url = f"https://your-domain.atlassian.net/rest/api/3/issue/{issue_key}/transitions"

data = {
    "transition": {"id": "21"}
}

response = requests.post(url, json=data, auth=auth, headers=headers)
```