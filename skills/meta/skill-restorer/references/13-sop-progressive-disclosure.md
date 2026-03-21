# SOP 4: Progressive Disclosure Setup

## Purpose

Create navigation-first structure for optimal token usage.

## Input

Architecture Blueprint

## Output

Structural framework with SKILL.md and references/

## Process

### Step 1: Create SKILL.md Skeleton (10 min)

```yaml
---
name: [skill-name]
description: '[One-line description]'
license: MIT
metadata:
  author: [name]
  version: 1.0.0
  updated: '[date]'
  tags: [tag1, tag2, tag3]
  category: [category]
  difficulty: [level]
  score: 9.5/10
  quality: exemplary
  text_score: 9.5
  runtime_score: 9.5
  variance: 0.0
---

# [Skill Title]

## One-Liner

[Compelling one-line description]

---

## § 1 · System Prompt

### § 1.1 · Identity & Worldview

[Summary - 100 lines max]

📄 **Details**: [references/01-identity-worldview.md](references/01-identity-worldview.md)

### § 1.2 · Decision Framework

[Summary - 50 lines max]

📄 **Details**: [references/02-decision-framework.md](references/02-decision-framework.md)

### § 1.3 · Thinking Patterns

[Table of patterns]

📄 **Details**: [references/03-thinking-patterns.md](references/03-thinking-patterns.md)
```

### Step 2: Create references/ Directory (5 min)

Create 21 reference files:

```bash
mkdir -p references/
touch references/01-identity-worldview.md
touch references/02-decision-framework.md
touch references/03-thinking-patterns.md
touch references/04-problem-signature.md
touch references/05-layer1-xxx.md
touch references/06-layer2-xxx.md
touch references/07-layer3-xxx.md
touch references/08-domain-knowledge.md
touch references/09-decision-frameworks.md
touch references/10-sop-xxx.md
touch references/11-sop-xxx.md
touch references/12-sop-xxx.md
touch references/13-sop-xxx.md
touch references/14-risk-documentation.md
touch references/15-workflow-phases.md
touch references/16-example-xxx.md
touch references/17-example-xxx.md
touch references/18-example-xxx.md
touch references/19-example-xxx.md
touch references/20-example-xxx.md
touch references/21-anti-patterns.md
```

### Step 3: Add Navigation Links (5 min)

Every section in SKILL.md should link to references/.

**Pattern**:
```markdown
## § X · Section Name

[Summary content - key points only]

📄 **Full Details**: [references/XX-file-name.md](references/XX-file-name.md)
```

### Step 4: Verify Structure (5 min)

**Checks**:
- [ ] SKILL.md < 350 lines
- [ ] 21 reference files exist
- [ ] All sections have links
- [ ] File naming is consistent

## Deliverable: Structural Framework

```
skill-name/
├── SKILL.md (skeleton with navigation)
└── references/
    ├── 01-identity-worldview.md (empty)
    ├── 02-decision-framework.md (empty)
    └── ... (19 more empty files)
```
