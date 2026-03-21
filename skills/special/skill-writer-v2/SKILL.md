---

name: skill-writer-v2
display_name: Skill Writer
author: awesome-skills
version: 3.2.0
quality: expert
difficulty: expert
category: special
tags: [skill-creation, scaffolding]
platforms: [kimi, claude, cursor, codex, opencode, cline, openclaw]
description: "Write skills. Triggers ONLY: 'write skill', 'create skill', 'new skill', 'skill template', 'skill structure'. Usage: Pick tier (Lite/Standard/Enterprise) → Load tier-{X}.md → Execute."

---

# Skill Writer v2

> **v3.2.0** | **Minimal Load** | **High Precision**

## System Prompt

```
You write skills. Three complexity tiers:

Lite (Tool): 50-150 lines, 5 sections, 30 min
Standard (Domain): 150-400 lines, 10 sections, 2 hrs  
Enterprise (Methodology): 400-800 lines, 16 sections, 1 day

Rule: Load references/tier-{X}.md after tier selection. SKILL.md is index only.
```

## Tier Selection

```
Input: "Create a skill for..."

"...PDF rotate / API call" → Lite
"...React patterns / medical terms" → Standard
"...Tesla engineer / Crisis negotiator" → Enterprise
```

## 30-Second Start

```bash
./scripts/init-skill.sh --tier={lite|standard|enterprise} --name={skill-name}
```

## Resources (Load on Demand)

| Need | Load |
|------|------|
| Tier details | `references/tier-{lite|std|ent}.md` |
| Templates | `assets/TEMPLATE-{tier}.md` |
| Design patterns | `references/design-patterns.md` |
| Quality rubric | `references/quality-rubric.md` |

## Quality Targets

| Tier | Lines | Score |
|------|-------|-------|
| Lite | 50-150 | 5.0-6.5 |
| Standard | 150-400 | 6.5-8.0 |
| Enterprise | 400-800 | 8.0-9.5 |

## Evaluation

After creating, evaluate with skill-evaluator:
```
"Evaluate this skill" → 6-dimension score → Upgrade guidance
```

Quick check: `./scripts/quick-eval.sh path/to/SKILL.md`

## Version

v3.2.0 — MIT
