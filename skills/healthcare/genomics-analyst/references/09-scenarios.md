# Scenario Examples

## 9.1 Rare Disease Variant Interpretation

**User:** "WES reveals a heterozygous missense variant in a gene associated with an autosomal recessive condition. The variant is absent from population databases and predicted damaging by multiple in silico tools. How do I classify this?"

**Expert:**
> **Analysis:**
>
> **Variant Information:**
> - Gene: Associated with autosomal recessive disease
> - Inheritance: AR condition
> - Population frequency: Absent
> - In silico: Predicted damaging (SIFT, PolyPhen, CADD)
>
> **ACMG Criteria Evaluation:**
> ```
> Pathogenic Criteria:
> ├── PVS1: Null variant in gene causing LOF disease? (missense = possibly)
> ├── PM2: Absent from controls (exomes/genomes) ✓
> ├── PP3: Multiple predictors damaging ✓
> └── PP4: Phenotype matches disease ✓
> ```
>
> **Classification:**
> - Current evidence: PM2 + PP3 + PP4 = **Likely Pathogenic**
> - Upgrade to Pathogenic requires:
>   - Functional studies showing LOF
>   - Co-segregation in affected family members
>   - Additional supporting evidence
>
> **Clinical Recommendations:**
> - Test parents for variant status
> - If one parent carrier → consistent with diagnosis
> - If neither parent carries → consider de novo or mosaicism
> - Offer targeted variant testing for future pregnancies

## 9.2 Pharmacogenomics Action

**User:** "Patient is scheduled to start clopidogrel after PCI. Pre-procedure genetic testing shows CYP2C19 *2/*2 genotype (poor metabolizer). What is the recommendation?"

**Expert:**
> **Analysis:**
>
> **CYP2C19 *2/*2 Implications:**
> - Poor metabolizer phenotype
> - Cannot convert clopidogrel to active metabolite
> - Reduced platelet inhibition
> - Increased cardiovascular events
>
> **Clinical Evidence:**
> ```
> CPIC Guidelines (2022):
> ├── Poor metabolizers: Alternative antiplatelet recommended
> ├── Recommendation: Prasugrel or ticagrelor
> ├── Contraindication: Standard clopidogrel dosing
> └── Evidence: Multiple studies show increased MACE
> ```
>
> **Recommended Action:**
> ```
> 1. Do NOT use clopidogrel
> 2. Prescribe prasugrel (if no contraindications)
>    - Prasugrel dose: 5-10mg daily
>    - Caution: Bleeding risk, elderly
> 3. OR ticagrelor (if prasugrel contraindicated)
>    - Ticagrelor dose: 90mg BID
> 4. Document genotype result in medical record
> 5. Consider pharmacogenomic note for future prescribing
> ```
>
> **Documentation:**
> - Alert added to EHR for CYP2C19 PM
> - Flag relevant drugs (SSRIs, PPIs, opioids)
