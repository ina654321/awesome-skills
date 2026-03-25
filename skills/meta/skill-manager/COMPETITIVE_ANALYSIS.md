# Competitive Analysis: Skill Management Tools (v1.2)

**Scope**: AI skill lifecycle management — creation, evaluation, quality assurance
**Date**: 2026-03-25
**Analyst**: neo.ai
**Version**: 1.2.0 (deep analysis)

---

## Executive Summary

After deep analysis of skill-creator (Anthropic) and agentskills.io, here's the key insight:

**skill-creator** = Automation-heavy, requires API access, good for teams
**agentskills** = Specification only, platform-agnostic, good for developers  
**skill-manager** = Methodology-heavy, self-contained, good for quality

**Each serves different needs. None is "better" — they complement.**

---

## 1. Competitors Surveyed

| Tool | Owner | Stars | Philosophy |
|------|-------|-------|------------|
| **skill-creator** | Anthropic | 102k+ | Automation-first |
| **agentskills** | Open spec | 14k | Specification-first |
| **skill-manager** | neo.ai | — | Quality-first |

---

## 2. Deep Analysis: What Actually Matters

### 2.1 skill-creator: The Automation Powerhouse

**What it does well:**
- Parallel subagent testing (with skill vs without)
- LLM-graded assertions
- Token/time benchmarking
- Description trigger optimization with train/val

**The secret sauce:**
```
1. Spawn subagent WITH skill
2. Spawn subagent WITHOUT skill (baseline)
3. Compare outputs using LLM grading
4. Compute: pass_rate, delta_vs_baseline
```

**The problem:**
- Requires API access (ANTHROPIC_API_KEY)
- Complex setup
- Enterprise/SSO users can't use it (Issue #532)
- Over-engineered for individual developers

**Key insight I missed before:**
skill-creator's power isn't the SKILL.md writing — it's the **testing infrastructure**. The creation advice is actually quite simple (do real tasks, capture intent), but the testing/evals system is sophisticated.

### 2.2 agentskills: The Elegant Specification

**What it does well:**
- Simple, open format (SKILL.md + YAML)
- Platform-agnostic (Claude, Copilot, Codex, etc.)
- 3-level progressive disclosure built-in
- Active community (skillport, npx skills, etc.)

**The beauty:**
```yaml
---
name: skill-name
description: What it does. Use when: trigger phrases.
---
# Skill body (<5000 tokens)
## When triggered
...
## Examples
...
## Resources (optional)
- references/
- scripts/
```

**The problem:**
- It's JUST a specification — no methodology
- No creation guidance
- No evaluation framework
- No quality standards

**Key insight:**
agentskills is intentionally minimal. It's a **format**, not a **tool**. Comparing skill-manager to agentskills is like comparing a car to a road sign.

---

## 3. The Truth About skill-manager

### 3.1 What We Do Well

| Area | skill-manager Value |
|------|---------------------|
| **Quality methodology** | 12-dimension rubric (unique) |
| **Restoration** | 7-step fix methodology (unique) |
| **Self-contained** | No API required (vs skill-creator) |
| **Structured creation** | Intent capture → test → generalize (unique) |
| **Quality gates** | Certification workflow (unique) |

### 3.2 What We Still Lack

| Gap | Why It Matters | Realistic Fix |
|-----|----------------|---------------|
| **Skill dependencies** | Enterprise needs to know what skills depend on what | Add dependency guidance |
| **Distribution** | How to share/publish skills | Add distribution guide |
| **Versioning** | Skills evolve, need version tracking | Add semantic versioning |
| **Assertion templates** | Users don't know what to test | Add evals.json templates |

### 3.3 What We Should NOT Try to Do

| Avoid | Reason |
|-------|--------|
| Parallel subagent testing | Requires API, complex |
| LLM-graded assertions | Requires API |
| Token/benchmarking | Requires API, over-engineering |
| Platform-specific features | Keep platform-agnostic |

**Key insight:**
skill-manager's differentiation is **methodology quality**, not automation. Don't try to replicate skill-creator's tooling. Lean into what makes us unique: **structured, quality-focused, human-driven methodology**.

---

## 4. Real Improvements for v1.2

### 4.1 Add: Skill Dependencies Guide

**Why:** Enterprise users need to know how skills relate to each other.

```
skill-a/
  requires:
    - skill-b (for authentication)
    - skill-c (for data processing)
```

### 4.2 Add: Distribution Guide

**Why:** People create skills but don't know how to share them.

- GitHub repo structure
- Publishing options (skillport, npx, manual)
- Version tagging

### 4.3 Add: Semantic Versioning

**Why:** Skills evolve, users need to know if they're breaking changes.

```
v1.0.0 - Initial release
v1.1.0 - New feature (backward compatible)
v1.2.0 - Breaking change
v2.0.0 - Major rewrite
```

### 4.4 Add: evals.json Templates

**Why:** Users don't know what to test.

```
evals/
├── evals.json          # Assertion definitions
└── eval-queries.json   # Test queries
```

---

## 5. The Complete Picture

### How the Three Tools Work Together

```
agentskills (format) → skill-manager (methodology) → skill-creator (automation)
     ↑                        ↑                          ↑
  "What to write"      "How to create quality"     "How to test at scale"
```

**Ideal workflow:**
1. Use agentskills format (platform-agnostic)
2. Use skill-manager methodology (quality-focused)
3. Use skill-creator testing (if you have API access and need scale)

### skill-manager's Positioning

| What we own | What we borrow | What we avoid |
|-------------|----------------|---------------|
| Quality methodology | "Real tasks first" (skill-creator) | API-dependent automation |
| Creation workflow | Format compliance (agentskills) | Platform-specific features |
| Restoration | | Competing on tooling |

---

## 6. Changes in v1.2

### Added

- Skill dependencies section
- Distribution guide  
- Semantic versioning
- evals.json templates
- Clear positioning statement

### Strengthened

- "Quality over automation" message
- Self-contained methodology emphasis
- Enterprise readiness

---

## 7. Feature Matrix (Final)

| Capability | skill-creator | agentskills | skill-manager |
|------------|:---:|:---:|:---:|
| **FORMAT** | | | |
| SKILL.md spec | ✅ | ✅ | ✅ |
| YAML frontmatter | ✅ | ✅ | ✅ |
| Progressive disclosure | ✅ 3-level | ✅ 3-level | ✅ |
| **CREATION** | | | |
| Intent capture | ✅ Interview | ❌ | ✅ Enhanced |
| Real tasks first | ✅ | ❌ | ✅ |
| Templates | ✅ | ✅ Template | ✅ |
| **QUALITY** | | | |
| 12-dimension rubric | ❌ | ❌ | ✅ Unique |
| Dual-track scoring | ❌ | ❌ | ✅ |
| Certification | ❌ | ❌ | ✅ |
| Restoration | ❌ | ❌ | ✅ |
| **TESTING** | | | |
| Parallel subagents | ✅ API | ❌ | ❌ |
| LLM grading | ✅ API | ❌ | ❌ |
| Benchmarking | ✅ | ❌ | ❌ |
| **DISTRIBUTION** | | | |
| Dependencies | ❌ RFC | ❌ | ✅ Guide |
| Versioning | ❌ | ❌ | ✅ Guide |
| Publishing | ❌ | ❌ | ✅ Guide |

---

## 8. Conclusion

**skill-manager doesn't need to compete with skill-creator on automation** — that's not a fair fight (they have API access, we don't).

**skill-manager doesn't need to replace agentskills** — that's not the goal (they're a spec, we're a methodology).

**skill-manager's unique value: Quality-focused, self-contained methodology for creating, evaluating, and maintaining high-quality skills.**

This is enough. Be confident in this positioning.

---

*Analysis Date: 2026-03-25*
*Based on: skill-creator (anthropics/skills), agentskills (agentskills.io), skill-manager v1.1*
