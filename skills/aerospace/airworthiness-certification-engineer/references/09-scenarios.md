## § 9 Scenario Examples

### Scenario 1: Novel Electric Propulsion System Certification

**User**: We have an eVTOL with 12 distributed electric motors. There's no specific regulation for this configuration. How do we certify it?

**Expert**:
> **This is a classic novel features certification challenge.** Here's the systematic approach:
>
> **Step 1 — Identify the Applicable Basis**:
> For eVTOL, FAA currently uses Part 23 PoweredLift or Part 27 as the basis, depending on weight and configuration. For 12 motors, you'll need Special Conditions (SCs) because standard Part 23/27 doesn't address distributed electric propulsion at this scale.
>
> **Step 2 — Issue Paper (IP) Submission**:
> File an Issue Paper to the ACO covering:
> - Description of the novel feature (12 distributed motors, electric power architecture)
> - Why existing regulations don't adequately address it
> - Proposed means of addressing the novel feature
> - Your proposed equivalent safety level
>
> **Step 3 — Special Conditions Content**:
> Based on eVTOL precedent (Joby S4, Archer Midnight programs), expect Special Conditions addressing:
> ```
> SC-1: Propulsion system reliability
>   → Single motor failure: must complete takeoff and land safely (demonstrated by analysis + flight test)
>   → Dual adjacent motor failure: must not be catastrophic (FTA required; probability < 1×10⁻⁹)
>
> SC-2: Battery system protection
>   → Cell thermal runaway propagation: must not cause loss of aircraft (ARP4761 analysis)
>   → Battery energy depletion: automatic warnings at defined reserve thresholds
>
> SC-3: Flight control redundancy
>   → FBW system with no single failure causing loss of control
>   → Min. dual redundancy for all flight-critical paths (DAL-A, §25.1309 basis)
> ```
>
> **Step 4 — ELOS (Equivalent Level of Safety) Demonstration**:
> For distributed propulsion OEI, you need to show the safety level is equivalent to or better than a single-engine aircraft losing its engine. Use FTA to prove:
> - P(loss of all propulsion) < 1×10⁻⁹/FH
> - Any single motor failure results in ≥ 25% residual hover power
>
> **Timeline**: IP submission → ACO review (3-6 months) → SC publication (6-12 months) → compliance program → typically 18-24 months extra vs. conventional aircraft certification.

