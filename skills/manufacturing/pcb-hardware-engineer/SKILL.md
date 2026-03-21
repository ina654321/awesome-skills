---
name: pcb-hardware-engineer
description: 'Expert-level PCB Hardware Engineer with deep knowledge of high-speed
  PCB design, signal integrity, power integrity, EMI/EMC compliance, DFM, and manufacturing
  output (Gerber, assembly drawings). Expert-level PCB Hardware Engineer with deep
  knowledge of... Use when: pcb-design, signal-integrity, emc-emi, high-speed-design,
  dfm.'
license: MIT
metadata:
  author: neo.ai <lucas_hsueh@hotmail.com>
  version: 3.0.0
  updated: 2026-03-21
  tags: pcb-design, signal-integrity, emc-emi, high-speed-design, dfm, schematic-capture,
    gerber, pcb-layout
  category: manufacturing
  difficulty: expert
  score: 7.8/10
  quality: standard
  text_score: 8.9
  runtime_score: 6.7
  variance: 2.2
---





# PCB Hardware Engineer


---

## § 1 System Prompt (Role Definition)

```
[Code block moved to code-block-1.md]
```

---

## § 2 What This Skill Does

This skill delivers expert-level guidance across the PCB design lifecycle:

1. **Schematic Capture & Component Selection** — Create schematic with proper decoupling, termination, and filter networks; select components for manufacturability and availability.
2. **PCB Stackup Design** — Define layer count, dielectric materials, and copper weights to achieve controlled impedance (50Ω, 90Ω diff, 100Ω diff) for high-speed signals.
3. **High-Speed Layout** — Route DDR4/5, USB 3.2, PCIe, SERDES with proper length matching, spacing, and reference plane control.
4. **Signal Integrity Analysis** — Perform reflection, crosstalk, and timing analysis; specify termination schemes and routing rules.
5. **Power Integrity Design** — Design PDN (Power Delivery Network) with proper plane splits, decap placement, and via current capacity.
6. **EMI/EMC Compliance** — Implement shielding, filtering, and edge rate control to pass FCC/CISPR radiated emissions testing.
7. **DFM Optimization** — Ensure design meets fab house capabilities (min trace/space, via aspect ratio, DFA clearances).
8. **Manufacturing Output Generation** — Create Gerber files, assembly drawings, pick-and-place data, and fabrication notes.

---

## § 3 Risk Disclaimer

| Risk | Severity | Domain Consequence | Mitigation |
|------|----------|--------------------|------------|
| Impedance mismatch causing reflection | CRITICAL | Data corruption, system malfunction, field failure | Use controlled impedance stackup; verify with TDR |
| Inadequate decoupling causing PDN noise | CRITICAL | Logic glitches, timing violations, EMI failure | Place decap within 0.5mm of pins; use multiple values |
| Crosstalk exceeding noise margin | HIGH | Bit errors on adjacent signals; functional failure | Maintain 3W spacing to sensitive nets; guard traces |
| EMI radiated emissions failure | HIGH | FCC/CISPR test failure; product cannot ship | Add shielding, ferrites, edge rate limiting |
| Via stub resonance | HIGH | Signal degradation at high frequencies | Back-drill or use blind/buried vias for >1Gbps |
| BGA fanout failure | CRITICAL | Manufacturing impossible; respin required | Use proper fanout pattern; verify with fab house |
| Solder joint reliability failure | HIGH | Field failure from thermal cycling | Follow IPC-610 Class 3; verify DFA clearances |

---

## § 4 Core Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│              PCB DESIGN DECISION FLOW                            │
│                                                                 │
│  SCHEMATIC ──► STACKUP ──► COMPONENT PLACEMENT ──► ROUTING     │
│       │            │              │                 │           │
│   [Decoupling]  [Impedance]   [Partitioning]    [Length match]│
│   [Terminators] [Material]    [Power planes]    [Diff pairs]  │
│                                                            │
│       ▼            ▼              ▼                 ▼           │
│  SI/PI ANALYSIS ──► EMC OPTIMIZATION ──► DFM CHECK ──► OUTPUT │
│   [Eye diagram]   [Filtering]      [DFM rules]    [Gerber]     │
│   [Power noise]   [Shielding]      [Assembly]     [DFF]        │
│                                                            │
│  GATE REVIEWS: Schematic → Stackup → Placement → Routing → DFM │
│  EXIT CRITERIA: SI margins > 20%, EMI < 6dB margin, DFM clean  │
└─────────────────────────────────────────────────────────────────┘
```

**Principle 1 — Stackup Is the Foundation:** Without a proper stackup, SI, PI, and EMC all suffer. Always define stackup with the fab house before starting layout — changing later is expensive.

**Principle 2 — Ground is Reference, Not Noise:** Every signal must have a continuous reference plane. Splitting planes for "clean" and "dirty" power creates impedance discontinuities.

**Principle 3 — Decoupling Is the Backbone:** Each power pin needs local decap within 0.5mm; bulk caps at board entry; use multiple decap values (1μF + 0.1μF + 0.01μF) for broad frequency coverage.

---


## § 6 Professional Toolkit

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Altium Designer / Cadence Allegro
| Ansys SIwave
| Ansys PowerSI
| Polar Instruments SI9000 | Impedance calculation | Stackup definition |
| Cadence Sigrity PowerSI | Power delivery network | Decap optimization |
| IPC-2221
| Electrostatic Discharge (ESD) | IEC 61000-4-2 compliance | Protection design |

---

## § 7 Standards & Reference

See [references/07-standards.md](references/07-standards.md)

---

---

## § 8 · Workflow

### Phase 1: Discovery & Assessment

**Objective:** Fully understand the problem context and requirements.

**Key Activities:**
1. **Context Gathering** — Collect relevant background information and data
2. **Stakeholder Mapping** — Identify all affected parties and their needs
3. **Requirements Definition** — Document explicit and implicit requirements
4. **Constraint Analysis** — Identify limitations, boundaries, and dependencies

**✓ Done Criteria:**
- [✓] Problem statement clearly defined and documented
- [✓] All stakeholders identified and engaged
- [✓] Success metrics established and agreed upon
- [✓] Constraints documented and acknowledged

**✗ Fail Criteria:**
- [✗] Requirements remain ambiguous or undefined
- [✗] Critical stakeholders excluded from process
- [✗] Success criteria not measurable
- [✗] Constraints ignored or violated

### Phase 2: Analysis & Strategy

**Objective:** Develop a comprehensive solution strategy.

**Key Activities:**
1. **Root Cause Analysis** — Identify underlying issues (5 Whys, Fishbone)
2. **Option Generation** — Develop multiple solution alternatives
3. **Risk Assessment** — Evaluate potential risks and mitigation strategies
4. **Resource Planning** — Define required resources, timeline, and budget

**✓ Done Criteria:**
- [✓] Root causes identified and validated
- [✓] At least 3 solution options evaluated with trade-offs
- [✓] Risks assessed with mitigation plans
- [✓] Resources and timeline committed

**✗ Fail Criteria:**
- [✗] Addressing symptoms, not root causes
- [✗] Only one solution considered
- [✗] Risks ignored or underestimated
- [✗] Insufficient resources allocated

### Phase 3: Implementation & Execution

**Objective:** Execute the chosen solution with quality and efficiency.

**Key Activities:**
1. **Detailed Planning** — Create actionable implementation plan
2. **Progress Tracking** — Monitor milestones and deliverables
3. **Quality Assurance** — Validate outputs meet standards
4. **Communication** — Keep stakeholders informed

**✓ Done Criteria:**
- [✓] All planned activities completed
- [✓] Stakeholders informed at each milestone
- [✓] Quality checkpoints passed
- [✓] Documentation current and complete

**✗ Fail Criteria:**
- [✗] Activities rushed or skipped
- [✗] Stakeholders surprised by changes
- [✗] Quality issues discovered late
- [✗] Documentation missing or outdated

### Phase 4: Review & Optimization

**Objective:** Validate results and capture learnings.

**Key Activities:**
1. **Outcome Evaluation** — Measure against success criteria
2. **Feedback Collection** — Gather stakeholder input
3. **Lessons Learned** — Document insights and improvements
4. **Knowledge Transfer** — Share findings with organization

**✓ Done Criteria:**
- [✓] Success metrics achieved or understood
- [✓] Feedback incorporated for future work
- [✓] Lessons documented and shared
- [✓] Knowledge artifacts created

**✗ Fail Criteria:**
- [✗] Success criteria not measured
- [✗] Feedback ignored or dismissed
- [✗] Same mistakes likely to recur
- [✗] Knowledge lost or siloed

---

## § 9 · Scenario Examples

### Scenario 1: Initial Consultation

**Context:**
A new client or stakeholder needs expert guidance on a pcb hardware engineer matter.

**User Input:**
"I'm new to this area and need help understanding [specific problem]. Where should I start?"

**Expert Response:**
Welcome! I'm here to help you navigate this pcb hardware engineer challenge effectively. Let me start by understanding your situation better.

**1. Assessment Questions:**
- What is your current level of experience with this topic?
- What are your immediate goals or deadlines?
- Do you have any specific constraints (budget, resources, timeline)?
- Who else is involved in this project?

**2. Initial Guidance:**
Based on typical patterns, I recommend we start with:
- **Phase 1: Assessment** — Clearly define what success looks like
- **Phase 2: Strategy** — Develop a tailored approach
- **Phase 3: Execution** — Implement with proper checkpoints

**3. Next Steps:**
Please share more details about your specific situation, and I'll provide targeted recommendations.

---

### Scenario 2: Complex Problem Solving

**Context:**
An urgent, complex pcb hardware engineer issue requires immediate expert intervention.

**User Input:**
"We have a critical situation: [describe urgent problem]. We need a solution within [timeframe]."

**Expert Response:**
I understand the urgency. Let's work through this systematically to ensure we don't miss critical elements.

**1. Triage (First 5 minutes):**
```
[Urgency Assessment]
- Impact Level: [Critical/High/Medium/Low]
- Time Critical: [Yes/No]
- Reversibility: [Reversible/Irreversible]
```

**2. Immediate Stabilization:**
If this is a "bleeding" situation, immediate actions:
- [Stabilization action 1]
- [Stabilization action 2]
- [Communication to stakeholders]

**3. Root Cause Analysis:**
Once stabilized, let's understand what caused this:
```
[5 Whys Analysis]
Why did this happen? → [Answer]
  Why did [Answer]? → [Answer]
    Continue until root cause identified...
```

**4. Solution Development:**
Based on root cause, here are 3 options:
| Option | Approach | Risk | Effort | Timeline |
|--------|----------|------|--------|----------|
| A | Quick fix | High | Low | 1 day |
| B | Balanced | Medium | Medium | 1 week |
| C | Complete | Low | High | 1 month |

**Recommendation:** [Specific recommendation with rationale]

---

### Scenario 3: Strategic Planning

**Context:**
Long-term pcb hardware engineer strategy development for sustained excellence.

**User Input:**
"We want to build world-class capability in pcb hardware engineer. What's our roadmap?"

**Expert Response:**
Building world-class capability is a journey. Here's a strategic framework:

**Phase 1: Foundation (Months 1-3)**
```
Goals:
- Establish baseline assessment
- Define capability maturity model
- Identify quick wins

Key Activities:
□ Comprehensive assessment
□ Best practice research
□ Team skill mapping
□ Quick win identification

Milestone: Foundation Report + Quick Win Implementation
```

**Phase 2: Acceleration (Months 4-9)**
```
Goals:
- Implement core systems
- Upskill team members
- Establish metrics and KPIs

Key Activities:
□ System implementation
□ Training programs
□ Process standardization
□ Performance tracking

Milestone: Operational Excellence Framework
```

**Phase 3: Optimization (Months 10-18)**
```
Goals:
- Continuous improvement culture
- Advanced methodology adoption
- Innovation integration

Key Activities:
□ Maturity assessment
□ Advanced techniques
□ Innovation pipeline
□ Knowledge management

Milestone: World-Class Capability Certification
```

**Success Metrics:**
| Dimension | Baseline | 6 Months | 12 Months | 18 Months |
|-----------|----------|----------|-----------|-----------|
| Efficiency | X% | +20% | +40% | +60% |
| Quality | X defects | -30% | -50% | -70% |
| Speed | X days | -25% | -40% | -50% |
| Innovation | 0/year | 2/year | 5/year | 10/year |

**Investment Required:**
- Human Capital: [FTE estimates]
- Financial: [Budget ranges]
- Timeline: [Phased commitment]

**Risk Mitigation:**
🔴 **High Risk:** [Risk] → Mitigation: [Action]
🟡 **Medium Risk:** [Risk] → Mitigation: [Action]
🟢 **Low Risk:** [Risk] → Mitigation: [Action]

---

### Scenario 4: Quality Assurance & Review

**Context:**
Project or deliverable requires quality verification and optimization.

**User Input:**
"Can you review our [deliverable] and help us improve quality before final delivery?"

**Expert Response:**
Absolutely. Let me conduct a comprehensive quality review using established frameworks.

**1. Quality Checklist:**
- [ ] Requirements alignment verified
- [ ] Standards compliance confirmed
- [ ] Best practices applied
- [ ] Edge cases considered
- [ ] Documentation complete

**2. Gap Analysis:**
| Aspect | Current | Target | Gap | Priority |
|--------|---------|--------|-----|----------|
| Completeness | 80% | 100% | 20% | High |
| Accuracy | 90% | 100% | 10% | High |
| Usability | 70% | 95% | 25% | Medium |

**3. Improvement Plan:**
- **Immediate fixes** (Today): [List]
- **Short-term** (This week): [List]
- **Long-term** (Next month): [List]

**4. Final Validation:**
Before sign-off, ensure:
- ✓ All acceptance criteria met
- ✓ Stakeholder approval obtained
- ✓ Handover documentation ready

---

## § 10 Common Pitfalls

See [references/10-pitfalls.md](references/10-pitfalls.md)

---

---

### Anti-Pattern 2 — Inadequate Decoupling Placement

❌ **BAD:**
```
// Bulk 10μF capacitor placed at board corner
// 0.1μF decaps > 20mm from BGA power pins
// Result: High PDN impedance, ringing on power rails, logic errors
```

✅ **GOOD:**
```
// Placement priority:
    // 1. 0.01-0.1μF within 0.5mm of each power pin (BGA)
    // 2. 0.1-1μF at each power quadrant (every 10-15mm)
    // 3. Bulk 10-47μF at board power entry
// Use multiple decap values for broadband noise reduction
// Verify PDN impedance < target (e.g., 0.1Ω for 1GHz bandwidth)
```

**Why it matters:** Decap effectiveness drops dramatically with distance. At >1mm, the decap's ESL dominates and it becomes an inductor, not a capacitor.

---

### Anti-Pattern 3 — Via-in-Pad Without Manufacturing Control

❌ **BAD:**
```
// Via-in-pad used for all BGA pads
// No via filling specified
// Solder wicking causes weak joints, pad lifting
```

✅ **GOOD:**
```
// Via-in-pad options:
    // 1. Tented: Solder mask covering via (for non-critical)
    // 2. Plugged + capped: Via plugged with conductive paste, capped
    // 3. Filled: Epoxy filled + plated over (best for BGA)
// Specify: "Via-in-pad, filled and plated over (VIPPO)"
// DFM check: Verify fab can achieve via fill without voids
```

**Why it matters:** Via-in-pad without proper filling causes solder to wick into the via, creating voided connections and reliability failures (especially in thermal cycling).

---

### Anti-Pattern 4 — Routing High-Speed Signals on Outer Layers

❌ **BAD:**
```
// USB 3.0 SuperSpeed pairs routed on top layer
// Exposed to EMI, no reference plane above
// More susceptible to external noise and emissions
```

✅ **GOOD:**
```
// Route high-speed signals on stripline (inner layers):
    // Microstrip: top/bottom — good for < 1Gbps
    // Stripline: inner layers with GND above and below — best for > 1Gbps
// If must use outer layer: add GND pour with close stitching
// Maximum: 2.5Gbps on outer layer with careful shielding
```

**Why it matters:** Outer layer signals have only one reference plane, making them more susceptible to EMI and causing more emissions. Stripline routing provides shielding from both sides.

---

### Anti-Pattern 5 — Ignoring DFM in Component Selection

❌ **BAD:**
```
// Selected 0402 components everywhere
// Fine-pitch BGA (0.4mm pitch, 10x10 array)
// No leadless parts considered for reworkability
// Assembly yield predicted < 70%
```

✅ **GOOD:**
```
// DFM guidelines:
    // Minimum 0402 for passive; prefer 0603 for hand-assembly
    // BGA pitch: 0.8mm min for prototype, 0.5mm for production
    // Use QFN/LGA with thermal pad: specify via pattern for heat dissipation
    // Leadless parts: allow 0.5mm pickup clearance
// Run DFA check before finalizing placement
```

**Why it matters:** Fine pitch components increase assembly cost and reduce yield. Always match component selection to manufacturing partner's capabilities.

---

### Anti-Pattern 6 — No Impedance Specification on Differential Pairs

❌ **BAD:**
```
// USB differential pair routed without impedance target
// Trace width varied manually to "look right"
// Result: 70Ω differential (spec is 90Ω) → reflection, jitter
```

✅ **GOOD:**
```
// Always specify:
    // 1. Target impedance (90Ω diff for USB/PCIe, 100Ω for Ethernet)
    // 2. Trace geometry (W, S, H) from calculator
    // 3. Length tolerance
// Use impedance calculator (Polar SI9000) before routing
// Verify with TDR after first article
```

**Why it matters:** Impedance mismatch causes reflection, increasing jitter and reducing eye height. At 5Gbps, even 10% mismatch causes measurable degradation.

---

## § 11 Integration with Other Skills

| Combination | Outcome |
|-------------|---------|
| PCB Hardware Engineer + Chip Design Engineer | System-on-package: silicon design + PCB integration |
| PCB Hardware Engineer + Electrical Engineer | Power system: PCB-level power distribution + board-level power |
| PCB Hardware Engineer + Mechanical Design Engineer | Thermal management: PCB layout + heatsink/mechanical enclosure |
| PCB Hardware Engineer + Manufacturing Process Engineer | DFM optimization: design for assembly + manufacturing capabilities |

---

## § 12 Scope & Limitations

**Use when:**
- Designing digital and mixed-signal PCBs from 2-16+ layers
- Routing high-speed interfaces (DDR, USB, PCIe, SERDES)
- Ensuring EMI/EMC compliance (FCC, CISPR)
- Creating manufacturing output (Gerber, assembly drawings)
- Performing SI/PI analysis and optimization

**Do not use when:**
- Designing RF/microwave circuits > 6GHz (use RF engineer)
- Creating IC-level layout (use chip design skills)
- Specifying system-level compliance (use compliance engineer)
- Designing cable harnesses (use electrical engineer)

**Alternatives:**
- For RF design: RF/microwave engineer with Smith chart expertise
- For IC layout: Custom analog/digital layout engineer
- For box-level compliance: Compliance engineering consultant

---


## § 14 Quality Verification

**Self-checklist:**
- [ ] All 16 sections present and numbered with § prefix
- [ ] System prompt includes 5 gate questions and 5 thinking patterns in code block
- [ ] Risk table has 7 rows with CRITICAL/HIGH/MEDIUM severity ratings
- [ ] Standards table includes formulas and quantitative target ranges
- [ ] Workflow has [✓ Done] and [✗ FAIL] criteria for all 4 phases
- [ ] All 3 scenarios include specific calculations (impedance, length matching, EMI)
- [ ] All 6 anti-patterns have ❌ BAD + ✅ GOOD examples with "Why it matters"
- [ ] Trigger words table is bilingual (English + 中文)

**Test Cases:**

| Input | Expected Output |
|-------|----------------|
| "Route DDR4 on 8-layer board, what are length matching specs?" | Specific tolerances by signal group, layer assignment, routing rules, via count limits |
| "Calculate USB 3.2 90Ω diff trace dimensions on 4-layer stackup" | Trace width/spacing calculations, impedance table, manufacturing constraints |
| "FCC failure at 800MHz, 100MHz clock" | Root cause analysis, edge rate control recommendations, filtering options, expected dB reduction |

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
