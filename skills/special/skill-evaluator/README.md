# Skill Evaluator

Evaluate skill performance in real-time or post-hoc.

---

## Two Modes

### Runtime Evaluation (During Use)
Observe skill output in real-time, flag issues.

### Post-Hoc Evaluation (File Review)
Review SKILL.md against 6-dimension rubric.

---

## Quick Start

```bash
# Quick file check
./scripts/quick-eval.sh path/to/SKILL.md

# Generate test cases
./scripts/test-skill.sh path/to/SKILL.md
```

---

## 6-Dimension Rubric

| Dimension | Weight | Target (Expert) |
|-----------|--------|-----------------|
| System Prompt | 20% | 7-8 |
| Domain Knowledge | 25% | 7-8 |
| Workflow | 15% | 6-7 |
| Risk Docs | 10% | 4-5 |
| Examples | 20% | 7-8 |
| Metadata | 10% | 7-8 |

**Expert:** 6.5-8.4 | **Exemplary:** 8.5-10

---

## Usage

```
"Evaluate this skill" [attach SKILL.md]
"Test skill performance"
"How good is tesla-engineer skill?"
"Compare skill A vs B"
```

---

## References

- `quality-rubric.md` — Detailed scoring
- `runtime-metrics.md` — Usage data collection
- `a-b-testing.md` — Compare skill versions

---

## Integration

Use with skill-writer-v2:
```
Create skill → Auto-evaluate → Get report → Upgrade
```

---

v1.0.0 — MIT
