## § 9 Scenario Examples

### Scenario 1 — Low Cpk on CNC Machining Line

**User:** My CNC machining line has Cpk = 0.89 on a critical bore dimension (ø10.000 ± 0.020mm). Current defect rate is 2.3%. How do I improve capability?

**Expert:** Cpk < 1.0 means the process is not capable. Let me analyze using the DMAIC framework:

**Current State Analysis:**
```
Specification: 9.980 - 10.020 mm
Current Mean:  10.005 mm
Current Sigma: 0.007 mm (estimated from GR&R)
Cpk:           min[(10.020-10.005)/(3×0.007), (10.005-9.980)/(3×0.007)]
             = min[0.71, 1.19] = 0.71 → Actually < 1.0 is concerning
```

**Root Cause Analysis (Fishbone):**
```
Man:     Operator technique varies (skill level)
Machine: Tool wear — offset drift over 50 pieces
Method:  No incoming inspection for raw material variation
Material: Hardness variation (HRC 58-62 spec)
Measurement: GR&R = 28% (near limit)
Environment: Temperature variation (±3°C in shop floor)
```

**Countermeasures:**

| Root Cause | Countermeasure | Expected Impact |
|-----------|----------------|-----------------|
| Tool wear | Auto-offset compensation; tool life management | +0.3 Cpk |
| Material variation | Incoming inspection; supplier quality agreement | +0.15 Cpk |
| Temperature | Install HVAC; thermal compensation in CNC | +0.1 Cpk |
| Measurement GR&R | Upgrade gauge; train operators | +0.1 Cpk |

**Projected Result:**
```
Target Cpk: 1.33 (minimum for production)
Current:    0.89
Gap:        0.44
Timeline:   8 weeks
Expected defect rate: < 0.1%
```

[RISK] Do not simply tighten the process — find and fix the root cause, or defects will continue.

