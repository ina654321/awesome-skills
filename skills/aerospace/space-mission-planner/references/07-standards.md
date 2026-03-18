## § 7 Standards & Reference

### Delta-V Budget Reference (approximate)
| Maneuver | Delta-V (m/s) | Notes |
|---------|-------------|-------|
| LEO → GTO (chemical) | ~2,500 m/s | From 200km circular |
| GTO → GEO | ~1,800 m/s | Apogee kick; includes plane change |
| LEO → TLI (Trans-Lunar Injection) | ~3,200 m/s | From 400km circular |
| Lunar Orbit Insertion (LOI) | ~900 m/s | Into 100km circular lunar orbit |
| Earth → Mars (Hohmann, ideal) | ~5,600 m/s | From Earth surface; includes launch |
| Earth → Mars (minimum energy transfer) | ~3,600 m/s | C3 = 8.7 km²/s² for 2026 window |
| LEO orbital maintenance/drag | ~20-50 m/s/year | At 400km altitude, Cd = 2.2 |

### Tsiolkovsky Rocket Equation
```
ΔV = Isp × g₀ × ln(m₀/mf)

Where:
  Isp = specific impulse (s): typical values:
    Hydrazine monoprop:    220 s
    Bi-propellant (MMH/NTO): 311 s
    Electric (Hall thruster): 1600 s
    LOX/LH2 (J-2X):        448 s
  g₀ = 9.806 m/s² (standard gravity)
  m₀ = initial (wet) mass
  mf = final (dry + residual propellant) mass

Example: 500 m/s ΔV with Isp=311s, 100 kg dry mass:
  mass_ratio = e^(500
  m₀ = 1.178 × 100 = 117.8 kg → propellant = 17.8 kg
```

### Launch Window Decision Tree
```
Mission destination?
├─ LEO/GEO/HEO: Any date (continuous access), launch window = day × inclination constraints
├─ Moon: ~2 week cycle (lunar phase); TLI window 3-5 days per month
├─ Mars: 26-month synodic cycle; optimal 2026 window C3 = 8.7 km²/s²
├─ Venus: 19-month synodic cycle; 2027 next favorable window
└─ Outer planets: Multiple gravity assists required; resonance opportunities every 5-20 years
```

