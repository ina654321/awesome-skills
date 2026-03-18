## § 9 Scenario Examples

### Scenario 1: Urban Drone Delivery Corridor Design

**User**: We need to design a UTM system for a city-wide drone delivery network with 500 simultaneous deliveries during peak hours. The city has a mix of Class D airspace (around a regional airport) and Class G (elsewhere). How do we structure the UTM?

**Expert**:
> **Regulatory Gate Check**: Class D airspace requires ATC coordination with a LOA; Class G operations under 400 AGL with Remote ID can proceed under Part 107/108. You'll need a bilateral LOA with the airport tower to define lateral/vertical buffers — typically 3nm lateral and altitude layer separation (delivery drones operate 200-400 AGL; GA traffic 700+ AGL).
>
> **Architecture Recommendation for 500 simultaneous ops**:
>
> **Tier 1 — Airspace Segmentation** (solve the density problem first):
> ```
> Urban Core (high density):   Cell size 500m × 500m × 100m altitude bands
> Suburban Transition:         Cell size 1km × 1km × 150m altitude bands
> Class D Buffer Zone:         Sterile corridor, no UTM autonomous ops; ATC-coordinated only
> ```
>
> **Tier 2 — UTM Architecture**:
> - Deploy 3 geographically redundant USS nodes (active-active, sub-50ms synchronization via DSS)
> - Implement ASTM F3548-21 DSS with cell-based indexing (H3 hexagonal grid at resolution 8)
> - Strategic CD: Priority-based volume reservation, FCFS within same priority tier
> - Tactical CD: Velocity Obstacle algorithm, 60-second lookahead, 5 Hz telemetry update
>
> **Tier 3 — Class D Integration**:
> - SWIM interface to airport ATIS for real-time weather and active runway data
> - Automated NOTAM parsing to trigger geofence activations within 60 seconds of publication
> - Dedicated ATC hotline procedure for lost-comm or emergency situations
>
> **Capacity validation**: At 500 ops, strategic CD runs O(n log n) via R-tree spatial index. Benchmark target: full batch plan approval < 30 sec, individual approval < 3 sec.
>
> **Next step**: I recommend a detailed airspace capacity study using historical ADS-B data from OpenSky Network to characterize actual manned aircraft density by altitude and time-of-day before finalizing the buffer zones.

