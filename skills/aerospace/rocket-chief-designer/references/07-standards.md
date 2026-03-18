## § 7 Standards & Reference

### Vehicle Performance Benchmarks
| Vehicle | GLOW (kg) | PML to LEO (kg) | Payload Fraction | Stages | Reusable |
|---------|----------|----------------|-----------------|--------|---------|
| Falcon 9 Block 5 (new) | 549,054 | 22,800 | 4.15% | 2 | No |
| Falcon 9 Block 5 (reuse) | 549,054 | ~17,000 | ~3.1% | 2 | Stage 1 |
| Falcon Heavy (expendable) | 1,420,788 | 63,800 | 4.49% | 2+2 | No |
| Long March 5 | 879,000 | 25,000 | 2.84% | 2 | No |
| Ariane 6-4 | 530,000 | 21,650 | 4.08% | 2 | No |
| Electron | 13,000 | 300 | 2.3% | 2 | No |
| New Glenn | ~1,000,000 | 45,000 | ~4.5% | 2 | Stage 1 |

### Staging Optimization Formula (ideal Tsiolkovsky multi-stage)
```python
# For n-stage vehicle, optimal delta-V split minimizes GLOW
# Key insight: each stage should have similar mass ratio (m_wet/m_dry)

# Two-stage to LEO (approximate):
# Target LEO delta-V = 9,400 m/s (gravity + drag losses + orbit)
# Optimal split for LOX/RP-1 + LOX/LH2:
#   Stage 1 (Isp=311s): delta-V ≈ 3,800 m/s
#   Stage 2 (Isp=348s vacuum): delta-V ≈ 5,600 m/s

def compute_propellant_mass(dv, Isp, m_final):
    """Tsiolkovsky: compute propellant for given delta-V, Isp, and final mass"""
    mass_ratio = math.exp(dv
    m_initial = m_final * mass_ratio
    return m_initial - m_final  # propellant mass

# Stage 2 sizing (working backward from payload):
# Given: payload = 10,000 kg, dv_stage2 = 5,600 m/s, Isp2 = 348 s
# Assume structural fraction ε₂ = 0.08 (structure
m_prop_2 = compute_propellant_mass(5600, 348, m_payload)
m_struct_2 = m_prop_2 * epsilon_2
m_wet_2 = m_prop_2 + m_struct_2 + m_payload
```

### Vehicle Performance Loss Breakdown (LEO)
| Loss Type | Typical Value | Drivers |
|-----------|-------------|---------|
| Gravity losses | 1,100–1,500 m/s | Burn time at vertical velocity; lower T/W ratio → more gravity loss |
| Drag losses | 100–300 m/s | Vehicle slenderness, max-Q altitude, atmospheric density |
| Steering losses | 50–200 m/s | Range safety steering, wind steering, orbit plane change |
| **Total losses** | **1,250–2,000 m/s** | (on top of ideal orbital velocity) |
| Ideal LEO velocity | 7,780 m/s | Circular orbit at 200 km |
| **Total delta-V needed** | **9,030–9,780 m/s** | Use 9,400 m/s as design point |

