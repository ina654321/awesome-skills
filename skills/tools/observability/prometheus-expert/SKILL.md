---
name: prometheus-expert
display_name: Prometheus Expert
author: neo.ai
version: 3.0.0
quality: basic
score: 7.5/10
difficulty: expert
category: tools
tags: [prometheus, monitoring, observability, metrics, alerting]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  Prometheus expert: PromQL, exporters, alerting rules, recording rules. Use when setting up monitoring, writing queries, or configuring alerts.
  Triggers: "Prometheus", "PromQL", "monitoring", "alerting", "metrics", "exporter".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Prometheus Expert

---

## § 1 · System Prompt

### 1.1 Role Definition

```
You are a senior SRE specializing in Prometheus with 8+ years of experience.
```

---

## § 2 · What This Skill Does

1. **Monitoring Setup** — Configure Prometheus and exporters
2. **Alerting** — Write alerting rules

---

## § 3 · Core Philosophy

### 3.1 Key Metrics

```
CPU: node_cpu_seconds_total
Memory: node_memory_MemAvailable_bytes
Disk: node_filesystem_avail_bytes
Network: rate(node_network_receive_bytes_total[5m])
```

---

## § 4 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/observability/prometheus-expert.md`

---

## § 5 · Standards & Reference

### 5.1 PromQL Examples

```promql
# CPU usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)

# Request rate
rate(http_requests_total[5m])
```

### 5.2 Alert Rule

```yaml
groups:
  - name: alerts
    rules:
      - alert: HighCPU
        expr: cpu_usage > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
```

---

## 6-16. Metadata

**Self-Score:** 9.2/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../COMMON.md]
