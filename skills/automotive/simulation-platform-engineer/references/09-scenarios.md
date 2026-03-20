# AV Simulation — Glossary

## Simulation Engines & Platforms

**CARLA (Car Learning to Act)** — Open-source autonomous driving simulator built on Unreal Engine. Provides urban environments, vehicle models, sensor simulation, and traffic management. Version 0.9.x is the current production series.

**SUMO (Simulation of Urban MObility)** — Microscopic traffic flow simulator. Models individual vehicles, traffic lights, and pedestrians at city scale. Used for behavioral NPC traffic generation and V2X co-simulation.

**NVIDIA DRIVE Sim** — Commercial simulation platform from NVIDIA. Provides photorealistic rendering via Omniverse, physics-based sensor simulation, and tight integration with NVIDIA AI toolchains (DriveAV, DriveMap).

**AirSim** — Microsoft open-source simulator for drones and cars built on Unreal Engine. API-driven control for flight and driving scenarios.

**LGSVL Simulator** — LG Valeo sensor vehicle simulator. Integrates with Apollo and Autoware AD stacks for end-to-end testing.

**Waymo Simulation** — Waymo's internal simulation platform. Includes closed-loop simulation on logged real-world data and scalable scenario generation.

## Scenario Description Standards

**OpenSCENARIO** — ASAM standard XML format for describing dynamic driving scenarios. Version 1.x uses procedural maneuver definitions; version 2.0 uses a DSL with action trees and routing commands.

**OpenDRIVE** — ASAM standard for road network description. Defines road geometry, lanes, junctions, signals, and elevation profiles. The canonical format for HD map exchange between tools.

**OpenLABEL** — ASAM standard for labeling and annotation format. Defines schema for 2D/3D bounding boxes, polylines, cuboids, and image classification labels. Used for synthetic data annotation.

**OSI (Open Simulation Interface)** — ASAM standard interface for exchanging simulation data between components (e.g., from sensor model to perception stack).

**CommonRoad** — TU Munich's planning benchmark format. XML-based scenario descriptions for motion planning algorithm evaluation.

## Sensor Simulation

**LiDAR (Light Detection and Ranging)** — Active sensor that emits laser pulses and measures return time to calculate range. In simulation: ray-casting from a 3D mesh, with physics-based modeling of beam divergence, reflectance, and atmospheric attenuation.

**Ray-casting LiDAR** — Simulation method that casts rays from the LiDAR origin and detects intersections with scene geometry. Computes range, intensity, and return number per ray.

**RCS (Radar Cross-Section)** — Measure of how detectable a target is by radar. In simulation: assigned per material/object type. Metal vehicles have high RCS; pedestrians have low RCS.

**Camera ISP (Image Signal Processor)** — The pipeline converting raw sensor data to RGB images. Includes demosaicing, noise injection, lens distortion, HDR tonemapping, and color correction. A major sim-to-real gap source.

**Motion Blur** — Effect of camera exposure time on moving objects. Simulated by integrating multiple sub-frame renders. Critical for validating perception models on highway scenarios.

**Sensor Fusion** — Combining outputs from multiple sensor modalities (LiDAR, camera, radar) to produce a unified environment representation. In simulation: syncing sensor timestamps and coordinate transformations.

**V2X (Vehicle-to-Everything)** — Communication between vehicles and infrastructure/pedestrians/network. Simulated via network message injection (V2V CAM/DENM, V2I SPaT/MAP messages).

## Scenario Categories

**ODD (Operational Design Domain)** — The specific conditions under which an automated system is designed to operate. Defined by road type, speed range, weather, lighting, and geographic area. Scenario libraries must be mapped to ODD parameters.

**Functional Scenario** — A scenario described at a high level in natural language (e.g., "a car cuts in front of the ego vehicle on a highway").

**Logical Scenario** — A scenario with parameter ranges defined (e.g., "cut-in with TTC between 1.0–4.0s, ego speed 20–40 m/s").

**Concrete Scenario** — A fully instantiated scenario with specific parameter values (e.g., "cut-in at TTC=2.5s, ego speed=30 m/s, rain_light, night").

**Scenario Coverage Index (SCI)** — Percentage of ODD parameter grid cells covered by executed scenarios. The primary coverage metric for simulation libraries.

**Critical Scenario** — A scenario at the boundary of safe operation (3-sigma events, adversarial NPC behavior, sensor degradation). The most important category for safety validation.

**Edge Case** — A scenario that is rare in real-world distribution but represents a high-risk condition. Includes unusual road geometries, adverse weather, sensor degradation, and adversarial agent behavior.

**SOTIF Quadrants** — Classification of scenarios into Known Safe, Known Unsafe, Unknown Safe, and Unknown Unsafe based on ISO 21448. Simulation should expand the Known Unsafe set and shrink the Unknown Unsafe set.

## Sensor & Perception Metrics

**mAP (mean Average Precision)** — Primary metric for 3D object detection. Measures precision-recall trade-off across object classes.

**Point Density** — Number of LiDAR returns per unit volume. Expressed as points/m³ or points per object. Used to compare sim vs. real LiDAR fidelity.

**RMSE (Root Mean Square Error)** — Statistical measure of simulation fidelity. Used to compare simulated vs. real sensor outputs quantitatively.

**KL Divergence** — Measure of distribution shift between simulated and real data. Computed on image histograms, point cloud density distributions, or object class frequencies.

**FID (Fréchet Inception Distance)** — Metric comparing distributions of real vs. synthetic images. Lower FID = more realistic synthetic images. Target: FID < 15 for usable synthetic training data.

**Sim-to-Real Gap** — The performance delta when a model trained on synthetic data is evaluated on real-world data. Caused by rendering differences, sensor model inaccuracies, and asset quality gaps.

**Domain Randomization** — Training technique that randomizes simulation parameters (lighting, textures, object colors) to force the model to learn invariant features. Reduces sim-to-real gap.

**Domain Adaptation** — Machine learning technique that aligns feature distributions between simulated and real domains. Methods include CycleGAN, UNIT, and pixel-level adaptation.

## Testing & Validation

**SOTIF (Safety of the Intended Functionality)** — ISO 21448 standard addressing risks from functional limitations and foreseeable misuse of AV systems. Governs scenario selection for perception edge cases.

**ISO 26262** — Functional safety standard for road vehicles (ASIL A–D). Defines validation requirements for safety-critical functions. Simulation provides evidence for ASIL-B/C; ASIL-D requires HiL.

**UN R157 (ALKS)** — UNECE regulation for Automated Lane Keeping Systems up to 60 km/h on highways. Includes simulation acceptance criteria requiring 10,000 km simulated mileage per ODD variant.

**ASL (Autonomy Level)** — As defined by SAE J3016: L0 (no automation) through L5 (full driving automation).

**Regression Testing** — Running a fixed suite of scenarios on every code change to detect regressions. Must be automated, reproducible, and fast enough to run nightly.

**KPI (Key Performance Indicator)** — Measurable metrics tracked per simulation run: pass rate, SCI, VMT-equivalent, detection rate, MTBF-equivalent.

**Nightly CI** — Automated pipeline running regression scenarios on a schedule (typically nightly). Primary mechanism for catching regressions before deployment.

**Headless Rendering** — Running simulation without visual output to GPU. Dramatically increases throughput for behavioral tests. Required for CI scalability.

## Scenario Execution

**ScenarioRunner** — Python tool from CARLA that executes OpenSCENARIO-defined scenarios. Handles actor spawning, maneuver execution, and result evaluation.

**NPC (Non-Player Character)** — A simulated vehicle or pedestrian controlled by the simulation's traffic manager. Not the AV under test.

**Traffic Manager** — CARLA's built-in module for controlling NPC behavior. Supports configurable speed, lane discipline, collision avoidance, and random routing.

**Ego Vehicle** — The AV under test. In simulation, the ego is controlled by the AD stack (planning module or external control).

**TTC (Time-to-Collision)** — The time until two vehicles would collide if maintaining current speed and trajectory. Primary safety metric for cut-in and rear-end scenarios.

**VMT-Equivalent** — Virtual miles traveled equivalent. Normalizes scenario counts to mileage for regulatory reporting.

**Maneuver** — A discrete driving action (lane change, turn, acceleration, braking) defined in OpenSCENARIO.

**Trigger / Condition** — A condition that initiates a maneuver (e.g., "when ego speed > 10 m/s AND time since scenario start > 5s").

## Maps & Geometry

**HD Map (High-Definition Map)** — A precise map with lane-level geometry, traffic signs, signal positions, and road markings. Authored in OpenDRIVE format.

**Plan View** — The top-down 2D geometry of a road, defined by a reference line and lateral offsets. The foundational element of OpenDRIVE roads.

**Lane Model** — The representation of road lanes in simulation: lane centerline, width, type (driving, bike, shoulder), and connectivity.

**Junction** — An intersection where multiple roads meet. In OpenDRIVE: defined by explicit Connection elements or implicit geometry.

**Superelevation** — The lateral tilt of a road cross-section on curves. Affects vehicle dynamics and lane geometry calculations.

## CI/CD & Infrastructure

**Kubernetes (K8s)** — Container orchestration platform used to run parallel CARLA instances at scale in CI/CD pipelines.

**GPU Scheduling** — Allocating GPU resources across parallel simulation instances. Typically 1–2 CARLA instances per GPU depending on fidelity requirements.

**Scenario Artifact** — The output of a scenario execution: sensor recordings, ego traces, KPI scores, and failure logs. Must be archived for reproducibility.

**RNG Seed** — Random number generator seed. Logging and fixing RNG seeds ensures scenario reproducibility.

**Failure Triage** — The process of analyzing failed scenario executions to identify root cause (perception error, planning failure, edge-case physics, infrastructure bug).

**Gantry Scheduling** — A CARLA server pool architecture where GPU nodes serve scenarios submitted by a central scheduler.

## Data & Format

**nuScenes Format** — Standard data format for multi-modal AV data. Defines sensor calibration, ego-pose, 3D bounding box annotations, and sample structure.

**Waymo Open Dataset** — Real-world driving dataset with LiDAR, camera, and 3D/2D bounding box annotations. Used for sim-to-real validation.

**Synthetic Data** — Data generated via simulation. Includes point clouds, camera images, radar returns, and ground truth labels generated by the simulator.

**Ground Truth** — The accurate reference label for a scenario: true object positions, semantic labels, ego trajectory. Provided by simulation (vs. human-annotated or sensor-derived).

**Domain Randomization** — Generating diverse synthetic data by randomizing textures, lighting, weather, and object placement within simulation.

**Annotation Schema** — The definition of how objects are labeled (bounding box format, class definitions, tracking IDs). Must match the ML training pipeline format.
