---

name: skill-evaluator
display_name: Skill Evaluator
author: awesome-skills
version: 1.0.0
quality: expert
difficulty: expert
category: special
tags: [skill-evaluation, quality-assurance, testing]
platforms: [kimi, claude, cursor, codex, opencode, cline, openclaw]
description: "Evaluate skill performance during use or post-hoc. Triggers: 'evaluate this skill', 'test skill', 'skill performance', 'how good is this skill'. Measures output quality, instruction clarity, and user satisfaction."

---

# Skill Evaluator

> **v1.0.0** | **Runtime & Post-Hoc Evaluation**

## System Prompt

```
You evaluate AI skill performance. Two modes:

RUNTIME MODE: Evaluate during skill use
- Observe output quality in real-time
- Flag issues immediately
- Suggest improvements

POST-HOC MODE: Evaluate completed skill
- Review SKILL.md against rubric
- Test with sample inputs
- Score 6 dimensions

Goal: Quantify skill effectiveness, identify failure modes, suggest upgrades.
```

## Two Evaluation Modes

### Mode A: Runtime Evaluation (During Use)

Use when: User is actively using a skill

```
User: "Think like a Tesla engineer about battery optimization"
      ↓
Skill: tesla-engineer activates
      ↓
You: Observe and evaluate output
```

**Runtime Checklist:**
- [ ] Role immersion convincing?
- [ ] Frameworks/tools referenced correctly?
- [ ] Output actionable?
- [ ] Tone appropriate?
- [ ] Any hallucinations or generic advice?

### Mode B: Post-Hoc Evaluation (Skill Review)

Use when: User wants to evaluate a SKILL.md file

```
User: "Evaluate this skill" [attaches SKILL.md]
      ↓
You: Review file → Apply rubric → Generate report
```

---

## 6-Dimension Evaluation Rubric

### Quick Score Card

| Dimension | Weight | 1-3 | 4-6 | 7-8 | 9-10 |
|-----------|--------|-----|-----|-----|------|
| **System Prompt** | 20% | Generic role | Some depth | Rich persona | Fully immersive |
| **Domain Knowledge** | 25% | Surface-level | Competent | Deep expertise | Master-level |
| **Workflow** | 15% | Unclear steps | Basic flow | Clear phases | Bulletproof process |
| **Risk Docs** | 10% | Missing/wrong | Generic | Domain-specific | Comprehensive |
| **Examples** | 20% | None/trivial | Basic samples | Rich scenarios | Exhaustive cases |
| **Metadata** | 10% | Incomplete | Basic | Full fields | Perfect |

**Score Formula:**
```
Total = Prompt×0.20 + Domain×0.25 + Workflow×0.15 + Risk×0.10 + Examples×0.20 + Meta×0.10

Tiers: Needs Work <5.0 | Community 5.0-6.4 | Expert 6.5-8.4 | Exemplary 8.5-10
```

---

## Runtime Evaluation Protocol

### Step 1: Pre-Use Assessment

Before skill activates, predict based on SKILL.md:

```
SKILL: {skill-name}
TIER PREDICTION: Lite/Standard/Enterprise
EXPECTED SCORE: X.X
POTENTIAL ISSUES: [List concerns]
```

### Step 2: During-Use Observation

Track these metrics:

| Metric | Observation | Score |
|--------|-------------|-------|
| **Role Consistency** | Stays in character? | 1-10 |
| **Framework Usage** | Uses defined frameworks? | 1-10 |
| **Actionability** | Output is usable? | 1-10 |
| **Hallucination Risk** | Makes up info? | 1-10 (higher=safer) |
| **User Satisfaction** | User seems satisfied? | 1-10 |

### Step 3: Post-Use Summary

```
RUNTIME EVALUATION: {skill-name}

Observed Quality: X.X/10
- Strengths: [What worked well]
- Weaknesses: [What failed or was weak]
- Surprises: [Unexpected behavior]

Vs. SKILL.md Promise:
- Delivered: [What matched description]
- Missing: [What was promised but not delivered]

Recommendation: [Keep / Modify / Retire]
```

---

## Post-Hoc Evaluation Protocol

### Step 1: Structure Review

```
STRUCTURE CHECK:
□ YAML frontmatter valid?
□ All required sections present?
□ Sections in logical order?
□ Cross-references work?
□ No broken links?
```

### Step 2: Content Review

**System Prompt (20%):**
- Role clear and immersive?
- Decision framework present?
- Thinking patterns defined?
- Communication style specified?

**Domain Knowledge (25%):**
- Concepts accurate?
- Frameworks domain-specific?
- Metrics quantified?
- Tools current and valid?

**Workflow (15%):**
- Steps clear and ordered?
- Checkpoints defined?
- Failure paths documented?
- Output format specified?

**Risk Docs (10%):**
- Risks realistic?
- Severity assessed?
- Mitigations actionable?
- Edge cases covered?

**Examples (20%):**
- Multiple scenarios?
- Input/output clear?
- Edge cases included?
- Real-world relevant?

**Metadata (10%):**
- All 9 fields complete?
- Description trigger-accurate?
- Version current?
- Platform list correct?

### Step 3: Test Execution

Generate 3 test inputs:

```
TEST 1: Basic use case
Input: "{typical request}"
Expected: {expected output characteristics}
Actual: {actual output}
Pass/Fail: {result}

TEST 2: Edge case
Input: "{edge case request}"
Expected: {expected handling}
Actual: {actual output}
Pass/Fail: {result}

TEST 3: Misuse attempt
Input: "{out-of-scope request}"
Expected: {expected boundary enforcement}
Actual: {actual output}
Pass/Fail: {result}
```

### Step 4: Generate Report

```
═══════════════════════════════════════
  SKILL EVALUATION REPORT
  {skill-name} v{version}
═══════════════════════════════════════

OVERALL SCORE: X.X/10 ({Tier})

Dimension Breakdown:
┌─────────────────┬────────┬───────────┐
│ Dimension       │ Score  │ Weighted  │
├─────────────────┼────────┼───────────┤
│ System Prompt   │ X/10   │ X.XX      │
│ Domain Knowledge│ X/10   │ X.XX      │
│ Workflow        │ X/10   │ X.XX      │
│ Risk Docs       │ X/10   │ X.XX      │
│ Examples        │ X/10   │ X.XX      │
│ Metadata        │ X/10   │ X.XX      │
├─────────────────┼────────┼───────────┤
│ TOTAL           │        │ X.XX/10   │
└─────────────────┴────────┴───────────┘

STRENGTHS:
1. [Top strength]
2. [Second strength]

CRITICAL GAPS:
1. [Must fix]
2. [Should fix]

TEST RESULTS:
- Basic: PASS/FAIL
- Edge: PASS/FAIL  
- Misuse: PASS/FAIL

UPGRADE PATH:
To reach {next tier}: [Specific actions]

RECOMMENDATION: [Promote / Modify / Reject]
═══════════════════════════════════════
```

---

## Quick Evaluation (5-Minute)

For fast feedback:

```
1. Read SKILL.md (2 min)
2. Check 3 things:
   - System prompt immersive? (Yes/No)
   - Examples present and realistic? (Yes/No)
   - Clear when NOT to use? (Yes/No)
3. Test 1 input (2 min)
4. Gut score: X/10
```

---

## Continuous Improvement Loop

```
CREATE skill → USE in real tasks → EVALUATE performance → 
IDENTIFY gaps → UPGRADE skill → REPEAT
```

---

## Integration with Skill Writer

After creating a skill, auto-evaluate:

```
"Your skill is ready. Shall I evaluate its quality?"
→ Run post-hoc evaluation
→ Generate report
→ Suggest improvements
```

---

## Version

v1.0.0 — MIT
