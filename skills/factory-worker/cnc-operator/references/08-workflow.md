# CNC Operator — Troubleshooting Guide

## Chatter & Vibration Problems

**Problem: Severe chatter marks on finished surface**
- Diagnosis: Measure wavelength of marks to identify source frequency
- Causes: Too much DOC, wrong spindle speed, loose workholding, long tool stick-out
- Fix:
  1. Reduce DOC by 25-50%
  2. Change spindle speed to find resonance-free zone (try ±20%)
  3. Shorten tool stick-out
  4. Check workholding rigidity
  5. Add damping if available

**Problem: Vibration marks at regular intervals**
- Diagnosis: Regular spacing indicates specific frequency source
- Check: Spindle bearing condition, chuck runout, tool holder condition
- Fix: Replace worn bearings; check chuck for wear; verify tool holder taper

**Problem: Surface finish worse in one area of workpiece**
- Diagnosis: Likely uneven clamping or workpiece distortion
- Check: Magnetic chuck flatness; vacuum chuck sealing; clamps properly distributed
- Fix: Re-clamp or add support; check for workpiece distortion from prior operations

## Dimensional Accuracy Problems

**Problem: Part dimensions consistently off by same amount**
- Diagnosis: Systematic error = offset problem, not random variation
- Check: Tool length offsets — are they set correctly?
- Check: Work coordinate — did you re-set after tool change?
- Check: Machine thermal growth — is machine warmed up?
- Check: G54/G55 correct?
- Fix: Re-touch tools; verify work coordinates; let machine warm up 20+ minutes

**Problem: Dimensions vary across the part (锥度 or bow)**
- Diagnosis: Part deflection under cutting force
- Check: Cantilever length — is too much material unsupported?
- Fix: Add work support; reduce depth of cut; increase rigidity of fixture

**Problem: Dimensions drift over time during a run**
- Diagnosis: Thermal growth or tool wear
- Check: Ambient temperature variation; coolant temperature
- Fix: Implement in-process gauging; compensate for thermal drift; replace worn tools

**Problem: First piece good, subsequent pieces out of spec**
- Diagnosis: Tool wear, thermal shift, or chip packing
- Check: Measure tool after first piece (compare to initial offset)
- Check: Coolant flow — is it maintaining temperature?
- Fix: Adjust tool offsets mid-run; implement tool wear compensation

## Tool Breakage & Wear

**Problem: Tool breaks suddenly mid-cut**
- Diagnosis: Root cause — too much force, impact load, or fatigue
- Causes: Too high feed rate, too low speed (rubbing), worn tool, hard spot in material
- Prevention:
  1. Use correct feeds and speeds for material
  2. Inspect tools before each run for wear/damage
  3. Use chip load monitoring if available
  4. Ensure correct chip flute geometry for material

**Problem: Premature tool wear on one job**
- Diagnosis: Identify wear pattern
- Crater wear (top face): Too high speed, use harder grade
- Flank wear (side): Normal — but excessive indicates wrong parameters
- Built-Up Edge (BUE): Too low speed, too high feed, improve coolant
- Chipping: Micro-chipping indicates vibration or wrong grade

**Problem: Carbide insert cracked or broken**
- Causes: Thermal shock (coolant on hot insert), impact load, wrong insert grade
- Prevention: Pre-heat coolant gradually; use appropriate insert grade; avoid interrupted cuts with weak grades

## Surface Finish Problems

**Problem: Bumpy or ridged finish on flat surfaces**
- Diagnosis: Feed rate too high or tool too coarse
- Fix: Reduce feed rate per tooth; use finer stepover; check for tool deflection

**Problem: Burn marks on aluminum surface**
- Diagnosis: Too slow spindle speed (causing welding) or too heavy cut
- Fix: Increase spindle RPM; reduce feed rate; improve coolant delivery; check tool geometry

**Problem: Sanding marks (fine scratches)**
- Diagnosis: Too coarse abrasive grain size or dull tool
- Fix: Resharpen/replace tool; use finer stepover for finishing pass

**Problem: Orange peel texture**
- Diagnosis: Too high feed rate or tool too dull to shear cleanly
- Fix: Reduce feed rate; sharpen tool; try different tool geometry

## Programming & Control Problems

**Problem: Program runs but produces wrong dimensions**
- Diagnosis: Is it a machine issue or program issue?
- Check: Verify correct tool number in program matches spindle
- Check: Verify correct offset values in control
- Check: Verify work coordinate matches part datum location
- Check: Verify correct fixture offset if used

**Problem: Tool change goes to wrong position**
- Diagnosis: Tool change position not set or wrong
- Fix: Check G28 reference return; verify tool change M06 code position
- Prevention: Test tool change path in MDI before running program

**Problem: Cutter compensation causing wrong dimensions**
- Diagnosis: Using wrong compensation direction or wrong diameter value
- Check: G41 vs G42 — should match cut direction
- Check: Tool diameter in program vs actual measured diameter
- Check: Worn tool diameter vs fresh insert diameter

## Machine Operation Problems

**Problem: Spindle won't start**
- Diagnosis: Check door interlocks, E-stop, and spindle load
- Check: Is the spindle overload tripped?
- Check: Coolant levels (some machines won't start without coolant)
- Check: Air pressure if pneumatic clamping

**Problem: Chuck won't open/close**
- Diagnosis: Hydraulic pressure, air supply, or control signal issue
- Check: Hydraulics pressure gauge
- Check: Chuck lubrication
- Check: Control M-code for chuck (M10/M11, M12/M13)

**Problem: Coolant not flowing**
- Diagnosis: Pump, line blockage, or nozzle position
- Check: Pump prime — air in lines?
- Check: Coolant level in tank
- Check: Nozzle clogged or aimed incorrectly
- Check: Coolant pressure setting
