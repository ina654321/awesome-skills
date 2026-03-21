# § 5 · Validation Framework - Full Details

## skill-evaluator v2.1 Assessment

### Evaluation Dimensions

**Text Quality (50% of total score)**:

| Dimension | Weight | What to Check |
|-----------|--------|---------------|
| System Prompt | 20% | §1.1 Identity, §1.2 Framework, §1.3 Thinking |
| Domain Knowledge | 20% | Specific data, methodologies, benchmarks |
| Workflow | 20% | Phases, Done/Fail criteria, gates |
| Error Handling | 15% | Anti-patterns, risk matrix, playbooks |
| Examples | 15% | Realism, variety, detail |
| Metadata | 10% | YAML completeness |

**Runtime Quality (50% of total score)**:

| Dimension | What to Check |
|-----------|---------------|
| Role Immersion | Believable, consistent persona |
| Framework Execution | Correct application of frameworks |
| Output Actionability | Usable, practical results |
| Knowledge Accuracy | Factually correct information |
| Long-Conversation Stability | Consistent over time |
| Resilience | Handles edge cases gracefully |

### Scoring Scale

| Score | Quality Level | Description |
|-------|---------------|-------------|
| 9.5-10 | EXEMPLARY | Reference implementation |
| 8.5-9.4 | OUTSTANDING | Production-ready, excellent |
| 8.0-8.4 | CERTIFIED | Meets all requirements |
| 7.0-7.9 | PRODUCTION | Acceptable, some gaps |
| 6.0-6.9 | DEVELOPMENT | Needs significant work |
| < 6.0 | INADEQUATE | Major reconstruction needed |

### Certification Requirements

**Must Meet All**:
- Text Score ≥ 8.0
- Runtime Score ≥ 8.0
- Variance < 1.0
- All dimensions ≥ 6.0

**Quality Levels**:
- CERTIFIED: Meets minimums
- EXEMPLARY: Scores ≥ 9.5, variance < 0.5

### Evaluation Process

**Step 1: Self-Assessment**

Rate your skill before external evaluation:

```markdown
## Self-Assessment

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| System Prompt | | |
| Domain Knowledge | | |
| Workflow | | |
| Error Handling | | |
| Examples | | |
| Metadata | | |
| **Text Total** | | |

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| Role Immersion | | |
| Framework Execution | | |
| Output Actionability | | |
| Knowledge Accuracy | | |
| Long-Conversation Stability | | |
| Resilience | | |
| **Runtime Total** | | |

**Self-Estimated Overall**: ___/10
```

**Step 2: External Evaluation**

Run skill-evaluator v2.1:

```markdown
## Evaluator Results

**Text Quality**: ___/10
**Runtime Quality**: ___/10
**Variance**: ___
**Certified**: Yes/No
```

**Step 3: Gap Analysis**

Compare self vs external:

```markdown
## Gap Analysis

| Dimension | Self | External | Gap | Action |
|-----------|------|----------|-----|--------|
| | | | | |
```

**Step 4: Improvement**

If score < 9.0:
1. Identify lowest scoring dimension
2. Apply targeted fixes
3. Re-run evaluator
4. Repeat until target met

### Common Issues and Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Low System Prompt | Missing §1.1/1.2/1.3 | Add standard sections |
| Low Domain Knowledge | Generic content | Research and add specifics |
| Low Workflow | No Done/Fail | Add criteria to phases |
| Low Error Handling | Missing anti-patterns | Document 6-10 patterns |
| Low Examples | < 5 scenarios | Add detailed examples |
| Low Metadata | Incomplete YAML | Fill all fields |

### Evaluation Report Template

```markdown
# Evaluation Report: [skill-name]

## Executive Summary

| Metric | Score | Status |
|--------|-------|--------|
| Overall | | |
| Text | | |
| Runtime | | |
| Variance | | |

## Text Quality Assessment

[Dimension-by-dimension breakdown]

## Runtime Quality Assessment

[Dimension-by-dimension breakdown]

## Gap Analysis

[Self vs External comparison]

## Recommendations

[Specific fixes]

## Certification

**Status**: [Certified/Not Certified]
```
