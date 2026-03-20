# Common Pitfalls & Anti-Patterns

## 10.1 Common Mistakes

| # | Mistake | Severity | Prevention |
|---|---------|----------|------------|
| 1 | Too many custom metrics | 🔴 High | Use metric types wisely |
| 2 | Missing tags | 🔴 High | Always add env, service, version |
| 3 | No cardinality limits | 🔴 High | Avoid high-cardinality tags |
| 4 | Logging sensitive data | 🔴 High | Sanitize logs before sending |
| 5 | Alerting on raw metrics | 🟡 Medium | Use derived metrics |
| 6 | No monitor maintenance | 🟡 Medium | Review periodically |

## 10.2 Anti-Patterns

### Custom Metrics

```python
# BAD: Too many metrics
for user_id in range(10000):
    statsd.gauge(f"user_{user_id}_balance", balance)
    # Creates 10000 unique metrics!

# GOOD: Tagged metrics
statsd.gauge("user.balance", balance, tags=[f"user_id:{user_id}"])
# Single metric with tag values
```

### Alerting

```python
# BAD: Alert on every spike
alert if metric > threshold

# GOOD: Sustained threshold
# Monitor for 5+ minutes before alerting
```

## 10.3 Cardinality Guidelines

| Tag Type | Cardinality | Examples |
|----------|-------------|----------|
| Low | < 100 values | env, service, region |
| Medium | < 1000 values | instance, availability-zone |
| High | > 10000 | user_id, session_id, request_id |

## 10.4 Best Practices

```
Instrumentation:
□ Use APM auto-instrumentation
□ Add custom spans for business logic
□ Include relevant tags
□ Set appropriate sample rates

Dashboards:
□ Start with overview
□ Use variables for filtering
□ Keep dashboards focused
□ Use templates for reusability

Alerting:
□ Alert on symptoms not causes
□ Set appropriate thresholds
□ Include context in messages
□ Test alerts periodically
```
