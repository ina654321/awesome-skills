# § 1.2 · Decision Framework - Full Details

## The Restoration Priority Hierarchy

### 1. Structural Integrity (Priority 1)

**Impact**: Accounts for 20% of total score
**Consequence of Missing**: Quality ceiling at 7.0

**Requirements**:
- §1.1 Identity & Worldview: Professional DNA, context, success metrics
- §1.2 Decision Framework: Hierarchy, gates, boundaries
- §1.3 Thinking Patterns: Minimum 3 distinct patterns

**Validation**:
```bash
grep -c "§ 1\.1" SKILL.md  # Should be 1
grep -c "§ 1\.2" SKILL.md  # Should be 1
grep -c "§ 1\.3" SKILL.md  # Should be 1
```

### 2. Domain Authenticity (Priority 2)

**Impact**: Accounts for 20% of total score
**Consequence of Generic**: Loses 2.0+ points

**Transformation Rules**:

| Generic (Bad) | Specific (Good) |
|---------------|-----------------|
| "20+ years experience" | "Tsinghua NLP lab, 200K+ context window" |
| "Industry leader" | "Clash of Clans generated $10B+ revenue" |
| "Professional methodology" | "Cell structure: 5-15 people, 90% kill rate" |
| "Expert consultant" | "Former Pixar story artist, 15+ films" |
| "Best practices" | "Kill-or-Continue framework, D1>50% threshold" |

**Research Sources**:
- Company annual reports
- Industry analysis (App Annie, Sensor Tower)
- Academic papers
- Books by domain experts
- Interview transcripts

### 3. Workflow Clarity (Priority 3)

**Impact**: Accounts for 20% of total score
**Consequence of Vague**: Loses 1.5+ points

**Requirements**:
- 4-5 distinct phases
- Each phase has Done Criteria
- Each phase has Fail Criteria
- Clear gates between phases

**Example Structure**:
```markdown
### Phase X: Name

**Objective**: Clear, measurable goal

**Key Activities**:
1. Specific action
2. Specific action
3. Specific action

**✓ Done Criteria**:
- [ ] Measurable criterion 1
- [ ] Measurable criterion 2

**✗ Fail Criteria**:
- [ ] Observable failure 1
- [ ] Observable failure 2
```

### 4. Example Richness (Priority 4)

**Impact**: Accounts for 15% of total score
**Consequence of Sparse**: Loses 1.5+ points

**Requirements**:
- Minimum 5 detailed scenarios
- Cover different use cases
- Include edge cases
- Realistic data and outcomes

**Scenario Types**:
1. **Standard Case**: Typical usage
2. **Complex Case**: Multiple variables
3. **Edge Case**: Unusual situation
4. **Error Case**: Problem resolution
5. **Ethics Case**: Value judgment

### 5. Token Efficiency (Priority 5)

**Impact**: User experience, maintainability
**Consequence of Poor**: Hard to use, expensive to process

**Progressive Disclosure Standard**:

```
SKILL.md: < 350 lines
├── Overview (50 lines)
├── System Prompt summary (100 lines)
├── Three-Layer Architecture summary (50 lines)
├── Key frameworks (100 lines)
└── Navigation links (50 lines)

references/: 3000+ lines
├── 01-identity-worldview.md (500 lines)
├── 02-decision-framework.md (400 lines)
├── 03-thinking-patterns.md (600 lines)
├── ... (20 files)
└── 21-anti-patterns.md (500 lines)
```

## Quality Gates

### Gate 1: Diagnosis Complete

**Criteria**:
- [ ] Current score identified
- [ ] Missing sections documented
- [ ] Generic content catalogued
- [ ] Fix scope defined

**Fail Actions**:
- Cannot identify issues → Request user clarification
- Scope unclear → Expand diagnosis

### Gate 2: Research Sufficient

**Criteria**:
- [ ] Specific data collected (10+ data points)
- [ ] Methodology documented
- [ ] Key terminology identified
- [ ] Real-world examples found

**Fail Actions**:
- Insufficient data → Continue research
- Generic sources only → Find better sources

### Gate 3: Architecture Complete

**Criteria**:
- [ ] System Prompt structure designed
- [ ] All 6 dimensions planned
- [ ] Progressive disclosure mapped
- [ ] 5 examples outlined

**Fail Actions**:
- Missing sections → Revise architecture
- Structure unclear → Redesign

### Gate 4: Structure Ready

**Criteria**:
- [ ] SKILL.md skeleton created
- [ ] references/ directory ready
- [ ] Navigation links working
- [ ] File naming consistent

**Fail Actions**:
- Navigation unclear → Restructure
- Links broken → Fix references

### Gate 5: Content Complete

**Criteria**:
- [ ] All sections filled
- [ ] No placeholder text
- [ ] No generic terms remaining
- [ ] Data validated

**Fail Actions**:
- Generic content found → Replace with specifics
- Missing sections → Add content

### Gate 6: Quality Verified

**Criteria**:
- [ ] Evaluator score ≥ 9.0
- [ ] Text score ≥ 8.5
- [ ] Runtime score ≥ 8.5
- [ ] Variance < 1.0

**Fail Actions**:
- Score < 9.0 → Iterate improvements
- Variance high → Check consistency

### Gate 7: Delivery Ready

**Criteria**:
- [ ] EVALUATION_REPORT.md saved
- [ ] File structure verified
- [ ] Improvements documented
- [ ] Ready for handoff

**Fail Actions**:
- Missing files → Complete deliverables
- Structure wrong → Fix organization
