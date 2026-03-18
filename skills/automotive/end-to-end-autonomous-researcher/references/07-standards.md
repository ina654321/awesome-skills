## 7. Standards & Reference

**Key Benchmarks and Target Metrics:**

| Benchmark | Key Metric | SOTA (2025) | Good Threshold | Notes |
|-----------|-----------|------------|----------------|-------|
| nuScenes Detection | NDS
| nuScenes Detection Camera-Only | NDS | 0.635 (SparseDrive) | NDS > 0.55 | Camera-only track |
| nuScenes Planning | L2@3s / Collision | L2 0.31m
| Waymo OD | mAPH L2 3D | 82.3 vehicle | > 75 mAPH | LiDAR primary |
| nuPlan Closed-Loop | PDM-Score | 92.1 (PDM-Closed) | > 80 | Reactive agents |
| CARLA Leaderboard | Driving Score | 85+ top entries | DS > 65 | Town05 Long |

**Foundational Architectures:**

| Architecture | Paper | Key Innovation | BEV Encoder | Planning Head |
|-------------|-------|---------------|-------------|---------------|
| UniAD | Hu et al., CVPR 2023 | Unified query-based E2E | BEVFormer | GRU ego query |
| VAD | Jiang et al., ICCV 2023 | Vectorized scene representation | BEVFormer | Trajectory MLP |
| SparseDrive | Sun et al., 2024 | Sparse BEV, fast inference | Sparse attention | Multi-modal planner |
| DriveLM | Sima et al., 2024 | Graph VQA + driving | CLIP + BEV | LLM-guided |
| BEVFormer | Li et al., ECCV 2022 | Temporal deformable attention | Deformable DETR | — |
| BEVFusion | Liu et al., ICRA 2023 | Unified camera+LiDAR | Dual BEV | — |

