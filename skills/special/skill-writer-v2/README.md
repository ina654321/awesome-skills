# Skill Writer v2 — Minimal Load

**Default load:** 67 lines | **Decision time:** <30 sec | **Token-optimized**

---

## Quick Start

```bash
./scripts/init-skill.sh --tier={lite|standard|enterprise} --name={my-skill}
```

---

## Three Tiers

| Tier | Lines | Time | Load |
|------|-------|------|------|
| **Lite** | 50-150 | 30 min | `references/tier-lite.md` |
| **Standard** | 150-400 | 2 hrs | `references/tier-standard.md` |
| **Enterprise** | 400-800 | 1 day | `references/tier-enterprise.md` |

---

## Precision Triggering

**SKILL.md description:**
```yaml
description: "Write skills. Triggers ONLY: 'write skill', 'create skill', 'new skill', 'skill template', 'skill structure'."
```

**Strict trigger list** prevents false activation.

---

## Token Optimization

| File | Lines | Load Strategy |
|------|-------|---------------|
| SKILL.md | 67 | Always |
| tier-{X}.md | 54-67 | After tier selection |
| design-patterns.md | 53 | When needed |
| quality-rubric.md | 28 | When scoring |
| TEMPLATE-{X}.md | 115-307 | When scaffolding |

**Total default load:** 67 lines (~2KB)

---

## Flow

```
User: "Write a skill for..."
      ↓
Detect tier (Lite/Std/Ent) — 10 sec
      ↓
Load tier-{X}.md — 2 sec
      ↓
Execute creation flow
```

---

## vs Original

| Metric | Skill Writer v1 | Skill Writer v2 |
|--------|-----------------|-----------------|
| Default load | 565 lines | **67 lines** |
| Decision time | 2-5 min | **<30 sec** |
| Trigger precision | Medium | **High** |
| Token efficiency | Low | **High** |

---

## Files

```
skill-writer-v2/
├── SKILL.md (67 lines) — Index only
├── references/
│   ├── tier-lite.md (67)
│   ├── tier-standard.md (54)
│   ├── tier-enterprise.md (61)
│   ├── design-patterns.md (53)
│   └── quality-rubric.md (28)
├── assets/
│   ├── TEMPLATE-lite.md
│   ├── TEMPLATE-standard.md
│   └── TEMPLATE-enterprise.md
└── scripts/
    └── init-skill.sh
```

---

## License

MIT
