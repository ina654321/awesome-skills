## § 8 Standard Workflow

### Phase 1 — Concept & Requirements
- Capture functional requirements, performance specs, and constraints
- Generate 2–3 concept sketches; evaluate for manufacturability
- Select candidate materials based on properties and cost
- [✓ Done]: Concept selected, materials short-listed, DFM issues identified
- [✗ FAIL]: Requirements ambiguous, no DFM assessment, material unsuitable

### Phase 2 — CAD Modeling & GD&T
- Build 3D model with proper feature tree; create configurations
- Apply GD&T per ASME Y14.5; specify datums, position, profile controls
- Run interference checks; validate clearance for assembly
- [✓ Done]: 3D model complete, GD&T applied, all features inspectable
- [✗ FAIL]: Undefined datums, non-inspectable controls, missing draft

### Phase 3 — DFM/DFA Analysis & DFMEA
- Conduct injection molding / casting
- Perform tolerance stack analysis (RSS + worst-case); verify fit-up
- Complete DFMEA; calculate RPN; assign corrective actions
- [✓ Done]: All DFM issues resolved, stack within tolerance, RPN < 100
- [✗ FAIL]: Unresolved sink marks/warpage, stack failure, RPN > 250

### Phase 4 — Validation & Release
- Run FEA for structural/thermal verification (FoS ≥ 1.5)
- Create production drawings with full GD&T and notes
- Generate tool buyoff samples; approve first article (FAIR)
- [✓ Done]: FEA validated, drawings released, FAIR approved
- [✗ FAIL]: FEA FoS < 1.5, open drawing issues, FAIR rejected

