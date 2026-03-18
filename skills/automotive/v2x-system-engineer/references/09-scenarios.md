## § 9 Scenario Examples

### Scenario 1: Cooperative Perception Range Extension

**User**: Our AV's LiDAR sees 120m ahead in urban canyons. We want to use V2X to extend this to 300m. How do we design the CPM system?

**Expert**:
> **Cooperative Perception via CPM (Collective Perception Message, ETSI TR 103 562)** is exactly the right tool. Here's the design:
>
> **CPM Design for 300m Effective Range**:
>
> **1. Relay Chain Design**:
> ```
> Your vehicle (ego) → receives CPMs from vehicles up to 300m ahead
> Vehicles 100-200m ahead relay objects detected up to 200m ahead of them
> Net effect: ego vehicle sees objects 300-400m ahead
>
> Required: CPM transmission at 10 Hz; latency compensation in received objects
> ```
>
> **2. CPM Message Fields for Effective Cooperative Perception**:
> ```
> PerceivedObjects per CPM:
>   objectID:          Unique ID for tracking continuity across CPMs
>   sensorType:        Camera/LiDAR/Radar (affects trust weight in fusion)
>   objectRefPoint:    Position relative to sending vehicle (lat/lon delta)
>   objectAge:         How old is this detection? (discard if > 500ms)
>   objectConfidence:  Detection confidence 0-100%
>   objectDimensions:  Width × Length × Height estimates
>   speed + heading:   For trajectory prediction
> ```
>
> **3. Latency Budget for 300m Range Extension**:
> ```
> GPS/sensor capture at remote vehicle:   20 ms
> CPM generation:                          5 ms
> DSRC/C-V2X transmission:               10 ms
> Ego reception + authentication:         5 ms
> Object latency compensation (predict
>   forward 40ms at 30 m/s): ~1.2m offset correction
> Fusion with local sensor data:          10 ms
> Total: 50 ms — within 100ms budget ✓
> ```
>
> **4. Fusion Architecture**:
> - Use position uncertainty ellipse from CPM to weight fusion (high accuracy GPS → high weight)
> - Track objects across multiple CPM sources; prefer source with best accuracy
> - Age-gate: discard CPM objects > 500ms old; they may have moved significantly
>
> **Key implementation requirement**: Your ego vehicle needs GPS accuracy ≤ 1.5m to accurately compensate for the geometric offset between sender and receiver positions. Standard lane-level accuracy GNSS (RTK or SBAS-corrected) is required — standard autonomous driving GNSS, not consumer GPS.

---

### Scenario 2: SPAT/MAP Implementation for Smart Intersection

**User**: We're equipping 50 intersections with V2X RSUs. How do we design the SPAT/MAP broadcast?

**Expert**:
> **SPAT (Signal Phase and Timing) + MAP (Map Data) is the core V2I application.** Here's the deployment design:
>
> **MAP Message Configuration**:
> ```
> MapData message transmitted at: 1 Hz (static; only needs updating when geometry changes)
> Content per intersection:
>   IntersectionGeometry: Lat/lon of intersection reference point
>   LaneList: Each lane with:
>     laneID (1-255, unique within intersection)
>     nodes: List of waypoints defining lane geometry (every 5-10m, UPER-compressed)
>     connectsTo: Downstream lanes + signal group assignment
>     maneuverSharingOrPrioritization: Turn restrictions
>   SpeedLimit: Posted and advisory speeds per approach
>
> MAP transmission power: adjust for 500m coverage (typically 23 dBm EIRP)
> ```
>
> **SPAT Message Configuration**:
> ```
> SPAT transmitted at: 10 Hz (must update when signal phase changes)
> Critical timing fields:
>   signalGroup:     Maps to intersection signal controller phase
>   eventState:      GREEN/YELLOW/RED (current state)
>   minEndTime:      Guaranteed minimum time until phase ends (milliseconds)
>   maxEndTime:      Maximum time current phase continues
>
> Integration with signal controller:
>   Connect RSU to signal controller via SNMP or proprietary API
>   Achieve SPAT-to-controller latency < 100ms
>   SPAT accuracy requirement: ±1 second on signal timing prediction
> ```
>
> **RSU Deployment for 50 Intersections**:
>
> | Parameter | Specification |
> |-----------|-------------|
> | RSU per intersection | 1 (basic) or 2 (redundancy, complex intersections) |
> | Antenna height | 5-7m above ground (below traffic signals) |
> | Channel assignment | CCH (Control Channel, 178) for BSM relay; SCH for SPAT/MAP |
> | RSU transmit power | 23-27 dBm EIRP (verify FCC Part 95S compliance) |
> | Backhaul | 4G LTE for management + SPAT/MAP distribution from traffic mgmt center |
>
> **Application: GLOSA (Green Light Optimal Speed Advisory)**: With SPAT/MAP, equipped vehicles can compute the speed to arrive at the intersection during green phase. Target advisory speed accuracy: ±2 m/s for satisfying driver behavior. This requires SPAT timing accuracy ≤ 1 second over a 300m approach.

---

### Scenario 3: V2X Security Misbehavior Detection

**User**: In our V2X pilot, we're receiving BSMs from a vehicle claiming to be at impossible positions (teleporting 200m in 100ms). How do we handle this?

**Expert**:
> **You've detected a V2X misbehavior — either a bug or a deliberate attack.** Here's the response framework:
>
> **Step 1 — Immediate Plausibility Check**:
> ```python
> def check_bsm_plausibility(prev_bsm, curr_bsm):
>     """Returns True if BSM position change is physically plausible"""
>     dt = (curr_bsm.time - prev_bsm.time)
>
>     # Position delta
>     dist_m = haversine_distance(prev_bsm.position, curr_bsm.position)
>
>     # Max physically possible speed (250 km/h = 69.4 m/s for any road vehicle)
>     max_speed_ms = 70.0
>     max_dist = max_speed_ms * dt * 1.2  # 20% margin for GPS jitter
>
>     # Acceleration check (max 1.5g = 14.7 m/s²)
>     speed_delta = abs(curr_bsm.speed - prev_bsm.speed)
>     max_speed_change = 14.7 * dt * 1.3
>
>     position_plausible = dist_m <= max_dist
>     speed_plausible = speed_delta <= max_speed_change
>
>     return position_plausible and speed_plausible
>
> # 200m in 100ms = 2000 m/s = 7200 km/h → clearly not plausible
> ```
>
> **Step 2 — Response Actions**:
> 1. **Immediate**: Drop the invalid BSM; do NOT feed to cooperative perception fusion
> 2. **Log**: Record sender temporary ID, violation type, timestamp for misbehavior reporting
> 3. **Track**: If same sender ID misbehaves 3+ times in 10 seconds → local revocation blacklist
> 4. **Report**: Submit Misbehavior Report (MBR) to SCMS Misbehavior Authority per IEEE 1609.2/ETSI TS 102 941
>
> **Step 3 — Root Cause Analysis**:
> - If position jumps 200m → likely GPS position fix lost and then reacquired; common in urban canyons
> - Check: did speed and heading update continuously? (if speed was 0 → GPS fix lost scenario)
> - Distinguish between GPS glitch (unintentional) and attack (look for pattern: does it correlate with specific location? specific vehicles?)
>
> **MBR Format** (simplified IEEE 1609.2 misbehavior report):
> ```
> MisbehaviorReport {
>   reporterCertificate: [reporter's pseudonym cert]
>   reportedMessageEvidence: [original BSM + signature]
>   detectionRationale: POSITION_IMPLAUSIBLE_HIGH_SPEED
>   timestamp: [time of detection]
> }
> ```
> Upload to SCMS Misbehavior Authority; if confirmed, offending vehicle's certificates will be revoked in next CRL update.
