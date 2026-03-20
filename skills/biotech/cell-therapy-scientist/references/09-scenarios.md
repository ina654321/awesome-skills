# Scenario Examples

## 9.1 CAR-T Release Failure — Low Cytotoxicity Despite High Transduction

**User:** "Our CAR-T batch shows VCN = 2.1 and CAR expression = 38% (both pass), but cytotoxicity at E:T 5:1 is only 8% when our spec is ≥20%. The product is frozen and we're 2 days from scheduled infusion. What do we do?"

**Cell Therapy Scientist:**
> **Immediate decision: Do NOT release this product.**
> - Cytotoxicity is a critical quality attribute (CQA) — not optional
> - A CAR-T product that doesn't kill is a clinical failure, not just a spec miss
>
> **Root cause investigation (parallel track):**
>
> **Step 1: Check T cell exhaustion phenotype**
> - Run flow for PD-1, LAG-3, TIM-3, TIGIT
> - If PD-1+LAG-3+ > 30%: exhausted T cells from heavily pretreated patient
> - If exhausted: consider early harvest at Day 10 (vs. Day 14) for next batch
>
> **Step 2: Check CD4:CD8 ratio**
> - If CD8 < 15%: CD4-dominant product → poor cytotoxicity
> - Fix: implement CD4/CD8 sorting (1:1) before activation on next run
>
> **Step 3: Check CAR internalization**
> - High-affinity scFv → tonic signaling → antigen-induced CAR downregulation
> - Fix: reduce MOI (target VCN 1.0–1.5) to reduce surface CAR density
>
> **Step 4: Check target cell line**
> - Raji/Nalm-6 may have downregulated CD19
> - Confirm CD19 MFI on target by flow; use fresh vial; retest with confirmed antigen+
>
> **Step 5: Re-run potency assay**
> - Post-thaw viability drop: recount viable cells
> - Gate on live CD3+CAR+ cells for E:T calculation (not total cells)
> - Retest on fresh target cells
>
> **In this case:** Root cause was PD-1+LAG-3+ = 45% (exhausted starting material).
> - Next batch: harvest at Day 10 instead of Day 14
> - Result: cytotoxicity = 34% (pass)
>
> **Patient management during investigation:**
> - Delay infusion until replacement batch is ready
> - Bridge therapy if disease is aggressive (blinatumomab, chemotherapy)
> - Notify clinical team and IRB/ethics committee if delay > 7 days
> - Document deviation in batch record; investigate; don't release

## 9.2 Allogeneic iPSC-NK Cell Therapy — CRISPR Multiplex Editing

**User:** "We're developing an allogeneic off-the-shelf NK cell therapy from iPSCs. We need CAR expression (anti-BCMA), HLA-I KO (prevent host rejection), and PD-1 KO (prevent TME exhaustion). We also want to prevent NK self-attack. Walk me through the editing strategy."

**Cell Therapy Scientist:**
> **Multiplex CRISPR Editing Strategy (4 edits, sequential):**
>
> **Edit 1: B2M KO (HLA-I elimination)**
> - Target: Exon 1 of B2M gene
> - Purpose: Eliminate HLA-ABC surface expression → prevent host CD8+ T cell recognition
> - Target efficiency: ≥ 90% by flow (anti-HLA-ABC)
> - Risk: B2M-KO triggers NK cell attack via missing-self → mitigate below
>
> **Edit 2: PDCD1 KO (PD-1 elimination)**
> - Target: Exon 1 of PDCD1
> - Purpose: Prevent PD-L1/PD-L2 mediated checkpoint inhibition in TME
> - Target efficiency: ≥ 80% by flow (anti-PD-1)
>
> **Edit 3: KLRC1 KO (NKG2A elimination, optional)**
> - Target: Exon 2 of KLRC1 (NKG2A)
> - Purpose: Remove inhibitory signal from HLA-E on tumor cells
> - Target efficiency: ≥ 75% by flow (anti-NKG2A)
>
> **Edit 4: CAR knock-in at TRAC locus**
> - Method: HDR with 2A linker-truncated EGFRt donor template
> - Benefit: CAR under endogenous promoter → physiologic expression, reduced tonic signaling
> - Simultaneous selection: EGFRt enables antibody-mediated depletion if needed
>
> **Anti-NK "self" protection (critical for B2M-KO):**
> ```
> Strategy A: HLA-E overexpression (bystander)
>   - Lentiviral: HLA-E (HLA-B7 leader peptide + HLA-E open reading frame)
>   - Binds NKG2A/CD94 on NK cells → delivers inhibitory signal
>   - Does NOT trigger T cell recognition (no peptide presentation)
> 
> Strategy B: CD47 "don't eat me" signal
>   - Overexpress CD47 (SIRPα ligand) on iPSC-NK cells
>   - Prevents macrophage phagocytosis
>   - Widely used in cell therapy for persistence
> ```
>
> **Manufacturing sequence:**
> 1. iPSC → NK differentiation (IL-15 + IL-2, 28 days)
> 2. RNP electroporation: B2M sgRNA + PD1 sgRNA (simultaneous)
> 3. Antibiotic selection: puromycin (if HDR-based KI includes selection cassette)
> 4. CAR transduction: lentiviral at Day 14 of NK differentiation
> 5. Expansion: feeder-free or K562-based expansion
> 6. QC: CAR+ NK phenotype (CD56+CD3-), B2M-KO efficiency, PD-1-KO efficiency
>
> **Genotoxicity considerations:**
> - Check karyotype after each editing round (G-banding, SNP array)
> - ddPCR for large deletions at edited loci
> - Consider off-target analysis: GUIDE-seq or CIRCLE-seq
> - 3' and 5' integration site analysis by LM-PCR / LAM-PCR for lentiviral CAR

## 9.3 CAR-T Persistence Failure — Patient Relapse at Day 90

**User:** "A CD19 CAR-T patient achieved CR at Day 28 with confirmed B-cell aplasia. By Day 60, CAR-T copies were undetectable in blood. By Day 90, the patient relapsed with CD19+ disease. What happened and what's the salvage strategy?"

**Cell Therapy Scientist:**
> **Three possible mechanisms — differential diagnosis:**
>
> **Mechanism 1: T cell exhaustion (most likely given Day 60 disappearance)**
> - Evidence: Early high Cmax (> 10,000 copies/μg) with rapid collapse = hyper-expansion → exhaustion
> - Check peak PBMC: PD-1+LAG-3+TIM-3+ triple-positive T cells
> - Solution: Switch to 4-1BB co-stim domain (if CD28 was used); add ex vivo checkpoint blockade
>
> **Mechanism 2: Immune rejection of CAR-T (murine scFv immunogenicity)**
> - Evidence: CAR-T present at Day 28, disappears before Day 60
> - Test: Anti-CAR antibody titer (bridging ELISA)
> - Solution: Humanize scFv (CDR-grafting); switch from FMC63 (murine) to humanized variant
>
> **Mechanism 3: CD19 antigen escape (would have CD19- relapse, not CD19+)**
> - Evidence: Relapse tumor is CD19-dim or negative by flow/IHC
> - Solution: Tandem CD19/CD22 CAR; or switch to CD22 CAR if CD22 retained
>
> **Salvage strategy for this patient (CD19+ relapse):**
> ```
> Immediate (next 2 weeks):
> ├── Bridging therapy: blinatumomab or salvage chemo (e.g., R-DHAP)
> ├── Confirm disease burden: PET-CT, bone marrow biopsy
> ├── Assess whether second CAR-T infusion is feasible
> └── Consider clinical trial: allogeneic CAR-T, CAR-NK, CD22 CAR
>
> If second CAR-T infusion considered:
> ├── Prior CRS/ICANS history: ≥ Grade 2 → increased risk on re-challenge
> ├── Tumor burden at infusion: high burden → increased CRS/ICANS risk
> ├── If using same product: consider adding ex vivo PD-1 blockade during manufacturing
> └── If using different product: CD22 CAR or allogeneic product
>
> Long-term: 
> ├── Clinical trial enrollment if available
> ├── Allogeneic CAR-T: off-the-shelf, no patient-specific manufacturing delay
> └── Bispecific antibody: blinatumomab (CD3×CD19) as bridge or alternative
> ```
>
> **Root cause analysis for the product:**
> - Review manufacturing record: was the T cell starting material from heavily pretreated patient?
> - Check expansion protocol: was the product pushed to Day 14 (exhaustion risk)?
> - Validate CAR construct: was tonic signaling present (CD28 domain, high affinity scFv)?
> - Use this case to improve the product: next iteration should address exhaustion pathway

## 9.4 Replication-Competent Retrovirus (RCR) Detection — Contamination Suspected

**User:** "Our RCR testing came back positive on our lentiviral vector lot. We have 30 patient doses already manufactured using this lot. What do we do?"

**Cell Therapy Scientist:**
> **FDA compliance note:** A positive RCR result on a GMP vector lot requires immediate quarantine, FDA notification, and product hold. Do not administer affected doses.
>
> **Immediate actions (Day 1):**
> - Quarantine all patient product manufactured with this vector lot
> - Notify QA and Regulatory Affairs immediately
> - Do NOT release or administer any doses until investigation complete
>
> **Root cause investigation:**
> - Review vector production record: packaging plasmid integrity, producer cell bank characterization
> - Check for VSV-G recombination events in producer cell line
> - Review cell culture conditions: serum lot, confluence at transfection, passage number
> - Identify whether contamination is from production batch or detection assay (false positive)
>
> **Regulatory actions:**
> - Contact FDA: RCR positive finding must be disclosed (IND amendment)
> - Provide investigation summary and corrective/preventive action (CAPA) plan
> - Discuss with FDA: is there a path forward using a new vector lot with enhanced controls?
> - If patient doses were administered: extended clinical monitoring for RCR-related events
>
> **Patient management:**
> - Patients who received doses: extended follow-up monitoring (every 3 months × 2 years)
> - Testing for RCR in patient blood: S+L⁻ assay or qPCR at 3, 6, 12, 24 months
> - Provide bridging therapy if disease is active and CAR-T was the only planned treatment
>
> **Corrective actions for manufacturing:**
> - Revert to validated RCR-negative vector lot
> - Enhance screening: screen every vector lot before GMP product manufacturing
> - Review packaging plasmid design: is the 3-plasmid split maintained?
> - Implement additional RCR testing at producer cell bank level (not just vector harvest)
> - Consider switching to non-replicating vector (integration-deficient lentiviral, IDLV)
