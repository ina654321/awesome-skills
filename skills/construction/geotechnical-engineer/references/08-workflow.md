## 8. Standard Workflow

### 8.1 Foundation Design

```
Phase 1: Data Collection (Week 1)
├── Obtain site investigation report: borings, SPT, lab tests, groundwater
├── Request structural loads from architect/engineer
├── Review architect's performance criteria (settlement limits)
└── [✓ Done]: Complete SI data and load summary
    [✗ FAIL]: No SI data → STOP, cannot proceed without ground parameters

Phase 2: Preliminary Sizing (Week 2)
├── Determine foundation type: shallow vs deep based on soil and loads
├── Estimate footing sizes for bearing capacity
├── Calculate preliminary settlement
└── [✓ Done]: Preliminary foundation layout
    [✗ FAIL]: Shallow foundation not viable → specify deep foundation

Phase 3: Detailed Design (Week 3-4)
├── Final bearing capacity and settlement analysis
├── Design reinforcement for footings/raft
├── Check differential settlement
├── Specify construction requirements
└── [✓ Done]: Foundation design drawings and specifications
    [✗ FAIL]: Settlement exceeds criteria → modify foundation or improve ground

Phase 4: Construction Support (Construction)
├── Review contractor's pile driving or excavation records
├── Respond to RFI regarding ground conditions
├── Verify foundation construction matches design
└── [✓ Done]: Foundation construction complete
```

### 8.2 Slope Stability Analysis

```
Step 1: Site Characterization
  → Obtain cross-sections from survey/topography
  → Soil parameters from SI (c, φ, γ)
  → Groundwater conditions (piezometric levels)

Step 2: Analysis Methods
  → Method of slices (Ordinary, Bishop, Spencer)
  → Use multiple methods to bound solution
  → Consider seismic loading if applicable

Step 3: Factor of Safety Evaluation
  → Calculate FoS for critical failure surface
  → Check if FoS > 1.5 (static) or 1.3 (seismic)
  → Identify critical surface

Step 4: Mitigation Design
  → If FoS inadequate: flatten slope, add drainage, add reinforcement
  → Design soil nails, anchors, or retaining structures as needed
  → Specify construction sequence

[✓ Done]: Slope design with FoS > target, mitigation if needed
```

