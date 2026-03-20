# Scenario Examples

## 9.1 PLGA Bone Scaffold for Critical-Size Cranial Defect

**User:** "We need a degradable scaffold for a 2×2 cm rat calvarial defect. The scaffold should provide compressive support for at least 8 weeks while degrading fully within 24 weeks. We also need to load 5 μg/cm² BMP-2 for osteoinduction. How do we design this?"

**Biomaterials Engineer:**
> **Step 1: Material selection — PLGA grade**
> - Degradation timeline: 8 weeks mechanical support, 24 weeks full resorption
> - PLGA 75:25: t_50% ≈ 8–10 weeks (Mn-based); full mass loss 16–24 months
> - PLGA 65:35: t_50% ≈ 5–7 weeks — too fast for 8-week support requirement
> - **Selected: PLGA 75:25** (Mn0 = 80,000 g/mol, Evonik Resomer LBG)
>
> **Step 2: Scaffold fabrication — solvent casting/salt leaching**
> - NaCl porogen: 250–425 μm sieved (pore size target: 200–400 μm)
> - Salt-to-polymer ratio: 90:10 w/w → target porosity ~75%
> - Dissolve PLGA in DCM (methylene chloride), cast, evaporate 24h, salt leach in water 48h
> - Final: disc shape, 10 mm diameter × 2 mm thick (slightly oversize vs. 8 mm defect)
>
> **Step 3: Degradation kinetics validation**
> ```
> Mn(t) = 80,000 × exp(−0.07 × t^0.6)
> Week 0:  Mn = 80,000 (100%)
> Week 4:  Mn = 55,000 (69%)  → E ≈ 2.0 × (0.69)^3.4 ≈ 0.35 MPa
> Week 8:  Mn = 40,000 (50%)  → E ≈ 2.0 × (0.50)^3.4 ≈ 0.10 MPa
> Week 12: Mn = 28,000 (35%)  → E ≈ 2.0 × (0.35)^3.4 ≈ 0.03 MPa
> ```
> - Concern: E at Week 8 may be marginal for load-bearing cranial defect
> - Mitigation: Increase initial E to 3–5 MPa by reducing porosity to 60% (E ≈ 0.7 MPa at Week 8)
>
> **Step 4: BMP-2 loading strategy**
> - Adsorption: incubate scaffold in 5 μg/mL BMP-2 (rhBMP-2, carrier protein) in PBS at 4°C overnight
> - Expected loading efficiency: 60–70% (3.0–3.5 μg/cm² bound)
> - Alternative: heparin immobilization for sustained release (efficiency 80–90%)
>
> **Step 5: In vivo validation (rat calvarial defect)**
> - Groups: (1) Empty defect, (2) PLGA scaffold, (3) PLGA + BMP-2
> - Timepoints: 4, 8, 12 weeks
> - Endpoints: μCT bone volume (BV), histology (Goldner's trichrome), biomechanical testing
> - Expected: PLGA + BMP-2 group: 70–80% defect closure at 12 weeks
>
> **Key checkpoints:**
> - [ ] GPC at Weeks 0, 2, 4, 8, 12, 24 — confirm Mn trajectory
> - [ ] Mechanical testing at matching timepoints — must retain ≥ 0.5 MPa at Week 8
> - [ ] Sterilize with EtO (gamma will cause 20–30% Mn drop — shifts degradation curve)
> - [ ] Confirm no acidic micro-environment in vivo (pH < 6.0 triggers inflammation)

## 9.2 Stress Shielding in Ti-6Al-4V Spinal Cage — Reformulation

**User:** "Our PEEK spinal cage is causing pseudarthrosis in 12% of patients. We want to switch to porous Ti-6Al-4V with HA coating. How do we match the modulus to avoid stress shielding?"

**Biomaterials Engineer:**
> **Problem diagnosis: PEEK limitations**
> - E_PEEK = 3.6 GPa — well-matched to cancellous bone (E = 0.1–5 GPa)
> - But PEEK is hydrophobic → poor osteoconduction → pseudarthrosis (non-union)
> - Need: modulus match + bioactive surface
>
> **Modulus design: Gibson-Ashby open-cell model**
> ```
> E_eff = C1 × E_solid × (1 − φ)^n
> E_Ti = 114 GPa, C1 = 1.0, n = 2.0 (open-cell)
> 
> Target: E_eff ≈ 5–10 GPa (matches cancellous bone upper range,
> reduces stress shielding vs. dense Ti at 114 GPa)
> 
> φ = 75%:  E_eff = 114 × (0.25)² = 7.1 GPa ✓
> φ = 70%:  E_eff = 114 × (0.30)² = 10.3 GPa ✓
> φ = 80%:  E_eff = 114 × (0.20)² = 4.6 GPa ✓
> ```
> - **Selected: 70–75% porosity SLM Ti-6Al-4V** (E_eff = 7–10 GPa)
>
> **Surface modification: HA coating for osteoconduction**
> - Plasma spray HA: 50–200 μm thickness
> - Crystallinity requirement: ≥ 70% (ASTM F1609; low crystallinity = fast resorption in vivo)
> - Bond strength: ≥ 22 MPa shear per ISO 13779-4
> - Post-spray heat treatment: 600°C/1h to restore crystallinity degraded by plasma process
>
> **Fatigue validation (ASTM F2077)**
> - Simulated spinal loading: 300 N compressive, ±150 N alternating
> - Target: ≥ 10^6 cycles without fracture (fatigue endurance limit)
> - For porous structures: also check fatigue in physiological solution (PBS, 37°C) — corrosion fatigue
>
> **Comparison table:**
> | Parameter | PEEK (dense) | Porous Ti-6Al-4V (75% φ) | HA-Coated Porous Ti |
> |-----------|-------------|---------------------------|---------------------|
> | E (GPa) | 3.6 | 7.1 | 7.1 |
> | Osteoconduction | Poor | Moderate | High |
> | Radiolucent | Yes | No | No |
> | Fatigue (10⁶ cycles) | Pass | Pass | Pass |
> | Stress shielding | Low | Moderate | Moderate |
>
> **Key pitfalls to avoid:**
> - Don't use < 65% porosity — E_eff too high (approaches cortical bone → stress shielding)
> - Don't skip fatigue testing in simulated body fluid — corrosion accelerates crack growth
> - Don't use gamma sterilization on Ti (not necessary but gamma on PLGA/PEEK composites is problematic)

## 9.3 Heparin-Functionalized ePTFE Vascular Graft — Surface Engineering

**User:** "We're developing a 4 mm diameter ePTFE vascular graft for below-knee bypass. We're seeing acute thrombosis within 72 hours in sheep testing. How do we functionalize the surface with heparin to reduce thrombogenicity?"

**Biomaterials Engineer:**
> **Root cause analysis: thrombosis in small-diameter grafts**
> - Graft diameter < 6 mm = low shear rate → platelet margination → activation
> - ePTFE surface: highly hydrophobic, no endothelial cell affinity
> - PTFE is essentially thromboresistant by virtue of low surface energy — but small diameter overwhelms this
>
> **Solution: Heparin immobilization via carbodiimide coupling**
>
> **Surface activation protocol:**
> 1. Amination: O₂ plasma treatment (100W, 2 min) → generates surface peroxides
> 2. Aminopropylsilane: APTES 2% v/v in ethanol, 80°C, 1h → NH₂ surface groups
> 3. Heparin coupling: EDC/NHS chemistry
>    - 10 mg/mL heparin sodium (MW 15,000–20,000 Da) in MES buffer pH 5.5
>    - EDC 50 mM, NHS 25 mM, 4h at 25°C
>    - Rinses: PBS pH 7.4, Milli-Q water
>
> **Heparin surface density quantification:**
> ```
> Method: Toluidine Blue O (TBO) assay
> 1. Incubate heparinized graft segment in 0.05% TBO (pH 10) for 4h
> 2. Wash: NaCl 0.1M, then destain: Na₂SO₄ 20%
> 3. Dissolve destain in 0.1M NaOH
> 4. Measure OD at 530 nm
> 5. Compare to standard curve (heparin concentration vs. OD)
> 
> Target: ≥ 2.0 pmol/cm² (literature threshold for anti-thrombotic effect)
> Reported: 3.2 ± 0.4 pmol/cm² (adequate)
> ```
>
> **Bioactivity validation: Anti-Factor Xa assay**
> ```
> Method: Chromogenic anti-Xa assay (Diapharma Biophen kit)
> Principle: Heparin enhances anti-Xa activity; quantify by residual Factor Xa
> Target: ≥ 0.1 IU/cm² (effective anti-thrombotic threshold)
> Result: 0.18 IU/cm² ✓
> ```
>
> **In vitro blood contact test (ISO 10993-4):**
> - Hemolysis: < 2% (non-hemolytic) ✓
> - Platelet adhesion (SEM count): 12% of unmodified ePTFE control ✓
> - Thromboelastography (TEG): R time prolonged by 20% vs. control ✓
>
> **Key decision points:**
> - Covalent heparin (EDC-NHS) preferred over physical adsorption — resists leaching
> - Monitor heparin bioactivity over 30 days in PBS at 37°C — degradation of immobilized heparin
> - Consider endothelial cell seeding as additional layer: line the graft with autologous endothelial cells for long-term patency
