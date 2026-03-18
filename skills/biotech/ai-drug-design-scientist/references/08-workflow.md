## § 8 Standard Workflow

### Phase 1: Target Assessment & Structure Preparation

**Steps:**
1. Retrieve target sequence; BLAST against UniProt; confirm biological relevance.
2. Search PDB for experimental structures; if absent, run AlphaFold2 (colabfold) with MSA depth >= 512.
3. Assess pLDDT scores; use only residues with pLDDT > 70 for pocket definition.
4. Run fpocket or SiteMap; select druggable pocket (Dscore > 0.5, volume > 300 A3).
5. Prepare protein: remove waters beyond 5 A, add hydrogens at pH 7.4, assign AMBER/OPLS force field.

[✓ Done]: High-quality pocket defined; pharmacophore features mapped; protein PDB file ready for docking.
[✗ FAIL]: pLDDT < 70 in binding site; Dscore < 0.5; multiple conflicting conformations — acquire experimental structure or use ensemble docking.

### Phase 2: Hit Identification & Virtual Screening

**Steps:**
1. Define hit criteria: IC50 < 10 µM, LE > 0.25, no PAINS alerts, Ro5 compliant.
2. Prepare screening library: ZINC22 or ChEMBL filtered by MW < 450, LogP < 4.
3. Run Gnina or AutoDock Vina docking; score top 1% by docking score.
4. Apply ADMET filter: remove hERG IC50 < 1 µM, mutagenic alerts (Ames), reactive groups.
5. Cluster by Tanimoto similarity (threshold 0.4); select diverse representatives.
6. Prioritize top 50-100 for experimental confirmation.

[✓ Done]: Ranked hit list with docking poses, ADMET flags, diversity clustering; synthesis/purchase plan ready.
[✗ FAIL]: Hit rate < 1% in assay; revisit pharmacophore hypothesis or switch to fragment screening.

### Phase 3: Hit-to-Lead Optimization (MPO)

**Steps:**
1. Build GNN-QSAR model on confirmed hits (AttentiveFP, R2 > 0.70 on test set).
2. Define MPO desirability function: weight potency (40%), ADMET (30%), LE (15%), selectivity (15%).
3. Generate analogs via REINVENT or matched molecular pair analysis (MMPA).
4. Predict MPO scores; select top 20 for synthesis.
5. Iterate: synthesize -> assay -> update model -> repeat (DBTL cycle, 3-5 iterations).
6. Confirm selectivity against closest off-targets (kinome panel, GPCR panel).

[✓ Done]: Lead compound IC50 < 100 nM, LE > 0.30, LipE > 4, HLM CLint < 50, hERG ratio > 30-fold.
[✗ FAIL]: ADMET cliff (potency gain accompanied by metabolic instability) — redesign metabolic soft spot; use deuteration or bioisostere replacement.

### Phase 4: Candidate Selection & IND Preparation

**Steps:**
1. Confirm activity in cellular assay (EC50 < 1 µM); check mechanism (target engagement, target modulation).
2. Run in vitro DMPK panel: Caco-2 permeability, PPB, metabolic ID, CYP inhibition (5-enzyme panel).
3. Complete genotoxicity assessment per ICH M7: Ames test, structural alert review, TTC analysis.
4. Prepare IND toxicology package: 28-day GLP rodent study design, NOAEL estimation.
5. Finalize candidate selection memo: potency, selectivity, DMPK, safety, synthetic route, scalability.

[✓ Done]: IND-enabling study plan approved by medicinal chemistry and regulatory team; candidate nominated.
[✗ FAIL]: Unresolved genotoxicity or hERG liability — candidate rejection; initiate backup series.

