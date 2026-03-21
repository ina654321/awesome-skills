# code Example

```
QUANTUM SENSING MENTAL MODEL

  MEASURAND (gravity, B-field, time, rotation)
       |
       v
  +--------------------------------------------------+
  |  SENSING PLATFORM SELECTION                       |
  |  Inertial → Atom interferometer                  |
  |  Magnetic → SQUID / NV-center
  |  Time/Frequency → Optical atomic clock           |
  |  Force/displacement → Optomechanical resonator  |
  +--------------------+-----------------------------+
                       |
                       v
  +--------------------------------------------------+
  |  SENSITIVITY LIMIT ANALYSIS                       |
  |  SQL: δφ = 1/√N (uncorrelated, shot-noise)       |
  |  HL:  δφ = 1/N  (maximally entangled, GHZ)       |
  |  Practical: limited by coherence T2, efficiency  |
  +--------------------+-----------------------------+
                       |
                       v
  +--------------------------------------------------+
  |  SYSTEMATIC ERROR BUDGET                          |
  |  Identify ALL shifts (Zeeman, Stark, BBR, ...)   |
  |  Quantify bias uncertainty vs stat. precision     |
  |  Design rejection (differential, modulation)     |
  +--------------------+-----------------------------+
                       |
                       v
  +--------------------------------------------------+
  |  ALLAN DEVIATION CHARACTERIZATION                 |
  |  White noise: σ_y ∝ τ^(-1/2)                    |
  |  Flicker noise: σ_y ∝ τ^0                        |
  |  Frequency drift: σ_y ∝ τ^(+1/2)                |
  +--------------------------------------------------+
```
