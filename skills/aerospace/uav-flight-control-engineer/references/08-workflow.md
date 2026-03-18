## § 8 Standard Workflow

### Phase 1: Requirements & Architecture

**Activities:**
- Define vehicle configuration, mission profile, and performance requirements
- Select control architecture (PID cascade vs. LQR vs. INDI) based on requirements
- Identify sensor suite and establish observability requirements
- Draft system safety assessment (preliminary FMEA)
- Establish hardware-software interface definition

**✓ Done Criteria:**
- Control requirements document with quantified performance targets
- Block diagram of complete FCS architecture with latency budget
- Sensor selection with justification for each axis of state estimation
- Preliminary FCS FMEA with preliminary safety objectives

**✗ FAIL Criteria:**
- Proceeding to design without quantified stability margin requirements
- No sensor redundancy analysis for flight-critical state variables
- Missing environmental requirements (wind, temperature, EMI)

