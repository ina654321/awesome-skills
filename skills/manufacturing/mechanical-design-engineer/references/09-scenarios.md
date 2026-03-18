## § 9 Scenario Examples

### Scenario 1 — Injection Molded Part Sink Marks

**User:** My injection-molded ABS housing shows sink marks on the thick section where the mounting boss connects. The wall is 4mm. How do I fix this?

**Expert:** Sink marks occur when the internal thick section cools slower than the surrounding thin wall, causing differential shrinkage. For ABS with 4mm wall:

**Root cause:** 4mm exceeds the 3:1 ratio guideline (max wall should be ~2mm for uniform cooling).

**Solution options:**
1. **Reduce wall thickness to 2.5mm** — adds weld line but eliminates sink:
```solidworks
// Create uniform wall: 2.5mm thickness throughout
// Add 0.8mm thick ribs (≤60% of wall) for stiffness
```

2. **Add hidden cavity** — pocket the thick area from inside:
```solidworks
// Pocket 1.5mm deep in interior wall
// Reduces effective wall to 2.5mm locally
```

3. **Change material to ABS+PC** — higher modulus reduces sink visibility:
```
| Material | Shrinkage | Sink Mark Resistance |
|----------|-----------|----------------------|
| ABS | 0.5-0.7% | Poor |
| ABS+PC (20%) | 0.4-0.6% | Moderate |
| PA6+30% GF | 0.3-0.5% | Excellent |
```

[RISK] Do not increase cooling time — it reduces cycle time and does not fix the root cause.

