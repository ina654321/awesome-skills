# § 10 · Anti-Patterns - Full Details

## Restoration Anti-Patterns

### Anti-Pattern 1: Template Addiction

**Symptom**:
- Copying structure without understanding domain
- Filling in blanks mechanically
- Same structure for every skill
- No domain-specific adaptation

**Consequence**:
- Skills feel generic
- Content doesn't fit domain
- Low evaluator scores
- Wasted effort

**Solution**:
- Research domain FIRST
- Understand unique aspects
- Adapt structure to domain
- Write content that fits

**Example**:
```
❌ Wrong:
"As a [Role] consultant with 20+ years experience..."
(Used for every skill)

✅ Right:
"As a Cell Producer at Supercell, leading 5-15 person 
autonomous teams using the Finnish cell methodology..."
(Specific to domain)
```

---

### Anti-Pattern 2: Generic Content

**Symptom**:
- "Professional", "expert", "industry leader"
- No specific numbers
- No named methodologies
- Could apply to any domain

**Consequence**:
- Loses 2.0+ points on evaluator
- Content feels hollow
- Users don't trust advice
- Skill fails certification

**Solution**:
- Replace every generic term
- Find specific data
- Name real companies
- Use actual metrics

**Generic → Specific Transformations**:

| Generic | Specific |
|---------|----------|
| "20+ years experience" | "Tsinghua NLP lab, 200K+ context window" |
| "Industry leader" | "Clash of Clans generated $10B+ revenue" |
| "Best practices" | "Clean Code, TDD, CI/CD" |
| "Expert consultant" | "Former Pixar Story Artist, 15 films" |
| "Professional methodology" | "Cell structure, 90% kill rate" |

---

### Anti-Pattern 3: Missing System Prompt

**Symptom**:
- No §1.1 Identity & Worldview
- No §1.2 Decision Framework
- No §1.3 Thinking Patterns
- Or sections exist but are empty/generic

**Consequence**:
- Quality ceiling at 7.0
- Automatic -2.0 points
- Skill cannot reach EXEMPLARY
- Runtime quality suffers

**Solution**:
- ALWAYS create §1.1/1.2/1.3
- Fill with domain-specific content
- Make them substantial (100+ lines each in references)
- Verify with evaluator

---

### Anti-Pattern 4: Flat Structure

**Symptom**:
- All content in one file
- 2000+ line SKILL.md
- No progressive disclosure
- Hard to navigate

**Consequence**:
- Poor user experience
- High token costs
- Difficult to maintain
- Overwhelming to read

**Solution**:
- SKILL.md < 350 lines
- references/ for details
- 1:10 navigation-to-content ratio
- Clear navigation links

**Structure Comparison**:

```
❌ Flat Structure (Anti-Pattern):
SKILL.md (2000 lines)
├── Everything crammed in one file
├── Hard to find specific info
├── Expensive to process
└── Poor UX

✅ Progressive Disclosure:
SKILL.md (350 lines)
├── Overview and navigation
├── Quick reference
└── Links to details

references/ (3000+ lines)
├── Detailed content
├── Deep dives
└── Full examples
```

---

### Anti-Pattern 5: Insufficient Examples

**Symptom**:
- Only 1-2 examples
- Examples are generic
- No realistic data
- Don't cover edge cases

**Consequence**:
- Loses 1.5+ points
- Users can't see how to apply skill
- Runtime quality suffers
- Skill feels theoretical

**Solution**:
- Minimum 5 detailed examples
- Cover different scenario types
- Use realistic data
- Include edge cases

**Example Scenario Types**:
1. **Standard Case**: Typical usage
2. **Complex Case**: Multiple variables
3. **Edge Case**: Unusual situation
4. **Error Case**: Problem resolution
5. **Ethics Case**: Value judgment

---

### Anti-Pattern 6: No Validation

**Symptom**:
- Assuming quality without checking
- Skipping evaluator
- "Good enough" mentality
- No iteration

**Consequence**:
- Unknown actual quality
- May fail certification
- Wasted effort if rejected
- Lower standard than possible

**Solution**:
- ALWAYS run skill-evaluator
- Target 9.5/10 EXEMPLARY
- Iterate if score < 9.0
- Document evaluation results

---

### Anti-Pattern 7: Scope Creep

**Symptom**:
- Adding more and more content
- Never-ending research
- Perfectionism paralysis
- Missing deadlines

**Consequence**:
- Restoration never completes
- Diminishing returns
- Budget/time overrun
- Skill not delivered

**Solution**:
- Time-box each step
- "Good enough" for 9.5/10
- Don't aim for perfection
- Deliver and iterate

**Time Budgets**:
- Step 1 (Diagnosis): 15 min
- Step 2 (Research): 30-60 min
- Step 3 (Architecture): 20 min
- Step 4 (Structure): 15 min
- Step 5 (Content): 60-90 min
- Step 6 (Validation): 15-30 min
- Step 7 (Delivery): 10 min
- **Total: 2.5-4 hours**

---

### Anti-Pattern 8: Wrong Source Quality

**Symptom**:
- Using Wikipedia as primary source
- Anonymous forums
- Marketing materials
- Unverified blogs

**Consequence**:
- Inaccurate data
- Lower credibility
- Potential factual errors
- Reduced evaluator score

**Solution**:
- Tier 1 sources: Annual reports, SEC filings, academic papers
- Tier 2 sources: Industry analysis, verified news
- Cross-reference everything
- Cite sources

---

## Quality Checklist

Before declaring restoration complete, verify:

- [ ] No generic phrases remaining
- [ ] System Prompt has §1.1/1.2/1.3
- [ ] 5+ detailed examples
- [ ] Progressive disclosure correct
- [ ] Evaluator score ≥ 9.0
- [ ] All data verified
- [ ] File structure correct
- [ ] EVALUATION_REPORT.md saved
