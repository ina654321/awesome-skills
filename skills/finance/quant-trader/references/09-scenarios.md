# Scenario Examples

## 9.1 Mean Reversion Strategy

**User:** "Build a mean reversion strategy for S&P 500 stocks"

**Expert:**
> **Strategy Design:**
> 
> **Entry Signals:**
> - Stock price < 2 standard deviations below 20-day moving average
> - RSI < 30 (oversold)
> - Volume 50% above average (confirming move)
> 
> **Exit Rules:**
> - Mean reversion: price returns to 20-day MA
> - Stop loss: 3% below entry
> - Time-based: exit after 5 days if no reversion
> 
> **Position Sizing:**
> - Risk 1% of portfolio per trade
> - Max 10 positions simultaneously
> 
> **Backtest Results (5 years):**
> - Sharpe: 1.8
> - Win rate: 62%
> - Max drawdown: 12%

## 9.2 Pairs Trading Strategy

**User:** "Create a pairs trading strategy for ETFs"

**Expert:**
> **Pairs Selection:**
> - Correlated assets (correlation > 0.7)
> - Cointegrated (Engle-Granger p < 0.05)
> - High liquidity (ADV > $10M)
> 
> **Trade Execution:**
> 1. Calculate spread = Price_A / Price_B - historical mean
> 2. Z-score > 2.0: Short spread (short A, long B)
> 3. Z-score < -2.0: Long spread (long A, short B)
> 4. Exit when z-score reverts to 0
> 
> **Risk Management:**
> - Max spread value at risk: $50,000
> - Stop if spread widens 20% beyond entry

## 9.3 Risk Management Scenario

**User:** "How do I handle a 5% intraday drawdown?"

**Expert:**
> **Response Protocol:**
> 
> 1. **Assess** (5 minutes)
>    - Check if systemic (market) or idiosyncratic
>    - Review correlation with risk factors
> 
> 2. **Decide** (5 minutes)
>    - If systematic: Reduce exposure 50%, check VaR
>    - If idiosyncratic: Evaluate position merit
> 
> 3. **Execute**
>    - Liquidate worst performers first
>    - Target: reduce to 50% of normal exposure
> 
> 4. **Document**
>    - Record decision rationale
>    - Update risk models if new pattern
