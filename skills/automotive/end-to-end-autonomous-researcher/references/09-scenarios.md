## 9. Scenario Examples

### Example 1: Choosing Between Camera-Only and LiDAR-Fusion E2E Architecture

**User:** We are building an E2E model for a robotaxi and need to decide between camera-only (like BEVFormer) vs camera+LiDAR fusion (BEVFusion). What factors should guide this decision?

**Researcher:**
This is fundamentally a cost-safety-performance trade-off. Let me break it down systematically.

Camera-Only (BEVFormer/SparseDrive): Cost is roughly $500-2000 sensor suite with simpler calibration. NDS achieves ~0.63 (SparseDrive, nuScenes val camera-only track). Key weakness is that depth estimation is ambiguous from monocular views and performance degrades in low-light and adverse weather. Velocity estimation via temporal attention is noisy for fast-moving objects. Best for cost-sensitive deployment at scale at urban speeds under 50 km/h with redundant safety monitors.

Camera+LiDAR Fusion (BEVFusion): Cost is $5k-50k sensor suite depending on LiDAR SKU, with complex calibration and time-sync requirements. NDS achieves ~0.76, and L2 planning error is roughly 15% lower than camera-only in occluded scenarios. Key strength is that metric depth from LiDAR eliminates scale ambiguity and the system is robust to lighting changes. Best for safety-critical deployment, highway speeds, and regulatory approval pathways.

Recommendation for robotaxi: Use camera+LiDAR fusion. The safety case for L4 robotaxi will require demonstrating SOTIF coverage in adverse conditions where camera-only fails. BEVFusion gives you a unified BEV feature for both detection and planning, and LiDAR provides the ground-truth depth anchor that tightens velocity estimates critical for safe gap acceptance in merging scenarios.

```python
# BEVFusion unified encoder sketch (PyTorch pseudocode)
class BEVFusionEncoder(nn.Module):
    def __init__(self, cam_channels=256, lidar_channels=256, bev_h=200, bev_w=200):
        super().__init__()
        # Camera BEV via LSS (Lift-Splat-Shoot)
        self.cam_bev = LiftSplatShoot(
            in_channels=cam_channels, bev_h=bev_h, bev_w=bev_w
        )
        # LiDAR BEV via voxelization + pillar encoder
        self.lidar_bev = PointPillarEncoder(
            out_channels=lidar_channels, bev_h=bev_h, bev_w=bev_w
        )
        # Fusion: channel-wise concat followed by conv
        self.fusion_conv = nn.Sequential(
            nn.Conv2d(cam_channels + lidar_channels, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True)
        )

    def forward(self, cam_imgs, cam_params, lidar_points):
        cam_bev_feat = self.cam_bev(cam_imgs, cam_params)   # [B, C, H, W]
        lidar_bev_feat = self.lidar_bev(lidar_points)        # [B, C, H, W]
        fused = torch.cat([cam_bev_feat, lidar_bev_feat], dim=1)
        return self.fusion_conv(fused)                       # [B, 256, H, W]
```

### Example 2: Debugging Closed-Loop Collapse After Good Open-Loop Results

**User:** Our model achieves L2@3s = 0.42m on nuScenes open-loop (better than UniAD baseline), but in CARLA closed-loop the driving score is only 28. Why?

**Researcher:**
This is classic covariate shift failure. Here is the diagnosis and treatment plan.

Diagnosis: Open-loop L2 measures how well you predict the expert's future trajectory given ground-truth past context. In closed-loop, the vehicle's own past actions create the context — any deviation from the training distribution compounds exponentially. A model with L2=0.42m can still drive into a wall when its own suboptimal actions push it into an out-of-distribution state.

Root cause checklist:
1. No recovery data — if training data contains only smooth expert trajectories, the model has never seen how to recover from slight lane departure. Add perturbation augmentation (random lateral offsets 0.1-0.5m during training).
2. Frozen perception context — if your planning head takes GT boxes as input during training but predicted boxes at inference, that is a perception-planning gap. Train end-to-end with detected boxes.
3. Temporal context mismatch — model uses 2s history at train time; at inference in CARLA the first 2s have no clean history. Use warmup strategy or mask temporal attention during rollout start.

Treatment using DAgger online imitation learning:
```python
# DAgger online imitation learning loop
for iteration in range(num_dagger_iters):
    # Linearly anneal expert mixing probability
    beta = max(0.0, 1.0 - iteration * 0.1)

    # Collect trajectories from mixed policy
    trajectories = collect_carla_rollouts(
        policy=lambda obs: beta * expert(obs) + (1 - beta) * learner(obs)
    )

    # Aggregate into growing dataset
    dataset = dataset + trajectories

    # Retrain behavior cloning on full aggregated dataset
    learner = train_bc(dataset, epochs=10)
    score = evaluate_carla(learner)
    print(f"Iter {iteration}: DAgger DS={score:.1f}, beta={beta:.2f}")
```

After 5 DAgger iterations, expect driving score to recover to 60-70+ without changing the model architecture.

### Example 3: Anti-Pattern — Reporting Only Open-Loop Results as Driving SOTA

**User:** Our new architecture gets NDS 0.70 on nuScenes — much better than UniAD's 0.65. We want to claim it drives better. Is that justified?

**Researcher:**
No — and this is one of the most common misleading claims in E2E driving research. NDS 0.70 means your model better predicts future object positions and ego trajectory in a replay scenario where ground-truth history is given. This measures perception quality and short-horizon imitation accuracy. It does NOT mean your model drives more safely, handles more scenarios, or is closer to deployment.

The correct claim chain: NDS 0.70 supports "improved open-loop scene understanding." NDS 0.70 plus CARLA DS 80+ supports "improved driving in simulation." Only NDS 0.70 plus CARLA DS 80+ plus 10k real miles without intervention supports "improved real-world driving."

Recommendation: Add a nuPlan closed-loop evaluation (PDM-Score) before the paper submission. It takes roughly 4 GPU-hours on a single A100 and provides the reactive closed-loop evidence that reviewers at CVPR/ICCV now expect as standard. Without it, expect a reject or major revision request.

