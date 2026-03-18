## § 9 Scenario Examples

### Scenario 1: BEV Platform ADAS Sensor Integration

**User**: We're integrating a LiDAR on the roof for Level 3 autonomy. The styling team wants it flush with the roofline. What are the engineering constraints?

**Expert**:
> **Roof-mounted LiDAR integration is a classic styling vs. engineering conflict.** Here are the constraints:
>
> **1. LiDAR FOV Requirements** (typical Level 3 requirements):
> ```
> 360° horizontal FOV (mechanical or solid-state array)
> Vertical FOV: +15° to -25° (must see ground at ~10m in front)
> Range: 200m for highway L3 (PCNDFs moving @ 130 km/h)
>
> For the vertical FOV to work flush with roofline:
>   At roof height H = 1.5m, ground 10m ahead requires:
>   Depression angle = arctan(1.5/10) = 8.5°
>   → Needs sensor positioned to see 8.5° downward → needs to protrude above roofline
>   or sensor tilted (but this creates aerodynamic issue with flush design)
> ```
>
> **2. Structural Integration Constraints**:
> - Roof panel is typically 0.6mm AHSS — adding LiDAR (2-5 kg) requires local reinforcement
> - Roof stiffness target (bowing resonance > 50 Hz) must be maintained after cutout
> - Any roof cutout affects rollover protection; FMVSS 216a roof crush test must be re-run
>
> **3. Wiring & Connector**:
> - LiDAR power and data connector must route through A-pillar or B-pillar without sharp bends
> - IP67 sealing required for roof penetration; consider drain channel for water management
>
> **4. Aerodynamics Impact**:
> - A 40mm protrusion above roofline adds ~0.5 counts to Cd (≈ +0.5% range loss on BEV)
> - Flush integration saves aero but requires tilted mounting or periscope optics arrangement
>
> **Recommendation**: For Level 3 highway autonomy, a 40-50mm protrusion with flush cover panel when not in use (retractable) provides best FOV performance with acceptable aero impact. Full flush integration requires custom optics arrangement that currently adds cost and complexity. Align with styling on a "performance flush" design that optimizes both aesthetics and FOV without full protrusion.

