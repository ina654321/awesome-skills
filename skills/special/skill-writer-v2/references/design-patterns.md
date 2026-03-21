# Design Patterns

**Quick Pick:**

| Pattern | Use When |
|---------|----------|
| **Tool Wrapper** | "Use X correctly" — If-then by task |
| **Generator** | "Create output" — Vars → Template → Output |
| **Reviewer** | "Audit" — Checklist → Evaluate → Report |
| **Inversion** | "Gather first" — Questions → Validate → Act |
| **Pipeline** | "Ordered steps" — Step 1 → Step 2 → Step 3 |

---

## Details

**Tool Wrapper:**
```
IF "rotate" → rotate.py
IF "merge" → merge.py
```

**Generator:**
```
Collect: audience, purpose
template = select( audience )
generate( template, constraints )
```

**Reviewer:**
```
for item in checklist:
    verdict = evaluate(item)
report(verdicts)
```

**Inversion:**
```
ASK questions
[STOP: validate]
THEN act
```

**Pipeline:**
```
Step 1 [PREREQ: X, DONE: Y]
Step 2 [PREREQ: Step 1]
[NO SKIP]
```

---

**Composition:** Generator+Inversion, Pipeline+Reviewer
