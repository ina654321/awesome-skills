# AV Simulation — Standards & Reference

## Official Documentation

### Simulation Engines

- [CARLA Simulator Documentation](https://carla.readthedocs.io/en/latest/) — Urban autonomous driving simulator built on Unreal Engine. Covers sensor blueprints, actor management, traffic manager, and OpenDRIVE map support.
- [SUMO (Simulation of Urban MObility)](https://sumo.dlr.de/docs/) — Microscopic traffic simulation. Supports co-simulation with CARLA via Traci API. Covers vehicle routing, traffic light logic, and large-scale network simulation.
- [CARLA ScenarioRunner](https://carla-scenariorunner.readthedocs.io/) — Tool for running OpenSCENARIO-defined scenarios in CARLA. Handles scenario execution, actor lifecycle, and maneuver definitions.
- [NVIDIA DRIVE Sim](https://docs.nvidia.com/drive/drive-sim/) — High-fidelity simulation platform for AV development. Supports sensor simulation (LiDAR, camera, radar) with physics-accurate rendering.
- [AirSim (Microsoft)](https://microsoft.github.io/AirSim/) — Open-source simulator for drones and cars built on Unreal Engine. API for flight control and car driving.
- [LGSVL Simulator](https://www.svlsimulator.com/) — LG valeo sensor vehicle simulator. Supports Apollo and Autoware AD stacks with sensor fusion testing.

### Standards & Formats

- [ASAM OpenSCENARIO 2.0](https://www.asam.net/standards/detail/openscenario/) — XML-based DSL for describing dynamic content in driving simulation. Defines actions, maneuvers, triggers, and trajectories. Current version 2.0 replaces the 1.x series.
- [ASAM OpenDRIVE 1.7](https://www.asam.net/standards/detail/opendrive/) — Standard format for describing road network geometry and topology. Covers lanes, signals, elevations, and superelevation. Used by CARLA, SUMO, and most HD map tools.
- [ASAM OpenLABEL 1.0](https://www.asam.net/standards/detail/openlabel/) — Open labeling format for machine learning in autonomous driving. Defines annotation schema for 2D/3D bounding boxes, polylines, cuboids, and text classification.
- [ASAM OSI (Open Simulation Interface)](https://www.asam.net/standards/detail/osi/) — Standardized interface for exchanging simulation data between components. Defines GroundTruth and SensorView messages.
- [BAIDU Apollo Cyber RT](https://cyber RT.readthedocs.io/) — Real-time computing framework for Apollo. Includes integrated simulator for scenario playback.
- [nuScenes Dataset Format](https://www.nuscenes.org/nuscenes) — Multi-modal sensor dataset format. Defines sensor calibration, localization, and annotation schema. Widely used as ground truth reference for sim-to-real validation.

## Industry Standards & Regulatory Bodies

### Functional Safety & SOTIF

- **ISO 21448 (SOTIF)** — Safety of the Intended Functionality. The primary standard driving scenario selection for perception edge cases. Defines Known Safe, Known Unsafe, Unknown Unsafe, and Unknown Safe scenario quadrants. All simulation libraries must be mapped to SOTIF quadrants.
- **ISO 26262 (ASIL)** — Functional safety for road vehicles. Covers hazard analysis (HARA), safety goals, and validation requirements. Simulation provides evidence for ASIL-B and ASIL-C requirements; ASIL-D requires hardware-in-the-loop (HiL).
- **IEEE 2846-2022** — Formal model for minimum safety assumptions in AV decision-making. Informs the boundary conditions for scenario parameter ranges (e.g., TTC thresholds, deceleration limits).

### Regulatory & Type Approval

- **UN Regulation 157 (ALKS)** — UNECE regulation for Automated Lane Keeping Systems up to 60 km/h on highways. Includes simulation acceptance criteria: 10,000 km simulated mileage per ODD variant with zero uncooperative scenario failures.
- **FMVSS (Federal Motor Vehicle Safety Standards)** — US NHTSA standards. AV developers use simulation to demonstrate compliance with standards that cannot be tested physically at scale.
- **Euro NCAP AEB Protocols** — European New Car Assessment Programme test protocols for autonomous emergency braking. Defines standard scenarios (CCRm, CCRb, CCRs) with defined vehicle speeds and trajectories.
- **NHTSA AEB Test Protocols** — US National Highway Traffic Safety Administration AEB test procedures. Defines Car-to-Car rear crash scenarios.

### Professional Associations

- **SAE International (J3016)** — Defines Levels of Driving Automation (L0–L5). The reference taxonomy for describing AV system capability levels.
- **ASAM e.V.** — Association for Standardization of Automation and Measuring Systems. Develops OpenSCENARIO, OpenDRIVE, OpenLABEL, and OSI standards. The primary standards body for AV simulation interoperability.
- **Euro NCAP** — European New Car Assessment Programme. Publishes safety test protocols including AEB, LSS, and highway assist tests. Simulation scenarios must match Euro NCAP scoring protocols.
- **SAE AV IV&V Committee** — Society of Automotive Engineers committee on AV independent verification and validation. Publishes recommended practices for simulation-based testing.

## Coverage & Metrics Frameworks

### Scenario Coverage Standards

- **ISO 34502 (SOTIF Scenario Categories)** — Defines the process for identifying and categorizing driving scenarios based on SOTIF risk assessment. Used to derive the scenario parameter space for simulation.
- **PEGASUS Project (Germany)** — Research program that established the 6-level hierarchy for scenario description (functional, conceptual, logical, concrete, actual, measured). Foundational work for OpenSCENARIO 2.0.
- **UN R157 Scenario Catalog** — Defines the minimum set of scenarios required for ALKS type approval under UN R157.
- **NHTSA Pre-Crash Data Scenarios** — NHTSA publishes 37 pre-crash scenario types (e.g., vehicle-to-vehicle rear-end, lane change, crossing/intersecting). Used as a baseline scenario taxonomy.

### KPI Definitions

- **Scenario Coverage Index (SCI)** — Metric defined as the percentage of ODD parameter cells covered by executed scenarios in a combinatorial coverage matrix. Formula: SCI = (covered cells / total cells) × 100%.
- **VMT-Equivalent (Virtual Miles Traveled)** — Normalized metric converting scenario execution counts to miles driven. Formula: Σ(execution_time_hours × avg_speed_mph) for each scenario.
- **Critical Scenario Density** — Ratio of edge-case/critical scenarios to total scenarios in the library. Tracked to ensure sufficient adversarial coverage.
- **MTBF-Equivalent for AV** — Mean time between failures, adapted for simulation. Tracked per scenario category for reliability reporting.

## Synthetic Data & ML Standards

- **nuScenes Annotation Format** — The de facto standard for 3D bounding box annotations in AV perception. Defines sample structure, calibration matrices, ego-pose, and instance tracking IDs.
- **KITTI Dataset Format** — Pioneer standard for LiDAR-camera fusion annotations. References for coordinate system conventions (camera, LiDAR, GPS/IMU).
- **Waymo Open Dataset** — Large-scale real-world dataset with 3D bounding box labels, LiDAR, and camera data. Used for sim-to-real validation benchmarks.
- **Synscapes** — Synthetic driving dataset with photorealistic rendering. Reference for realistic synthetic image quality benchmarks.
- **nuPlan Dataset** — Closed-loop planning benchmark using log-based simulation. Defines log replay format for motion forecasting validation.

## Open Source Reference Implementations

- [CARLA OpenSCENARIO Parser](https://github.com/carla-simulator/scenario_runner) — Reference implementation of OpenSCENARIO 1.x in Python.
- [Scenic (MIT)](https:// Scenic-lang.github.io/) — Probabilistic programming language for scenario generation. Uses domain-randomized sampling with formal coverage guarantees.
- [CommonRoad](https://commonroad.in.tum.de/) — Planning benchmark with scenario files in CommonRoad XML format. Reference for motion planning algorithms.
- [MetaDrive](https://github.com/decisionforce/metadrive) — Lightweight AV simulation with procedural generation for reinforcement learning.
- [longrel](https://github.com/waymo-research/waymo-open-simulator) — Waymo's motion prediction simulation environment.
