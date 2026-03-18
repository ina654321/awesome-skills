## 8. Standard Workflow

### 8.1 New Process Development

```
Phase 1: Conceptual Design (Week 1-2)
├── Define feed composition, product specifications, utilities available
├── Perform literature survey for similar processes and published kinetics
├── Preliminary material balance (100% conversion basis)
├── Select major unit operations (reactor type, separation sequence)
├── Rough equipment sizing for major items
└── [✓ Done]: Process Flow Diagram (PFD) with stream table
    [✗ FAIL]: Missing thermodynamic data → STOP, collect data before proceeding

Phase 2: Process Simulation (Week 3-4)
├── Build model in Aspen Plus/HYSYS with validated property package
├── Tune model against any available experimental data
├── Perform sensitivity analysis on key variables
├── Optimize operating conditions (temperature, pressure, recycle ratio)
└── [✓ Done]: Validated simulation with material/energy balance
    [✗ FAIL]: Simulation won't converge → check recycle convergence, physical properties

Phase 3: Detailed Engineering (Week 5-8)
├── Heat exchanger network design (Pinch analysis)
├── Equipment sizing with safety margins per applicable codes
├── P&ID development with instrumentation and safety systems
├── Hazop study and action item closure
└── [✓ Done]: P&ID, equipment datasheets, Hazop report
    [✗ FAIL]: Unresolved Hazop actions → DO NOT proceed to detailed design

Phase 4: Capital Estimate (Week 9-10)
├── ISBL estimate using factorial method (±25% accuracy)
├── OSBL estimate (20-30% of ISBL)
├── Operating cost estimate (utilities, labor, materials)
├── Economics: IRR, payback period
└── [✓ Done]: Technical/economic package for investment decision
```

### 8.2 Safety Relief System Design

```
Step 1: Identify Overpressure Scenarios
  → Fire, blocked outlet, heat exchanger tube failure, runaway reaction, loss of cooling
  → Document each scenario with basis and calculated flow

Step 2: Determine Required Relief Rate
  → Fire case: Q = (A^0.82)
  → Runaway: Use DIERS methodology or experimental data (RC1)
  → Select highest rate as design basis

Step 3: Size Relief Device
  → API 520 Part 1: Orifice area = W
  → Verify: orifice available, no chatter, proper discharge

Step 4: Select Device Type
  → Conventional: for single vessel
  → Balanced: for variable backpressure
  → Pilot-operated: for precision, large capacities

[✓ Done]: PSV sized, specified, tagged on P&ID
```

