# Competitive Analysis: Skill Management Tools (v1.2)

**Scope**: AI skill lifecycle management — creation, evaluation, quality assurance
**Date**: 2026-03-25
**Version**: 1.2.1

---

## Executive Summary

After multiple rounds of analysis and iteration:

| Tool | Owner | Philosophy |
|------|-------|------------|
| **skill-creator** | Anthropic | Automation-first (API required) |
| **agentskills** | Open spec | Specification-only |
| **skill-manager** | neo.ai | **Methodology-first** (self-contained) |

**Our positioning**: Quality-focused methodology for individual developers and teams without API access.

---

## What Makes skill-manager Unique

### 1. Complete Methodology

| Phase | skill-creator | agentskills | skill-manager |
|-------|:---:|:---:|:---:|
| Intent capture | ✅ | ❌ | ✅ Enhanced |
| Creation workflow | ✅ | ❌ | ✅ 6-phase |
| Quality rubric | ❌ | ❌ | ✅ 12-dim |
| Evaluation | Automated | ❌ | Interactive |
| Restoration | ❌ | ❌ | ✅ 7-step |
| Certification | ❌ | ❌ | ✅ |
| Dependencies | ❌ | RFC | ✅ Guide |
| Versioning | ❌ | ❌ | ✅ Guide |
| Distribution | ❌ | ❌ | ✅ Guide |

### 2. Real Examples

We don't just describe methodology — we show it:
- Complete creation example (references/example.md)
- Real evaluation walkthrough with scores
- Before/after skill comparison

### 3. Quick Tools

- 5-minute quick checklist
- 20-minute standard protocol
- 60-minute deep evaluation
- 2-hour certification

### 4. Self-Contained

No API required. Works offline. No dependencies.

---

## v1.2.1 Improvements

### What's New

1. **Quick Evaluation Checklist** (5 min)
   - 7-item checklist for fast assessment
   - "Likely ≥7.0" or "needs work" decision

2. **Complete Creation Example**
   - Full walkthrough: commit-message-writer skill
   - Shows all 6 phases in action
   - Real testing, failures, fixes

3. **Real Evaluation Example**
   - Before/after score comparison
   - Detailed gap analysis
   - Pattern-based fixes

### Files Added/Updated

| File | Change |
|------|--------|
| references/example.md | New - Complete creation walkthrough |
| references/evaluate.md | Updated - Quick checklist + real example |
| COMPETITIVE_ANALYSIS.md | Updated - v1.2.1 |

---

## Feature Matrix

| Capability | skill-creator | agentskills | skill-manager |
|------------|:---:|:---:|:---:|
| **FORMAT** | | | |
| SKILL.md spec | ✅ | ✅ | ✅ |
| YAML frontmatter | ✅ | ✅ | ✅ |
| Progressive disclosure | ✅ 3-level | ✅ 3-level | ✅ |
| **CREATION** | | | |
| Intent capture | ✅ | ❌ | ✅ |
| Real tasks first | ✅ | ❌ | ✅ |
| Templates | ✅ | ✅ | ✅ |
| Complete example | ❌ | ❌ | ✅ |
| **QUALITY** | | | |
| 12-dimension rubric | ❌ | ❌ | ✅ |
| Quick checklist | ❌ | ❌ | ✅ |
| Dual-track scoring | ❌ | ❌ | ✅ |
| Certification | ❌ | ❌ | ✅ |
| Restoration | ❌ | ❌ | ✅ |
| **ENTERPRISE** | | | |
| Dependencies | ❌ | RFC | ✅ |
| Versioning | ❌ | ❌ | ✅ |
| Distribution | ❌ | ❌ | ✅ |
| **TESTING** | | | |
| Parallel subagents | ✅ | ❌ | ❌ |
| LLM grading | ✅ | ❌ | ❌ |
| Benchmarking | ✅ | ❌ | ❌ |

---

## What We Don't Try to Do

| Avoid | Reason |
|-------|--------|
| API-dependent automation | Excludes users without keys |
| Platform-specific features | Keep compatible |
| Automated benchmarking | Over-engineering for most users |
| Compete on tooling | Compete on methodology instead |

---

## Conclusion

skill-manager is the **methodology choice** for:

1. **Individual developers** who want quality without complexity
2. **Teams** without API access
3. **Enterprises** needing dependency/versioning guidance
4. **Quality-focused** workflows over automated testing

This is enough. Be confident.

---

*Version: 1.2.1 | Date: 2026-03-25*
