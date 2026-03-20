# Examples

## 10.1 Dashboard JSON

```json
{
  "dashboard": {
    "title": "My Dashboard",
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "CPU Usage",
        "type": "graph",
        "datasourceId": 1,
        "targets": [
          {
            "expr": "rate(node_cpu_seconds_total{mode='idle'}[5m]) * 100",
            "legendFormat": "{{instance}}"
          }
        ]
      }
    ]
  }
}
```

## 10.2 Prometheus Datasource Query

```
# CPU usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Request rate
rate(http_requests_total[5m])
```

## 10.3 Alert Rule

```yaml
groups:
- name: example
  rules:
  - alert: HighCPU
    expr: cpu_usage > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage detected"
```

## 10.4 Variables

```json
{
  "variables": [
    {
      "name": "hostname",
      "type": "query",
      "query": "label_values(node_cpu_seconds_total, instance)"
    }
  ]
}
```

## 10.5 Provisioning Datasource

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    isDefault: true
```