## § 8 Standard Workflow

### Phase 1: Concept Performance Analysis
```
1.1 Propellant Selection & CEA Analysis
  - [ ] Run CEA for candidate propellants at target Pc and O/F range
  - [ ] Compute Isp_vac, T_chamber, c*, γ, M_mol at optimal O/F
  - [ ] Evaluate density-Isp = Isp × ρ_propellant for tank volume constraint
  - [✓ Done] Output: Propellant Trade Report with selected propellant combination and O/F
  - [✗ FAIL] If Isp < mission requirement → change propellant or accept higher mass fraction

1.2 Engine Cycle Selection
  - [ ] Compute turbopump power requirement for target Pc and mass flow
  - [ ] Trade GG vs. staged combustion vs. FFSC vs. expander for efficiency/complexity
  - [ ] Compute delivered Isp for each cycle accounting for turbine exhaust dump (GG) loss
  - [✓ Done] Output: Cycle Selection with power balance and Isp comparison
  - [✗ FAIL] If FFSC required but turbopump technology TRL < 6 → use staged combustion

1.3 Thrust and Nozzle Sizing
  - [ ] Size throat area from required thrust and Pc: At = F
  - [ ] Select area ratio for operating altitude (sea level: ε=16-30, vacuum: ε=40-200)
  - [ ] Compute exit plane conditions to verify no over-expansion at sea level
  - [✓ Done] Output: Nozzle geometry specification (At, Ae, ε, contour type)
```

### Phase 2: Detailed Design
```
2.1 Thrust Chamber Design
  - [ ] Size combustion chamber (diameter from At, L* = 1.0-1.5 m for storable, 1.3-1.7 for cryo)
  - [ ] Design injector: select element type (coaxial for LH2, impinging for RP-1/MMH)
  - [ ] Compute injector pressure drop (ΔP_inj = 15-25% of Pc for stability)
  - [ ] Design regen cooling jacket: compute heat flux, coolant velocity, wall temperature
  - [✓ Done] Output: Thrust Chamber Design Specification
  - [✗ FAIL] If wall temp > 0.8 × material limit → redesign cooling channels or reduce Pc

2.2 Turbopump Design
  - [ ] Compute turbopump speed for minimum size (Ns/Ds diagram)
  - [ ] Check NPSH requirements vs. available from tank head
  - [ ] Analyze rotor dynamics: verify critical speeds are 20% away from operating range
  - [ ] Select bearing type (rolling element vs. hydrostatic for reusable engines)
  - [✓ Done] Output: Turbopump Preliminary Design with dynamic analysis
  - [✗ FAIL] If critical speed within 20% of operating range → modify rotor geometry

2.3 Combustion Stability Analysis
  - [ ] Predict chug frequency (feed system coupled instability)
  - [ ] Predict tangential mode frequencies for chamber geometry
  - [ ] Design damping devices (baffles, Helmholtz resonators) if needed
  - [✓ Done] Output: Stability Analysis Report with predicted stable operating range
```

### Phase 3: Test Program
```
3.1 Developmental Testing
  - [ ] Ignition characterization test (minimum propellant fill, igniter energy sweep)
  - [ ] Performance characterization (Pc, O/F sweep; map c*, CF, Isp)
  - [ ] Stability assessment (bomb testing or pulse rating at full thrust)
  - [✓ Done] Output: Engine performance map validated against analysis

3.2 Qualification Testing
  - [ ] Duty cycle: rated thrust × 4× mission life (or as per MIL-HDBK-343)
  - [ ] Environmental: thermal cycling, vibration per DO-160G (or MIL-STD-1540)
  - [ ] Margin testing: 110% rated thrust, 90% rated propellant supply pressure
  - [✓ Done] Output: Engine qualification report; readiness for flight certification
```

