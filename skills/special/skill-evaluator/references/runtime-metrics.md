# Runtime Metrics

Collect data during skill execution.

---

## Automatic Metrics

| Metric | How | Target |
|--------|-----|--------|
| Latency | Trigger → First token | <2s |
| Output size | Tokens generated | Context-appropriate |
| Tool success | Scripts/assets load | 100% |

---

## User Signals (Implicit)

**Positive:**
- Accepts output without change
- Follow-up in same thread
- "Thanks", "Perfect", "Great"

**Negative:**
- Immediate correction
- Repeats differently
- Switches skills

---

## Engagement Score

```
1-2 turns: Low
3-5 turns: Medium
6+ turns: High
```

---

## Quick Report

```
SKILL: {name}
Uses: N
Avg Latency: X ms
Acceptance: Y%
Engagement: Z%
Trend: ↑/→/↓
```
