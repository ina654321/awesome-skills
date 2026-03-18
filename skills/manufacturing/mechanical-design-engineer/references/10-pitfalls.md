## § 10 Common Pitfalls

### Anti-Pattern 1 — GD&T Without Functional Requirement

❌ **BAD:**
```
// Drawing specifies: Position Ø0.1mm at MMC
// No functional requirement defined — why Ø0.1mm?
// Supplier guesses; inspection may not catch actual failure mode
```

✅ **GOOD:**
```
// Drawing specifies: Position Ø0.1mm at MMC to ensure:
    // 1. Bolt clearance for M4 fastener (Ø4.2mm hole + 0.8mm margin)
    // 2. Pin alignment within 0.2mm for mating connector
// Note: "MMC modifier applied — bonus tolerance 0.4mm"
```

**Why it matters:** GD&T without functional basis leads to over-constrained (expensive) or under-constrained (failed) parts. Always document the "why" on the drawing or in a design note.

