## § 10 Common Pitfalls

### Anti-Pattern 1: Docking Score as Absolute Truth

❌ **BAD:**
> "Compound X scored -11.2 kcal/mol in AutoDock Vina, so it must be highly potent. Let's order 100 mg immediately."

✅ **GOOD:**
> "Compound X ranks in the top 0.5% of our virtual screening library by Vina score (-11.2 kcal/mol). This is a promising hypothesis. Before synthesis, we will verify: (1) the docking pose makes chemical sense at the pharmacophore level, (2) no PAINS alerts, (3) ADMETlab ADMET profile is acceptable. We will synthesize and test in our primary assay at 10 µM first."

**Why it matters:** Docking score correlates with experimental IC50 with R2 ~ 0.2-0.4 in most benchmarks. Hit rates from virtual screening alone are typically 5-15%. Treating docking as truth wastes synthesis resources and poisons SAR campaigns.

