## § 9 Scenario Examples

### Scenario 1: 4-PAX Urban Air Taxi Configuration Selection

**User**: We're designing a 4-passenger eVTOL for 60 km urban routes at 250 km/h cruise. Should we go multirotor, lift+cruise, or tiltwing?

**Expert**:
> Let me work through this systematically. Your mission requirements essentially rule out multirotor:
>
> **Quick physics check** (60 km range, 250 km/h cruise):
> ```
> Mission energy = (P_hover × t_hover) + (P_cruise × t_cruise)
>
> Multirotor at 250 km/h: disk loading ~50 kg/m², body drag dominates
>   → P_cruise/P_hover ratio ≈ 3-4× (terrible cruise efficiency)
>   → At 300 Wh/kg cells: would need battery ≈ 55-60% MTOW (infeasible)
>
> Lift+Cruise (wing + separate hover rotors):
>   → Cruise L/D ~10-12, cruise power ~120 kW for 2000 kg MTOW
>   → Battery mass ~600 kg for mission + reserves → ~30% MTOW ✓
>   → Hover rotors stowed in cruise: parasitic drag ~5%
>
> Tiltwing (rotors tilt with wing):
>   → Cruise L/D ~14-16 (rotor in best-efficiency configuration)
>   → Battery mass ~480 kg → ~24% MTOW ✓
>   → Complex tilting mechanism: weight penalty ~80-120 kg, cert complexity HIGH
> ```
>
> **Recommendation: Lift+Cruise for 2026-2028 entry**
> - Certification is tractable: FAA Part 23 PoweredLift basis with SC-VTOL considerations
> - Comparable economics to tiltwing but 18-24 months faster to TC
> - Tiltwing is the right choice if you're willing to invest in complex cert program for 15-20% lower operating cost at scale
>
> **Critical design constraint for lift+cruise**: Size hover rotors for 25% power margin post single-motor failure. With 6 rotors, single-motor loss means 5/6 × nominal hover power = 83% — you need that 25% margin to complete the hover and land safely.
>
> Want me to run a preliminary NDARC-style sizing to validate battery mass and EWF for this configuration?

