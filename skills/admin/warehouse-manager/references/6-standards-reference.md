## § 6 · Standards & Reference

### 7.1 Warehouse Operations Frameworks

| Framework | When to Use | Key Steps |
|-----------------|----------------------|-------------------|
| **ABC Analysis** | Every quarter to prioritize cycle counting and slotting | 1. Sort SKUs by annual dollar usage → 2. Classify: A=top 20% ($), B=next 30%, C=bottom 50% → 3. Set count frequency: A=weekly, B=monthly, C=quarterly |
| **Safety Stock Calculation** | When lead time or demand variance is high | Safety Stock = Z × σ × √LT (Z=service factor, σ=demand std dev, LT=lead time) |
| **Dock-to-Stock** | For standard received goods that don't require inspection | 1. Receive → 2. Scan → 3. Verify quantity → 4. Direct to bin location → 5. Update WMS (target: <2 hours) |
| **Cross-Docking** | For fast-moving goods with known demand | 1. Receive → 2. Sort to outbound door → 3. Load to outbound trailer (target: <30 minutes) |

### 7.2 Warehouse Metrics

| Metric | Formula | Target |
|--------------|--------------|---------------|
| **Inventory Accuracy** | (Closing inventory value - variance)
| **Dock-to-Stock Time** | Time from trailer arrival to bin location | < 2 hours |
| **Order Accuracy** | Perfect orders
| **On-Time In-Full (OTIF)** | Orders shipped on time and complete
| **Pick Productivity** | Lines picked per hour per picker | > 150 lines/hour |
| **Dock Utilization** | Active dock doors

---
