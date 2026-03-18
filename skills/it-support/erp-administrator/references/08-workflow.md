## 8. Standard Workflow

### Phase 1: ERP Security Role Design

**Input:** Business process description, job function matrix, existing role catalog (if available), SOX in-scope process list.

**Step 1 — Job Function Analysis [✓ Done: all job functions documented with process steps]**
Map each job function to its required business process steps. Example: "AP Clerk" → create vendor invoice, match to PO, post invoice; NOT: approve PO, create vendor master, release payment. Document the mapping in a role concept matrix: job function, process steps, required SAP transactions, required authorization objects with permitted values.
[✗ FAIL: any job function with access to approve their own transactions — return for process redesign]

**Step 2 — SoD Conflict Check [✓ Done: GRC simulation run; 0 critical conflicts; all medium conflicts documented]**
Before creating roles, run a GRC Access Control simulation with the proposed role assignments. Review all critical SoD conflicts. For each critical conflict: either redesign the role to eliminate the conflict, or document a formal compensating control (who performs the compensating control, how frequently, and what evidence is retained).
[✗ FAIL: any critical SoD conflict without a documented and approved compensating control]

**Step 3 — Role Build and Unit Test [✓ Done: roles built in DEV; all required transactions accessible; no unauthorized transactions accessible]**
Build roles in the DEV client using PFCG (SAP role maintenance). Test each role with a test user: verify all required transactions are accessible with required authorization object values, verify unauthorized transactions are blocked (negative testing). Document test results with screenshots for audit evidence.
[✗ FAIL: any negative test passes (user can access a transaction they should not have access to)]

**Step 4 — Transport to QAS and Business Sign-Off [✓ Done: transport to QAS complete; business process owner sign-off received]**
Transport roles to QAS via the transport system (never copy roles manually between clients). Business process owners test roles using business scenarios, not SAP transactions. Sign-off is obtained in writing (ticket, email chain, or formal test sign-off document) before the transport to PRD is released.
[✗ FAIL: transport to PRD without written business sign-off]

**Step 5 — Production Transport and Access Certification [✓ Done: roles active in PRD; user assignments complete; GRC shows 0 critical conflicts in PRD]**
Transport approved roles to PRD. Assign roles to users via SU01. Run a GRC Access Control production report immediately after assignment to confirm the live system matches the approved design. Schedule the first access certification review for 90 days after go-live.
[✗ FAIL: PRD GRC report shows any SoD conflict not present in the QAS simulation]

