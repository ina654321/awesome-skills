# Scenario Examples

## 9.1 Unclear Diagnosis

**User:** "The discharge summary says 'likely sepsis, rule out other causes.' The provider documented sepsis in the assessment. How should this be coded?"

**Expert:**
> **Analysis:**
>
> **Coding Decision:**
> ```
> If sepsis documented:
> ├── Assign sepsis code
> ├── Sequence as principal if treated
> └── Document clinical indicators supporting
>
> If only "likely sepsis":
> ├── Query provider for clarification
> ├── If confirmed as sepsis: code as confirmed
> └── If ruled out: code underlying condition
> ```
>
> **Query Format:**
> ```
> Dear Dr. [Name],
>
> Upon review of [Patient Name]'s record, we noted:
> - "Likely sepsis" documented in the discharge summary
> - Clinical indicators supporting sepsis: [list]
>
> Please clarify:
> □ Sepsis confirmed - assign code
> □ Sepsis ruled out - assign underlying cause
> □ Other: [specify]
>
> Thank you for your clarification.
> ```
>
> **Guideline Application:**
> - Code the condition as documented by the provider
> - Query when documentation is ambiguous
> - Cannot assume diagnosis without provider confirmation

## 9.2 Postoperative Complication Coding

**User:** "A patient had a postoperative wound infection following bowel surgery. The surgeon documented 'SSI, deep incisional, post-op day 5.' How do we code this?"

**Expert:**
> **Analysis:**
>
> **SSI Coding:**
> ```
> Classification:
> ├── Superficial incisional (T84.4xxA)
> ├── Deep incisional (T84.4xxA)
> └── Organ/space (T81.4xxA)
>
> Required Codes:
> ├── Postprocedural infection code (T81.4xxA)
> ├── Specify type and timing
> ├── Code the organism if known
> └── CC/MCC designation
> ```
>
> **Coding Logic:**
> ```
> 1. Primary procedure code (e.g., bowel resection)
> 2. Postoperative complication code
> 3. Organism code (e.g., E. coli)
> 4. Additional treatment codes
>
> DRG Impact:
> - Infection → CC or MCC
> - May affect MS-DRG assignment
> - Document medical necessity for extended stay
> ```
