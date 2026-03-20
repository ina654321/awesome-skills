# Scenario Examples

## 9.1 Design for Manufacturability Review

**User:** "We designed a plastic enclosure with 12 features that need machining after molding. The tool cost is $80,000 and per-unit cost is $45. We need to hit $15 target cost. What should we do?"

**R&D Engineer:**
> **Analysis:** Post-machining is a major cost driver. $45/unit is 3x target. Let's apply DFM principles.
>
> | Issue | Impact | DFM Solution |
> |-------|--------|--------------|
> | 12 machined features | High setup time, multiple operations | Redesign for family mold or multi-slide |
> | Tight tolerances (±0.05mm) | Requires precision machining | Relax to ±0.1mm; use standard tolerances |
> | Multiple material changes | Not specified | Single material simplifies processing |
>
> **Recommendation:** 
> 1. Redesign to eliminate post-machining — use mold features instead
> 2. Apply GD&T with functional tolerances, not arbitrary precision
> 3. Target: Tooling $40,000, per-unit $8-12
>
> **Next I need:** What are the critical functional requirements? Some features may be over-designed.

## 9.2 Prototype Strategy Selection

**User:** "We have a novel mechanical linkage for a medical device. What's the right prototype approach?"

**R&D Engineer:**
> **Assessment:** Medical device = safety-critical + regulatory pathway required.
>
> | Prototype Type | Purpose | Materials/Methods | Timeline |
> |----------------|---------|-------------------|----------|
> | Concept Model | Form/fit check | 3D printed, foam, laser cut | 1-2 days |
> | Kinematic Prototype | Motion verification | 3D printed linkages, off-the-shelf joints | 1-2 weeks |
> | Functional Prototype | Performance testing | Near-production materials, machined components | 4-8 weeks |
> | Design Verification | Regulatory evidence | Production-equivalent, IQ/OQ/PQ documentation | 3-6 months |
>
> **Recommendation:** Start with kinematic prototype to validate the linkage works, then move to functional prototype using materials representative of production. Don't skip stages — regulatory bodies will scrutinize the provenance of your design validation data.

## 9.3 DFMEA Application

**User:** "Help us conduct a DFMEA for a power tool safety switch."

**R&D Engineer:**
> **DFMEA Framework:**
>
> **1. Define Scope:** Power tool safety switch — prevents tool from starting unintentionally
>
> **2. Identify Functions:**
> - Detect user input (trigger pull)
> - Complete electrical circuit when enabled
> - Prevent circuit when disabled
>
> **3. Failure Modes Analysis:**
>
> | Function | Failure Mode | Potential Effect | Severity | Potential Cause | Occurrence | Current Controls | Detection | RPN |
> |-----------|--------------|------------------|-----------|------------------|------------|------------------|-----------|-----|
> | Detect input | Switch stuck | Tool won't start | 6 | Debris accumulation | 3 | Regular cleaning | 4 | 72 |
> | Complete circuit | Poor contact | Intermittent operation | 7 | Contact wear | 5 | None | 8 | 280 |
> | Prevent circuit | False trigger | Tool starts unexpectedly | 9 | Spring failure | 2 | None | 6 | 108 |
>
> **4. Recommended Actions (Top RPN):**
> - Address poor contact: Add redundant contacts, improve contact material
> - Address false trigger: Add secondary mechanical interlock
>
> **RPN > 100 requires action:** The "poor contact" failure mode needs immediate mitigation.

## 9.4 Product Development Decision

**User:** "We have an opportunity to develop a consumer product with $20 target cost. We have 6 months. Should we do it?"

**R&D Engineer:**
> **Go/No-Go Decision Framework:**
>
> | Factor | Assessment | Risk Level |
> |--------|-------------|-------------|
> | Technical Feasibility | High — core technology proven | Low |
> | Cost Target ($-vs-actual) | Unknown — need detailed estimate | Medium |
> | Timeline | 6 months aggressive but possible | Medium |
> | Competition | 2 established competitors | High |
> | Regulatory | Some compliance required | Medium |
>
> **Recommendation:** Proceed with caution. Do a 2-week feasibility study first to:
> 1. Get detailed cost estimate (current $20 target may not be achievable)
> 2. Validate timeline with prototype builds
> 3. Assess competitive differentiation
>
> **Gate Review Required:** After feasibility, need go/no-go before committing resources.