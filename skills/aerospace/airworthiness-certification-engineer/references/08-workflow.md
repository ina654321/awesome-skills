## § 8 Standard Workflow

### Phase 1: Certification Program Initiation
```
1.1 Regulatory Basis Establishment
  - [ ] Identify applicable regulations (Part, amendment level)
  - [ ] Submit application for TC/STC to FAA ACO or EASA PCM
  - [ ] Attend pre-application meeting; receive project number
  - [ ] Identify novel/unusual features; submit Issue Papers (IPs)
  - [ ] Receive agreed certification basis document
  - [✓ Done] Output: Signed Certification Plan
  - [✗ FAIL] If authority identifies additional novelty → additional Issue Papers before proceeding

1.2 Safety Assessment Initiation
  - [ ] Conduct Functional Hazard Assessment (FHA) for all aircraft functions
  - [ ] Determine failure condition classifications (Catastrophic/Hazardous/Major/Minor)
  - [ ] Establish DAL assignments for systems and software
  - [✓ Done] Output: FHA Report and Preliminary DAL Assignments accepted by authority
  - [✗ FAIL] If DAL assessment disputed → escalate to ACO chief; prepare ELOS analysis if warranted
```

### Phase 2: Design & Compliance Planning
```
2.1 System Safety Assessment
  - [ ] Conduct PSSA (Preliminary System Safety Assessment) at architecture level
  - [ ] Allocate safety objectives to subsystems (apportionment to required probabilities)
  - [ ] Perform SSA (System Safety Assessment) at detailed design level; FMEA + FTA
  - [ ] Verify all Catastrophic failure modes are < 1×10⁻⁹/FH
  - [✓ Done] Output: SSA v1.0 with all failures meeting regulatory probability requirements
  - [✗ FAIL] If Catastrophic failure mode exceeds 1×10⁻⁹ → architecture redesign required

2.2 Software Certification Planning (DO-178C)
  - [ ] Establish Software Plans (SDP, SVP, SCMP, SQAP) per DO-178C §11
  - [ ] Identify all software items and their DAL assignments
  - [ ] Plan structural coverage strategy for DAL-A items (MC/DC)
  - [ ] Identify tool qualification requirements (DO-330)
  - [✓ Done] Output: Software Plans submitted and accepted by authority (SAS)
  - [✗ FAIL] If independence plan rejected → restructure development/verification teams

2.3 Compliance Matrix Development
  - [ ] List every applicable regulation in the certification basis
  - [ ] Assign MoC (analysis, test, similarity, inspection) for each requirement
  - [ ] Identify compliance documents and responsible DER
  - [✓ Done] Output: Compliance Checklist (CCL)
```

### Phase 3: Compliance Demonstration & TC Issue
```
3.1 Ground & Flight Test Compliance
  - [ ] Submit TIA (Test Initiation Acknowledgment) for FAA-witnessed tests
  - [ ] Complete ground test program; generate test reports
  - [ ] Complete flight test program per test plan
  - [ ] Collect all test data; generate compliance reports
  - [✓ Done] Output: Complete test data package; all test findings closed

3.2 Type Inspection Authorization (TIA) & Final Review
  - [ ] Complete all open findings on compliance matrix
  - [ ] DER issues Statement of Compliance for each compliance item
  - [ ] ACO conducts final conformity inspection
  - [ ] Flight Standardization Board (FSB) approves flight crew training (if applicable)
  - [✓ Done] Output: Type Certificate issued
```

