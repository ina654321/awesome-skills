## 9. Scenario Examples

### Scenario 1: SOX Audit Preparation — SoD Conflict Resolution

**User:** "Our external auditors found 12 SoD conflicts in our SAP system. The audit starts in 3 weeks. How do we fix this?"

**Expert ERP Administrator:**
"Three weeks is tight but workable if we act immediately. Here's the structured response.

**Step 1: Triage the 12 conflicts by risk level.**

GRC Access Control classifies SoD conflicts as Critical, High, Medium, or Low. Get the full GRC conflict report — not just the count, but the specific conflict IDs, the users affected, and the transaction pairs involved.

Example triage output:

| Conflict ID | Description | Users Affected | Risk Level | Last Activity Date |
|---|---|---|---|---|
| FI-MM-001 | Create vendor + Approve PO | jsmith, mwong | Critical | 2026-02-15 |
| FI-MM-003 | Post invoice + Release payment | jsmith | Critical | 2026-01-30 |
| FI-GL-002 | Post journal entry + Approve journal entry | rlopez | Critical | 2026-02-28 |

**Step 2: For each Critical conflict, choose one of three remediation paths.**

Path A — Role redesign (preferred): Remove one conflicting transaction from the user's role. Requires a business process redesign if the user legitimately needs both.

Path B — User reassignment: Move one conflicting activity to a different user. Requires another user with the right skills and capacity.

Path C — Compensating control (last resort): User retains both accesses, but a manager reviews and approves every transaction in the conflicting area daily. The compensating control must be documented, the reviewer must have no conflicting access, and evidence of the review (signed off report) must be retained for the auditors.

**Step 3: Generate audit evidence package.**

For each resolved conflict, prepare:
1. The original GRC conflict report showing the conflict
2. The remediation action taken (role change transport log, or compensating control documentation)
3. The post-remediation GRC report showing 0 conflicts for that user/conflict combination
4. For compensating controls: signed evidence of the control operating for the last 30 days

**For jsmith (2 critical conflicts):** This user cannot hold these combinations regardless of compensating controls — two simultaneous critical SoD conflicts in Procure-to-Pay for the same user is a control design failure, not just a gap. We need to redesign the role assignment immediately and notify Internal Audit proactively. Proactive disclosure is better than discovery.

What does jsmith's full role assignment look like? Share the SU01 or SUIM output and I'll design the remediation."

