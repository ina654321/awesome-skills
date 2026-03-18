## 7. Standards & Reference

### 7.1 Microarchitecture Dataflow Comparison

| Dataflow / 数据流 | Stationary Element / 驻留元素 | Best For / 最适合 | Data Reuse
|------------------|-------------------------------|------------------|----------------------|
| **Weight-Stationary (WS)** | Weights in PE registers | Inference: small batch, large models (reuse weights across inputs) | Weight reuse ↑, activation traffic high |
| **Output-Stationary (OS)** | Partial sums in PE registers | Dense GEMM with large output tiles | Reduces accumulation traffic; good for batched inference |
| **Row-Stationary (RS)** | Row of inputs + weights | Conv2D with sliding window; flexible reuse | Optimal for convolutional layers (MIT TPU-like) |
| **No Local Reuse (NLR)** | Nothing stationary | Fully irregular sparse compute | Maximizes hardware flexibility; low efficiency for regular ops |

### 7.2 Key Benchmarks & Targets

| Metric / 指标 | Formula / 公式 | Industry Target
|--------------|--------------|--------------------------|
| **TOPS/W (Energy Efficiency)** | Tera-ops / Total chip power | Edge NPU: >10 TOPS/W; Cloud AI: >3 TOPS/W |
| **HBM BW Utilization** | Measured BW
| **MAC Utilization** | Actual FLOPS
| **Memory Capacity / Model Size** | HBM GB
| **Roofline Ridge Point** | Peak GFLOPS / Peak GB/s | H100: ~1.18 FLOPs/byte; A100: ~0.84 FLOPs/byte |

