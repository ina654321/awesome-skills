## § 7 Standards & Reference

### Key Standards & Frameworks

| Standard | Scope | Key Requirements |
|----------|-------|-----------------|
| **DO-178C** | Airborne software | DAL A-E; structural coverage (MC/DC for DAL-A); independent V&V |
| **DO-254** | Airborne electronic hardware | COTS justification; capture/validation/assurance levels |
| **DO-160G** | Environmental qualification | EMI, temperature, vibration, humidity testing |
| **ASTM F3005** | Balloon-borne and small UAS | Risk-based compliance for sub-25kg UAS |
| **FAA AC 20-193** | UAS type certification guidance | Means of compliance for novel UAS configurations |
| **EASA CS-UAS** | EU UAS certification standard | A1-A3 categories, specific category SORA methodology |
| **MIL-HDBK-516C** | Military airworthiness criteria | Structural, propulsion, FCS qualification for defense UAS |
| **AS9100D** | Aerospace QMS | Quality management for design and manufacturing |

### Key Performance Metrics

| KPI | Target | Measurement Method |
|-----|--------|--------------------|
| **Position Hold Accuracy (hover)** | <10 cm RMS in calm air | RTK GPS or motion capture ground truth |
| **Attitude Tracking Error** | <0.5° RMS during maneuvers | IMU vs. commanded attitude log comparison |
| **Disturbance Rejection Bandwidth** | >5 Hz for attitude loop | Frequency sweep flight test, transfer function ID |
| **Phase Margin (attitude loop)** | ≥45° | Frequency sweep at operating points |
| **Gain Margin (attitude loop)** | ≥6 dB | Frequency sweep at operating points |
| **EKF Position Uncertainty (GPS)** | <0.5 m 1σ horizontal | Comparison with RTK reference during level flight |
| **VTOL Transition Time** | <10 seconds (configuration-dependent) | Airspeed log during transition |
| **Loop Rate (inner/attitude)** | ≥500 Hz (target 1kHz) | Real-time scheduler monitoring |
| **Control Latency (sensor to actuator)** | <5 ms total pipeline | Hardware timestamp comparison |

