# Create Reference

> Full creation workflow based on "real tasks first" philosophy.

---

## Core Philosophy: Real Tasks First

**From skill-creator**: "Do real tasks, not just write documentation. Generalize from feedback, not specific examples."

A skill that looks perfect on paper but fails in practice is useless. The creation process must be **task-driven**, not **documentation-driven**.

---

## Phase 1: Intent Capture (15 min)

### The Problem

Most skills fail because they're built from assumptions, not real needs:
- ❌ "I want a skill for code review" — too vague
- ✅ "I want to review PRs for security issues, suggest fixes" — specific

### Intent Capture Questions

Ask the user (don't skip this!):

1. **What real task** do you want this skill to help with?
2. **What would you type** to invoke this skill? (list 3-5 example queries)
3. **What does success look like?** — concrete output
4. **What edge cases** have you encountered?

### Output: Intent Document

```
## Skill Intent

**Task**: [One sentence]

**Example Queries**:
1. "analyze my sales data"
2. "find anomalies in this dataset"
3. "make a chart from this CSV"

**Expected Output**: A markdown report with 3 key insights

**Edge Cases**: Empty files, malformed CSV, timeout
```

---

## Phase 2: First Draft — Do Real Tasks (30-60 min)

### The Process

1. Write a minimal SKILL.md that handles the 3-5 example queries
2. **Test it** — actually run the skill on those queries
3. Fix failures — but **generalize the fix**, don't just handle that specific query
4. Iterate until it works on all example queries

### Key: Don't Skip Testing!

```
Draft skill → Test on query 1 → Fail → Fix pattern → Test again
                                              ↓
                                      Don't just handle query 1!
                                      Handle all queries like query 1!
```

---

## Phase 3: Evaluation — Find Patterns (15 min)

### Run Evals

Test on example queries + variations. Group failures into **patterns**:

| Failed Query | Root Pattern |
|--------------|--------------|
| "analyze empty file" | Missing null/empty handling |
| "analyze malformed CSV" | Input validation missing |
| "chart without data" | Graceful degradation needed |

### Generalization Principle

❌ **Bad**: "Failed on query X, add handling for X"
✅ **Good**: "Failed on edge cases, add edge case handling framework"

---

## Phase 4: Generalization — Fix Patterns (30-60 min)

**Key principle**: Fix the pattern, not the specific failure.

| Specific Fix | Generalized Fix |
|--------------|-----------------|
| Handle "empty file" | Add null/empty input handling |
| Handle "malformed CSV" | Add input validation + error messages |
| Handle "no data for chart" | Add graceful degradation |

---

## Phase 5: Documentation (15 min)

Now write proper SKILL.md **from the patterns** discovered:

- §1.1/1.2/1.3 System Prompt (from what worked)
- Workflow (from the actual process)
- Examples (real ones from testing)
- Error handling (real edge cases)
- Anti-patterns (lessons learned)

---

## Phase 6: Description Optimization (15 min)

**Critical**: A perfect skill that doesn't trigger is useless.

### Pushy Description Pattern

From skill-creator: "Make descriptions a little bit pushy"

❌ **Passive**: "A skill for data analysis"
✅ **Pushy**: "Analyze data, find trends, generate visualizations. Use when: 'analyze data', 'find trends', 'make chart'"

### Trigger Rate Test

1. Write 20 eval queries (10 should trigger, 10 shouldn't)
2. Test description trigger rate
3. Iterate until ≥ 85%

---

## Tier Selection

| Tier | When to Use | Real Task Scope |
|------|-------------|-----------------|
| **Lite** | 1 capability, 15 min | Generate skill, test on 3 queries |
| **Standard** | 2-5 capabilities, 1-2 hrs | Full intent capture, eval, generalize |
| **Enterprise** | 5+ capabilities, 2+ hrs | Full workflow, comprehensive evals |

---

## System Prompt Design (§1.1 / §1.2 / §1.3)

### §1.1 — Identity & Worldview

```markdown
### § 1.1 · Identity & Worldview

You are a **[Role Title]**, specialized in [specific domain].

**Professional DNA**:
- [Specific expertise 1]: [Real methodology or company]
- [Specific expertise 2]: [Quantified capability]
- [Specific expertise 3]: [Domain-specific lens]
```

### §1.2 — Decision Framework

```markdown
### § 1.2 · Decision Framework

**Priority Hierarchy**:
1. [Highest priority]
2. [Second priority]
...
**When inputs conflict**: [Tie-breaking rule]
```

### §1.3 — Thinking Patterns

```markdown
### § 1.3 · Thinking Patterns

**Pattern 1: [Name]**
[Decision tree or reasoning approach]
```

---

## Creation Checklist

```
[ ] Intent captured (3-5 real example queries)
[ ] First draft tested on real queries
[ ] Failures grouped into patterns
[ ] Patterns generalized (not specific fixes)
[ ] Re-tested on all queries + edge cases
[ ] SKILL.md written from patterns
[ ] Progressive disclosure applied (≤300 lines)
[ ] Description tested for trigger rate ≥ 85%
[ ] Dual-track score ≥ 9.0, variance < 1.0
```

---

## Key Principles Summary

| Principle | What It Means |
|-----------|---------------|
| Real Tasks First | Test on actual queries, not hypotheticals |
| Intent Capture | Ask what users will type |
| Generalize Patterns | Fix root causes, not symptoms |
| Pushy Descriptions | Make triggers explicit |
| Evals-Driven | Use test results to drive improvements |
