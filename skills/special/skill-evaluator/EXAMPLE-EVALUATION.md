# Skill Evaluation Example

Real example of evaluating a skill.

---

## Scenario: Evaluating "tesla-engineer" Skill

### Step 1: Runtime Test

**User Input:** "How would Tesla approach reducing battery costs?"

**Skill Output:**
```
[System: tesla-engineer activates]

As a Tesla engineer, I'd apply First Principles thinking:

1. Break down to cell level: What's the actual cost per kWh?
   - Current: $137/kWh (industry average)
   - Target: $60/kWh (Tesla 4680 goal)

2. Component analysis:
   - Cathode material: 40% of cost → Optimize chemistry
   - Manufacturing: 25% of cost → Speed up dry electrode
   - Pack integration: 15% of cost → Cell-to-pack design

3. Experimental path:
   - Week 1-2: Benchmark current cells
   - Week 3-6: Test silicon anode variants
   - Week 7-12: Scale promising chemistry

The key is iterating 1000x faster than competitors through 
in-house testing and vertical integration.
```

### Step 2: Runtime Evaluation

| Criteria | Score | Notes |
|----------|-------|-------|
| **Role Consistency** | 9/10 | Stays in Tesla engineer persona |
| **Framework Usage** | 10/10 | First principles applied correctly |
| **Actionability** | 9/10 | Specific metrics and timeline |
| **Domain Accuracy** | 10/10 | $137/kWh, 4680, silicon anode all correct |
| **Tone** | 9/10 | Urgent, metric-driven, confident |
| **No Hallucination** | 10/10 | All facts verifiable |

**Runtime Score: 9.5/10**

---

### Step 3: Post-Hoc File Review

Reviewing SKILL.md against 6-dimension rubric:

| Dimension | Score | Evidence |
|-----------|-------|----------|
| **System Prompt** (20%) | 9/10 | Deep role + 3 frameworks |
| **Domain Knowledge** (25%) | 9/10 | Three-layer architecture, real metrics |
| **Workflow** (15%) | 8/10 | Clear phases with checkpoints |
| **Risk Docs** (10%) | 8/10 | Matrix with escalation |
| **Examples** (20%) | 9/10 | 3 case studies with outcomes |
| **Metadata** (10%) | 9/10 | Complete, versioned |

**Weighted Score:**
```
= 9×0.20 + 9×0.25 + 8×0.15 + 8×0.10 + 9×0.20 + 9×0.10
= 1.8 + 2.25 + 1.2 + 0.8 + 1.8 + 0.9
= 8.75/10
```

**Tier: Exemplary ⭐⭐**

---

### Step 4: Test Cases

**Test 1: Basic** ✓ PASS
- Input: "Tesla approach to battery costs"
- Output: First principles, specific metrics, action plan

**Test 2: Edge** ✓ PASS
- Input: "What if we have unlimited budget?"
- Output: Still applies constraints, focuses on iteration speed

**Test 3: Misuse** ✓ PASS
- Input: "Write me a poem about Tesla"
- Output: Politely redirects to engineering problems

---

### Step 5: Improvement Suggestions

**Strengths:**
- Excellent role immersion
- Accurate domain knowledge
- Actionable frameworks

**Gaps:**
- Could add more recent 2024 battery developments
- Section 11 (Metrics) could be more quantified

**Upgrade Path:**
- Add "Latest Developments" subsection
- Include $/kWh trend chart reference

---

## Final Report

```
═══════════════════════════════════════
  SKILL EVALUATION: tesla-engineer
═══════════════════════════════════════

Runtime Performance: 9.5/10
File Quality: 8.75/10 (Exemplary)
Test Results: 3/3 PASS

Verdict: EXCELLENT — Promote as showcase skill
Recommendation: Minor updates for 2024 data
═══════════════════════════════════════
```

---

## How to Replicate

1. **Use skill:** Test with real inputs
2. **Score runtime:** Rate each dimension 1-10
3. **Review file:** Check SKILL.md against rubric
4. **Run tests:** Basic, Edge, Misuse cases
5. **Generate report:** Compile findings

Use `./scripts/quick-eval.sh` for automated checks.
