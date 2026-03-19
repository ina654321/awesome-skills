# Scenario Examples

## 9.1 Common Scenario: MRI Magnet Training Issues

**User:** Our 1.5T NbTi MRI magnet trained to only 90% of expected current and shows large training steps. What went wrong?

**Expert:**
> **Analysis:**
> Training steps > 5% of operating current indicate frictional motion between coil and former during Lorentz force loading.
>
> 1. Verify preload: coils must be preloaded above maximum Lorentz force (typically 2× operating load)
> 2. Check epoxy impregnation: void fraction should be < 2% by volume
> 3. Review conductor movement: ROXY-style winding with insufficient bladder preload causes inter-turn slippage
> 4. Inspect coil former: surface roughness Ra < 3.2 µm recommended
>
> **Fix:** Warm up and re-preload coils using calibrated shims; repeat cooldown. Target: training steps < 0.5% of operating current after 5 training cycles.
>
> **Prevention:** Implement mandatory pre-stress protocol per IEC 61788-4; use strain gauges during assembly.

## 9.2 Complex Scenario: REBCO Tape Delamination in High-Field Coil

**User:** Our REBCO no-insulation coil shows voltage spikes during fast charging at 400 A/s. Cross-section analysis shows delamination at the substrate layer. How do we diagnose and prevent this?

**Expert:**
> **Comprehensive Solution:**
> Delamination in REBCO tapes under Lorentz force loading is caused by:
> - Insufficient adhesive strength between Hastelloy substrate and REBCO layers
> - Thermal contraction mismatch: CTE of Hastelloy (14 µm/m·K) vs. YBCO (12 µm/m·K)
> - Peel stress from coil winding tension
>
> **Diagnostic steps:**
> 1. Cross-section SEM analysis: identify delamination plane (substrate/Hastelloy interface)
> 2. Peel test per IEC 61788-22: adhesion strength should be > 5 N/cm width
> 3. Finite element analysis: calculate peel stress at winding tension
>
> **Mitigation:**
> 1. Reduce winding tension to < 5 N/mm² for HAST tapes
> 2. Use solder-coating (Sn60Ag40) for additional mechanical bonding
> 3. Apply soft insulation (Kapton) between layers to distribute load
> 4. Consider lamination: Cu-stabilized tapes reduce delamination risk
>
> **Next step:** Replace damaged tapes with higher-adhesion grade (tested per IPC JEDEC J-STD-002); re-wind with reduced tension.

## 9.3 Edge Case: Quench During Persistent Mode Operation

**User:** Our NMR magnet (Nb₃Sn, 23.5T) is in persistent mode at 40 A. The persistent switch opened due to a thermal fluctuation and caused a quench. How do we recover?

**Expert:**
> **Special Handling:**
>
> This is a known risk in high-field persistent-mode magnets with insufficient persistent switch heater coverage.
>
> **Immediate recovery:**
> 1. Do NOT enter the cryostat area during quench — risk of helium release
> 2. Open vent valves if pressure rises above 3 bar
> 3. Allow full quench dump; do not attempt to re-energize until:
>    - All coils above 80K have been warmed to RT
>    - Vacuum integrity confirmed
>    - Helium inventory replenished
>
> **Root cause fix:**
> - Increase switch heater power: 10% above minimum quench energy (MQE) threshold
> - Add redundant switch heater circuit
> - Implement switch heater temperature monitoring
> - Consider persistent current converter (PC) instead of switch for >20T magnets
>
> **Prevention protocol:**
> - Annual switch resistance check: should be < 10^-8 Ω when closed
> - MQE test per IEC 61788-9: verify coil stability margin > 3× MQE
