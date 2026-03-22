# Apple Silicon Deep Dive

## Apple Silicon Generations

### M1 Series (2020)
**Process:** TSMC 5nm (N5)
**Transistors:** 16 billion

| Chip | CPU Cores | GPU Cores | Neural Engine | Memory | Target |
|------|-----------|-----------|---------------|--------|--------|
| M1 | 8 (4P+4E) | 8 | 11 TOPS | 8-16GB | MacBook Air, Pro 13", mini |
| M1 Pro | 10 (8P+2E) | 16 | 11 TOPS | 16-32GB | MacBook Pro 14"/16" |
| M1 Max | 10 (8P+2E) | 32 | 11 TOPS | 32-64GB | MacBook Pro 16", Studio |
| M1 Ultra | 20 (16P+4E) | 64 | 22 TOPS | 64-128GB | Mac Studio |

### M2 Series (2022)
**Process:** TSMC 5nm (N5P)
**Transistors:** 20 billion

| Chip | CPU Cores | GPU Cores | Neural Engine | Memory | Target |
|------|-----------|-----------|---------------|--------|--------|
| M2 | 8 (4P+4E) | 10 | 15.8 TOPS | 8-24GB | MacBook Air, Pro 13" |
| M2 Pro | 12 (8P+4E) | 19 | 15.8 TOPS | 16-32GB | MacBook Pro 14"/16", mini |
| M2 Max | 12 (8P+4E) | 38 | 15.8 TOPS | 32-96GB | MacBook Pro 16", Studio |
| M2 Ultra | 24 (16P+8E) | 76 | 31.6 TOPS | 64-192GB | Mac Studio, Pro |

### M3 Series (2023)
**Process:** TSMC 3nm (N3B) — First 3nm consumer chip
**Transistors:** 25 billion

| Chip | CPU Cores | GPU Cores | Neural Engine | Memory | Target |
|------|-----------|-----------|---------------|--------|--------|
| M3 | 8 (4P+4E) | 10 | 18 TOPS | 8-24GB | MacBook Pro 14", iMac |
| M3 Pro | 12 (6P+6E) | 18 | 18 TOPS | 18-36GB | MacBook Pro 14"/16" |
| M3 Max | 16 (12P+4E) | 40 | 18 TOPS | 36-128GB | MacBook Pro 16" |
| M3 Ultra | - | - | - | - | (Not released) |

**M3 Key Features:**
- Hardware-accelerated ray tracing (GPU)
- Mesh shading
- Dynamic Caching
- AV1 decode support

### M4 Series (2024)
**Process:** TSMC 3nm (N3E) — Second generation 3nm
**Transistors:** 28 billion (base)

| Chip | CPU Cores | GPU Cores | Neural Engine | Memory | Target |
|------|-----------|-----------|---------------|--------|--------|
| M4 | 10 (4P+6E) | 10 | 38 TOPS | 16-32GB | iPad Pro, iMac, Mac mini, MacBook Pro |
| M4 Pro | 14 (10P+4E) | 20 | 38 TOPS | 24-64GB | MacBook Pro 14"/16", Mac mini |
| M4 Max | 16 (12P+4E) | 40 | 38 TOPS | 36-128GB | MacBook Pro 14"/16" |
| M4 Ultra | Expected 2025 | | | | |

**M4 Key Features:**
- 2x Neural Engine performance vs M3
- Hardware ray tracing + mesh shading
- Dynamic Caching
- Optimized for Apple Intelligence
- 2nd gen 3nm = better efficiency

## Architecture Details

### CPU Design
**big.LITTLE Architecture:**
- **Performance Cores:** High IPC, high frequency (Everest in M4)
- **Efficiency Cores:** Power efficient for background tasks (Sawtooth in M4)
- **Asymmetric Design:** macOS/iOS scheduler optimizes task placement

**Cache Hierarchy:**
- L1 I-Cache: 192KB (P-core), 64KB (E-core)
- L1 D-Cache: 128KB (P-core), 64KB (E-core)
- L2 Cache: 16MB shared (P-cores), 4MB shared (E-cores)
- System Level Cache: 48MB+ (varies by chip)

### Neural Engine
**M4 Neural Engine:**
- 16 cores
- 38 TOPS (INT8)
- Accelerates: ML inference, transformer models, computer vision
- Apple Intelligence: Runs 7B parameter models on-device

### Memory Architecture
**Unified Memory:**
- Shared pool between CPU, GPU, Neural Engine
- No copying between processors
- High bandwidth: 120GB/s (M4) to 546GB/s (M4 Max)
- Low latency access for all compute units

## Performance Benchmarks

### Geekbench 6 (M4 Series)

| Chip | Single-Core | Multi-Core | Metal GPU |
|------|-------------|------------|-----------|
| M4 | 3,767 | 14,677 | 53,792 |
| M4 Pro | 3,920 | 22,000 | ~80,000 |
| M4 Max | 4,050 | 24,000 | ~140,000 |

### Comparison to Intel
- M4 single-core: ~2x Intel Core i9-13900K
- M4 multi-core: Comparable to Intel i7-13700H at 1/4 the power
- GPU: M4 Max ~RTX 4080 Laptop in some workloads

---

*Last Updated: March 2026*
