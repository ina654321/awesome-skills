## § 7 Standards & Reference

### Regulatory & Scientific Frameworks

1. **ICH M7**: Assessment and control of DNA reactive (mutagenic) impurities in pharmaceuticals — defines acceptable intakes and structural alert classes; mandatory for IND filings.

2. **ICH S7B

3. **Lipinski's Rule of Five (Ro5) + Veber Rules**: Oral bioavailability guidelines; Veber adds rotatable bonds (≤ 10) and TPSA (≤ 140 A2) for intestinal permeability.

### Key Metrics Table

| Metric | Formula
|--------|-----------------|--------------|-------------------|
| Binding Affinity (IC50) | Competitive binding
| Ligand Efficiency (LE) | LE = -deltaG / N_heavy_atoms | > 0.30 kcal/mol/atom | < 0.25 |
| Lipophilic Efficiency (LipE) | LipE = pIC50 - LogP | > 5 (excellent) | < 3 (flag) |
| LogP (cLogP) | Calculated partition coefficient | 0 to 3 (oral drug) | > 5 (high CYP risk) |
| TPSA | Sum of polar surface areas (A2) | < 90 A2 (good permeability) | > 140 A2 (poor oral) |
| HLM CLint | Human liver microsome intrinsic clearance | < 20 µL/min/mg | > 100 µL/min/mg (high) |
| hERG IC50 | Patch-clamp
| Solubility (kinetic) | Nephelometry / UV at pH 7.4 | > 50 µg/mL | < 10 µg/mL |
| SA Score | RDKit synthetic accessibility (1=easy, 10=hard) | < 3.5 | > 5 (deprioritize) |
| Selectivity Ratio | IC50(off-target)
| QSAR R2 (test) | Pearson R2 on external test set | > 0.70 | < 0.50 (retrain) |
| Docking Score (Vina) | Binding free energy estimate (kcal/mol) | < -8.0 kcal/mol | > -5.0 (weak) |

