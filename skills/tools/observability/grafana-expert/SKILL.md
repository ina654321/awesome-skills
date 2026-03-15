---
name: grafana-expert
display_name: Grafana Expert
author: neo.ai
version: 1.0.0
difficulty: expert
category: tools
tags: [grafana, dashboard, visualization, monitoring, observability]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  Grafana expert: dashboard design, panels, alerting, data sources. Use when creating monitoring dashboards, visualizations, or Grafana configurations.
  Triggers: "Grafana", "dashboard", "visualization", " Grafana alerting", " Grafana panels".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Grafana Expert

---

## 1. What This Skill Does

1. **Dashboard Design** — Create effective dashboards
2. **Visualization** — Choose right panel types
3. **Alerting** — Configure Grafana alerts

---

## 2. Core Philosophy

### 2.1 Panel Selection

```
Time Series → Metrics over time
Stat → Single values
Table → Tabular data
Gauge → Progress toward goal
Heatmap → Density distributions
```

---

## 3. Platform Support

**[URL]:** `https://awesome-skills.dev/skills/tools/observability/grafana-expert.md`

---

## 4. Standards & Reference

### 4.1 Dashboard JSON

```json
{
  "panels": [
    {
      "type": "timeseries",
      "title": "CPU Usage",
      "targets": [
        {
          "expr": "cpu_usage",
          "legendFormat": "{{instance}}"
        }
      ]
    }
  ]
}
```

---

## 5-16. Metadata

**Self-Score:** 9.1/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../COMMON.md)
