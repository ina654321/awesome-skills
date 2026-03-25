# Description Optimization Guide

> How to write skill descriptions that trigger reliably — evals-driven methodology.

---

## Why Description Matters

**The Problem**: A skill with perfect rubric scores but poor description will **never activate**. This is a silent failure — the skill exists, it's excellent, but users never see it.

**The Evidence**: skill-creator identifies "undertriggering" as a key issue: "currently Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful."

---

## The Pushy Description Pattern

From skill-creator: "Make descriptions a little bit pushy."

❌ **Passive** (bad): "Helps with skill management"
✅ **Pushy** (good): "Manage the complete AI skill lifecycle. Use when: 'create skill', 'write skill', 'evaluate skill', 'restore skill'"

### Why "Pushy" Works

- Passive descriptions rely on Claude guessing intent
- Pushy descriptions explicitly list trigger phrases
- Users see themselves in the description

---

## The Trigger Rate Problem

| Scenario | Symptom | Impact |
|----------|---------|--------|
| Overly generic | Triggers on unrelated queries | User frustration |
| Too narrow | Never triggers for valid queries | Skill goes unused |
| Passive language | Claude doesn't recognize intent | Inconsistent activation |

---

## Evals-Driven Optimization

### Step 1: Generate 20 Eval Queries

Create a set of 20 queries:
- **10 should trigger** (positive examples) — phrases users would actually type
- **10 should not trigger** (negative examples) — unrelated tasks

**Positive examples** should cover:
- Direct commands: "create a skill", "evaluate my skill"
- Questions: "how do I write a skill?"
- Keywords: "restore", "certify", "score"

**Negative examples** should cover:
- Unrelated tasks: "write code", "explain physics"
- Edge cases: "help me", "do something"

### Step 2: Initial Test

Test the current description against the 20 queries:
- Count how many positive queries trigger
- Count how many negative queries don't trigger

```
Trigger Rate = (correct positives + correct negatives) / 20
```

### Step 3: Iterate

```
Initial: "Helps with skill management"
         → Trigger rate: 45%

Iteration 1: "Manages AI skill lifecycle"
             → Trigger rate: 65%

Iteration 2: "Manage the complete AI skill lifecycle: create, evaluate, restore"
             → Trigger rate: 80%

Iteration 3: "Manage the complete AI skill lifecycle. Use when: 'create skill', 'write skill', 'evaluate skill', 'restore skill', 'score skill'"
             → Trigger rate: 90%
```

### Step 4: Validate

After reaching ≥85%, test on held-out validation set (5 queries).

---

## Description Anatomy

### Structure

```
<What it does> — <Use when: trigger phrases>
```

### Components

| Component | Purpose | Example |
|-----------|---------|---------|
| Main verb | Core capability | "Manage", "Create", "Analyze" |
| Domain | What field | "AI skill lifecycle" |
| Trigger phrases | User query examples | "Use when: 'create skill'" |

### Template

```yaml
description: >
  [What it does]. 
  Use when: [phrase 1], [phrase 2], [phrase 3], ...
```

---

## Common Patterns

### Pattern 1: Verb Forward

Start with the primary action verb.

| Bad | Good |
|-----|------|
| "A skill for..." | "Create..." |
| "Provides the ability to..." | "Evaluate..." |
| "Helps with..." | "Restore..." |

### Pattern 2: Explicit Triggers

End with concrete phrases users will type:

```
Use when: "create skill", "write skill", "build skill"
Use when: "evaluate skill", "test skill", "score skill"
Use when: "restore skill", "fix skill", "improve skill"
```

### Pattern 3: Context Examples

Include specific contexts:

```
Use when: user wants to create a new skill from scratch
Use when: user asks to evaluate existing skill quality
Use when: user has a poorly performing skill that needs fixing
```

---

## Testing Checklist

```
[ ] 20 queries generated (10 positive, 10 negative)
[ ] Initial trigger rate recorded
[ ] Description iterated ≥ 3 times
[ ] Final trigger rate ≥ 85%
[ ] Validation set (5 queries) tested
[ ] No false positives on negative examples
[ ] All positive examples still trigger
```

---

## Tools

| Script | Purpose |
|--------|---------|
| `scripts/optimize.sh` | Interactive description optimization |

---

## Reference

- skill-creator: "Make descriptions a little bit pushy"
- agentskills spec: Description field ≤ 1024 chars
