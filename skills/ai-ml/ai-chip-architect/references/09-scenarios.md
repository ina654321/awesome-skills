## 9. Scenario Examples

### 9.1 Scenario: Sizing the PE Array for LLaMA-70B Inference

**User:** "We need to design a chip for LLaMA-70B inference at batch=1. Target: 30 tokens/sec, 300W TDP. How many TOPS do we need and how should we size the memory system?"

**AI Chip Architect:**
> **Step 1 — Workload Analysis (LLaMA-70B, batch=1 decode phase):**
>
> - Parameters: 70B × 2 bytes (BF16) = 140 GB weights
> - Per-token decode: 70B multiply-adds = 140 GFLOPS (2 FLOPS per weight)
> - Memory traffic: all 140 GB weights must be streamed each token (no reuse at batch=1)
> - **Arithmetic Intensity** = 140 GFLOPS / 140 GB = **1.0 FLOPs/byte** — right at the roofline ridge!
>
> **Step 2 — Memory Bandwidth Requirement:**
>
> - 30 tokens/sec × 140 GB/token = **4.2 TB/s minimum** required memory bandwidth
> - Available: HBM3e = 1.2 TB/s per stack; need **4 stacks = 4.8 TB/s** (1.14× headroom)
> - Practical (70% utilization): 4 × 1.2 × 0.7 = 3.36 TB/s → insufficient!
> - **Recommendation**: 6× HBM3e stacks = 7.2 TB/s → effective 5.04 TB/s → 36 tokens/sec ✓
>
> **Step 3 — Compute Requirement:**
>
> - At the ridge point (AI ≈ 1.0), TOPS = bandwidth × AI = 5.04 TB/s × 1.0 = **5.04 PFLOPS BF16**
> - At 300W TDP → efficiency target: 5,040 TOPS / 300W = **16.8 TOPS/W** — achievable at 5nm (NVIDIA H100: ~3.5 TOPS/W at 700W; custom AI chip at 5nm: 15–20 TOPS/W feasible)
>
> **Step 4 — Architecture Summary:**
>
> | Component | Specification | Rationale |
> |-----------|--------------|-----------|
> | PE Array | 512×512 BF16 systolic array | 5.04 PFLOPS at 3.8 GHz |
> | Memory | 6× HBM3e stacks (6×96 GB = 576 GB) | Fits 70B model with 4× batch buffer |
> | SRAM | 128 MB on-chip L2 | KV cache for 2K context, attention activations |
> | Process | TSMC 5nm | 15+ TOPS/W efficiency target |
> | TDP | 300W sustained | 10% thermal headroom from 330W burst |

