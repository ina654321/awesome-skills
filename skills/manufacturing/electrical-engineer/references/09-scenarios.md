## § 9 Scenario Examples

### Scenario 1 — Motor Starter Coordination

**User:** I need to specify a 50HP motor (460V, 3-phase, 65A FLA) with a VFD. What are the wire and protection requirements per NEC?

**Expert:** For a 50HP motor at 460V, here are the NEC requirements:

**Wire Sizing (NEC 430.122):**
```
Motor FLA: 65A
Wire Ampacity: 65A × 1.25 = 81.25A → Use #3 AWG THHN (90°C = 85A minimum)
```

**Overload Protection (NEC 430.32):**
```
Motor overload: 125% of FLA = 65A × 1.25 = 81.25A → Use 80A overload heater
```

**Short-Circuit Protection (NEC 430.52):**
```
Max breaker: 250% of FLA = 65A × 2.5 = 162.5A → Use 150A inverse-time breaker
Min breaker: 150% of FLA = 65A × 1.5 = 97.5A → Must be ≥ 100A
```

**VFD Input Wiring:**
```
VFD FLA = 65A × 1.25 = 81.25A → Use same #3 AWG to VFD
VFD output: Use shielded motor cable (VFD-rated for EMI)
```

| Component | Specification |
|-----------|---------------|
| Wire | #3 AWG THHN, 90°C |
| Breaker | 150A, 480V, 25kAIC |
| Contactor | 100A, 3-pole, AC-3 |
| Overload | 80A, adjustable |
| VFD | 50HP, 480V, EMC filter |

[CODE VIOLATION] Do not use #4 AWG — wire ampacity (85A) < 150% FLA (98A) violates NEC 430.52.

