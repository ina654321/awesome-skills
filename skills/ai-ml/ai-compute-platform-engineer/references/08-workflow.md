## 8. Standard Workflow

### 8.1 New Cluster Bring-Up

```
Phase 1: Hardware Validation (2–4 weeks)
├── GPU health check: nvidia-smi, DCGM DIAG, ECC error baseline
├── Network validation: IB link speed test (ib_send_bw), fabric latency (ib_send_lat)
├── NCCL bandwidth test: nccl-tests all-reduce across 8, 64, 512, all nodes
│   Target: >70% of theoretical IB BW at large message sizes (>1 GB)
├── Storage I/O: fio benchmark on Lustre OSTs; measure per-OST IOPS and bandwidth
└── Baseline MFU: run standard training script (GPT-2, Llama-7B) → record MFU

Phase 2: Software Stack Configuration (1–2 weeks)
├── SLURM: configure partitions, QoS, backfill scheduler, gang scheduling
├── Container: build NCCL-optimized container (CUDA 12.x, NCCL 2.20+, PyTorch nightly)
├── Monitoring: deploy DCGM exporter → Prometheus → Grafana dashboards
│   Key dashboards: per-GPU power/temp, MFU time-series, NCCL bandwidth, job queue depth
└── Checkpoint: configure shared Lustre quota, implement sharded checkpoint pipeline

Phase 3: Production Hardening (ongoing)
├── Fault injection test: simulate GPU failure mid-training; verify recovery < 5 min
├── Checkpoint integrity: verify load after write on every checkpoint (hash check)
├── Preemption test: verify jobs resume correctly after SLURM preemption
└── Runbook: document top 10 failure modes and recovery procedures (on-call wiki)
```

### 8.2 MFU Optimization Process

```
Step 1: Profile baseline MFU with NVIDIA Nsight Systems
  → Identify top 3 time sinks (comm wait, compute, I/O)

Step 2: Tune NCCL if communication > 20% of step time
  → export NCCL_ALGO=Ring for large messages (>1 MB); Tree for small
  → export NCCL_BUFFSIZE=33554432 (32MB) — increase for large clusters
  → export NCCL_SOCKET_IFNAME=ib0 — force IB interface (avoid Ethernet fallback)

Step 3: Tune parallelism if pipeline bubble > 15%
  → Reduce PP degree; increase microbatch count to hide bubble
  → Formula: bubble_ratio = (PP-1)
  → Target bubble_ratio < 5% → num_microbatches > 20×(PP-1)

Step 4: Tune checkpoint if I/O > 5% of step time
  → Switch from full checkpoint to per-rank sharded (PyTorch DCP)
  → async checkpoint: write in background thread while next step runs
  → Verify checkpoint doesn't block training: add timing assert

Step 5: Validate: re-run Nsight profile → confirm MFU improvement
```

