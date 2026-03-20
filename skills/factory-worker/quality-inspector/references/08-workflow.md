# Quality Inspector — Troubleshooting Guide

## Measurement Problems

**Problem: Two inspectors get different readings on the same part**
- Diagnosis: Measurement system variation or inspector technique difference
- Check: Is the measurement system capable (gauge R&R study)?
- Check: Is measurement taken at same location on part?
- Check: Is temperature controlled? (Metal expands/contracts)
- Check: Are inspectors using the same technique?
- Resolution: Perform gauge R&R study; standardize technique; use same gauge

**Problem: Part measures in tolerance but assembly fails**
- Diagnosis: Combined tolerance stack-up or wrong measurement location
- Check: Are you measuring the functional feature or a cosmetic one?
- Check: Is the tolerance stack-up from multiple parts exceeding acceptable range?
- Check: Has the drawing been interpreted correctly?
- Resolution: Review functional requirements with engineering; measure all critical dimensions

**Problem: Micrometer reads consistently high (known-good master)**
- Diagnosis: Instrument damage, zero error, or temperature issue
- Check: Clean the micrometer faces; check for debris
- Check: Zero the micrometer on master gauge
- Check: Is master gauge certified and within calibration?
- Check: Allow part and gauge to reach room temperature
- Resolution: Return out-of-calibration gauges; repair or replace damaged instruments

**Problem: CMM results don't match hand measurements**
- Diagnosis: Reference frame difference, probe offset, or thermal drift
- Check: Is CMM datum aligned with part datum?
- Check: Is part properly placed on CMM fixture?
- Check: Has CMM been thermally compensated?
- Check: Probe qualification current?
- Resolution: Re-fixture part; recalibrate CMM; consult metrology specialist

## Inspection Process Problems

**Problem: Lot rejected at AQL but inspection feels subjective**
- Diagnosis: Attribute inspection relies on inspector judgment
- Check: Are defect definitions documented and clear?
- Check: Was the same inspector evaluating all samples?
- Check: Was lighting adequate for visible defects?
- Resolution: Implement visual standard samples; use attribute grading scales; consider switching to variable measurements

**Problem: Supplier disputes rejection (part passes with another gauge)**
- Diagnosis: Gauge variation or measurement location difference
- Check: Compare both gauges on master specimen
- Check: Measure at exact same location on disputed part
- Check: Verify both gauges are within calibration
- Resolution: Use calibrated reference gauge; document measurement discrepancy; review gauge capability

**Problem: Incoming inspection finds defect but supplier claims it was at supplier's spec limit**
- Diagnosis: Tolerancing interpretation dispute
- Check: Is the drawing spec clear about measurement method?
- Check: Is the defect functional (affects fit/form/function) or cosmetic?
- Resolution: Reference ANSI/ASQ Z1.4 rules; invoke contractual AQL; if functional: reject regardless of AQL

## Documentation Problems

**Problem: NCR form incomplete or inconsistent**
- Diagnosis: Inspector rushing or unclear on requirements
- Check: Required fields completed? (Date, lot #, defect description, quantities)
- Check: Are photos attached?
- Check: Has disposition authority signed?
- Resolution: Complete NCR before releasing; use checklist; supervisor review of NCRs

**Problem: Disputed NCR — engineering says to accept parts**
- Diagnosis: Communication gap between quality and engineering
- Action: If functional defect: Quality cannot approve out-of-spec parts
- Action: If cosmetic at limit: Request engineering deviation/waiver
- Process: Engineering must formally accept via deviation document
- Document: All decisions in writing, signed by authorized personnel

**Problem: Inspection records lost or incomplete**
- Diagnosis: Poor documentation practices
- Prevention: Inspect and document immediately; use digital systems; no inspecting without recording
- Resolution: Retrace steps if possible; reconstruct from available data; implement better controls

## Defect Classification Problems

**Problem: Unclear whether defect is major or critical**
- Diagnosis: Classification criteria not clear for this defect type
- Check: Does it affect safety? → Critical
- Check: Does it affect function? → Major (at minimum)
- Check: Is it visible/in cosmetic? → Minor
- When in doubt: Classify higher; require engineering review
- Prevention: Maintain defect classification guide with examples

**Problem: Defect appears on multiple parts — pattern failure**
- Diagnosis: Systematic issue, not random inspection error
- Action: Quarantine all affected lots
- Action: Initiate supplier corrective action request
- Action: Implement 100% inspection of suspect production
- Prevention: Track defect trends; early detection of patterns

## Gauge & Equipment Problems

**Problem: Gauge due for calibration during production**
- Action: Remove gauge from service; replace with calibrated spare
- Do NOT use out-of-calibration gauge — invalidates all inspection results
- Prevention: Maintain calibration schedule with spare gauges

**Problem: Gauge R&R shows >30% of tolerance variation from gauge**
- Diagnosis: Gauge is not capable for the tolerance required
- Action: Use more precise gauge; consider upgrading measurement capability
- Action: Widen acceptance criteria if possible (engineering approval required)
- Prevention: Perform gauge studies before selecting gauges for critical dimensions

**Problem: Temperature fluctuation causing measurement drift**
- Diagnosis: Room temperature not controlled (standard: 68-72°F)
- Action: Allow parts and gauges to stabilize at room temperature for 30+ minutes
- Action: Measure in controlled environment
- Prevention: Maintain temperature-controlled inspection room; use thermal compensation

## Sampling Problems

**Problem: Sample size calculation disputes**
- Diagnosis: Different parties using different confidence levels
- Resolution: Reference ANSI/ASQ Z1.4 standard tables
- Standard: General Inspection Level II is default
- AQL: Agreed upon in quality agreement
- Document: Always cite standard used in inspection records

**Problem: Small lot size — need to inspect all parts**
- Decision rule: If lot size < sample size from Z1.4 tables, inspect 100%
- Example: Lot of 8 pieces < sample size 13 (from 26-50 lot size)
- Action: 100% inspection required for lot
- Document: Note "lot size less than minimum for AQL sampling — 100% inspection performed"
