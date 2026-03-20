# Standard Workflow

## 8.1 Monitoring Setup

```
Phase 1: Agent Installation
├── Install Datadog Agent
├── Configure API key
├── Enable integrations
└── Verify connection

Phase 2: Instrumentation
├── Add APM tracing
├── Configure custom metrics
├── Set up log collection
└── Deploy dashboards

Phase 3: Alerting
├── Define SLOs
├── Create alert conditions
├── Configure notifications
└── Test alerts

Phase 4: Maintenance
├── Review dashboards
├── Tune thresholds
├── Update monitors
└── Archive unused items
```

## 8.2 APM Integration

```python
# Flask APM
from ddtrace import patch_all
patch_all()

from flask import Flask
app = Flask(__name__)

@app.route("/api/users/<int:user_id>")
def get_user(user_id):
    with tracer.trace("db.fetch_user") as span:
        span.set_tag("user.id", user_id)
        user = db.get_user(user_id)
    return {"user": user}
```

## 8.3 Custom Metrics

```python
from datadog import statsd

# Gauge - point in time
statsd.gauge("app.active_users", 150)

# Counter - events
statsd.increment("app.page_views", tags=["page:home"])

# Histogram - distribution
statsd.histogram("app.request_latency", 0.125, tags=["endpoint:/api"])

# Distribution - percentiles
statsd.distribution("app.payment_amount", 99.99)
```

## 8.4 Log Collection

```python
import logging
from ddtrace import patch_logging

patch_logging()

logger = logging.getLogger(__name__)
logger.info("User logged in", extra={
    "user_id": 123,
    "action": "login"
})
```

## 8.5 Alert Configuration

```yaml
# Monitor YAML
type: metric alert
name: High Error Rate
query: >
  sum(last_5m):sum:app.errors{env:production}.as_count() 
  / 
  sum(last_5m):sum:app.requests{env:production}.as_count() 
  > 0.05
message: |
  Error rate is above 5%
  
  {{#is_alert}}
  Investigate at: {{infra_url}}
  {{/is_alert}}
  
  @slack-datadog
priority: 2
tags:
  - service:myapp
  - env:production
```
