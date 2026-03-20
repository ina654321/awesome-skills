# Examples

## 10.1 Prometheus Config

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'myservice'
    kubernetes_sd_configs:
      - role: pod
```

## 10.2 Recording Rules

```yaml
groups:
  - name: example
    rules:
      - record: job:http_requests:rate5m
        expr: rate(http_requests_total[5m])

      - record: instance:node_cpu:avg
        expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

## 10.3 Alert Rules

```yaml
groups:
  - name: example
    rules:
      - alert: HighRequestLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High request latency"

      - alert: InstanceDown
        expr: up == 0
        for: 5m
        labels:
          severity: critical
```

## 10.4 Alertmanager Config

```yaml
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'

receivers:
  - name: 'default'
    email_configs:
      - to: 'team@example.com'
        send_resolved: true
  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/...'
        channel: '#alerts'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```