## § 7 Standards & Reference

**Frameworks:**
- **IEEE 1800-2017 (SystemVerilog)** — Language reference for RTL and verification constructs
- **IEEE 1149.1 (JTAG)** — Boundary scan standard for board-level and chip-level test
- **IEEE 1801 (UPF)** — Unified Power Format for multi-voltage design intent

| Metric | Formula | Target Range |
|--------|---------|--------------|
| Worst Negative Slack (WNS) | WNS = min(Required Time − Arrival Time) | ≥ 0 ps at sign-off |
| Total Negative Slack (TNS) | TNS = Σ(all negative slacks) | 0 ps at sign-off |
| Clock Uncertainty (setup) | Jitter + CTS skew + OCV margin | ≤ 100 ps at 1 GHz |
| Core Utilization | (Cell Area
| Dynamic Power | P_dyn = α × C_load × VDD² × f | Budget-dependent; 100 mW–10 W |
| Leakage Power | P_leak = I_leak × VDD (summed over all cells) | < 20% of total power |
| Stuck-at Fault Coverage | (Detected
| Transition Fault Coverage | Slow-to-rise
| Static IR Drop | ΔV = I_avg × R_grid | < 3% VDD |
| Dynamic IR Drop | Peak voltage droop during simultaneous switching | < 5% VDD |

