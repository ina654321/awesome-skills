## 8. Standard Workflow

### 8.1 Architecture Specification Phase

```
Phase 1: Workload Characterization
├── Profile target models (ResNet, BERT, LLaMA-70B, etc.) for:
│   ├── Op breakdown: % Conv2D, % GEMM, % Attention, % Elementwise
│   ├── Arithmetic intensity per op: FLOPS
│   └── Batch-size sensitivity: roofline position at batch=1 vs. batch=64
├── Identify dominant bottleneck: memory BW vs. compute throughput
└── Deliverable: Roofline chart + Op-type distribution per model

Phase 2: Architecture Decision
├── Select dataflow (WS/OS/RS) based on dominant op type
├── Size PE array: target MAC count = (TOPS_target × 10^12)
├── Size SRAM hierarchy: L1 per-PE scratchpad + L2 shared buffer
│   Rule of thumb: L2 SRAM ≥ 2× largest activation tile
│   SRAM area at 7nm: ~0.3 MB/mm²
├── Select HBM variant: HBM2e (460 GB/s) / HBM3 (819 GB/s) / HBM3e (1.2 TB/s)
└── Deliverable: Architecture spec document (PPA estimates, block diagram)

Phase 3: Microarchitecture Design
├── Define ISA: vector ops (VLOAD, VMAC, VSTORE), matrix ops (MATMUL, CONV)
├── Design pipeline: fetch → decode → execute → writeback (depth 4–8 stages)
├── Implement memory controller: burst prefetch, bank interleaving, write-combine
├── Integrate sparse compute unit (optional): 2:4 structured sparsity accelerator
└── Checkpoint: RTL functional simulation with synthetic workloads
```

### 8.2 Tape-out Preparation

```
Step 1: RTL freeze → synthesis (Synopsys DC): area, power, timing closure
Step 2: Physical design (Cadence Innovus): floorplan, P&R, DRC/LVS sign-off
Step 3: Timing sign-off (Synopsys PrimeTime): setup/hold timing at all corners
Step 4: Power sign-off (Ansys RedHawk): IR drop < 3% Vdd; EM within limits
Step 5: Tapeout checklist: eCO review, mask data verification, PDK sign-off
```

