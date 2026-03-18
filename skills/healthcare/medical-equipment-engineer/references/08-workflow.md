## 8. Standard Workflow

### 8.1 Preventive Maintenance Procedure

```
Phase 1: Preparation (15 min)
├── Review equipment service manual and PM checklist
├── Gather required tools, test equipment, replacement parts
├── Verify equipment is clean and ready for service
├── Power down if required; disconnect from patient
└── Document equipment ID, model, serial number, location

Phase 2: Visual Inspection
├── Check for physical damage: cracks, loose components, worn cables
├── Verify all labels intact: manufacturer, model, serial, safety labels
├── Inspect power cord: no cuts, exposed wires, proper grounding
├── Check applied parts: cables intact, connectors undamaged
└── Note any issues for repair

Phase 3: Electrical Safety Testing (IEC 60601-1)
├── Connect ESA to equipment earth (if applicable)
├── Measure Earth Leakage Current: must be <500 μA
├── Measure Enclosure Leakage Current: must be <100 μA
├── Measure Patient Leakage Current: must be <100 μA
├── Test protective earth resistance: <0.2Ω
└── Record all measurements on PM form

Phase 4: Functional Testing
├── Power on equipment; verify self-test passes
├── Test all alarm functions (high/low limits, technical alarms)
├── Verify displays: brightness, readability, no dead pixels
├── Test applied parts: sensors, probes, accessories
├── Run performance verification: use patient simulator if applicable
└── Document all test results

Phase 5: Completion
├── Update equipment service record in CMMS
├── Apply PM sticker with next service date
├── Return equipment to clinical area
├── Notify charge nurse of equipment return
└── Document time spent and any additional findings
```

### 8.2 Corrective Repair Workflow

```
Step 1: Service Call Receipt
├── Obtain complaint from user: what stopped working, error codes, when started
├── Check equipment history in CMMS: last PM, recent issues, service notes
└── Gather service manual, schematics, troubleshooting guide

Step 2: Troubleshooting
├── Perform visual inspection for obvious failures (burned components, loose cables)
├── Power on; observe error codes or self-test failures
├── Use diagnostic mode if available
├── Isolate problem to subsystem: power, control board, applied part, network
└── Check for firmware updates that may address the issue

Step 3: Repair
├── Obtain correct replacement parts (OEM recommended)
├── Power down; follow lockout/tagout procedures
├── Replace defective component; verify proper installation
├── Update firmware if applicable
├── Reassemble equipment; verify all connections secure

Step 4: Testing
├── Perform electrical safety testing before functional tests
├── Run complete functional test per service manual
├── Test all alarm conditions
├── Verify with patient simulator if applicable
└── Ensure equipment operates within specifications

Step 5: Return to Service
├── Document repair: symptoms, cause, action taken, parts used
├── Update CMMS with work order completion
├── Apply service sticker
├── Return to clinical area; brief user on any limitations
└── Close work order
```

