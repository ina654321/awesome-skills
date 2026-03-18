## § 7 Standards & Reference

### SAE J2945/1 Performance Requirements (V2V Safety)
| Parameter | Requirement | Notes |
|-----------|------------|-------|
| Transmission rate (BSM) | 10 Hz minimum | Can be reduced by DCC if CBR > 60% |
| Communication range | > 300m (99th percentile PDR > 90%) | At relative closing speed; urban environment |
| End-to-end latency | < 100ms (E2E delay 95th percentile) | From vehicle sensor capture to recipient application |
| Position accuracy | < 1.5m 95th percentile | Required for meaningful cooperative tracking |
| Message authentication | IEEE 1609.2 ECDSA P-256 | Mandatory for public deployment |

### BSM Part 1 Critical Fields (SAE J2735)
```
BSM Part 1 (transmitted every 100ms):
  msgCnt:        Message counter (0-127, wraps)
  id:            Temporary ID (changes with pseudonym cert)
  secMark:       Time of week in ms (synchronization)
  lat:           Latitude × 10⁻⁷ degrees
  long:          Longitude × 10⁻⁷ degrees
  elev:          Elevation in 10cm increments
  accuracy:      GPS semi-major/minor axis, heading of semi-major
  speed:         0.02 m/s resolution, 0-163.8 m/s range
  heading:       0.0125° resolution
  brakes:        ABS, traction control, stability control status
  size:          Vehicle width × length (for path prediction)

BSM Part 2 (optional, 0-7 additional parts):
  PathHistory, PathPrediction, ExteriorLights, VehicleAlerts...
```

### Technology Comparison: DSRC vs. C-V2X PC5
| Feature | DSRC (IEEE 802.11p) | C-V2X PC5 (LTE/NR) |
|---------|--------------------|--------------------|
| Standard | IEEE 802.11p / WAVE | 3GPP Rel-14/16 |
| Spectrum | 5.9 GHz (75 MHz, USA) | 5.9 GHz
| Latency (99th pct) | ~10-30 ms | ~10-20 ms (LTE-V2X) |
| Range (highway LOS) | 300-1000m | 500-1000m |
| NLOS performance | Moderate | Better (resource scheduling) |
| Infrastructure dependency | None (direct) | None for PC5 direct mode |
| Coexistence with cellular | None built-in | Integrated (Mode 3/4) |
| Deployment status (2026) | Japan, some USA | China, Germany, USA (growing) |
