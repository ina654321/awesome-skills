# Competitive Analysis: Skill Management Tools (v1.1)

**Scope**: AI skill lifecycle management — creation, evaluation, quality assurance
**Date**: 2026-03-25
**Analyst**: neo.ai
**Version**: 1.1.0 (after optimization)

---

## 1. Competitors Surveyed

| Tool | Owner | Stars | License | Source |
|------|-------|-------|---------|--------|
| **skill-creator** | Anthropic | 102k+ | Apache 2.0 | [anthropics/skills](https://github.com/anthropics/skills) |
| **agentskills-ref** | agentskills.io | — | — | [agentskills/agentskills](https://github.com/agentskills/agentskills) |
| **skill-manager** | neo.ai | — | MIT | theneoai/awesome-skills |

---

## 2. What Makes skill-creator Great (Lessons Learned)

After deep analysis, here are skill-creator's key strengths that influenced skill-manager v1.1:

### 2.1 "Real Tasks First" Philosophy
- "Do real tasks, not just write documentation"
- Test on actual queries, not hypotheticals
- Generalize from feedback, not specific examples

### 2.2 Interview-Based Intent Capture
- Structured questions to understand user needs
- Extract real example queries before writing
- Don't assume — ask what users will actually type

### 2.3 "Pushy" Descriptions
- "Make descriptions a little bit pushy"
- Explicit trigger phrases, not passive language
- Use "Use when:" pattern

### 2.4 Evals-Driven Improvement Loop
- Run eval → analyze failures → identify patterns → fix patterns → re-run
- Fix root causes, not symptoms
- Continuous feedback loop

### 2.5 Lightweight but Thorough
- Works without API keys (claude -p fallback)
- Scales from quick to comprehensive

---

## 3. skill-manager v1.1 Improvements

### Changes from v1.0 → v1.1

| Feature | v1.0 | v1.1 (Now) |
|---------|------|------------|
| Creation philosophy | Documentation-first | **Real Tasks First** |
| Intent capture | Tier selection only | **Structured interview questions** |
| Description optimization | Manual | **Evals-driven with trigger rate target** |
| Improvement loop | Gap analysis only | **Evals-driven feedback loop** |
| Mode count | 3 (Create/Evaluate/Restore) | **4 (added Optimize)** |
| Scripts | 4 | **5 (added optimize.sh)** |

### New §4: CREATE Mode — Real Tasks First

```
Phase 1: Intent Capture (15 min)    → Extract real queries
Phase 2: First Draft (30-60 min)     → Test on real queries
Phase 3: Evaluation (15 min)         → Find patterns in failures
Phase 4: Generalization (30-60 min) → Fix patterns, not specific failures
Phase 5: Documentation (15 min)      → Write from patterns
Phase 6: Description Optimization    → Trigger rate ≥ 85%
```

### New §6: OPTIMIZE Mode

- Dedicated description trigger optimization
- Pushy description pattern from skill-creator
- Target: ≥85% trigger rate on 20 eval queries

### New references/descriptions.md

Complete guide to description optimization:
- Pushy description pattern
- Evals-driven methodology
- 20-query test set generation

---

## 4. Feature Comparison (Updated)

| Capability | skill-creator | agentskills-ref | skill-manager v1.1 |
|------------|:---:|:---:|:---:|
| **CREATION** | | | |
| Intent capture / interviewing | ✅ Structured | ❌ | ✅ **Enhanced** |
| Tier-based creation guide | ❌ | ❌ | ✅ Lite/Standard/Enterprise |
| System prompt methodology (§1.1/1.2/1.3) | ❌ | ❌ | ✅ |
| Real tasks first philosophy | ✅ | ❌ | ✅ **Adopted** |
| Progressive disclosure guide | ✅ 3-level spec | ✅ Spec | ✅ Enforced |
| **EVALUATION** | | | |
| Text quality rubric (6 dimensions) | ❌ | ❌ | ✅ |
| Runtime quality rubric (6 dimensions) | ❌ | ❌ | ✅ |
| Automated parallel eval runs | ✅ Subagents | ❌ | ❌ |
| Interactive human evaluation | ❌ | ❌ | ✅ eval.sh |
| Heuristic pre-check | ❌ | ❌ | ✅ score.sh |
| **OPTIMIZATION** | | | |
| Description trigger optimization | ✅ | ❌ | ✅ **Enhanced** |
| Pushy description pattern | ✅ | ❌ | ✅ |
| Evals-driven feedback loop | ✅ | ❌ | ✅ |
| **TOOLING** | | | |
| Spec validation | ❌ | ✅ | ✅ validate.sh |
| Description optimization | ✅ | ❌ | ✅ optimize.sh |
| HTML benchmark report | ✅ Live | ❌ | ❌ |
| Markdown evaluation report | ❌ | ❌ | ✅ EVALUATION_REPORT.md |
| Certification suite | ❌ | ❌ | ✅ certify.sh |
| **PLATFORM** | | | |
| Claude.ai | ✅ | ✅ | ✅ |
| Claude Code | ✅ | ✅ | ✅ |
| VS Code Copilot | ❌ | ✅ | ✅ |
| OpenAI Codex | ❌ | ✅ | ✅ |

---

## 5. Gap Analysis — Post-Optimization

### What skill-manager Now Has (After v1.1)

| Gap | Status | Solution |
|-----|--------|----------|
| Real tasks first | ✅ Fixed | New CREATE flow with 6 phases |
| Intent capture | ✅ Fixed | Structured interview questions |
| Description optimization | ✅ Fixed | New OPTIMIZE mode + descriptions.md |
| Evals-driven loop | ✅ Fixed | References updated |

### Remaining Gaps

| Gap | Priority | Status |
|-----|----------|--------|
| Automated parallel eval runs | P1 | Still require manual testing |
| Token + timing benchmarks | P2 | Not in scope |
| HTML report | P2 | Not in scope |

---

## 6. Differentiation

### skill-manager Now Has Unique

- **12-dimension dual-track rubric** — finest-grained quality assessment
- **7-step restoration methodology** — how to fix bad skills
- **Real tasks first + intent capture** — structured creation from actual user needs
- **Evals-driven description optimization** — trigger rate ≥85% target
- **Tier system** — Lite/Standard/Enterprise scope clarity
- **Certification suite** — production sign-off with stress testing
- **Self-contained** — no external API needed

### Complementary with skill-creator

skill-manager and skill-creator are **complementary**, not competing:

```
skill-manager: Content quality + structural guidance
skill-creator: Performance benchmarks + automated evals

Use together:
1. skill-manager: CREATE → ensure good structure
2. skill-manager: EVALUATE → measure quality
3. skill-creator: run evals → measure performance
4. skill-manager: OPTIMIZE → improve triggering
5. skill-manager: CERTIFY → production sign-off
```

---

## 7. Roadmap

| Priority | Feature | Status |
|----------|---------|--------|
| ✅ Done | Real tasks first philosophy | v1.1 |
| ✅ Done | Intent capture | v1.1 |
| ✅ Done | Description optimization | v1.1 |
| ✅ Done | Evals-driven feedback loop | v1.1 |
| ✅ Done | OPTIMIZE mode | v1.1 |
| P2 | HTML report generation | Future |
| P2 | Token/time benchmarks | Future |

---

*Analysis based on: skill-creator SKILL.md (anthropics/skills), agentskills spec v1.0, skill-manager v1.1*
