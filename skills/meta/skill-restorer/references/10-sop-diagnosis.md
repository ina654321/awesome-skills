# SOP 1: Problem Diagnosis

## Purpose

Accurately identify all skill deficiencies and restoration requirements.

## Input

SKILL.md file (the skill to be diagnosed)

## Output

Diagnosis Report with specific fix targets

## Process

### Step 1: Read Complete File (5 min)

Read the entire SKILL.md from start to finish. Don't skim.

**What to Notice**:
- Overall structure
- Section completeness
- Content depth
- Tone and voice

### Step 2: Check System Prompt (5 min)

Verify §1.1, §1.2, §1.3 exist and are complete.

**Checklist**:
```bash
# Search for sections
grep -n "§ 1\.1" SKILL.md
grep -n "§ 1\.2" SKILL.md
grep -n "§ 1\.3" SKILL.md

# Check for key elements
grep -i "identity" SKILL.md | head -5
grep -i "framework" SKILL.md | head -5
grep -i "thinking" SKILL.md | head -5
```

**Missing Element Log**:
- [ ] §1.1 not found
- [ ] §1.1 Identity incomplete
- [ ] §1.2 not found
- [ ] §1.2 Framework incomplete
- [ ] §1.3 not found
- [ ] §1.3 Patterns incomplete

### Step 3: Identify Generic Content (10 min)

Search for and catalog all generic phrases.

**Generic Phrase List**:
- "professional consultant"
- "industry leader"
- "20+ years experience"
- "best practices"
- "expert knowledge"
- "world-class"
- "cutting-edge"
- "innovative"

**Catalog Template**:
```
| Line | Generic Phrase | Should Be |
|------|----------------|-----------|
| 45 | "industry leader" | "#1 market share, 40%" |
| 67 | "best practices" | "Clean Code, TDD" |
```

### Step 4: Assess Current Score (5 min)

Use the scoring rubric to estimate current quality.

**Quick Score Estimator**:

| Dimension | Weight | Check | Score |
|-----------|--------|-------|-------|
| System Prompt | 20% | Has §1.1/1.2/1.3? | 0-20 |
| Domain Knowledge | 20% | Has specific data? | 0-20 |
| Workflow | 20% | Has Done/Fail? | 0-20 |
| Error Handling | 15% | Has risk matrix? | 0-15 |
| Examples | 15% | Has 5+ detailed? | 0-15 |
| Metadata | 10% | YAML complete? | 0-10 |
| **Total** | 100% | | **0-100** |

**Convert to 10-point scale**: Total / 10

### Step 5: Define Fix Targets (5 min)

Based on diagnosis, define what needs to be fixed.

**Fix Priority Matrix**:

| Priority | Issue | Impact | Fix |
|----------|-------|--------|-----|
| P0 | Missing §1.1/1.2/1.3 | -2.0 | Create standard sections |
| P0 | No specific data | -2.0 | Research and add |
| P1 | < 3 examples | -1.5 | Add to 5 |
| P1 | No Done/Fail | -1.5 | Add criteria |
| P2 | Flat structure | -0.5 | Progressive disclosure |

## Deliverable: Diagnosis Report

```markdown
# Diagnosis Report: [skill-name]

## Current State
- Estimated Score: X.X/10
- Quality Level: [Production/Certified/Outstanding/Exemplary]

## Structural Issues
- [ ] List of missing structural elements

## Content Issues
- [ ] List of generic content to replace

## Fix Plan
1. [Priority 0] Fix structural issues → +X.X points
2. [Priority 1] Add domain data → +X.X points
3. [Priority 2] Improve examples → +X.X points

## Target
- Target Score: 9.5/10
- Estimated Time: X hours
```
