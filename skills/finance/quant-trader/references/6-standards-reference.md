## § 6 · Standards & Reference

### 6.1 Strategy Frameworks

| Strategy | When to Use | Key Steps |
|----------|-------------|-----------|
| **Mean Reversion** | When price deviates from historical norm | 1. Calculate z-score of price vs. mean → 2. Enter when z-score exceeds threshold → 3. Exit when reverts to mean |
| **Momentum** | When trends persist | 1. Calculate returns over lookback period → 2. Go long top performers, short bottom → 3. Rebalance periodically |
| **Pairs Trading** | Two securities with high correlation | 1. Identify cointegrated pair → 2. Calculate spread z-score → 3. Long spread undervalue, short overvalue → 4. Close when spread normalizes |
| **Market Making** | When providing liquidity | 1. Post bid/ask quotes → 2. Manage inventory risk → 3. Adjust quotes based on order flow → 4. Capture bid-ask spread |
| **Volatility Trading** | When mispricing in options | 1. Calculate implied vs. realized vol → 2. Trade vol spread (long/short) → 3. Hedge delta → 4. Manage gamma risk |

### 6.2 Key Trading Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Sharpe Ratio** | (Return - Risk-free Rate) / Std Dev of Returns | ≥ 1.5 |
| **Sortino Ratio** | (Return - Target Return) / Downside Deviation | ≥ 2.0 |
| **Maximum Drawdown** | Peak to Trough | < 20% for most strategies |
| **Calmar Ratio** | Annual Return / Maximum Drawdown | ≥ 2.0 |
| **Win Rate** | Winning Trades / Total Trades | > 50% |
| **Profit Factor** | Gross Profit / Gross Loss | > 1.5 |
| **Information Ratio** | Active Return / Tracking Error | ≥ 1.0 |

---
