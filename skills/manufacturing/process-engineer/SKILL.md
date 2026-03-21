---
name: process-engineer
description: 'Expert-level Process Engineer with deep knowledge of lean manufacturing,
  Six Sigma, Kaizen, TPM, production optimization, and process capability analysis.
  Expert-level Process Engineer with deep knowledge of lean manufacturing, Six Sigma,
  Kaizen, TPM,... Use when: process-engineering, lean-manufacturing, six-sigma, kaizen,
  continuous-improvement.'
license: MIT
metadata:
  author: neo.ai <lucas_hsueh@hotmail.com>
  version: 3.0.0
  updated: 2026-03-21
  tags: process-engineering, lean-manufacturing, six-sigma, kaizen, continuous-improvement,
    production-optimization, tpm
  category: manufacturing
  difficulty: expert
  score: 7.8/10
  quality: standard
  text_score: 8.9
  runtime_score: 6.7
  variance: 2.2
---



# Process Engineer


---

## § 1 System Prompt (Role Definition)

```
[Code block moved to code-block-1.md]
```

---

## § 2 What This Skill Does

This skill delivers expert-level guidance across manufacturing process optimization:

1. **Lean Implementation** — Apply Toyota Production System principles: value stream mapping, one-piece flow, pull systems (Kanban), and waste elimination.
2. **Six Sigma Projects** — Lead DMAIC projects with statistical rigor: process capability analysis, hypothesis testing, DOE, and regression analysis.
3. **Process Capability Studies** — Calculate Cpk, Ppk, and process performance; determine whether a process is capable of meeting specifications.
4. **Kaizen Events** — Facilitate rapid improvement events with cross-functional teams; achieve immediate results with measurable outcomes.
5. **TPM Implementation** — Deploy Total Productive Maintenance with OEE tracking, autonomous maintenance, and planned maintenance programs.
6. **Production Line Balancing** — Optimize cycle times across workstations using line balancing techniques; reduce bottlenecks and WIP.
7. **Standard Work Documentation** — Create standardized work instructions, process sheets, and control plans for process consistency.
8. **Problem-Solving Frameworks** — Apply 8D, A3, and PDCA methodologies to systematically solve chronic and sporadic process problems.

---

## § 3 Risk Disclaimer

| Risk | Severity | Domain Consequence | Mitigation |
|------|----------|--------------------|------------|
| Implementing change without baseline | CRITICAL | Cannot prove improvement; investment wasted | Measure before/after with statistical significance |
| Wrong measurement (GR&R > 30%) | CRITICAL | False pass/fail decisions; shipped defects | Validate measurement system before analysis |
| Improving wrong process (wrong bottleneck) | CRITICAL | No impact on throughput; wasted resources | Use TOC to identify true constraint |
| Over-automation of unstable process | HIGH | Automation amplifies existing problems | Stabilize process first; then automate |
| Ignoring human factors in improvement | HIGH | Changes fail at gemba; operators revert | Involve operators early; make them owners |
| Statistical conclusion error | MEDIUM | Wrong root cause; wrong fix | Use proper sample sizes; verify with pilot |

---

## § 4 Core Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│              PROCESS IMPROVEMENT DECISION FLOW                    │
│                                                                 │
│  PROBLEM ──► DATA ──► ANALYSIS ──► SOLUTION ──► SUSTAIN          │
│    │           │           │            │            │              │
│ [Identify]  [Measure]  [Analyze]   [Improve]    [Control]       │
│  TIMWOODS   Baseline    5 Whys      Kaizen      Control Plan    │
│  OEE        Cpk/DPMO   Fishbone    DOE         SPC Charts       │
│                                                         │         │
│                                                         ▼         │
│  GATE REVIEWS: Define → Measure → Analyze → Improve → Control   │
│  EXIT CRITERIA: Cpk > 1.33, DPMO < 500, OEE > 85%              │
└─────────────────────────────────────────────────────────────────┘
```

**Principle 1 — The Process Is the Problem, Not the People:** When a process fails consistently, the system (process, equipment, method) is at fault — not the operator. Fix the process, not the person.

**Principle 2 — Variation Is the Enemy:** Common cause variation is inherent to the process; special cause variation comes from external factors. Do not adjust for common cause — it makes things worse.

**Principle 3 — Small Changes Compound:** A 1% improvement every week compounds to 67% improvement in one year. Continuous > Perfect is the lean mindset.

---


## § 6 Professional Toolkit

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Minitab
| Value Stream Mapping (VSM) | Waste identification, flow analysis | Lean transformation |
| Kaizen
| OEE Tracking (OEE.com) | Overall Equipment Effectiveness | TPM implementation |
| SPC Charts (SPC IV Excel) | Statistical process control | Ongoing monitoring |
| Control Plan (APQP) | Process control documentation | Production release |
| FMEA Software | Failure mode analysis | Process risk assessment |

---

## § 7 Standards & Reference

See [references/07-standards.md](references/07-standards.md)

---

---

## § 8 Standard Workflow

See [references/08-workflow.md](references/08-workflow.md)

---

---

## § 9 · Scenario Examples

See [references/09-scenarios.md](references/09-scenarios.md)

---

---

### Scenario 2 — Kaizen Event on Assembly Line Bottleneck

**User:** Our assembly line has a bottleneck at Station 3 (cycle time 65 seconds) that causes WIP buildup. Takt time is 55 seconds. How do I reduce cycle time?

**Expert:** Reducing the bottleneck by 10 seconds will improve flow. Let me run a Kaizen event:

**Kaizen Event: Station 3 Cycle Time Reduction**

**Day 1: Current State (Gemba Walk)**
```
Station 3 Operations Breakdown:
- Pick part from bin:        8 sec
- Insert fastener:         15 sec
- Tighten (4x bolts):      25 sec
- Visual inspection:         5 sec
- Place to conveyor:        7 sec
- Walk (tool retrieval):    15 sec  ← WASTE!
-----------------------------------
Total:                     65 sec
```

**Day 2: Root Cause & Countermeasures**

| Waste | Root Cause | Countermeasure |
|-------|-----------|----------------|
| Motion | Tools at separate station | Relocate tools to Station 3 |
| Motion | Operator walks to get parts | Add parts at point of use |
| Transport | Parts delivered batch | Convert to single-piece flow |

**Day 3: Implementation**

```
After Kaizen:
- Tool relocation:   saved 15 sec
- Point-of-use:       saved 8 sec
- Process improvement: saved 7 sec (re-sequenced)
-----------------------------------
New Cycle Time:       35 sec
```

**Results:**
```
Before: 65 sec (bottleneck)
After:  35 sec (under takt)
Improvement: 46% cycle time reduction
WIP reduced: 70%
```

[RISK] Document new standard work immediately — without it, operators will revert to old habits within 2 weeks.

---

### Scenario 3 — TPM Implementation for OEE Improvement

**User:** Our production line has OEE = 62%. Availability = 72%, Performance = 90%, Quality = 96%. Where should we focus improvement efforts?

**Expert:** OEE = A × P × Q. Let me calculate where the biggest opportunity is:

**Current OEE Analysis:**
```
Availability:  72%  → Target 90% → Gap 18%
Performance:  90%  → Target 95% → Gap 5%
Quality:      96%   → Target 99% → Gap 3%

OEE = 0.72 × 0.90 × 0.96 = 62% (matches actual)

Biggest gap: AVAILABILITY (18% loss)
```

**Root Cause Analysis (Availability Losses):**
```
Planned Downtime:     10% (shifts, breaks)
Unplanned Downtime:   18% (breakdowns)
  - Hydraulic failure:   40% of unplanned
  - Electrical fault:    30% of unplanned
  - Material jam:        20% of unplanned
  - Other:               10% of unplanned
```

**TPM Implementation Plan:**

| Focus Area | Action | Expected OEE Impact |
|-----------|--------|-------------------|
| Hydraulic failure | TPM program: filter replacement, fluid analysis | +8% Availability |
| Electrical fault | Autonomous maintenance: operator cleaning | +4% Availability |
| Material jam | Poke-Yoke: error-proof feeding | +3% Availability |
| Quick changeover | SMED to reduce changeover time | +3% Availability |

**Projected OEE After 6 Months:**
```
Availability:  72% → 87%  (+15%)
Performance:   90% → 93%  (+3%)
Quality:      96% → 98%  (+2%)
--------------------------------
OEE:          62% → 80%
Annual savings: $280K (reduced scrap, less overtime)
```

---

## § 10 Common Pitfalls

See [references/10-pitfalls.md](references/10-pitfalls.md)

---

---

### Anti-Pattern 2 — Treating All Variation as Special Cause

❌ **BAD:**
```
// Operator adjusts machine every time a point is out of control
// "This looks different, let me adjust"
// Result: Process actually gets worse, more variation
```

✅ **GOOD:**
```
// Use control chart rules (Western Electric):
    // - 1 point outside 3σ → investigate
    // - 2 of 3 points outside 2σ → investigate
    // - 4 of 5 points outside 1σ → investigate
// Only adjust for SPECIAL CAUSE variation (assignable cause)
// Do NOT adjust for COMMON CAUSE variation (inherent to process)
```

**Why it matters:** Over-adjustment (tampering) increases variation. The control chart separates common from special cause — act only on special cause.

---

### Anti-Pattern 3 — Skipping the Measurement System Validation

❌ **BAD:**
```
// Process Cpk = 1.33 claimed
// Used gauge that operator "trusts"
// GR&R never performed
// Reality: High measurement variation masks true process capability
```

✅ **GOOD:**
```
// GR&R Study before any capability analysis:
    // 1. Select 10 random parts from production
    // 2. Operator measures each part 3 times
    // 3. Calculate: %GR&R = 5.15 × σ_measurement
    // 4. If %GR&R > 30%: Improve gauge or method first
    // 5. If %GR&R < 10%: Excellent; proceed with capability study
// Example: %GR&R = 22% → Acceptable but monitor
```

**Why it matters:** If the measurement system is worse than the process, you cannot distinguish good parts from bad parts. Bad parts will ship.

---

### Anti-Pattern 4 — Focusing on the Wrong Bottleneck

❌ **BAD:**
```
// Improved Station 5 (bottleneck per operator opinion)
// Spent 3 months, $50K on improvements
// Station 5 cycle time: 65s → 58s
// Overall line output: unchanged
// Real bottleneck: Station 7 (was 72s)
```

✅ **TOC Analysis:
```
Identify true bottleneck:
    Station 1: 45s
    Station 2: 52s
    Station 3: 58s
    Station 4: 61s
    Station 5: 65s  ← Perceived
    Station 6: 55s
    Station 7: 72s  ← TRUE BOTTLENECK

Solution: Improve Station 7, not Station 5
Result: Output increases immediately
```

**Why it matters:** Theory of Constraints (TOC) teaches that improving non-bottlenecks has zero impact on throughput. Find the true constraint first.

---

### Anti-Pattern 5 — Implementing Without Standard Work

❌ **BEST:**
```
// New improved process implemented
// "Everyone do it their own way"
// No standard work document
// 2 weeks later: operators have reverted
// Improvement lost
```

✅ **GOOD:**
```
// Standard Work Elements:
    // 1. Takt Time: 55 sec
    // 2. Standard Sequence: [list all steps in order]
    // 3. Standard WIP: 2 parts at station
    // 4. Quality Checks: [list at which step]
// Document on:
    // - Process Flow Chart
    // - Standard Work Combination Sheet
    // - Control Plan
// Train all operators to standard
// Audit adherence weekly
```

**Why it matters:** Without standard work, improvement is not sustainable. People revert to habit. Standard work is the baseline for future improvement.

---

### Anti-Pattern 6 — Six Sigma Without Practical Significance

❌ **BAD:**
```
// DOE found statistically significant factor (p < 0.05)
// Factor: Temperature variation of 0.1°C
// Recommendation: Install $50K temperature control
// Cost savings: $200/year (2 year payback)
// Project killed by finance
```

✅ **Practical Significance Check:
```
Before launching Six Sigma project:
    1. Estimate cost of implementation
    2. Estimate annual savings
    3. Calculate ROI
    4. Ensure ROI > 200% (or meet company hurdle)

Example: $50K investment, $50K annual savings → 1 year payback ✓
vs.    $50K investment, $200 annual savings → 250 year payback ✗
```

**Why it matters:** Statistical significance ≠ practical significance. Projects must have business justification or they will be cancelled.

---

## § 11 Integration with Other Skills

| Combination | Outcome |
|-------------|---------|
| Process Engineer + Mechanical Design Engineer | DFM optimization: design for manufacturability, design for assembly |
| Process Engineer + QC Specialist | SPC implementation: control charts, process capability, measurement systems |
| Process Engineer + Electrical Engineer | Production test optimization: fixture design, test coverage |
| Process Engineer + Manufacturing Operator | Gemba improvement: operator-driven improvement, kaizen |

---

## § 12 Scope & Limitations

**Use when:**
- Optimizing manufacturing processes (assembly, machining, packaging)
- Implementing lean manufacturing (TPS, one-piece flow, kanban)
- Leading Six Sigma projects (DMAIC)
- Improving OEE and equipment effectiveness (TPM)
- Conducting root cause analysis and problem solving

**Do not use when:**
- Designing new products (use Mechanical/Electrical Design Engineer)
- Managing production scheduling (use production planning skills)
- Handling supplier quality (use supplier quality engineer)
- Managing inventory (use materials planning)

**Alternatives:**
- For product design: Design engineering skills
- For supply chain: Supply chain engineering
- For maintenance: TPM or maintenance engineering

---


## § 14 Quality Verification

**Self-checklist:**
- [ ] All 16 sections present and numbered with § prefix
- [ ] System prompt includes 5 gate questions and 5 thinking patterns in code block
- [ ] Risk table has 7 rows with CRITICAL/HIGH/MEDIUM severity ratings
- [ ] Standards table includes formulas and quantitative target ranges
- [ ] Workflow has [✓ Done] and [✗ FAIL] criteria for all 4 phases
- [ ] All 3 scenarios include specific data (Cpk calculations, Kaizen results, TOC analysis)
- [ ] All 6 anti-patterns have ❌ BAD + ✅ GOOD examples with "Why it matters"
- [ ] Trigger words table is bilingual (English + 中文)

**Test Cases:**

| Input | Expected Output |
|-------|----------------|
| "Cpk = 0.89 on bore dimension, defect rate 2.3%" | Root cause analysis with fishbone, specific countermeasures, Cpk improvement projections |
| "Assembly line bottleneck at Station 3, cycle time 65s vs. takt 55s" | Kaizen event framework, waste identification, improvement targets |
| "OEE = 62%, where to focus?" | OEE calculation, gap analysis, TPM implementation plan |

---
## § 16 · Domain Deep Dive

### Specialized Knowledge Areas

| Area | Core Concepts | Applications | Best Practices |
|------|--------------|--------------|----------------|
| **Foundation** | Principles, theories | Baseline understanding | Continuous learning |
| **Implementation** | Tools, techniques | Practical execution | Standards compliance |
| **Optimization** | Performance tuning | Enhancement projects | Data-driven decisions |
| **Innovation** | Emerging trends | Future readiness | Experimentation |

### Knowledge Maturity Model

| Level | Name | Description |
|-------|------|-------------|
| 5 | Expert | Create new knowledge, mentor others |
| 4 | Advanced | Optimize processes, complex problems |
| 3 | Competent | Execute independently |
| 2 | Developing | Apply with guidance |
| 1 | Novice | Learn basics |

## § 17 · Risk Management Deep Dive

### 🔴 Critical Risk Register

| Risk ID | Description | Probability | Impact | Score |
|---------|-------------|-------------|--------|-------|
| R001 | Strategic misalignment | Medium | Critical | 🔴 12 |
| R002 | Resource constraints | High | High | 🔴 12 |
| R003 | Technology failure | Low | Critical | 🟠 8 |

### 🟠 Risk Response Strategies

| Strategy | When to Use | Effectiveness |
|----------|-------------|---------------|
| **Avoid** | High impact, controllable | 100% if feasible |
| **Mitigate** | Reduce probability/impact | 60-80% reduction |
| **Transfer** | Better handled by third party | Varies |
| **Accept** | Low impact or unavoidable | N/A |

### 🟡 Early Warning Indicators

- Stakeholder engagement dropping
- Requirement changes increasing
- Team velocity declining
- Defect rates rising

## § 18 · Excellence Framework

### World-Class Execution Standards

| Dimension | Good | Great | World-Class |
|-----------|------|-------|-------------|
| **Quality** | Meets requirements | Exceeds expectations | Redefines standards |
| **Speed** | On time | Ahead | Sets benchmarks |
| **Cost** | Within budget | Under budget | Maximum value |
| **Innovation** | Incremental | Significant | Breakthrough |

### Excellence Cycle

```
ASSESS → PLAN → EXECUTE → REVIEW → IMPROVE
   ↑                              ↓
   └────────── MEASURE ←──────────┘
```

---
## § 19 · Best Practices Library

### Industry Best Practices

| Practice | Description | Implementation | Expected Impact |
|----------|-------------|----------------|-----------------|
| **Standardization** | Consistent processes | SOPs | 20% efficiency gain |
| **Automation** | Reduce manual tasks | Tools/scripts | 30% time savings |
| **Collaboration** | Cross-functional teams | Regular sync | Better outcomes |
| **Documentation** | Knowledge preservation | Wiki, docs | Reduced onboarding |
| **Feedback Loops** | Continuous improvement | Retrospectives | Higher satisfaction |

## § 20 · Case Studies

### Success Story 1: Transformation
**Challenge:** Legacy system limitations
**Results:** 40% performance improvement, 50% cost reduction

### Success Story 2: Innovation  
**Challenge:** Market disruption
**Results:** New revenue stream, competitive advantage

## § 21 · Resources & References

| Resource | Type | Key Takeaway |
|----------|------|--------------|
| Industry Standards | Guidelines | Compliance requirements |
| Research Papers | Academic | Latest methodologies |
| Case Studies | Practical | Real-world applications |

---
