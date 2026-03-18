## § 7 Standards & Reference

### Regulatory Hierarchy
```
ICAO GUAS Framework (global)
    ↓
FAA UTM ConOps v2.0 (USA)          EASA U-Space Reg EU 2021/664-666 (EU)
    ↓                                       ↓
ASTM UTM Standards (F3548, F3411)    EASA AMC/GM for U-Space Services
    ↓                                       ↓
FAA Part 107/108 (operations)        National U-Space Competent Authority rules
```

### Key Performance Metrics
| Metric | Target | Warning | Critical |
|--------|--------|---------|---------|
| Strategic CD&R latency | < 3 sec for flight plan approval | 3-10 sec | > 10 sec |
| Tactical CD&R latency | < 500 ms per conflict check | 500ms-1s | > 1s |
| System availability (SLA) | 99.9% (8.7 hr/yr downtime max) | 99.5% | < 99% |
| Telemetry update rate | 1 Hz minimum, 5 Hz recommended | 0.5 Hz | < 0.2 Hz |
| Remote ID broadcast latency | < 1 sec (ASTM F3411 requirement) | 1-3 sec | > 3 sec |
| Geofence notification latency | < 5 sec before violation | 5-10 sec | > 10 sec |
| Separation standard (urban) | 50m horizontal / 25m vertical | 30m/15m | < 30m/15m |

### Decision Tree: Strategic Deconfliction
```
Flight Plan Submitted?
├─ NO → Request flight plan (reject if BVLOS without plan)
└─ YES → Within authorized airspace?
    ├─ NO → Reject + suggest alternative time/route
    └─ YES → Conflict with existing reservations?
        ├─ YES → Offer alternatives (time shift ±15min, altitude FL change)
        │   └─ Alternative accepted? → Issue modified authorization
        │   └─ No alternative → Reject with explanation
        └─ NO → Meets operator credentials for operation type?
            ├─ NO → Reject with certification requirement
            └─ YES → Issue authorization token with 4D trajectory
```

