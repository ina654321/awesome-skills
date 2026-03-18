## § 8 Standard Workflow

### Phase 1: Concept Definition & Mission Analysis
```
1.1 Mission Requirements Definition
  - [ ] Define design mission: range (km), payload (kg/PAX), cruise speed (km/h), hover duration
  - [ ] Define alternate missions: OEI (One Engine Inoperative) go-around, emergency landing
  - [ ] Define environmental envelope: temperature (-20°C to +45°C), altitude (MSL to 6000 ft)
  - [✓ Done] Output: Mission Requirements Document (MRD) signed by stakeholders
  - [✗ FAIL] If battery energy density < 250 Wh/kg AND range > 80 km → mission not physically viable at MTOW < 3000 kg

1.2 Configuration Trade Study
  - [ ] Size 3 candidate configurations (e.g., multirotor, lift+cruise, tiltwing) using NDARC
  - [ ] Compute hover power, cruise power, battery mass, and empty weight for each
  - [ ] Evaluate acoustic signature (tip speed, blade count), cert complexity, and manufacturing cost
  - [✓ Done] Output: Configuration Trade Report with selected architecture and rationale
  - [✗ FAIL] If all configurations exceed EWF > 0.60 → revisit mission requirements or wait for better battery technology

1.3 Certification Basis Selection
  - [ ] Engage FAA/EASA Aircraft Certification Office (ACO/EASA) for pre-application meeting
  - [ ] Define regulatory basis: Part 23 PoweredLift / SC-VTOL
  - [ ] Identify areas requiring Issue Papers (novel failure modes, electric propulsion, distributed propulsion)
  - [✓ Done] Output: Certification Plan (CP) accepted by certifying authority
```

### Phase 2: Preliminary Design
```
2.1 Aerodynamic Sizing
  - [ ] Rotor sizing: radius, blade count, chord, twist for target FM > 0.75
  - [ ] Wing sizing (if applicable): area, AR, taper for cruise L/D > 10
  - [ ] Motor/nacelle placement: optimize for rotor-wing interference, accessible for maintenance
  - [ ] CFD of hover+transition flow field; validate with BEMT predictions
  - [✓ Done] Output: Aerodynamic Database (ADB) v1.0 with uncertainty bounds
  - [✗ FAIL] If hover power > OEI-survivable level → add rotors or increase disk area

2.2 Propulsion System Sizing
  - [ ] Motor sizing: peak power, continuous power, torque, RPM
  - [ ] Battery pack sizing: energy, max C-rate, cell chemistry selection (NMC/LFP)
  - [ ] Thermal management: motor cooling (air/liquid), battery thermal runway mitigation
  - [ ] BMS design: cell balancing, fault detection, emergency power disconnect
  - [✓ Done] Output: Propulsion System Specification with weight and performance margins
  - [✗ FAIL] If battery mass > 35% MTOW → re-evaluate mission range or configuration

2.3 Structural Layout & Weight Estimation
  - [ ] Primary structure: fuselage, wing spar, motor mount load paths
  - [ ] Material selection: CFRP for primary structure, GFRP for secondary
  - [ ] Statistical weight estimation; compare to similar vehicles (NDARC database)
  - [ ] Identify highest-weight items for aggressive mass reduction
  - [✓ Done] Output: Weight Statement v1.0 with EWF target ≤ 0.54
```

### Phase 3: Detailed Design, Integration & Certification Testing
```
3.1 System Integration & Safety Analysis
  - [ ] FMEA for all propulsion, avionics, and control system components
  - [ ] FTA for Loss-of-Control and Catastrophic failure modes
  - [ ] Define Minimum Equipment List (MEL) and dispatch conditions
  - [✓ Done] Output: System Safety Assessment (SSA) v1.0

3.2 Flight Test Planning
  - [ ] Define flight envelope expansion sequence: ground runs → hover taxi → low-altitude hover → transition → cruise
  - [ ] Identify test points for stability & control (S&C), performance, and loads
  - [ ] Plan OEI certification flight tests; define test pilot safety procedures
  - [✓ Done] Output: Flight Test Plan (FTP) with test matrix and safety limits

3.3 Certification Compliance Demonstration
  - [ ] Complete all required rig and ground tests per Certification Plan
  - [ ] File compliance statements for each regulatory requirement
  - [ ] Respond to certifying authority Comments/Questions within 30 business days
  - [✓ Done] Output: Type Certificate (TC) or Supplemental Type Certificate (STC) issued
```

