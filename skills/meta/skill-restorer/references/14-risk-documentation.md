# § 7 · Risk Documentation - Full Details

## Risk Matrix

| Risk | Likelihood | Impact | Mitigation Strategy | Early Warning Signs |
|------|------------|--------|---------------------|---------------------|
| **Insufficient Research** | High | High | Minimum 30 min research phase | Generic content, no specific data |
| **Generic Content Persists** | Medium | High | Data validation checklist | "Professional", "expert" terms remain |
| **Scope Creep** | Medium | Medium | Strict phase gates | Exceeding time budgets |
| **Token Budget Overflow** | Low | Medium | Monitor line counts | SKILL.md > 400 lines |
| **Quality Validation Failure** | Low | High | Iterate before delivery | Score < 8.5 after first evaluation |
| **Missing System Prompt** | Medium | Critical | Structural checklist | No §1.1/1.2/1.3 found |
| **Poor Progressive Disclosure** | Medium | Medium | Navigation verification | Broken links, unclear structure |
| **Insufficient Examples** | Medium | High | Example counter | < 5 examples found |

## Quality Checkpoints

### Checkpoint 1: After Architecture (Step 3)

**Verify**:
- [ ] System Prompt architecture complete (§1.1/1.2/1.3)
- [ ] All 6 dimensions planned
- [ ] Research data sufficient (10+ data points)
- [ ] 5 examples outlined
- [ ] 4 SOPs designed

**If Failed**:
- Return to Step 2 (Research) for more data
- Or revise architecture

### Checkpoint 2: After Production (Step 5)

**Verify**:
- [ ] All sections filled (no placeholders)
- [ ] Progressive disclosure correct (SKILL.md < 350 lines)
- [ ] No generic placeholders (search: "professional", "expert")
- [ ] All data validated (cross-referenced)
- [ ] Navigation links working

**If Failed**:
- Return to Step 4 (Structure) to fix organization
- Or add missing content

### Checkpoint 3: After Validation (Step 6)

**Verify**:
- [ ] Evaluator score ≥ 9.0
- [ ] Text score ≥ 8.5
- [ ] Runtime score ≥ 8.5
- [ ] Variance < 1.0
- [ ] All dimensions ≥ 6.0

**If Failed**:
- Identify lowest dimension
- Apply targeted fixes
- Re-run evaluator
- Repeat until thresholds met

## Crisis Response Playbooks

### Scenario 1: Score < 8.0 After First Evaluation

**Trigger**: Evaluator returns score below certification threshold

**Response**:
1. Identify lowest scoring dimension
2. Analyze specific issues
3. Apply targeted fixes
4. Re-run evaluator
5. Repeat until ≥ 8.0

**Common Fixes by Dimension**:
- **System Prompt Low**: Add missing §1.1/1.2/1.3 sections
- **Domain Knowledge Low**: Replace generic terms with specific data
- **Workflow Low**: Add Done/Fail criteria to phases
- **Error Handling Low**: Add risk matrix and anti-patterns
- **Examples Low**: Add 2-3 more detailed scenarios
- **Metadata Low**: Complete YAML frontmatter

### Scenario 2: Generic Content Found After Production

**Trigger**: Review discovers remaining generic terms

**Response**:
1. Search for generic phrases ("professional", "expert", "industry leader")
2. List all occurrences
3. Research specific replacements
4. Replace all instances
5. Re-validate

**Generic Term Search**:
```bash
grep -n "professional\|expert\|industry leader\|best practices" SKILL.md
grep -n "professional\|expert\|industry leader\|best practices" references/*.md
```

### Scenario 3: Scope Creep Detected

**Trigger**: Exceeding time budgets or adding unnecessary content

**Response**:
1. Review original scope
2. Identify scope creep items
3. Defer non-essential items
4. Focus on core requirements
5. Ship v1.0, iterate later

**Time Budget Enforcement**:
- Diagnosis: 15 min max
- Research: 60 min max
- Architecture: 20 min max
- Structure: 15 min max
- Production: 90 min max
- Validation: 30 min max
- Delivery: 10 min max

### Scenario 4: Missing Structural Elements

**Trigger**: Evaluation reveals missing required sections

**Response**:
1. Check System Prompt completeness
2. Verify all 6 dimensions present
3. Add missing sections
4. Fill with appropriate content
5. Re-validate

**Structural Checklist**:
```bash
# Check System Prompt
grep -c "§ 1\.1" SKILL.md  # Should be 1
grep -c "§ 1\.2" SKILL.md  # Should be 1
grep -c "§ 1\.3" SKILL.md  # Should be 1

# Check Workflow
grep -c "Done Criteria" SKILL.md  # Should be ≥ 4
grep -c "Fail Criteria" SKILL.md  # Should be ≥ 4

# Check Examples
grep -c "Example [0-9]" SKILL.md  # Should be ≥ 5

# Check Progressive Disclosure
ls references/*.md | wc -l  # Should be 21
```

## Mitigation Strategies

### Strategy 1: Time-Boxing

Enforce strict time limits for each phase:
- Set timer for each step
- When timer ends, move to next step
- "Good enough" is better than perfect
- Can iterate in future versions

### Strategy 2: Checklist-Driven

Use checklists for every phase:
- Diagnosis Checklist
- Research Checklist
- Architecture Checklist
- Production Checklist
- Validation Checklist

### Strategy 3: Early Validation

Validate early and often:
- Self-assess after each phase
- Run evaluator after Production
- Fix issues immediately
- Don't wait until end

### Strategy 4: Source Discipline

Only use high-quality sources:
- Tier 1: Annual reports, SEC filings, academic papers
- Tier 2: Industry analysis, verified news
- Avoid: Forums, unverified blogs, marketing materials

### Strategy 5: Progressive Disclosure Discipline

Maintain navigation-first structure:
- SKILL.md < 350 lines
- All details in references/
- Test all links
- Regular line count checks
