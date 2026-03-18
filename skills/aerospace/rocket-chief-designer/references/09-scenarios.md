## § 9 Scenario Examples

### Scenario 1: Two-Stage to LEO Vehicle Sizing

**User**: I want to design a launch vehicle that delivers 10,000 kg to 400km LEO. Size the vehicle.

**Expert**:
> **Let me work through the top-level sizing**. Target: 10,000 kg to 400km circular (7,670 m/s orbital + ~1,800 m/s losses = ~9,400 m/s total delta-V).
>
> **Configuration selection**: 2-stage, LOX/RP-1 stage 1, LOX/LH2 upper stage (Falcon 9 analogue):
>
> **Stage 2 sizing** (working backward from payload):
> ```python
> # Stage 2: LOX/LH2, Isp_vac = 450s, structural fraction ε₂ = 0.10
> # Delta-V allocation: stage 2 handles 5,600 m/s
> dv2 = 5600  # m/s
> Isp2 = 450  # s (LOX/LH2 vacuum)
> m_payload = 10000  # kg
> epsilon2 = 0.10  # structural fraction = m_dry
>
> mass_ratio_2 = exp(5600
> m_wet_2 = m_payload * mass_ratio_2 / (1 - epsilon2 * (1 - 1/mass_ratio_2))
>         ≈ 10000 * 3.557
> m_prop_2 = 40200 * (1 - 1/3.557)
> m_dry_2 = 40200 - 28900 - 10000 = 1,300 kg (structural mass, check: 4.5% → OK)
> ```
>
> **Stage 1 sizing**:
> ```python
> # Stage 1: LOX/RP-1, Isp_vac = 311s, structural fraction ε₁ = 0.07 (denser propellant)
> # Delta-V allocation: stage 1 handles 3,800 m/s
> m_top_of_stage1 = m_wet_2 = 40,200 kg
>
> mass_ratio_1 = exp(3800
> m_wet_1 = m_top_of_stage1 * mass_ratio_1 / (1 - epsilon1 * (1 - 1/mass_ratio_1))
>          ≈ 40200 * 3.479
>
> GLOW = m_wet_1 + m_wet_2 = 145,000 + 40,200 = 185,200 kg
> Payload fraction = 10,000
> ```
>
> **Engine sizing**: T/W ≥ 1.3 at liftoff → min thrust = 185,200 × 9.806 × 1.3 = 2,360 kN. If using 9 engines: ~262 kN each (similar to Merlin 1D at 914 kN → use 3 engines at ~787 kN each, or similar trade).
>
> **Fairing sizing**: For 10,000 kg payload, expect ~8m diameter × 20m tall fairing; competes with Falcon 9 5.2m fairing range.

