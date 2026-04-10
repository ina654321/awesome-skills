## § 9 · Common Pitfalls & Anti-Patterns

### Anti-Pattern 1: Over-Diversification
```
BAD:  200-position "diversified" equity portfolio.
      Effectively becomes expensive index fund with higher fees.
      Active share → near 0; information ratio → negative.

GOOD: 20-40 high-conviction positions.
      Each position should be there because you have edge.
      Target: Active Share > 60% vs. benchmark.
```

### Anti-Pattern 2: Ignoring Factor Exposure
```
BAD:  "My 30% returns were pure alpha."
      (Actually: 20% came from momentum factor tilts)

GOOD: Run Fama-French 5-factor regression quarterly.
      Separate factor-driven returns from true alpha.
      Factor exposure can be replicated cheaply via ETFs.
```

### Anti-Pattern 3: VaR as the Only Risk Measure
```
BAD:  "VaR (95%) is only $3M/day. We're safe."
      VaR says nothing about loss magnitude when breached.
      2008: VaR models said ~2% max loss; actual drawdowns 50%+.

GOOD: Use CVaR (Expected Shortfall) alongside VaR.
      Stress test against 2008, 2020, 2022 explicitly.
      Scenario analysis > statistical models in tail risk.
```

### Anti-Pattern 4: Chasing Sharpe Ratio
```
BAD:  Strategies with high Sharpe (e.g., selling far OTM puts).
      Excellent Sharpe in normal markets; catastrophic in tail.
      (Short vol: Sharpe 1.5+ until VIX spike → blowup)

GOOD: Examine return distribution shape, not just Sharpe.
      Negative skewness = occasional large losses.
      If Sharpe > 2.0 and opaque strategy → red flag.
```

---
