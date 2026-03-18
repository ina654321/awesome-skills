## § 9 — Scenario Examples

### Scenario 1: Designing a Sensor Fusion Pipeline for a Robotaxi

**User**: "We need to design the sensor fusion architecture for a new L4 robotaxi. We have 8 cameras, 3 LiDARs (1 top, 2 corner), and 5 radars. How should we structure the perception stack?"

**Expert**:

Great sensor configuration. For a production L4 robotaxi, I recommend a hierarchical fusion architecture:

**Layer 1 — Per-Modality Detection (parallel pipelines):**
- Camera pipeline: BEVFormer or BEVFusion-Camera — 3D detection in BEV space, 30Hz
- LiDAR pipeline: CenterPoint or VoxelNet — 3D detection + velocity from top LiDAR, 10Hz
- Radar pipeline: RadarNet or custom CFAR — confirmed detections with Doppler velocity, 20Hz

**Layer 2 — Cross-Modal Fusion:**
- Use Track-to-Track fusion (T2TF) with probabilistic data association
- State vector: [x, y, z, vx, vy, length, width, height, class, confidence]
- Gating: Mahalanobis distance < chi2(0.99, dof=5) for association
- Output: Fused object list with per-object ASIL-compliant confidence

**Layer 3 — Temporal Tracking:**
- Extended Kalman Filter or LSTM-based motion model per track
- Track lifecycle: tentative (N=3 consecutive detections) then confirmed then lost (M=5 missed)

```python
# Cross-modal track association using Hungarian algorithm with Mahalanobis gating
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import mahalanobis

def associate_detections_to_tracks(detections, tracks, gating_threshold=9.488):
    """
    Associate new detections to existing tracks.
    gating_threshold: chi2(0.99, dof=4) = 9.488
    """
    if len(tracks) == 0:
        return [], list(range(len(detections))), []

    cost_matrix = np.zeros((len(detections), len(tracks)))
    for d_idx, det in enumerate(detections):
        for t_idx, trk in enumerate(tracks):
            innovation = det[:4] - trk.predicted_state[:4]
            S = trk.innovation_covariance[:4, :4]
            try:
                dist = mahalanobis(det[:4], trk.predicted_state[:4],
                                   np.linalg.inv(S))
                cost_matrix[d_idx, t_idx] = (
                    dist if dist < gating_threshold else 1e6
                )
            except np.linalg.LinAlgError:
                cost_matrix[d_idx, t_idx] = 1e6

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    matches, unmatched_dets, unmatched_trks = [], [], []
    matched_set = set()
    for r, c in zip(row_ind, col_ind):
        if cost_matrix[r, c] < gating_threshold:
            matches.append((r, c))
            matched_set.add(c)
        else:
            unmatched_dets.append(r)
    unmatched_trks = [i for i in range(len(tracks)) if i not in matched_set]
    return matches, unmatched_dets, unmatched_trks
```

**ASIL Allocation**: Camera detections alone are ASIL-B. LiDAR-confirmed detections are ASIL-C. Radar+LiDAR corroborated tracks are ASIL-D. The safety monitor gates actuator commands based on minimum ASIL level of relevant objects.

