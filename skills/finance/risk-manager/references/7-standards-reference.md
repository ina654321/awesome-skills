## § 7 · Standards & Reference

### 7.1 VaR Methodologies

| Method | Formula | Best For | Limitations |
|--------|---------|----------|-------------|
| **Parametric** | VaR = mu - z x sigma | Normal distributions, liquid markets | Underestimates tail risk |
| **Historical** | VaR = percentile of historical returns | Captures actual market behavior | Assumes history repeats |
| **Monte Carlo** | Simulate thousands of paths | Complex instruments, non-linear | Model-dependent; computationally intensive |

### 7.2 Credit Risk Parameters

```
Expected Loss (EL) = PD x LGD x EAD

Where:
- PD = Probability of Default (12-month or lifetime)
- LGD = Loss Given Default (1 - Recovery Rate)
- EAD = Exposure at Default (includes undrawn commitments)

Unexpected Loss (UL) = EAD x sqrt[PD x sigma^2LGD + LGD^2 x sigma^2PD]
```

### 7.3 Risk Appetite Metrics

| Metric | Definition | Typical Limit |
|--------|-----------|---------------|
| VaR Limit | Maximum daily VaR | 1% of Tier 1 capital |
| Stress Loss Limit | Maximum stress scenario loss | 5-10% of capital |
| Concentration Limit | Maximum single-name exposure | 5% of portfolio |
| Liquidity Ratio | HQLA / Net outflows | > 100% |

---
