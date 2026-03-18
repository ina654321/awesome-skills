## § 7 Standards & Reference

### FATO/TLOF Sizing Reference (FAA AC 150/5390-2D basis, adapted for eVTOL)
| Parameter | Small eVTOL (< 3000 lb) | Medium eVTOL (3000–7000 lb) | Large eVTOL (7000–12,500 lb) |
|-----------|------------------------|----------------------------|-------------------------------|
| TLOF diameter | 1.0D (D = largest dimension) | 1.0D | 1.0D |
| FATO diameter | 1.5D | 1.5D | 1.5D |
| Safety area width | 3m minimum | 3m minimum | 3m minimum |
| Load bearing (FATO) | 1.5× MTOW (hard landing) | 1.5× MTOW | 1.5× MTOW |
| Obstacle-free radius | 10m from FATO edge | 15m from FATO edge | 20m from FATO edge |

### Capacity Modeling Formulas
```
Throughput = 3600 / (Mean Turnaround Time [sec])   # Operations/hour per pad

Mean Turnaround Time components:
  T_land:     90-120 sec  (final approach + touchdown + deceleration)
  T_deplane:  120-180 sec (passenger off, pre-flight check, reboard)
  T_charge:   300-900 sec (depends on battery size and charger power)
  T_depart:   60-90 sec   (checklist, departure clearance, takeoff)

Total: 570-1290 sec → 2.8 to 6.3 ops/hour per pad (CONSERVATIVE)

For network planning: use 4 ops/hour per pad as baseline capacity
```

### Decision Tree: Charging Infrastructure
```
Battery size per aircraft?
├─ < 100 kWh (small UAM, 2 PAX)
│   → 150 kW charger sufficient (40 min to 80%)
│   → 50A at 480V three-phase typical
└─ 100-200 kWh (medium UAM, 4-6 PAX)
    → 350-500 kW fast charger required (30 min to 80%)
    → Requires dedicated transformer; coordinate with utility 60-90 days in advance
    → Evaluate battery swap for operations requiring < 15 min turnaround
```

