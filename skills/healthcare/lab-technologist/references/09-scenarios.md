# Scenario Examples

## 9.1 Critical Value Handling

**User:** "A potassium result of 6.8 mEq/L came back on a patient in the ED. The ordering physician is not immediately available. What do you do?"

**Expert:**
> **Assessment:**
> - Critical value: K+ >6.5 mEq/L
> - Life-threatening if untreated
>
> **Protocol:**
> ```
> Step 1: Verify Result
> ├── Check for hemolysis (releasable K+)
> ├── Verify calibration
> ├── Check previous K+ values
> └── Repeat test on original sample
>
> Step 2: Notification
> ├── Find ordering physician
> ├── If unavailable: Contact covering physician
> ├── If unavailable: Contact ED charge RN
> ├── Document all attempts
> └── Minimum 3 attempts documented
> ```
>
> **Documentation Requirements:**
> - Patient name, MRN
> - Test, result, units
> - Date and time
> - Who notified and when
> - Result relayed to
>
> **Escalation:**
> - If no response after 30 minutes
> - Contact lab supervisor
> - Consider clinical pathology consultation

## 9.2 ABO Discrepancy Resolution

**User:** "The forward group types as O, but the reverse shows anti-A antibodies. What investigation is needed?"

**Expert:**
> **Analysis:**
>
> **Possible Causes:**
> ```
> Forward O / Reverse Anti-A present:
> ├── Patient is truly group O (normal)
> ├── Weak subgroups of A
> ├── rouleaux formation
> ├──冷凝集素
> └── Recent transfusion
> ```
>
> **Resolution Steps:**
> ```
> 1. Incubate at room temp and 37°C
> 2. Perform direct antiglobulin test (DAT)
> 3. Check for cold-reactive antibodies
> 4. Review transfusion history
> 5. Adsorption studies if needed
> 6. Consult blood bank physician
> ```
>
> **Patient Safety:**
> - Do NOT release type until resolved
> - Consider units as type O if urgent
> - Document discrepancy resolution
> - Alert transfusion service of findings
