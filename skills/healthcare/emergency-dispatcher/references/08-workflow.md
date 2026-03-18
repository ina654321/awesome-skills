## 8. Standard Workflow

### 8.1 Emergency Call Processing

```
Phase 1: Call Answer & Location (0-30 seconds)
├── Answer within 3 rings: "911, what's your emergency?"
├── Obtain address: "Where is the emergency located?"
├── Verify address: "Can you confirm the address?"
└── [✓ Done]: Confirmed address with callback number
    [✗ FAIL]: No address → Ask for cross-street, landmark, phone number

Phase 2: Chief Complaint & Triage (30-90 seconds)
├── Ask: "What's the problem?"
├── Obtain patient info: "How old is the patient?"
├── Assign MPDS determinant based on key questions
└── [✓ Done]: Determinant assigned
    [✗ FAIL]: Unclear determinant → Ask more specific questions

Phase 3: Pre-Arrival Instructions & Dispatch (90 seconds+)
├── Provide life-saving instructions (CPR, bleeding control)
├── Dispatch appropriate response tier
├── Provide updates to responding units
└── [✓ Done]: Units dispatched; caller following instructions
    [✗ FAIL]: Caller disconnected → Use ANI/ALI; callback; dispatch to last-known
```

### 8.2 MCI (Mass Casualty Incident) Protocol

```
Step 1: Initial Report
  → Caller reports multiple injured (e.g., "5 people hurt in car crash")
  → Ask: "How many patients total?"

Step 2: MCI Classification
  → MCI Level 1: 3-5 patients
  → MCI Level 2: 6-10 patients
  → MCI Level 3: 11+ patients

Step 3: Response Staging
  → MCI-1: 2-3 ambulances + supervisor
  → MCI-2: 4-6 ambulances + supervisor + command
  → MCI-3: 8+ ambulances + multiple commands + hospital notification

Step 4: Triage Implementation (START)
  → Step 1: Can they walk? → YES → Green (Minor)
  → Step 2: Breathing > 30/min → YES → Red (Immediate)
  → Step 3: Cap refill > 2 sec → YES → Red (Immediate)
  → Step 4: Not following commands → YES → Red (Immediate)
  → → NO to all above → Yellow (Delayed)
```

