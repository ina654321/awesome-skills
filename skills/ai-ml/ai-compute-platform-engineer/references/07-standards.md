## 7. Standards & Reference

### 7.1 Network Topology Comparison

| Topology / 拓扑 | BW per Node / 节点带宽 | Cost Scaling / 成本扩展 | Best For
|----------------|----------------------|------------------------|------------------|
| **Rail-Optimized Fat-Tree** | 8× 200 Gb/s IB = 1.6 Tb/s | O(N log N) | Large clusters (>512 GPUs); standard for H100 DGX pods |
| **Spine-Leaf (2-tier)** | 4× 400 Gb/s IB = 1.6 Tb/s | O(N) but limited scale | Mid-size clusters (<512 nodes); simpler operations |
| **NVLink + IB** | NVLink: 900 GB/s (intra-node); IB: 400 Gb/s (inter-node) | High upfront (NVSwitch) | Dense all-reduce within DGX node, scale-out across nodes |
| **RoCEv2 Ethernet** | 2× 400 GbE = 800 Gbps | Lower cost than IB | Cost-sensitive clusters; acceptable for DP-heavy workloads |

### 7.2 Key Metrics & Targets

| Metric / 指标 | Formula / 公式 | Target
|--------------|--------------|--------------|
| **MFU (Model FLOP Utilization)** | actual_FLOPS
| **Cluster GPU Utilization** | GPU-hours used
| **Job Completion Rate** | Completed jobs
| **NCCL All-Reduce BW** | measured_busbw
| **Checkpoint Recovery Time** | Time from failure → training resumed | <5 minutes for production clusters |
| **Mean Time Between Job Failure** | training_hours

