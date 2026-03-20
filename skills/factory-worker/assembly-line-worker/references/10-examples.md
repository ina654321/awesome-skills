# Assembly Line Worker — Real-World Scenarios

## Scenario 1: Andon Pull at Station 4

**Context:** You are at Station 4 and notice that the torque specification on the work instruction says 12 Nm ± 1 Nm, but your torque wrench reads 14 Nm on the first fastener.

**Immediate Actions:**
1. Stop — Do not continue assembling with wrong torque
2. Andon — Pull the Andon cord/button
3. Isolate — Set aside any units assembled with incorrect torque
4. Document — Note which units, what time, what was wrong
5. Communicate — Notify supervisor and quality immediately

**When supervisor arrives:**
- Report: "Andon pulled at Station 4. Torque wrench reading 14 Nm but spec is 12 Nm ± 1. I stopped work."
- Together: Check torque wrench calibration date
- Check: Try another torque wrench from station kit
- Decision: If wrench is wrong, use correct one and re-torque affected units
- If units are scrapped: Document scrap count

**Root Cause Analysis (to participate in):**
- Why did this happen?
- Was the torque wrench dropped or mishandled?
- Was it calibrated correctly?
- How can we prevent this next time?

## Scenario 2: Wrong Component Discovered Mid-Assembly

**Context:** You pick up a capacitor from the bin and notice it has a different marking than what the work instruction shows. The work instruction calls for 100µF but the component reads 47µF.

**Immediate Actions:**
1. Stop — Do not install the wrong component
2. Verify — Check the bin label against the work instruction
3. Check — Look for lot code or supplier differences
4. Quarantine — Do not return to bin (mark as suspect)
5. Report — Notify supervisor and quality

**Why this matters:**
- Wrong component can cause product failure
- 47µF vs 100µF is a significant difference — this will affect function
- Could be a supplier picking error or bin mislabeling

**Investigation steps:**
- Check other components in the bin — are there mixed values?
- Check if this is the only bin affected
- Review receiving records for this lot
- Quality will quarantine and inspect the entire component lot

## Scenario 3: Takt Time Crisis Management

**Context:** Your station typically takes 14 seconds per unit and takt time is 15 seconds. A new product introduction has added two extra fasteners per unit, and you are now taking 18 seconds.

**Immediate Actions:**
1. Pull Andon — Signal that you cannot maintain takt
2. Finish current unit correctly — Do not rush and create quality issues
3. Communicate — Tell supervisor exactly: "18 seconds vs. 15 second takt. Two extra fasteners added."

**With supervisor, analyze the bottleneck:**
- Is the extra work truly necessary at this station?
- Can some fasteners be pre-installed upstream?
- Can the fixture be redesigned to speed insertion?
- Can tools be repositioned to reduce motion?

**Do NOT:**
- Skip torque checks to save time
- Rush and risk quality
- Keep working without telling anyone

**Result:** Supervisor re-evaluates takt time or reassigns work elements. You continue with Andon active until resolved.

## Scenario 4: Tool Count Discrepancy at Shift End

**Context:** During end-of-shift tool count, you count 3 torx screwdrivers but your count-in sheet shows 4.

**Immediate Actions:**
1. Stop — Do not leave the station
2. Search — Look in your immediate work area, under the workstation, in your apron
3. Check — Did a colleague borrow it?
4. Escalate — Notify supervisor immediately
5. Full search — With supervisor, conduct thorough area search
6. Report — If not found, this becomes a documented FOD concern

**Consequences if tool is found inside a completed unit:**
- Unit must be pulled from production
- X-ray or disassembly to locate tool
- Potential quality hold on entire batch

**Prevention:**
- Count tools in AND count tools out every shift
- Never leave tools unattended on workstation edge
- Return tools to designated storage immediately after use
- Visual scan of work area before releasing each unit

## Scenario 5: Engineering Change Notice Mid-Shift

**Context:** During production, an engineer arrives with a revised work instruction. Revision D supersedes Revision C. The engineering change adds a new sealant application step.

**Your response:**
1. Stop current work using old revision
2. Verify — Confirm you have Revision D (check revision number and date)
3. Review — Read the new instruction completely before resuming
4. Ask — Clarify any steps you don't understand
5. Source — Get any new tools or materials required
6. Resume — Start production with new revision

**What if you continued with old revision?**
- Units would not have the sealant
- Potential field failure (leakage)
- Costly recall or rework
- You could be held responsible

**Key principle:** Always check for ECN notifications at shift start and when approached by engineering.
