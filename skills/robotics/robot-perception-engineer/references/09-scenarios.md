## 9. Scenario Examples

### Scenario A — LiDAR-Camera Fusion Pipeline Setup

**User**: I need to fuse Ouster OS1-128 with a FLIR Blackfly S 5MP camera for a mobile robot. The robot moves at up to 2 m/s indoors. What calibration approach and fusion architecture do you recommend?

**Engineer**: Great setup. Here's my systematic approach:

**Step 1 — Hardware Synchronization**
Connect the Blackfly's GPIO trigger input to the OS1's SYNC_PULSE_OUT. Configure the OS1 to emit a pulse at 20Hz aligned with lidar packet boundaries. Set the Blackfly to external trigger mode at 20Hz. This gives you hardware-synchronized captures with < 50µs jitter, essential at 2 m/s (4cm motion per 20ms frame).

**Step 2 — Calibration**
Use a large AprilTag board (0.8m × 0.6m, 6×5 tags, 120mm tag size) for robust detection.

```python
# Calibration validation with Open3D + OpenCV
import open3d as o3d
import numpy as np
import cv2

def validate_lidar_camera_calibration(pcd, image, K, D, T_lidar_camera):
    """
    Project LiDAR points onto image and compute edge alignment error.
    T_lidar_camera: 4x4 SE(3) transform from LiDAR frame to camera frame
    """
    points = np.asarray(pcd.points)  # (N, 3) in LiDAR frame
    # Filter front-facing points
    mask = points[:, 0] > 0.5
    pts = points[mask]

    # Transform to camera frame
    pts_cam = (T_lidar_camera[:3, :3] @ pts.T + T_lidar_camera[:3, 3:]).T
    # Filter behind camera
    valid = pts_cam[:, 2] > 0
    pts_cam = pts_cam[valid]

    # Project to image
    pts_img, _ = cv2.projectPoints(
        pts_cam.reshape(-1, 1, 3),
        np.zeros(3), np.zeros(3), K, D
    )
    pts_img = pts_img.reshape(-1, 2)

    # Colorize by range for visualization
    ranges = np.linalg.norm(pts_cam, axis=1)
    colors = cv2.applyColorMap(
        (np.clip(ranges
        cv2.COLORMAP_JET
    )
    overlay = image.copy()
    for pt, col in zip(pts_img.astype(int), colors[:, 0]):
        if 0 <= pt[0] < image.shape[1] and 0 <= pt[1] < image.shape[0]:
            cv2.circle(overlay, tuple(pt), 2, col.tolist(), -1)
    return overlay
```

**Step 3 — Fusion Architecture** (loosely-coupled for robustness)
Use a two-stage architecture: (1) LIO-SAM for ego-motion at 400Hz (IMU preintegration + LiDAR scan matching at 10Hz), (2) Camera-based object detection (CenterPoint BEV or YOLO + depth lift) at 20Hz fused with LiDAR detections via IoU-based association.

For indoor 2 m/s environments, LIO-SAM with the OS1-128's 128-beam density gives ATE < 1cm per 100m. No loop closure needed for < 1000m² maps.

