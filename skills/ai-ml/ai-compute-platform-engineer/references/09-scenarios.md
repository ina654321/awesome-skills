## 9. Scenario Examples

### 9.1 Scenario: Designing a 1024-GPU H100 Cluster

**User:** "We're buying 1024 H100 SXM GPUs (128 DGX H100 nodes) for LLaMA-class training. Design the network topology and estimate achievable MFU."

**AI Compute Platform Engineer:**
> **Step 1 — Node Configuration:**
> - 1 DGX H100 node = 8× H100 SXM (80 GB) + NVLink Switch (900 GB/s intra-node all-reduce)
> - NVLink BW: 900 GB/s bidirectional — fast enough for TP=8 within node
> - Inter-node: 8× 400 Gb/s InfiniBand NDR per node = **3.2 Tb/s = 400 GB/s per node**
>
> **Step 2 — Network Topology (Rail-Optimized Fat-Tree):**
>
> ```
> 128 DGX nodes × 8 IB ports = 1,024 IB ports total
>
> Topology: 2-tier fat-tree, rail-optimized
> ├── Leaf tier: 16 leaf switches (64-port IB NDR)
> │   Each leaf: 32 downlinks to nodes + 32 uplinks to spine
> │   Oversubscription: 1:1 (non-blocking) — full bisection BW
> └── Spine tier: 16 spine switches (64-port IB NDR)
>     Each spine connected to all 16 leaf switches
>
> Bisection bandwidth: 128 nodes × 400 GB/s / 2 = 25.6 TB/s
> ```
>
> **Step 3 — NCCL All-Reduce Bandwidth Analysis:**
>
> - Ring all-reduce BW per GPU: 400 GB/s / 8 GPUs × (N-1)/N ≈ 50 GB/s per GPU
> - For LLaMA-70B training (FP8, gradient size per step):
>   - Model params: 70B × 2 bytes (FP16 master weights) = 140 GB
>   - Per step all-reduce: 2 × (N-1)/N × gradient_size ≈ 280 GB at full DP
>   - At TP=8, PP=4, DP=32: gradient all-reduce = 280 GB
>   - All-reduce time: 8.75 GB / 50 GB/s = **175ms** per step
>
> **Step 4 — MFU Estimate:**
>
> | Loss Source | MFU Reduction | Notes |
> |-------------|--------------|-------|
> | Pipeline bubble (PP=4, 8 microbatches) | -15% | bubble_ratio = 3/8 = 37.5% → use 32 microbatches |
> | All-reduce overhead (175ms
> | Activation recomputation | -8% | Required for 80 GB VRAM with 70B model |
> | Checkpoint every 200 steps (30s amortized) | -3% | Async checkpoint, minimal blocking |
>
> **Projected MFU: 100% - 15% - 10% - 8% - 3% ≈ 64% → realistic: 50–58% accounting for inefficiencies**
>
> **Recommendation**: increase microbatches to 32 (from 8) to reduce pipeline bubble from 37.5% to 9.4%; this alone adds ~10% MFU.

