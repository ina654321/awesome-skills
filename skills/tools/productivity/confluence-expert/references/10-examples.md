# Examples

## 10.1 Create Page

```python
import requests
from requests.auth import HTTPBasicAuth

url = "https://your-domain.atlassian.net/wiki/rest/api/content"
auth = HTTPBasicAuth("email@example.com", "API_TOKEN")

headers = {"Content-Type": "application/json"}
data = {
    "type": "page",
    "title": "My New Page",
    "space": {"key": "TEAM"},
    "body": {
        "storage": {
            "value": "<p>Page content here</p>",
            "representation": "storage"
        }
    }
}

response = requests.post(url, json=data, auth=auth, headers=headers)
print(response.json())
```

## 10.2 Update Page

```python
page_id = "123456"
url = f"https://your-domain.atlassian.net/wiki/rest/api/content/{page_id}"

data = {
    "id": page_id,
    "type": "page",
    "title": "Updated Title",
    "body": {
        "storage": {
            "value": "<p>Updated content</p>",
            "representation": "storage"
        }
    },
    "version": {"number": 2}
}

response = requests.put(url, json=data, auth=auth, headers=headers)
```

## 10.3 Search with CQL

```python
url = "https://your-domain.atlassian.net/wiki/rest/api/search"
params = {"cql": "type=page and space.key=TEAM"}

response = requests.get(url, auth=auth, params=params)
results = response.json()
for r in results["results"]:
    print(r["title"])
```

## 10.4 Get Page Children

```python
page_id = "123456"
url = f"https://your-domain.atlassian.net/wiki/rest/api/content/{page_id}/child"

response = requests.get(url, auth=auth)
children = response.json()
```