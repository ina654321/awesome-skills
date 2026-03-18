## § 10 — Common Pitfalls

### Anti-Pattern 1: Single-Sensor Confidence Threshold
**Name**: The Mono-Modal Oracle

❌ BAD:
```python
# Dangerous: trusting single camera confidence for emergency braking
if camera_detection.confidence > 0.85 and camera_detection.cls == 'pedestrian':
    trigger_emergency_brake()
```

✅ GOOD:
```python
def evaluate_emergency_brake(cam_det, lidar_tracks, radar_tracks):
    if cam_det.confidence < 0.85:
        return False
    # Require LiDAR or radar corroboration within 0.5m
    lidar_ok = any(
        np.linalg.norm(t.position - cam_det.position) < 0.5
        for t in lidar_tracks
    )
    radar_ok = any(
        np.linalg.norm(t.position[:2] - cam_det.position[:2]) < 1.0
        for t in radar_tracks
    )
    return lidar_ok or radar_ok
```

**Why it matters**: Camera DNN models have known failure modes (adversarial patches, heavy rain, lens flare). Emergency braking on uncorroborated detections causes dangerous false positives in production.

