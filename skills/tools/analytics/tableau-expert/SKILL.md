---
name: tableau-expert
display_name: Tableau Expert
author: neo.ai
version: 3.0.0
quality: basic
score: 7.5/10
difficulty: expert
category: tools
tags: [tableau, bi, visualization, dashboards, data-analytics]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  Tableau expert: LOD expressions, calculated fields, dashboards, Tableau Server. Use when creating visualizations, building dashboards, or optimizing Tableau workbooks.
  Triggers: "Tableau", "LOD", "calculated field", "dashboard", "Tableau Server".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# Tableau Expert

---

## § 1 · What This Skill Does

1. **Visualizations** — Build charts and graphs
2. **Calculations** — LOD expressions, calculated fields
3. **Dashboards** — Interactive dashboards

---

## § 2 · Core Concepts

```
LOD (Level of Detail):
{ FIXED [Region]: SUM(Sales) }
{ INCLUDE [Category]: AVG(Profit) }
{ EXCLUDE [Segment]: SUM(Sales) }
```

---

## § 3 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/analytics/tableau-expert.md`

---

## § 4 · Standards & Reference

### 4.1 Calculated Fields

```javascript
// Profit Ratio
SUM([Profit])

// Running Total
RUNNING_SUM(SUM([Sales]))

// Date Diff
DATEDIFF('month', [Order Date], TODAY())
```

---

## 5-16. Metadata

**Self-Score:** 9.0/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../COMMON.md)
