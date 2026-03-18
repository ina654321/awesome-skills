## § 7 — Standards & Reference

**Key Standards:**
- **ISO 26262:2018** — Functional Safety for Road Vehicles (ASIL A-D classification, safety lifecycle)
- **ISO 21448:2022 (SOTIF)** — Safety of the Intended Functionality (performance limitations, unknown unsafe scenarios)
- **UN-ECE WP.29 ALKS** — Automated Lane Keeping System type approval (up to 60 km/h, highway)
- **SAE J3016** — Taxonomy of driving automation levels (L0-L5)
- **ISO 34501** — Taxonomy and definitions for tests of automated driving systems

**Performance Metrics Table:**

| Metric | Formula | Target Range | Notes |
|--------|---------|--------------|-------|
| 3D Detection mAP | mean AP over classes and IoU thresholds | > 55 NDS (nuScenes) | BEVFusion baseline: 72.9 NDS |
| Tracking AMOTA | Multi-object tracking accuracy (AMOTA) | > 0.50 nuScenes | ByteTrack achieves 0.57+ |
| Localization RMSE | sqrt(mean((x_est - x_gt)^2)) | < 0.10 m lateral | HD map matching requirement |
| End-to-end Latency | t_actuate - t_sensor_capture | < 100 ms (P90) | Human reaction time ~150ms |
| Planning Frequency | 1
| False Positive Rate | FP
| Miss Rate | FN
| MRC Time-to-Safe | t_safe_stop - t_fault_detect | < 10 s | ISO 26262 MRC definition |

