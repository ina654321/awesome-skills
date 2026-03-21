# Lite Tier — Tool Skills

**Scope:** Single utility | **Lines:** 50-150 | **Time:** 30 min | **Score:** 5.0-6.5

---

## 5-Section Structure

1. **System Prompt** — Single task, clear I/O
2. **Quick Start** — Install + one-liner usage
3. **Capabilities** — What it does/doesn't
4. **Usage Examples** — 2-3 concrete I/O pairs
5. **Script** — External code (optional)

---

## 30-Min Flow

```
Min 0-5:   System Prompt → "You are X. Input Y, Output Z"
Min 5-10:  Quick Start → Install + usage
Min 10-15: Capabilities → 3 does, 2 doesn't
Min 15-25: Examples → 2-3 I/O pairs
Min 25-30: Polish → <150 lines, YAML valid
```

---

## Checklist

- [ ] One problem only
- [ ] 2-3 working examples
- [ ] <150 lines
- [ ] Code in scripts/ (not inline)

---

## Template

```markdown
---
name: {tool-name}
description: "{One-liner}. Triggers: '{keyword}'"
---

# {Name}

## System Prompt
You are a {tool} that {purpose}. Input: {X}, Output: {Y}.

## Quick Start
Install: `cp SKILL.md .agents/skills/{name}/`
Usage: "{example command}"

## Capabilities
✓ {Function 1}
✓ {Function 2}
✗ {Out of scope}

## Examples
Input: "{request}"
Output: {result}
```

---

**Lines:** 50-150 | **Template:** `assets/TEMPLATE-lite.md`
