# Example 1: Enterprise Skill Repair

## Context

**Skill**: supercell-cell-producer
**Starting Score**: 5.7/10
**Target Score**: 9.5/10
**Domain**: Game production (Supercell methodology)

## Original State Analysis

### Structural Issues
- ❌ Missing §1.1 Identity (had generic "Professional Consultation")
- ❌ Missing §1.2 Decision Framework
- ❌ Missing §1.3 Thinking Patterns

### Content Issues
- ❌ Generic phrases: "industry leader", "professional consultant"
- ❌ No specific Supercell data
- ❌ No real metrics (D1 retention, etc.)
- ❌ Hollow examples

### Workflow Issues
- ❌ Generic workflow without Done/Fail criteria
- ❌ No phase gates

## Restoration Process

### Step 1: Diagnosis (15 min)

```markdown
## Diagnosis Report

### Current State
- Score Estimate: 5.7/10
- Quality Level: Production (barely)

### Structural Issues
- [x] Missing §1.1 Identity & Worldview
- [x] Missing §1.2 Decision Framework  
- [x] Missing §1.3 Thinking Patterns

### Content Issues
- Generic: "Professional Consultation" → Need: Specific Cell methodology
- Generic: "Problem Diagnosis" → Need: Kill/Continue framework
- No data: Missing $8.6B, $10B+, 100M+ DAU

### Fix Plan
1. Research Supercell methodology → +1.0
2. Add System Prompt §1.1/1.2/1.3 → +2.0
3. Add specific data → +1.0
4. Improve examples → +0.5
5. Progressive disclosure → +0.3

Target: 9.5/10
```

### Step 2: Research (45 min)

**Supercell Data Collected**:
```
Founded: 2010, Helsinki, Finland
Acquired: 2016 by Tencent for $8.6B
Employees: ~300 (deliberately small)
Lifetime Revenue: $20B+
DAU: 100M+
Kill Rate: 90%+ of projects killed

Hit Games:
- Clash of Clans: $10B+ lifetime, 10+ years
- Clash Royale: $1B+ first year
- Brawl Stars: $63M first month
- Hay Day: 10+ years operation

Methodology:
- Cell structure: 5-15 people
- Autonomy: Cells decide everything
- Kill culture: Hall of Fail celebrates killed projects
- Metrics: D1>50%, D7>20%, D30>10%
```

### Step 3: Architecture (20 min)

**System Prompt Design**:
- §1.1: Cell Producer identity, Supercell context, $8.6B, ~300 employees
- §1.2: 5-tier decision hierarchy (Player → Long-term → Quality → Team → Business)
- §1.3: 5 thinking patterns (Kill-or-Continue, Constraint-Driven, Data-Informed, LiveOps, Finnish Directness)

### Step 4: Progressive Disclosure (15 min)

**Structure**:
```
supercell-cell-producer/
├── SKILL.md (323 lines)
├── EVALUATION_REPORT.md
└── references/
    ├── 01-identity-worldview.md (7624 bytes)
    ├── 02-decision-framework.md (5750 bytes)
    └── ... (21 files total)
```

### Step 5: Content Production (90 min)

**Key Content**:
- System Prompt with real data
- Domain Knowledge with game metrics
- 5-phase workflow (Concept → Prototype → Vertical Slice → Soft Launch → Global Launch)
- 5 detailed examples (Kill decision, Soft launch analysis, etc.)
- 4 SOPs (Concept, Playtest, Soft Launch, Crisis)
- Risk matrix and anti-patterns

### Step 6: Validation (20 min)

**Evaluator Results**:
```
Text Score: 9.5/10
Runtime Score: 9.5/10
Variance: 0.0
Status: CERTIFIED EXEMPLARY
```

### Step 7: Delivery (10 min)

**Final Stats**:
```
Before: 5.7/10
After: 9.5/10
Improvement: +3.8 points
Files: 23 (SKILL.md + EVALUATION_REPORT.md + 21 references)
Lines: 3,774 total
Time: 3.5 hours
```

## Key Learnings

### What Worked
1. Deep research (45 min) provided authentic data
2. Progressive disclosure kept SKILL.md manageable
3. 5 detailed examples covered key use cases
4. Real metrics made content credible

### Challenges
1. Finding specific Supercell data required multiple sources
2. Balancing detail with readability in references
3. Ensuring all 6 dimensions met high standards

### Results
- ✅ Score improved 5.7 → 9.5 (+3.8)
- ✅ EXEMPLARY quality achieved
- ✅ Certification passed
- ✅ Production-ready skill delivered
