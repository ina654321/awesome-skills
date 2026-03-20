# Standards & Reference

## 7.1 Official Documentation

- [Datadog Documentation](https://docs.datadoghq.com/)
- [Datadog API Reference](https://docs.datadoghq.com/api/latest/)
- [Datadog Integrations](https://docs.datadoghq.com/integrations/)
- [Datadog Synthetics](https://docs.datadoghq.com/synthetics/)
- [Datadog APM](https://docs.datadoghq.com/tracing/)
- [Datadog Logs](https://docs.datadoghq.com/logs/)

## 7.2 Configuration Reference

### Datadog Agent Config

```yaml
# datadog.yaml
init_config:
  instance_level_logs:
    - type: file
      path: /var/log/app/*.log
      service: myapp
      source: mysource

instances:
  - host: localhost
    port: 5432
    dbm: true
    tags:
      - env:production
      - service:database
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DD_API_KEY` | API key for authentication |
| `DD_SITE` | Datadog site (us5.datadoghq.com) |
| `DD_TAGS` | Global tags |
| `DD_LOG_LEVEL` | Logging level |

## 7.3 Metrics Reference

### Custom Metrics

| Type | Description | Example |
|------|-------------|---------|
| `gauge` | Point-in-time value | `metric.gauge("cpu", 45.2)` |
| `count` | Incremental counter | `metric.increment("requests")` |
| `histogram` | Distribution | `metric.histogram("latency", 150)` |
| `distribution` | Percentiles | `metric.distribution("request_size", 1024)` |

### APM Spans

```python
from ddtrace import tracer

@tracer.wrap("process_order")
def process_order(order_id):
    with tracer.trace("db.query") as span:
        span.set_tag("db.system", "postgresql")
        span.set_tag("db.statement", "SELECT * FROM orders")
        # Query database
    
    with tracer.trace("payment.process") as span:
        span.set_tag("payment.method", "credit_card")
        # Process payment
```

## 7.4 Dashboard Widgets

| Widget | Purpose |
|--------|---------|
| Timeseries | Metrics over time |
| Query Value | Single metric value |
| Top List | Ranked items |
| Alert Graph | Alerts on metrics |
| Log Stream | Log entries |
| Service Map | Service dependencies |

## 7.5 Version Compatibility

| Datadog Agent | Status | Notes |
|---------------|--------|-------|
| 7.x | Current | Latest features |
| 6.x | Supported | Legacy |
| 5.x | EOL | Old |

## 7.6 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/series` | POST | Submit metrics |
| `/api/v1/check_run` | POST | Submit check |
| `/api/v1/log` | POST | Send logs |
| `/api/v1/apm/traces` | POST | Send traces |
