# Glossary

## Arc-Minute (arcmin)
A unit of angular measurement: 1 arc-minute = 1/60 of a degree. Used to specify backlash, transmission error, and positioning accuracy in precision reducers. A harmonic drive with <1 arcmin backlash is considered "ultra-high precision."

## Backlash
The angular clearance between mating gear teeth when direction is reversed. In reducers, backlash is the "lost motion" at the output before the input begins to drive in the opposite direction. Measured in arc-minutes or arc-seconds. Lower is better for precision positioning.

## Bearing Life (L10)
The basic rating life of a bearing, defined as the life at which 90% of a group of identical bearings will survive under a given load. Calculated per ISO 281 as L10 = (C/P)^p × 10^6 revolutions, where C is dynamic load rating, P is equivalent load, and p = 3 for ball bearings, 10/3 for roller bearings.

## Circular Spline (CS)
The rigid outer ring of a harmonic drive, featuring internal gear teeth. The circular spline is typically fixed to the reducer housing and does not rotate. Its tooth count differs from the flexspline to create the gear reduction mechanism.

## Contact Ratio
The average number of teeth in contact at any given moment in a gear mesh. Must be >1.2 for continuous power transmission. Low contact ratio (<1.2) causes vibration, noise, and premature failure.

## Cycloidal Disc
The heart of an RV reducer. A disk with cycloidal-shaped teeth (trochoid curve) that engages with the pin gear. The disc's unique motion converts high-speed, low-torque input into low-speed, high-torque output through a rolling contact mechanism, resulting in near-zero backlash.

## Cycloidal Pin Gear
The input element of an RV reducer — a short cylinder with roller-like teeth that engage with cycloidal discs. Also called the "needle gear" or "RV pin gear." The pin gear typically rotates at high speed and has fewer teeth than the number of holes in the cycloidal disc.

## Flexspline (FS)
The flexible thin-walled steel cup of a harmonic drive, featuring external gear teeth. The flexspline deforms elastically under the action of the wave generator, engaging with the circular spline at two diametrically opposed points. The primary wearing component.

## Flexspline Rim Fatigue
The primary failure mode of harmonic drives. Under cyclic bending stress from the wave generator, the flexspline rim develops micro-cracks that propagate until fracture. Life depends on torque, speed, temperature, and material quality. Characterized by increased backlash and reduced torque capacity.

## Gear Ratio
The ratio of input speed to output speed. A 30:1 harmonic drive means the input must rotate 30 times to produce one output rotation. Also expressed as i = n_in / n_out. Higher ratios provide more torque multiplication but lower output speed.

## Harmonic Drive (Strain Wave Gear)
A precision speed reducer using a flexible steel cup (flexspline) deformed by an elliptical wave generator to engage with a rigid internal ring (circicular spline). Advantages: zero backlash (when preloaded), high reduction ratio in single stage, compact size, high torque-to-weight ratio. Limitations: lower torque capacity than RV, sensitivity to shock loads.

## Hertzian Contact Stress
The surface stress that develops where curved gear teeth meet. Calculated using Hertz's equations. Gear failure (pitting, spalling) is often caused by Hertzian contact fatigue exceeding the material's surface fatigue limit. Expressed in MPa.

## Input / Output Torque Relationship
The fundamental relationship in reducers: Output Torque = Input Torque × Reduction Ratio × Efficiency. For a 30:1 harmonic drive with 85% efficiency, an input of 10 Nm produces approximately 255 Nm of output torque.

## Inertia Ratio
The ratio of load inertia to motor inertia: J_load / J_motor. Critical in servo-driven reducer applications. High inertia ratio (>3:1) causes servo tuning difficulties, overshoot, and oscillation. Target <3:1; >10:1 requires special motor/drive sizing.

## Lost Motion
The total angular error in a transmission system, including backlash, elastic deformation under load, and transmission error. Measured as the difference between theoretical and actual output motion. The key performance metric for precision reducers.

## No-Load Starting Torque
The torque required to initiate rotation of a reducer with no external load. Primarily caused by bearing friction, seal friction, and initial gear mesh resistance. Should be measured during acceptance testing.

## Pitting (Surface Fatigue)
A gear failure mode where small pits form on the tooth surface due to Hertzian contact fatigue. Pitting progresses from micro-pitting (polish-like damage) to macro-pitting (visible craters). Caused by overload, inadequate lubrication, or material defects. Reducer must be replaced when pitting exceeds AGMA standards.

## Planetary Gearhead
A reducer using planetary (epicyclic) gear arrangement: one sun gear, multiple planet gears, and an annulus ring. Advantages: high torque capacity, high efficiency (90-98%), compact. Disadvantages: some backlash inherent in design. Used in mid-range precision applications.

## Preload (Bearing Preload)
The application of a constant axial load to eliminate clearance in bearings. In harmonic drives, the wave generator bearings are preloaded to maintain gear mesh geometry and minimize lost motion. Insufficient preload causes backlash increase; excessive preload causes heating and reduced life.

## Reduction Ratio (i)
The gear reduction factor. For a 50:1 reducer, the output rotates 1/50th as fast as the input. In harmonic drives, reduction ratio = (N_C - N_F) / N_F, where N_C = circular spline teeth, N_F = flexspline teeth.

## Rigidity (Torsional Stiffness)
The resistance of a reducer to angular deflection under load. Measured as torque per unit angular deflection (Nm/arcmin). Higher torsional rigidity means less elastic deformation under load, which is critical for precision positioning. Harmonic drives: 200-800 Nm/arcmin; RV reducers: 400-2000 Nm/arcmin.

## RV Reducer (Rotary Vector Reducer)
A precision reducer developed by Nabtesco (formerly帝人精機/Teijin Seiki). Uses a two-stage mechanism: a cycloidal disc stage (high reduction) followed by a spur gear stage. Advantages: high torque capacity, high rigidity, excellent durability (15,000+ hour life). Disadvantages: larger and heavier than harmonic drives of equivalent torque.

## Spalling
A more severe form of surface fatigue than pitting, where flakes of material separate from the gear tooth surface. Caused by high Hertzian contact stress, poor lubrication, or contamination. Spalling leads to rapid deterioration and requires immediate reducer replacement.

## Tilting Rigidity
The resistance of the output flange to angular deflection under applied moment loads. Critical when external forces (cutting forces, payload forces) act at a distance from the output shaft center. Measured in Nm/arcmin.

## Torque Ripple
The variation in output torque during a single input revolution due to gear geometry imperfections. In harmonic drives, torque ripple is extremely low due to the multiple-tooth engagement. In RV reducers, torque ripple is slightly higher but still excellent.

## Transmission Error (TE)
The deviation between the actual output position and the theoretical position predicted by the gear ratio. The most comprehensive measure of reducer accuracy. Measured in arc-seconds. TE includes elastic deflection, gear errors, and manufacturing variations.

## Two-Stage Reducer
A reducer combining two reduction stages in series: e.g., a planetary first stage followed by a harmonic second stage. Used when single-stage reduction ratios are insufficient. Two-stage reducers achieve higher ratios with better efficiency and smaller package size than multiple single-stage reducers.

## Wave Generator (WG)
The elliptical or camshell component of a harmonic drive that fits inside the flexspline cup. It contains a thin-walled bearing that presses against the flexspline inner diameter, causing it to deform into an elliptical shape. The wave generator is the input element.

## Wear (Abrasive)
Material removal from gear surfaces due to contamination (dirt, metal particles), inadequate lubrication film, or foreign material in the reducer. Early indicator of lubrication failure. If caught early, reducer may be rebuilt; if advanced, replacement is required.
