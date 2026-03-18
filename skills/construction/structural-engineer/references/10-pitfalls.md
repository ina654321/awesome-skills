## § 10 · Common Pitfalls & Anti-Patterns

| # | Anti-Pattern | Severity | Quick Fix |
|---|--------------|----------|-----------|
| 1 | **Ignoring load path continuity** | 🔴 High | Trace loads from roof to foundation before sizing members |
| 2 | **Skipping soft-story analysis** | 🔴 High | Require lateral analysis at all levels; flag discontinuities |
| 3 | **Under-designing connections** | 🔴 High | Design connections for member capacity, not applied load |
| 4 | **Neglecting foundation-soil interaction** | 🔴 High | Obtain geotechnical report; design within recommended bearing |
| 5 | **Ignoring torsion in lateral systems** | 🟡 Medium | Check building regularity; add torsion analysis for irregular plans |
| 6 | **Assuming existing conditions match drawings** | 🟡 Medium | Verify as-built conditions; don't rely solely on old drawings |
| 7 | **Specifying generic details without project context** | 🟡 Medium | Detail for specific loads, materials, and construction sequence |

```
❌ "The architect says use W12x26 beams, so I'll design for that."
✅ "What is the actual load? Let's calculate required size, then check if W12x26 works."

❌ "We don't need special inspection for this simple building."
✅ "IBC 1705 requires special inspection for welding, bolting, and concrete placement."

❌ "The connection is standard—use the typical detail."
✅ "Verify forces at this specific location; the typical detail may not apply here."
```

