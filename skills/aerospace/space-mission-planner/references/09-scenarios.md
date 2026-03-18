## § 9 Scenario Examples

### Scenario 1: Mars Mission Delta-V Budget

**User**: We want to send a 500 kg spacecraft to Mars orbit for an imaging mission. What launch vehicle do we need and what's the delta-V budget?

**Expert**:
> **Mars trajectory analysis for 2026 opportunity** (next favorable launch window):
>
> **Step 1 — Trajectory energy (C3)**:
> ```
> 2026 Mars launch window: approximately July-August 2026
> Optimal C3 ≈ 8.7 km²/s² (low-energy Hohmann-like transfer)
> Transfer time: ~8 months (TOA: March-April 2027)
> ```
>
> **Step 2 — Delta-V budget**:
> ```
> Launch + TLI (Earth to C3=8.7):    Handled by launch vehicle
> TCMs (trajectory correction):       +80 m/s (budget 15% margin on TCMs)
> Mars Orbit Insertion (MOI) to 400km circular: +900 m/s
> Aerobraking (if used):              Reduces MOI to ~100 m/s (but adds risk)
> Orbit maintenance (2 years):        +20 m/s
> Disposal (deorbit):                 +30 m/s
>
> Propulsion delta-V needed: ~1,030 m/s (without aerobraking)
>                            ~230 m/s (with aerobraking, much higher risk)
> ```
>
> **Step 3 — Spacecraft mass sizing**:
> ```python
> # Without aerobraking, chemical propulsion (MMH/NTO, Isp=311s)
> dv = 1030  # m/s
> Isp = 311  # s
> g0 = 9.806
> dry_mass = 500  # kg spacecraft dry mass
> mass_ratio = math.exp(dv
> wet_mass = dry_mass * mass_ratio  # = 699 kg
> propellant = wet_mass - dry_mass  # = 199 kg
> ```
>
> **Step 4 — Launch vehicle selection**:
> ```
> Required: deliver 699 kg wet mass to C3 = 8.7 km²/s²
> Options:
>   Falcon 9 Block 5: ~2,000 kg to Mars C3 → FITS with large margin
>   Atlas V 411: ~1,800 kg to Mars C3 → FITS
>   Ariane 62: ~1,200 kg to Mars C3 → FITS
>   CNSA CZ-3B: ~1,000 kg to Mars C3 → FITS
>
> Recommendation: Falcon 9 provides best margin at lowest current cost (~$67M launch)
> ```
>
> **Aerobraking consideration**: Reduces propellant by ~170 kg (saves ~$5-8M in wet mass) but adds 3-6 months of aerobraking operations, solar panel thermal risk, and nav uncertainty. For a 500 kg imaging mission, avoid aerobraking unless mission is mass-constrained.

