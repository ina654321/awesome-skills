# CNC Operator — Real-World Scenarios

## Scenario 1: New Program First Run

**Context:** You have written a new G-code program for a 4-inch aluminum housing. The program uses a 1/2" 3-flute carbide endmill for the pockets. This is the first run.

**Preparation steps:**
1. Load program into CNC control
2. Verify machine model matches program (Haas, Fanuc, Mazak)
3. Check tool list matches available tooling
4. Verify work coordinates (G54) are set correctly
5. Run dry-run mode — watch for collisions at 100% rapid
6. Clear dry-run, proceed to first part

**First part in single-block mode:**
1. Press cycle start
2. Stop at each tool change, verify correct tool installed
3. Stop before first cut, verify datum position
4. Complete first part and measure immediately

**Measurement results:**
- Pocket depth: 0.510" (target 0.500")
- Pocket width: 1.002" (target 1.000")
- Position: Correct

**Adjustments needed:**
- Depth is +0.010" — tool length offset needs to be reduced by 0.010"
- Width is within tolerance
- Apply Z offset adjustment in control, run second part

**Verification:**
- Second part measures: 0.498" — within tolerance
- Approve for production run

## Scenario 2: Aluminum Production Run Going Slow

**Context:** Running 500 units of aluminum brackets. Currently taking 18 minutes per part. Engineering says 12 minutes is required. Machine is a 3-axis vertical mill with 12,000 RPM spindle.

**Diagnosis:**
- Part has 8 pockets, 6 through-holes, 2 tapped holes
- Roughing: 0.030" DOC, full depth
- Finishing: 0.010" cleanup
- Current tools: HSS endmill for roughing

**Analysis:**
- HSS endmill in aluminum at 18 min/part = slow
- Carbide would cut 3-5× faster
- Current spindle speed: 1,500 RPM (HSS limited)
- Carbide allows: 6,000+ RPM

**Solution:**
1. Replace HSS with carbide 1/2" 3-flute endmill
2. New parameters:
   - Speed: 6,000 RPM (SFM: 942)
   - Feed: 0.004 IPR = 72 IPM
   - DOC: 0.050" roughing, 0.010" finishing
3. Expected cycle time: 10-12 minutes
4. Tool life: ~200 parts per insert (replace mid-run)

**Result:** Cycle time reduced to 11 minutes. 500 parts completed in 91.7 hours vs. estimated 150 hours.

## Scenario 3: Taper Problem on Turned Part

**Context:** Lathe turning a 2-inch diameter shaft. After rough and finish turning, the diameter measures larger at the tailstock end. Taper: 0.015" over 6 inches.

**Diagnosis:**
- Consistent taper suggests either:
  1. Tailstock misalignment
  2. Chuck pressure pushing workpiece toward headstock
  3. Tool offset shifting under cutting force

**Check sequence:**
1. Measure part at multiple points along length
2. If taper is consistent: tailstock or alignment issue
3. If only one end is off: tool shift or clamping issue

**Measurement:**
- Near chuck (Z=0): 1.998"
- Mid-point: 2.005"
- Near tailstock (Z=6"): 2.013"
- Taper confirmed: 0.015" total over 6"

**Root cause: Tailstock misalignment**
- Set up dial indicator on workpiece at tailstock
- Run indicator along workpiece length
- Tailstock center is 0.015" off from headstock center
- Adjust tailstock position and re-indicate

**Alternative fix:**
- If tailstock cannot be adjusted: program compensation
- Add small Z-axis correction in CAM to account for taper

## Scenario 4: Tool Change Malfunction

**Context:** During a production run, the machine's ATC (automatic tool changer) grabs a tool but doesn't release it properly.

**Immediate Actions:**
1. Press E-stop immediately
2. Do not attempt to manually remove tool
3. Inspect what happened — was the tool released into the carousel or is it partially engaged?

**Diagnosis:**
- Tool appears partially seated in spindle
- Possible issues: dirty taper, worn drawbar, or ATC mechanism failure

**Resolution steps:**
1. Clear chips from spindle taper area
2. Use tool release procedure (M28 on Fanuc)
3. If tool still stuck: maintenance required
4. Document incident for maintenance log

**Prevention:**
- Clean taper before every tool change
- Check for chip contamination
- Regular ATC maintenance schedule
- Monitor tool change cycle time — increase indicates wear

## Scenario 5: Thermal Expansion During Long Run

**Context:** Running a 24-hour unattended production run on steel parts. First 20 parts measure perfectly. Parts 50-100 show increasing diameter.

**Diagnosis:**
- Systematic positive drift indicates thermal growth
- Machine warms up from spindle/coolant heat
- Steel expands approximately 0.0006" per inch per 10°F

**Analysis:**
- Part is 4" diameter
- Observed growth: 0.008" over 8 hours
- Equivalent to ~3.3°F temperature rise
- Machine reaches thermal equilibrium, then overshoots

**Solutions:**
1. **Thermal compensation** — Most modern controls have thermal compensation. Enable and calibrate.
2. **Active cooling** — Use coolant at constant temperature; avoid heating from spindle
3. **Warm-up procedure** — Run machine 20-30 minutes at operating temperature before production
4. **In-process measurement** — Measure parts periodically and adjust offsets
5. **Programmed compensation** — Add small Z-offset drift compensation in program

**Best practice:** Implement thermal compensation in control, verify with test bar measurement at start and mid-run.
