## § 8 — Standard Workflow

### Phase 1 — Requirements & ODD Definition
- **Step 1.1**: Define Operational Design Domain (ODD): geography, weather, speed limits, road types, time-of-day.
- **Step 1.2**: Enumerate OEDR scenarios from ISO 34501 taxonomy relevant to ODD.
- **Step 1.3**: Perform HARA (Hazard Analysis and Risk Assessment) per ISO 26262 Part 3; assign ASIL levels.
- **Step 1.4**: Derive safety goals and functional safety requirements.
- [✓ Done] HARA table with ASIL assignments for all hazardous events; ODD boundary document.
- [✗ FAIL] Any driving scenario within ODD without an assigned ASIL level.

### Phase 2 — Architecture & Algorithm Design
- **Step 2.1**: Design sensor suite (camera count/placement, LiDAR type, radar configuration) for 360-degree coverage.
- **Step 2.2**: Select and design perception pipeline: 3D detection model, tracker, semantic segmentation.
- **Step 2.3**: Design prediction module: agent model, trajectory prediction horizon (5s), uncertainty representation.
- **Step 2.4**: Select planning approach per ODD: rule-based behavior planner + MPC/lattice motion planner.
- **Step 2.5**: Design safety monitor: probabilistic runtime assertion checker, fallback state machine.
- [✓ Done] Architecture diagram with data flows, latency budget per module, ASIL allocation.
- [✗ FAIL] Any safety-critical function without a designated ASIL level or redundant path.

### Phase 3 — Implementation & Integration
- **Step 3.1**: Implement and unit-test each module against benchmark (nuScenes, KITTI, or custom).
- **Step 3.2**: Integrate modules in simulation (CARLA); measure end-to-end latency and throughput.
- **Step 3.3**: Run adversarial scenario suite (occlusion, sensor noise, cut-in, jaywalker, construction zone).
- **Step 3.4**: Profile compute on target hardware (Orin/AGX); optimize bottlenecks (TensorRT, CUDA kernels).
- [✓ Done] All unit tests passing; integration test pass rate > 95% on defined scenario suite.
- [✗ FAIL] Any module exceeding its latency budget at P90; any safety monitor false negative in test.

### Phase 4 — Validation & Safety Case Closure
- **Step 4.1**: Execute SOTIF Part 2 scenario coverage analysis; identify triggering conditions and coverage gaps.
- **Step 4.2**: Perform closed-road testing covering ODD boundary scenarios with safety driver.
- **Step 4.3**: Shadow mode deployment: system runs in parallel with human driver, comparing decisions.
- **Step 4.4**: Compile safety case per ISO 26262 Part 2 (argument, evidence, context).
- [✓ Done] Safety case approved by functional safety manager; SOTIF coverage metrics meet targets.
- [✗ FAIL] Open safety case items; untested ODD conditions; missing evidence for any safety goal.

