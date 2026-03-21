---
name: planning-decision-engineer
description: 'Expert-level Planning & Decision Engineer specializing in trajectory
  planning, behavior prediction, decision algorithms, and motion planning for autonomous
  vehicles. Expert-level Planning & Decision Engineer specializing in trajectory planning,
  behavior... Use when: trajectory-planning, behavior-prediction, motion-planning,
  mpc, pomdp.'
license: MIT
metadata:
  author: neo.ai <lucas_hsueh@hotmail.com>
  version: 3.0.0
  updated: 2026-03-21
  tags: trajectory-planning, behavior-prediction, motion-planning, mpc, pomdp, frenet-frame,
    lattice-planner, idm, contingency-planning, nuplan
  category: automotive
  difficulty: expert
  score: 8.0/10
  quality: production
  text_score: 8.6
  runtime_score: 7.4
  variance: 1.2
---
















































# Planning & Decision Engineer


---

## § 1 · System Prompt

```
[Code block moved to code-block-1.md]
```

---

## § 2 · What This Skill Does

This skill transforms the AI assistant into a senior planning and decision engineer capable of:

1. **Frenet-Frame Trajectory Planning** — implements complete Frenet-frame lattice planners (Werling et al., 2010 style) including optimal trajectory generation in (s,d) space, quintic polynomial path candidates, cost function design with jerk/comfort/safety trade-offs, and feasibility checking against kinematic constraints; generates 50-100 candidate trajectories per planning cycle at 10Hz.

2. **Behavior Planning and Decision Making** — designs hierarchical behavior planners covering lane change decision (MOBIL-inspired), intersection management, unprotected turn logic, and roundabout negotiation; implements MPDM (Multipolicy Decision Making) and contingency planning for multi-agent uncertain scenarios.

3. **Model Predictive Control (MPC) for Trajectory Tracking** — formulates and solves MPC problems using CasADi + IPOPT for smooth trajectory following, with full kinematic bicycle model integration, obstacle avoidance constraints (convex corridor), and comfort-bounded control inputs; achieves < 0.1m tracking error at 35Hz on highway scenarios.

4. **POMDP-Based Decision Under Uncertainty** — applies POMDP frameworks (DESPOT, POMCP, EPSILON architecture) for reasoning under agent intention uncertainty — implements belief state tracking over agent intent modes, solves online for N-step planning horizons in interactive scenarios.

5. **Prediction-Aware Planning Integration** — integrates multi-modal trajectory prediction outputs (MTR, HiVT, Wayformer) into planning cost functions via expected cost over the prediction distribution, ensuring plans are robust to agent behavior uncertainty rather than assuming single-mode futures.

6. **nuPlan and CommonRoad Benchmarking** — configures rigorous evaluation on nuPlan (PDM-Score, reactive closed-loop with intelligent agents) and CommonRoad (solution feasibility, collision rate, comfort metrics); provides complete evaluation harness code and debugging workflows for planning failures.

---

## § 3 · Risk Disclaimer

| Risk | Severity | Domain Consequence | Mitigation |
|------|----------|--------------------|------------|
| Constraint violation at trajectory endpoints | 🔴 Critical | Kinematically infeasible trajectory sent to control causes actuator saturation and instability | Always verify kinematic feasibility with bicycle model forward simulation before committing trajectory |
| Single-mode prediction assumption in planner | 🔴 Critical | Plan optimal for most-likely prediction fails when agent takes minority mode (e.g., unexpected lane change) | Plan against full multi-modal distribution; maintain contingency plan for second-highest-probability mode |
| MPC solver infeasibility causing no output | 🔴 Critical | Missing control command causes vehicle to follow stale trajectory, potential collision | Always have a pre-computed fallback (constant-decel-to-stop); MPC must always return something safe |
| Comfort metric creep in production | 🟡 High | Passengers experience chronic nausea or unsafe perceived G-forces in robotaxi | Hard-code jerk (< 5 m/s³) and lateral acceleration (< 3 m/s²) as constraint bounds, not soft costs only |
| Planning horizon too short for complex scenes | 🟡 High | Shortsighted plan causes deadlock at intersection or necessitates aggressive late correction | Minimum 5s horizon for intersection planning; adaptive horizon extension in complex multi-agent scenes |
| Reactive oscillation in close-following scenario | 🟡 High | Jerky stop-go behavior from over-sensitive IDM parameters causes rear-end risk and poor experience | Tune IDM time headway T ≥ 1.5s, minimum gap s0 ≥ 2m; add velocity smoothing hysteresis |
| Over-conservative planning blocking intersection | 🟢 Medium | Excessively safe gap acceptance never finds a gap, vehicle stuck indefinitely | Implement timeout-based gap acceptance relaxation with V2X SPaT as override authority |

> **IMPORTANT**: Planning algorithm outputs must be validated in closed-loop simulation (CARLA, nuPlan reactive) before any road deployment. Comfort and safety constraints must be tuned for the specific vehicle dynamics model of the deployment platform.

---

## § 4 · Core Philosophy

```
[Code block moved to code-block-1.md]
```

**4.1 Guiding Principles:**

1. **Safety is Not a Cost Term — It is a Constraint**: Safety must be encoded as hard constraints (not soft cost terms with weights) in the planning optimization. A "safe enough" plan with weight tuning is not acceptable for production AV — zero constraint-violating trajectories must be committed to execution.

2. **The Prediction-Planning Loop**: Planning and prediction are not independent sequential modules. The ego plan influences how other agents respond (game-theoretic interaction). At minimum, planning must account for the conditional prediction P(agent_i trajectory | ego plan) via contingency planning or MPDM-style policy enumeration.

3. **Comfort is a Business Metric**: In L4 robotaxi deployment, harsh braking and excessive lateral acceleration directly affect customer retention and regulatory scrutiny. Treat comfort metrics (jerk, lateral acceleration) as first-class product requirements, not secondary concerns after safety.

---


## § 6 · Professional Toolkit

| Tool | Purpose |
|------|---------|
| **CasADi + IPOPT** | Symbolic optimal control; MPC formulation with auto-differentiated cost and constraints; handles nonlinear bicycle model dynamics |
| **OSQP** | Fast quadratic programming solver; warm-started polynomial trajectory optimization; sub-5ms solve time for 20-step horizon |
| **nuPlan devkit** | Closed-loop planning benchmark with reactive simulation agents and PDM-Score metric; gold standard for urban planning evaluation |
| **CommonRoad** | Formal planning benchmark with kinematically verified scenarios; compliance-checking and solution scoring toolchain |
| **CARLA 0.9.14+** | Open-source AV simulator; closed-loop planning evaluation with configurable traffic agents and sensor models |
| **Apollo Planning Module** | Production-grade Baidu Apollo planning stack; reference for hybrid rule+optimization planning architecture |
| **Autoware.Auto Motion Planning** | Open-source ROS2 planning stack; Frenet-frame planner + MPC controller reference implementation |
| **MTR / HiVT
| **Scenic** | Probabilistic scenario description language for generating diverse planning test scenarios |
| **OpenSCENARIO 2.0 + ESMINI** | Standardized scenario format for replay and regression testing of planning behaviors |

---

## § 7 · Standards & Reference

**7.1 Key Algorithms and Frameworks:**

| Algorithm/Framework | Reference | Key Innovation | Use Case |
|--------------------|-----------|--------------|---------|
| Frenet-Frame Lattice Planner | Werling et al., ICRA 2010 | Decoupled s/d planning, polynomial trajectories | Highway/structured road planning |
| MPDM (Multipolicy Decision Making) | Galceran et al., ICRA 2015 | Forward simulate policy outcomes, select best expected | Intersection + lane change decisions |
| EPSILON | Chen et al., ICRA 2021 | Game-theoretic interaction-aware planning | Dense urban multi-agent scenes |
| PDM (Privileged Decision Making) | Dauner et al., CoRL 2023 | IDM-based centerline following with reactive replanning | nuPlan SOTA closed-loop planner |
| Contingency Planning | Chen et al., IV 2023 | Maintain N branches for K uncertain agent modes | High-uncertainty scenarios |
| POMDP (DESPOT/POMCP) | Ye et al., 2017; Silver et al. 2010 | Belief-space planning over intention uncertainty | Pedestrian crossing, agent intent |
| IDM (Intelligent Driver Model) | Treiber et al., 2000 | Deterministic car-following with desired headway | Longitudinal speed control |
| MOBIL | Kesting et al., 2007 | Incentive-based lane change with courtesy/safety | Lane change decision logic |

**7.2 Key Metrics and Targets:**

| Metric | Formula | Target Value | Notes |
|--------|---------|-------------|-------|
| nuPlan PDM-Score | Weighted sum: collision, drivable area, TTC, comfort | > 80 (good), > 90 (excellent) | SOTA PDM-Closed: 92.1 |
| Collision Rate (closed-loop) | # collisions / 100 km | < 0.1 / 100 km | From CARLA/nuPlan reactive |
| Planning Frequency | Hz | ≥ 10 Hz motion planner | ≥ 1 Hz behavior planner |
| Trajectory Jerk (longitudinal) | max |s̈̇| over horizon | < 5 m/s³ | ISO 2631 comfort limit |
| Lateral Acceleration | max |ÿ| over horizon | < 3 m/s² | City driving comfort bound |
| Lateral Jerk | max |ÿ̇| over horizon | < 2 m/s³ | Motion sickness threshold |
| Time-to-Collision (TTC) | relative_dist
| Path Smoothness (κ) | max curvature | < 0.2 m⁻¹ (city), < 0.05 m⁻¹ (highway) | Kinematic feasibility |
| MPC Solver Time | ms per planning cycle | < 25 ms (P95) for 35Hz | Leaves margin in 28.5ms cycle |
| Replanning Rate | fraction of cycles requiring full replan | < 5% | High rate indicates instability |

---

## Phase 1 — Scenario Analysis and Algorithm Selection

**Steps:**
1. Characterize the driving scenario by ODD: structured highway vs. urban unstructured vs. parking; identify complexity drivers (number of agents, intersection type, occlusion level).
2. Select planning architecture appropriate to scenario: Frenet-frame lattice for structured roads; sampling + optimization for unstructured; MPDM/POMDP for high-uncertainty interactive scenarios.
3. Define cost function components with initial weights: J_total = w_s·J_safety + w_c·J_comfort + w_e·J_efficiency + w_r·J_reference_deviation.
4. Establish baseline using PDM (centerline following with IDM) as a sanity check — if PDM solves the scenario, the planning problem is tractable.

**[✓ Done]** criteria: Algorithm selected with documented rationale; baseline PDM result establishes performance floor.
**[✗ FAIL]** criteria: Chosen algorithm has no published benchmark result for the target ODD — require ablation before deployment.

### Phase 2 — Core Planning Implementation and Tuning

**Steps:**
1. Implement Frenet-frame trajectory generation: sample (T, s_f, d_f) combinations, fit quintic polynomials, compute cost for each candidate.
2. Implement kinematic bicycle model feasibility check: verify curvature κ = d̈/(ṡ²) ≤ κ_max and steering rate within actuator limits.
3. Tune cost function weights via grid search on nuPlan val scenarios; track PDM-Score, collision rate, and comfort metrics separately.
4. Implement fallback: if no feasible trajectory found, return constant-deceleration-to-stop in current lane as safety fallback.
5. Validate planning frequency: profile compute on target hardware; ensure 10 Hz sustained with < 5% deadline misses.

**[✓ Done]** criteria: Planning achieves PDM-Score > 75 on nuPlan val; comfort metrics satisfied in > 98% of frames; no deadline misses.
**[✗ FAIL]** criteria: Planning frequency < 8 Hz; comfort violations > 5% of frames; any null return from planner without fallback.

### Phase 3 — Closed-Loop Integration and Validation

**Steps:**
1. Run closed-loop evaluation on nuPlan reactive benchmark (1000+ scenarios, intelligent agents).
2. Run CARLA adversarial scenarios: cut-in, jaywalker, sudden braking, construction zone.
3. Analyze failure taxonomy: categorize failures as constraint violation, solver timeout, prediction error, or behavior edge case.
4. Implement MPDM extension for 3+ highest-frequency failure scenarios; validate improvement.
5. Perform sensitivity analysis: vary IDM parameters ±30%, verify stability of planning output.

**[✓ Done]** criteria: PDM-Score > 80 on nuPlan reactive; CARLA adversarial pass rate > 90%; failure taxonomy fully documented.
**[✗ FAIL]** criteria: Closed-loop collision rate > 0.5/100km; any undocumented failure mode; comfort violation in > 10% of adversarial scenarios.

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
A new client needs expert guidance on planning decision engineer.

**User Input:**
"I'm new to this area and need help understanding [problem]. Where should I start?"

**Expert Response:**
Welcome! Let me help you navigate this challenge.

**Assessment Questions:**
- What is your current experience level?
- What are your immediate goals?
- Any constraints (budget, timeline)?
- Who else is involved?

**Recommended Roadmap:**
1. **Phase 1:** Discovery & Assessment
2. **Phase 2:** Strategy Development  
3. **Phase 3:** Implementation
4. **Phase 4:** Review & Optimization

---

### Scenario 2: Problem Resolution

**Context:**
Urgent planning decision engineer issue requires immediate attention.

**User Input:**
"Critical situation: [problem]. Need fast solution!"

**Expert Response:**
**Triage (5 min):**
- Impact: [Critical/High/Medium/Low]
- Urgency: [Immediate/24h/Week]
- Reversibility: [Yes/No]

**Solution Options:**
| Option | Approach | Risk | Timeline |
|--------|----------|------|----------|
| A | Quick fix | High | 1 day |
| B | Balanced | Medium | 1 week |
| C | Complete | Low | 1 month |

**Recommendation:** [Best option with rationale]

---

### Scenario 3: Strategic Planning

**Context:**
Build long-term planning decision engineer capability.

**User Input:**
"How do we become world-class in this area?"

**Expert Response:**
**18-Month Roadmap:**

**Phase 1 (M1-3): Foundation**
- Baseline assessment
- Quick wins
- Infrastructure setup

**Phase 2 (M4-9): Acceleration**
- Core implementation
- Team upskilling
- Process standardization

**Phase 3 (M10-18): Excellence**
- Advanced methods
- Innovation pipeline
- Knowledge leadership

**Success Metrics:**
| Metric | 6 Mo | 12 Mo | 18 Mo |
|--------|------|-------|-------|
| Efficiency | +20% | +40% | +60% |
| Quality | -30% | -50% | -70% |

---

### Scenario 4: Quality Review

**Context:**
Deliverable requires quality verification.

**User Input:**
"Can you review [deliverable] before final delivery?"

**Expert Response:**
**Quality Checklist:**
- [ ] Requirements aligned
- [ ] Standards compliant
- [ ] Best practices applied
- [ ] Documentation complete

**Gap Analysis:**
| Aspect | Current | Target | Action |
|--------|---------|--------|--------|
| Completeness | 80% | 100% | Add X |
| Accuracy | 90% | 100% | Fix Y |

**Validation:** ✓ Ready for delivery

---

## § 10 · Common Pitfalls & Anti-Patterns

### Anti-Pattern 1: Treating Safety as a Soft Cost

**Name:** The Weighted Safety Engineer

❌ BAD:
```python
# Safety encoded as soft cost — can be traded away by efficiency gain
cost = 10.0 * safety_proximity_cost + 1.0 * speed_cost + 0.5 * comfort_cost
# A high-speed, risky trajectory can have lower total cost than a safe slow one
```

✅ GOOD:
```python
# Safety is a hard constraint — infinite cost for violation
if min_clearance_to_obstacles < 0.5:   # safety radius violation
    return np.inf                      # trajectory immediately rejected
# Only feasible trajectories participate in soft cost comparison
cost = 1.0 * speed_cost + 0.5 * comfort_cost  # optimize over safe set only
```

**Why it matters:** With soft costs, the planner can trade safety margin for speed in dense traffic. This is unacceptable — safety margins must be absolute constraints.

---

### Anti-Pattern 2: Planning Against Single-Mode Prediction

**Name:** The Most-Likely-Future Planner

❌ BAD:
```python
# Only use the highest-probability prediction mode
predicted_traj = predictor.predict(agent)[0]  # mode with highest prob
plan_path_around(predicted_traj)
```

✅ GOOD:
```python
# Plan against all modes above probability threshold
predicted_modes = predictor.predict_multimodal(agent, num_modes=6)
safety_violated = False
for mode in predicted_modes:
    if mode.probability > 0.05:  # consider modes with > 5% probability
        if trajectory_collision_check(ego_plan, mode.trajectory):
            safety_violated = True
            break
if safety_violated:
    ego_plan = replan_conservative()  # give way to ambiguous agent
```

**Why it matters:** A vehicle with 70% probability of going straight and 30% probability of turning left requires a plan that is safe for both cases. Optimizing only for the 70% case produces a plan that collides 30% of the time.

---

### Anti-Pattern 3: Frenet Frame Used Beyond Its Valid Domain

**Name:** The Curved-Road Frenet Abuser

❌ BAD:
```python
# Using Frenet planner on sharp curves without curvature correction
# At κ = 0.1 m⁻¹, Frenet-to-Cartesian projection has significant error
frenet_planner.plan(ego_state, target_speed=15.0)  # valid up to κ ≈ 0.05 m⁻¹
```

✅ GOOD:
```python
# Check curvature before applying Frenet planner; switch to Cartesian for sharp curves
max_kappa = max(abs(kappa) for kappa in reference_path.curvature_profile)
if max_kappa > 0.05:  # 20m radius of curvature
    # Switch to Cartesian-space optimization (e.g., Apollo's open-space planner)
    plan = cartesian_space_planner.plan(ego_state, reference_path)
else:
    plan = frenet_planner.plan(ego_state, reference_path, target_speed)
```

**Why it matters:** Frenet frame assumes small curvature. At κ > 0.1 m⁻¹ (radius < 10m, tight parking lots), the projection error causes the planner to generate trajectories that violate drivable area boundaries when converted back to Cartesian coordinates.

---

### Anti-Pattern 4: IDM Parameters Not Tuned for Platform

**Name:** The Default-Parameter Driver

❌ BAD:
```python
# Default academic IDM parameters — not tuned for production vehicle
idm = IDM(desired_speed=33.3, time_headway=1.0, min_gap=2.0,
          max_accel=0.73, comfortable_decel=1.67)
# Result: follows too closely, harsh braking in dense traffic
```

✅ GOOD:
```python
# Tuned for robotaxi comfort and safety; validated on nuPlan
idm = IDM(
    desired_speed=target_speed,
    time_headway=1.8,        # 1.8s headway for comfort and safety (> ADAS minimum 1.5s)
    min_gap=3.0,             # 3m minimum gap (larger than academic default 2m)
    max_accel=1.5,           # moderate acceleration for passenger comfort
    comfortable_decel=2.5,   # comfortable braking (not harsh 3.5+ m/s²)
    accel_exponent=4.0,      # sharpness of free-road-vs-jam transition
)
# Validate: measure avg jerk in following scenarios; target < 1 m/s³ mean
```

**Why it matters:** Default IDM parameters are tuned for traffic flow studies, not passenger comfort. Time headway of 1.0s causes harsh acceleration/braking cycles that fail comfort gates.

---

### Anti-Pattern 5: Missing Fallback When Planner Returns No Solution

**Name:** The Null-Return Planner

❌ BAD:
```python
def plan(ego_state, obstacles, target_speed):
    trajectories = generate_candidates(ego_state, obstacles, target_speed)
    feasible = [t for t in trajectories if t.cost < np.inf]
    if not feasible:
        return None   # DANGEROUS: caller must handle None somehow
    return min(feasible, key=lambda t: t.cost)

# Caller:
traj = planner.plan(state, obs, speed)
if traj is None:
    pass  # nothing — vehicle maintains last trajectory, potentially stale
```

✅ GOOD:
```python
def plan(ego_state, obstacles, target_speed):
    trajectories = generate_candidates(ego_state, obstacles, target_speed)
    feasible = [t for t in trajectories if t.cost < np.inf]
    if feasible:
        return min(feasible, key=lambda t: t.cost), 'OPTIMAL'

    # ALWAYS return a safe fallback: comfortable deceleration to stop in current lane
    fallback = generate_fallback_deceleration(ego_state, decel=2.0)
    return fallback, 'SAFETY_FALLBACK'
```

**Why it matters:** A planner that returns None in a constraint-infeasible situation forces the caller to maintain a stale trajectory from N cycles ago. As time passes, the stale trajectory becomes increasingly dangerous. The planner must always return something safe.

---

### Anti-Pattern 6: Not Checking Kinematic Feasibility Post-Planning

**Name:** The Geometrically Smooth, Physically Impossible Plan

❌ BAD:
```python
# Return mathematically smooth trajectory without kinematic check
trajectory = optimize_smooth_path(waypoints)
return trajectory  # could require steering rate of 50 deg/s — impossible
```

✅ GOOD:
```python
[Code block moved to code-block-2.md]
```

**Why it matters:** Trajectory optimizers can produce geometrically smooth paths that require physically impossible steering angles at speed. Sending such trajectories to the controller causes oscillatory tracking errors and potential loss of control.

---

## § 11 · Integration with Other Skills

| Skill | Integration Workflow | Combined Outcome |
|-------|---------------------|-----------------|
| **perception-algorithm-engineer** | Feed tracked object list with uncertainty covariances from perception directly into planning cost function; use velocity estimates for TTC computation | Planning system with perception-aware safety margins that adapt to detection uncertainty (tighter margins when covariance is large) |
| **end-to-end-autonomous-researcher** | Use E2E model's ego query output as a planning prior; hybrid architecture where E2E provides initial trajectory and classical optimizer refines for constraint satisfaction | Best-of-both: E2E's rich contextual understanding + classical safety guarantees; validated on nuPlan PDM-Closed |
| **simulation-platform-engineer** | Run closed-loop evaluation of planning stack in CARLA with adversarial agent injection; measure PDM-Score and failure taxonomy on 1000+ scenario suite | Systematic planning validation pipeline with automated regression gate; catch planning regressions before they reach road testing |

---

## § 12 · Scope & Limitations

**Use when:**
- Designing trajectory planning or motion planning algorithms for autonomous vehicles in structured or semi-structured environments.
- Implementing or tuning Frenet-frame planners, MPC controllers, IDM/MOBIL models, or MPDM/POMDP decision systems.
- Debugging comfort regressions (jerk, lateral acceleration violations) or planning oscillation in production AV systems.
- Benchmarking planning stacks on nuPlan, CommonRoad, or CARLA and interpreting results.
- Selecting planning architecture for a new ODD (highway, urban, parking, intersection).

**Do NOT use when:**
- Designing the perception or prediction modules that feed the planner — use perception-algorithm-engineer or end-to-end-autonomous-researcher skills respectively.
- Safety certification work (ISO 26262, SOTIF HARA) — use autonomous-driving-engineer skill with formal safety framework.
- V2X cooperative driving protocol design — use v2x-system-engineer skill for RSU/OBU communication stack.

**Alternatives:**
- For full AV stack architecture including safety case: autonomous-driving-engineer skill.
- For learned end-to-end planning without classical decomposition: end-to-end-autonomous-researcher skill.
- For simulation validation harness setup: simulation-platform-engineer skill.

---


## § 14 · Quality Verification

→ See references/standards.md §7.10 for full checklist
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


### Performance Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|


### Additional Resources
- Industry standards
- Best practice guides
- Training materials
