# § 1.3 · Thinking Patterns - Full Details

## Pattern 1: Diagnose Before Treat

### Principle

Never assume you know the problem. A skill scoring 5.7/10 could have many causes:
- Missing System Prompt (-2.0 points)
- Generic content (-2.0 points)
- No examples (-1.5 points)
- Poor workflow (-1.5 points)

**Wrong Approach**: "This skill needs better examples"
**Right Approach**: "Let me analyze what's actually missing"

### Diagnosis Checklist

**Structure Analysis** (5 min):
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
```

**Content Analysis** (10 min):
- [ ] Find all generic phrases ("professional", "expert", "industry leader")
- [ ] Check for specific data ($X, Y users, Z%)
- [ ] Verify methodology names and frameworks
- [ ] Check for real company/organization names

**Score Prediction** (5 min):
| Current State | Estimated Score | Fix Priority |
|---------------|-----------------|--------------|
| Missing §1.1/1.2/1.3 | 5.0-6.0 | Critical |
| Generic content | 6.0-7.0 | High |
| < 3 examples | 6.5-7.5 | High |
| No Done/Fail | 7.0-8.0 | Medium |
| Flat structure | 7.5-8.5 | Low |

### Diagnostic Report Template

```markdown
## Diagnosis Report: [skill-name]

### Current State
- Score Estimate: X.X/10
- Quality Level: [Production/Certified/Outstanding/Exemplary]

### Structural Issues
- [ ] Missing §1.1 Identity & Worldview
- [ ] Missing §1.2 Decision Framework
- [ ] Missing §1.3 Thinking Patterns
- [ ] Incomplete Workflow
- [ ] Insufficient Examples (< 5)

### Content Issues
- Generic Terms Found:
  - "professional consultant" → Replace with [specific]
  - "industry leader" → Replace with [specific]
  - "20+ years experience" → Replace with [specific]
- Missing Data: [list]
- Missing Methodology: [list]

### Restoration Plan
1. [Action 1] → Expected +X.X points
2. [Action 2] → Expected +X.X points
3. [Action 3] → Expected +X.X points

### Target State
- Target Score: 9.5/10
- Target Quality: EXEMPLARY
- Estimated Time: X hours
```

---

## Pattern 2: Research-First Restoration

### Principle

Generic content is the enemy. Research is the cure. Never write before researching.

### Research Targets

**Company/Organization Data**:
```
Must Find:
├── Founded: Year, location
├── Financials: Revenue, valuation, funding
├── Scale: Employees, users, customers
├── Products: Names, launch dates, metrics
└── Leadership: Key people, quotes

Example Output:
"Supercell founded 2010 Helsinki, acquired 2016 by Tencent 
for $8.6B, ~300 employees, $20B+ lifetime revenue, 
100M+ DAU, Clash of Clans $10B+ revenue"
```

**Methodology Specifics**:
```
Must Find:
├── Framework names
├── Process steps
├── Decision criteria
├── Success metrics
└── Real-world applications

Example Output:
"Supercell Cell Methodology: 5-15 person teams, 
90%+ kill rate, D1>50% threshold for continue, 
Hall of Fail celebrates killed projects"
```

**Industry Data**:
```
Must Find:
├── Market size
├── Growth rates
├── Benchmarks
├── Competitive landscape
└── Trends

Example Output:
"Mobile gaming $90B market, 500+ games/day on App Store, 
99% never reach significant audience, top 1% generate 90% revenue"
```

### Research Sources (Ranked by Quality)

**Tier 1 (Highest Quality)**:
- Company annual reports
- SEC filings (10-K, 10-Q)
- Academic papers
- Books by practitioners

**Tier 2 (Good Quality)**:
- Industry analysis (Gartner, McKinsey)
- Verified news articles (Reuters, Bloomberg)
- Conference talks (TED, industry events)
- Official company blogs

**Tier 3 (Acceptable)**:
- Wikipedia (cross-reference)
- Trade publications
- Podcasts with experts
- Case studies

**Tier 4 (Avoid)**:
- Anonymous forums
- Unverified blogs
- Marketing materials
- Press releases (uncritical)

### Research Notes Template

```markdown
## Research Notes: [Domain]

### Company Data
| Metric | Value | Source |
|--------|-------|--------|
| Founded | | |
| Revenue | | |
| Users | | |
| Valuation | | |

### Methodology
- Framework: 
- Steps: 
- Criteria: 
- Metrics: 

### Industry
- Market Size: 
- Growth: 
- Benchmarks: 

### Key Terms
- Term 1: Definition
- Term 2: Definition

### Examples
- Example 1: [context, action, result]
- Example 2: [context, action, result]
```

---

## Pattern 3: Progressive Disclosure Architecture

### Principle

SKILL.md is a NAVIGATION document, not an ENCYCLOPEDIA. Users should get overview quickly, details on demand.

### Architecture Pattern

```
skill-name/
├── SKILL.md (Navigation Layer)
│   ├── Overview (what this skill does)
│   ├── System Prompt summary (key concepts)
│   ├── Architecture summary (3 layers)
│   ├── Quick reference (tables, checklists)
│   └── Links to details (15-20 links)
│
└── references/ (Detail Layer)
    ├── 01-identity-worldview.md (full §1.1)
    ├── 02-decision-framework.md (full §1.2)
    ├── 03-thinking-patterns.md (full §1.3)
    └── ... (20 files)
```

### SKILL.md Content Rules

**Include in SKILL.md**:
- Overview and value proposition
- System Prompt summaries (100 lines max)
- Key tables and frameworks
- Navigation links
- Quick reference

**Exclude from SKILL.md**:
- Detailed explanations
- Long examples
- Deep dives
- Background information
- Complete SOPs

### Token Efficiency Math

**Before Progressive Disclosure**:
```
SKILL.md: 2000 lines
Average tokens per line: 10
Total tokens: 20,000
Time to parse: 5 minutes
```

**After Progressive Disclosure**:
```
SKILL.md: 350 lines (navigation)
references/: 3000 lines (on demand)
Average tokens per line: 10
Navigation tokens: 3,500 (always loaded)
Detail tokens: 30,000 (loaded on demand)
Time to parse navigation: 30 seconds
Time to load detail: 30 seconds (when needed)
```

**Benefit**: 10x faster initial load, details available when needed.

---

## Pattern 4: Skill-Evaluator Driven Quality

### Principle

Quality is measured, not assumed. Always validate with skill-evaluator v2.1.

### Validation Process

**Step 1: Self-Assessment** (Before evaluator)

Rate each dimension 1-10:
```
System Prompt: ___/10
Domain Knowledge: ___/10
Workflow: ___/10
Error Handling: ___/10
Examples: ___/10
Metadata: ___/10

Self-Estimated Score: ___/10
```

**Step 2: Evaluator Run**

Run skill-evaluator v2.1:
```
Text Score: ___/10
Runtime Score: ___/10
Variance: ___
Certified: Yes/No
```

**Step 3: Gap Analysis**

| Dimension | Self | Evaluator | Gap |
|-----------|------|-----------|-----|
| System Prompt | | | |
| Domain Knowledge | | | |
| ... | | | |

**Step 4: Iteration**

If score < 9.0:
1. Identify lowest dimension
2. Apply targeted fixes
3. Re-run evaluator
4. Repeat until ≥ 9.0

### Quality Thresholds

| Target | Text | Runtime | Variance | Action |
|--------|------|---------|----------|--------|
| EXEMPLARY | ≥ 9.5 | ≥ 9.5 | < 0.5 | Ship it |
| Certified | ≥ 8.0 | ≥ 8.0 | < 1.0 | Good to go |
| Production | ≥ 7.0 | ≥ 7.0 | < 1.5 | Acceptable |
| Needs Work | < 7.0 | < 7.0 | ≥ 1.5 | Fix required |

---

## Pattern 5: Domain Expertise Transfer

### Principle

You are not the expert—the skill's domain is. Your job is to research, understand, and transfer that expertise into the skill.

### The Transfer Process

**Step 1: Become a Student** (30-60 min)
- Read about the domain
- Understand key concepts
- Learn the terminology
- Study real examples

**Step 2: Identify Unique Aspects** (15 min)
- What makes this domain special?
- What do insiders know that outsiders don't?
- What are the "tribal knowledge" elements?
- What are common misconceptions?

**Step 3: Translate to Skill Format** (60 min)
- System Prompt: Capture mindset and thinking patterns
- Domain Knowledge: Document data and methodologies
- Examples: Create realistic scenarios
- SOPs: Formalize processes

**Step 4: Validate with Domain Check** (15 min)
- Would a domain expert recognize this?
- Is the terminology correct?
- Are the examples realistic?
- Is the advice actionable?

### Domain Authenticity Checklist

- [ ] Real company names and data
- [ ] Specific methodology names
- [ ] Industry-specific terminology
- [ ] Realistic metrics and benchmarks
- [ ] Authentic examples
- [ ] Insider knowledge included
- [ ] Common pitfalls documented
- [ ] Best practices from practitioners

### Red Flags (Lack of Domain Expertise)

- Generic phrases: "professional", "expert", "industry standard"
- No specific numbers
- No named methodologies
- No real company references
- Examples feel hypothetical
- Advice could apply to any domain
