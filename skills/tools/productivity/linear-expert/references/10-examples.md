# Examples

## 10.1 Create Issue (GraphQL)

```python
import requests

url = "https://api.linear.app/graphql"
headers = {"Authorization": "LIN_API_KEY", "Content-Type": "application/json"}

query = """
mutation IssueCreate($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      identifier
      title
    }
  }
}
"""

variables = {
    "input": {
        "teamId": "team_id",
        "title": "New issue",
        "description": "Description here"
    }
}

response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
```

## 10.2 List Issues

```python
query = """
query {
  issues(first: 10) {
    nodes {
      id
      title
      state { name }
    }
  }
}
"""
```

## 10.3 Update Issue

```python
mutation = """
mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
  }
}
"""
```