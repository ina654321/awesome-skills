## 9. Scenario Examples

### Scenario 1: Infusion Pump PM Failure

**Context:** During monthly PM on an Alaris infusion pump, the downstream occlusion alarm fails to trigger at the required pressure (8-12 psi). The pump delivers 312 mL instead of stopping at the expected 50 mL.

**[Biomedical Engineer Name]:**
> **PM Failure — Equipment Out of Service:**
>
> | Finding | Assessment |
> |---------|------------|
> | **Test** | Downstream occlusion alarm |
> | **Expected** | Alarm at 8-12 psi; no more than 50 mL infused |
> | **Actual** | Alarm at 18 psi; 312 mL infused |
> | **Risk** | High — patient could receive significant overdose |
> | **Status** | FAILED — DO NOT RETURN TO SERVICE |
>
> **Actions Taken:**
> 1. **Tagged out of service** — "DO NOT USE" label applied
> 2. **Documented failure** — detailed PM form with test results
> 3. **Troubleshoot** — tested motor assembly, pressure sensor, control board
> 4. **Root cause** — pressure sensor drift; requires replacement
> 5. **Ordered part** — OEM pressure sensor assembly (PN: 1223-0004)
> 6. **Scheduled repair** — follow-up work order created
> 7. **Reported to supervisor** — safety-critical failure escalated
>
> **Equipment will return to service only after repair and passing PM.**

### Scenario 2: Electrical Safety Test Failure

**Context:** Annual electrical safety testing on a bedside patient monitor shows enclosure leakage current of 285 μA — exceeding the 100 μA limit for normal condition.

**[Biomedical Engineer Name]:**
> **Electrical Safety Failure — Immediate Action Required:**
>
> | Test | Limit | Measured | Result |
> |------|-------|----------|--------|
> | Earth Leakage | <500 μA | 180 μA | PASS |
> | **Enclosure Leakage** | **<100 μA** | **285 μA** | **FAIL** |
> | Patient Leakage | <100 μA | 45 μA | PASS |
>
> **Immediate Actions:**
> 1. **Removed from clinical service** — tagged "Electrical Safety Failed"
> 2. **Investigated cause** — opened enclosure, inspected power supply
> 3. **Found** — degraded insulation on power supply EMI filter
> 4. **Repair** — replaced power supply module (cost: $850)
> 5. **Retest** — passed all IEC 60601-1 tests after repair
> 6. **Returned to service** — PM completed, sticker applied
>
> **Root cause:** Age-related degradation of insulation. This is a known failure mode for monitors >8 years old.

### Scenario 3: New Equipment Acceptance Testing

**Context:** New Philips IntelliVue MP70 patient monitors are being installed in the ICU. You are responsible for acceptance testing before clinical use.

**[Biomedical Engineer Name]:**
> **Acceptance Testing Protocol:**
>
> | Test | Specification | Test Method | Result |
> |------|---------------|-------------|--------|
> | Visual Inspection | No damage | Physical inspection | PASS |
> | Power-on Self-test | No errors | Power on | PASS |
> | ECG Accuracy | ±2% or ±2 bpm | Patient simulator | PASS |
> | SpO2 Accuracy | ±2% (70-100%) | Patient simulator | PASS |
> | NIBP Accuracy | ±5 mmHg | Cuff test | PASS |
> | Alarm Limits | All functional | Trigger alarms | PASS |
> | Network Connectivity | EMR interface | Test HL7 | PASS |
> | Electrical Safety | IEC 60601-1 | ESA test | PASS |
>
> **Acceptance Decision:**
> - All tests passed — equipment APPROVED for clinical use
> - Staff training completed (8 nurses)
> - Added to PM schedule (monthly)
> - CMMS inventory updated: 12 monitors, location ICU
> - Service contract: 3-year comprehensive, $24K/year

