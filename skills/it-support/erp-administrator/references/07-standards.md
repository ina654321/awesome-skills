## 7. Standards & Reference

**ITGC — IT General Controls Framework:**

IT General Controls are the foundational controls that auditors verify before relying on application controls in the ERP. Four ITGC domains relevant to ERP administration:

| ITGC Domain | Key Controls | Evidence for Audit |
|---|---|---|
| **Logical Access** | User access provisioning/deprovisioning, SoD enforcement, privileged access management | Access request forms, termination checklists, SoD conflict reports, quarterly access certifications |
| **Change Management** | Change request documentation, testing evidence, approval records, transport logs | Change tickets, test results, CAB meeting minutes, transport request lists |
| **Computer Operations** | Batch job scheduling, monitoring, failure response | SM37 job logs, incident tickets for failures, job schedule documentation |
| **Program Development** | SDLC documentation, code review, separation of dev/test/prod | Transport logs (DEV→QAS→PRD), ABAP code review evidence, functional sign-off |

**SOX Section 302/404 — ERP-Relevant Requirements:**

- Section 302: CEOs and CFOs must certify the accuracy of financial statements. ERP controls that ensure data integrity (period close controls, journal entry controls, access controls) are directly in scope.
- Section 404: Management must assess and report on the effectiveness of internal controls over financial reporting. ERP access controls, SoD controls, and change management controls are tested annually by external auditors.

**SAP SoD Conflict Matrix — Highest Risk Combinations:**

| Risk Scenario | Conflicting Capabilities | Fraud Enabled |
|---|---|---|
| Procure-to-Pay | Create vendor + Approve PO + Process payment | Ghost vendor payment fraud |
| Order-to-Cash | Create customer + Release credit block + Post AR | Revenue manipulation |
| Record-to-Report | Post journal entry + Approve journal entry | Earnings manipulation |
| Payroll | Maintain HR master data + Run payroll + Post payroll | Ghost employee fraud |
| Fixed Assets | Create asset master + Retire asset + Post depreciation | Asset misappropriation |

**Performance Metrics and Target Ranges:**

| Metric | Target | Alert Threshold | Measurement Tool |
|---|---|---|---|
| System Availability | 99.9% (< 8.7 hours downtime/year) | < 99.5% | Solution Manager system monitoring |
| Batch Job Completion Rate | > 99% complete within window | < 98% or any critical job failure | SM37 daily review |
| SoD Violation Count (Critical) | 0 unmitigated critical conflicts | Any unmitigated critical SoD | SAP GRC Access Control |
| Data Migration Accuracy | > 99.9% record-level accuracy | < 99.5% | Migration reconciliation report |
| Cutover Window Duration | < 24 hours for mid-market ERP | > 20 hours (escalate to extend window) | Cutover runbook tracking |
| IDOC Processing Success Rate | > 99.5% | < 99% triggers incident | BD87 daily monitoring |
| Dialog Response Time (95th percentile) | < 1 second | > 2 seconds sustained | SAP CCMS

**COBIT Framework for ERP Governance:**

Applicable COBIT 2019 processes for ERP administration:
- **APO01** (Manage IT Management Framework): ERP policies and standards
- **APO12** (Manage Risk): SoD risk management, integration risk
- **BAI06** (Manage IT Changes): ERP change management process
- **DSS01** (Manage Operations): Batch job management, system monitoring
- **DSS06** (Manage Business Process Controls): Application controls over financial transactions

