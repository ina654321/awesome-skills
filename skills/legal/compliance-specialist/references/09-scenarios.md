# Scenario Examples

## 9.1 FCPA Anti-Bribery Investigation

**User:** "Our sales team in Country X paid a $5,000 'facilitation fee' to a government health official to expedite a drug approval. Is this a violation?"

**Expert:**
> **FCPA Analysis:**
>
> | Element | Analysis |
> |---------|----------|
> | **Foreign official?** | Yes — government health official |
> | **Payment to obtain/retain business?** | Expediting drug approval = business advantage |
> | **Threshold** | No minimum — any payment can violate |
> | **Willfulness** | "Facilitation fee" is not a defense |
>
> **Immediate Actions:**
> 1. **Stop all payments** to that official immediately
> 2. **Preserve records** — emails, receipts, approval chains
> 3. **Notify CLO/CCO** — mandatory escalation
> 4. **Do NOT destroy** documents (obstruction risk)
>
> **Disclosure Decision:**
> | Factor | Consideration |
> |--------|---------------|
> | DOJ/SEC voluntary disclosure | Significant penalty reduction (up to 50%) |
> | Self-reporting timeline | Within 6 months preferred |
> | Remediation | Disgorgement + potential penalties |
> | Criminal referral | If willful, DOJ criminal exposure |
>
> **Key Defense Issues:**
> - Books and records accuracy (SOX books and records)
> - Internal controls failure
> - Was this isolated or systemic?
> - Were executives involved?

## 9.2 Data Breach Notification

**User:** "We discovered a ransomware attack that compromised 50,000 customer records including SSNs. What are our notification obligations?"

**Expert:**
> **Multi-Regulation Notification Analysis:**
>
> | Regulation | Trigger | Timeline | Authority |
> |------------|---------|----------|----------|
> | **State breach laws** | Each state has different law | 30-90 days (varies) | State AG |
> | **HIPAA** | If healthcare data | 60 days | HHS OCR |
> | **GDPR** | If EU residents affected | 72 hours | EU DPA |
> | **GLBA** | If financial data | 30 days | FTC |
> | **PCI-DSS** | If card data affected | Notify card brands | Card brands |
>
> **Notification Content Requirements:**
> ```
> Required in most state notifications:
> ├── What happened (general description)
> ├── Types of info compromised
> ├── Steps we're taking
> ├── Timeline of discovery and breach
> ├── Contact for questions
> └── Identity theft protection services (increasingly required)
> ```
>
> **Workflow:**
> 1. **Triage**: What data, how many, what states/countries
> 2. **Legal hold**: Preserve forensic evidence
> 3. **Forensic investigation**: Scope the breach
> 4. **Notification decisions**: State-by-state analysis
> 5. **Draft notices**: Legal review of each version
> 6. **Submit**: File with state AGs, HHS, EU DPA
> 7. **Notify individuals**: Direct mail or email
> 8. **Credit monitoring**: Offer identity protection

## 9.3 Third-Party Vendor Risk

**User:** "Our SaaS vendor who handles our customer billing data just got acquired. They claim nothing changes. How do we assess continuity of compliance?"

**Expert:**
> **Post-Acquisition Vendor Risk Assessment:**
>
> | Risk Area | Questions to Ask |
> |-----------|------------------|
> | **Contractual** | Change of control clause triggered? Does buyer assume obligations? |
> | **Data handling** | Are our data boundaries maintained? Is isolation preserved? |
> | **Certifications** | SOC 2, ISO 27001 still valid? Audit reports current? |
> | **Sub-processors** | New sub-processors added? GDPR Article 28 notification? |
> | **Security** | Penetration testing frequency? Incident history? |
> | **Financial** | Can buyer maintain service level commitments? |
>
> **Decision Framework:**
> 1. **Request updated security documentation**: SOC 2 Type II, penetration test
> 2. **Review buyer reputation**: Past incidents, regulatory actions
> 3. **Audit rights**: Can you audit per contract terms?
> 4. **Termination rights**: If risk unacceptable, can you exit?
> 5. **Renegotiation**: Update DPAs, BC/DR provisions
>
> **Key Contracts to Review:**
> - Data Processing Agreement (DPA) under GDPR §28
> - Business Associate Agreement (BAA) under HIPAA
> - Service Level Agreement (SLA) with remedy provisions
> - Indemnification provisions
