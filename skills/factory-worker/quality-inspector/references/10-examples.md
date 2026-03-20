# Quality Inspector — Real-World Scenarios

## Scenario 1: AQL Acceptance Decision

**Context:** Lot of 800 machined shafts received. You draw 80 samples (General Inspection Level II). You find 3 major defects and 1 minor defect. AQL is 1.0 for major, 2.5 for minor.

**Analysis using AQL tables:**
- Lot size: 801-1200 → Sample code J → Sample size 80
- Major defects found: 3
- AQL 1.0 acceptance numbers for sample 80: Ac=2, Re=3
- Decision: Major defects = 3, Ac=2, Re=3 → 3 > 2 = REJECT lot
- Minor defects: 1 (AQL 2.5, Ac=5, Re=6) → 1 < 5 = Accept on minor alone

**Required actions:**
1. Reject the lot based on major defect count
2. Quarantine all 800 shafts
3. Initiate NCR and Supplier Corrective Action Request (SCAR)
4. Document: Lot #, defect types, defect locations, quantities
5. Take photos of defects for documentation

**Root cause follow-up questions:**
- Is this an isolated incident or pattern?
- Check previous lots from same supplier
- If pattern: Escalate to supplier quality engineering

## Scenario 2: CTQ Dimension Out of Spec

**Context:** During final inspection of a hydraulic manifold, you measure a critical-to-quality port diameter as 0.625" but drawing shows 0.620" ± 0.002". USL = 0.622". Part is at limit but technically AT SPEC — actually 0.003" OVER USL.

**Classification:**
- This is a CTQ (critical to quality) dimension
- Any out-of-spec on CTQ = potential safety/functional failure
- Hydraulic leak or pressure failure possible

**Your decision:**
- REJECT — The dimension exceeds the upper specification limit
- At-limit is too risky for a CTQ — safety margin is exceeded
- Any measurement uncertainty pushes this further over

**Required actions:**
1. Reject the part
2. Quarantine entire lot pending investigation
3. Pull 10 more parts from lot — measure all
4. If pattern: 100% inspection required
5. Notify quality engineering and design engineering
6. Initiate NCR

**Measurement verification:**
- Check gauge calibration
- Measure on different gauge
- Consider measurement system capability (gauge R&R)
- Verify correct drawing revision is being used

## Scenario 3: Customer Complaint About Defect You Missed

**Context:** A customer returns a product with a scratch on the visible surface. Your final inspection passed this unit. The scratch is 2mm long, on the top panel of an appliance.

**Assessment:**
- Scratch location: Visible top surface = affects appearance
- Scratch length: 2mm — noticeable but not extreme
- Customer is unhappy — affects brand perception

**Root cause analysis:**
1. Was scratch present at final inspection?
   - If visible under good lighting: inspection failure
   - If only visible under certain angles: inspection lighting inadequate
2. Was scratch introduced after inspection?
   - Packaging issue?
   - Shipping damage?

**Corrective actions:**
- Improve inspection lighting to 100 foot-candles minimum
- Add scratch inspection to checklist explicitly
- Check packaging for sharp edges
- Implement anti-scratch material in packaging

**Your role:**
- Document the complaint and findings
- Initiate corrective action request
- Follow up to ensure improvements implemented
- Consider 100% inspection until process stabilized

## Scenario 4: Dispute With Production Over Rejection

**Context:** You rejected a batch of weldments for porosity visible on X-ray. Production supervisor says porosity is "within acceptable limits" and demands you release the lot.

**Your position:**
- X-ray shows voids > specification limit
- Weld strength could be compromised
- This is a functional defect

**Response to supervisor:**
1. Show the X-ray and specification
2. Explain: "Porosity exceeds the 2% maximum per our welding specification"
3. Explain: "I cannot release material that doesn't meet spec"
4. Offer: "You can request engineering disposition"
5. Offer: "Quality engineering can review and make final call"

**If supervisor escalates:**
- Bring in quality engineering manager
- Engineering may issue deviation/waiver if stress analysis shows acceptable
- Or: Rework the weldments
- Or: Scrap if unreworkable

**What you should NOT do:**
- Release material you believe is defective
- Be pressured into changing your assessment
- Skip documentation because of pressure

**Always document:**
- That you were pressured to release
- Your technical basis for rejection
- Engineering's disposition decision

## Scenario 5: Gauge Shows Drift Over Time

**Context:** You track measurements of a standard reference block over 3 weeks. The micrometer shows increasing readings: 0.5001", 0.5002", 0.5003", 0.5004". The master block is certified at exactly 0.5000".

**Analysis:**
- Drift is 0.0004" over 3 weeks
- This exceeds typical calibration stability
- The micrometer is reading progressively high
- Calibration date: Last calibrated 6 weeks ago

**Decision:**
- Pull micrometer from service
- Send for calibration
- Perform retrospective review: Were any parts measured with this micrometer questionable?
- If yes: Identify affected lots, re-inspect with calibrated gauge

**Prevention:**
- Check gauge against master at start of each shift
- Track gauge performance over time
- Don't wait for calibration date if drift is observed

## Scenario 6: Interpreting Inconclusive Test Results

**Context:** A batch of adhesive bonds tested for shear strength. Test results: 420 psi, 445 psi, 398 psi, 460 psi, 435 psi. Minimum requirement is 400 psi. One result (398 psi) is below minimum.

**Analysis:**
- Average: 431.6 psi (above 400 minimum)
- But: Individual result of 398 psi fails
- One failure in 5 tests = 20% failure rate on a pass/fail test

**Your decision:**
- REJECT the batch
- Any individual result below minimum is a failure
- Average above minimum does not override individual failures

**Required investigation:**
- Was the test specimen prepared correctly?
- Was the test performed correctly?
- Was this an anomaly or pattern?
- Request retest of failed specimen location
- Check material lot numbers for any differences

**Document:**
- All individual test results, not just average
- Test method and equipment used
- Specimen preparation method
- Material lot numbers
