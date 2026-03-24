## § 8 · Standard Workflow

### Phase 1: Qubit Bring-Up & Spectroscopy

```
Phase 1: Initial Characterization
├── 1.1 Cool down → Verify fridge temperatures (4K, still, MC plate)
├── 1.2 Search for qubit → Two-tone spectroscopy (pump vs detector)
├── 1.3 Find cavity → VNA measurement of resonator frequency
├── 1.4 Extract g, χ → Fit dispersive shift from cavity response
└── 1.5✓ Qubit found, cavity resolved → proceed or remount
```

**Key Activities:**
- Load and bias the dilution refrigerator
- Perform two-tone spectroscopy to locate qubit transition
- Identify resonator mode via VNA S21 measurement
- Extract coupling strength g and dispersive shift χ

**✓ Done Criteria:**
- [✓] Qubit frequency ω01 identified within ±10 MHz
- [✓] Resonator frequency ωr with visibility >10 dB
- [✓] Coupling g/2π > 50 MHz confirmed

**✗ Fail Criteria:**
- [✗] No qubit spectroscopy response after 3 frequency sweeps
- [✗] Resonator not visible — check wiring andattenuation

---

### Phase 2: Coherence Characterization

```
Phase 2: T1/T2 Extraction
├── 2.1 T1 (inversion recovery) → π pulse → wait t → measure
├── 2.2 T2* (Ramsey) → π/2 → wait t → π/2 → measure
├── 2.3 T2 (Hahn echo) → π/2 → τ → π → τ → π/2 → measure
├── 2.4 Noise spectral density → PSD from dynamical decoupling
└── 2.5✓ Dominant decoherence channel identified
```

**Key Activities:**
- Measure T1 via inversion recovery at qubit frequency
- Measure T2* via Ramsey fringe experiment
- Measure T2 via Hahn echo to isolate slow noise
- Characterize noise type (charge, flux, TLS, thermal)

**✓ Done Criteria:**
- [✓] T1 > 10 μs, T2* > T1/2
- [✓] Decoherence mechanism identified (TLS, charge, flux, photon)
- [✓] Noise PSD extracted for dynamical decoupling optimization

**✗ Fail Criteria:**
- [✗] T1 < 1 μs — check for quasiparticle poisoning or wiring issues
- [✗] T2* >> T2 —confirm echo experiment performed correctly

---

### Phase 3: Gate Calibration

```
Phase 3: Pulse-Level Control
├── 3.1 Single-qubit Rabi → Measure Rabi oscillation frequency ΩR
├── 3.2 π/2, π calibration → Find pulse amplitude for 90°/180° rotation
├── 3.3 DRAG optimization → Sweep β, minimize |2⟩ population
├── 3.4 ALLXY → Verify pulse fidelity across all XY combinations
├── 3.5 Two-qubit gates → Calibrate CZ/iSWAP/CR based on platform
├── 3.6 Randomized Benchmarking → Measure EPC < threshold
└── 3.7✓ Single and two-qubit gates at target fidelity
```

**Key Activities:**
- Calibrate DRAG pulses to suppress leakage to |2⟩
- Perform ALLXY to detect coherent.errors
- Run two-qubit gate calibration (CZ for transmon, exchange for spin)
- Execute RB to quantify average gate error

**✓ Done Criteria:**
- [✓] Single-qubit EPC < 0.1%, leakage L1 < 0.1%
- [✓] Two-qubit EPC < 0.5% (transmon) or < 1% (spin)
- [✓] AllXY fidelity > 99%

**✗ Fail Criteria:**
- [✗] Gate error > 1% after 10 calibration iterations
- [✗] Leakage > 1% — verify DRAG coefficient and anharmonicity

---

### Phase 4: Multi-Qbit Integration & Error Correction

```
Phase 4: System Integration
├── 4.1 Frequency allocation → Plan qubit spacing to avoid collisions
├── 4.2 Crosstalk characterization → Simultaneous RB
├── 4.3 Readout calibration → SQRT, for Qubit-state discrimination
├── 4.4 Surface code stabilizers → X, Z measurement circuits
├── 4.5 Syndrome extraction → Measure logical error rate
└── 4.6✓ Device ready for quantum error correction
```

**Key Activities:**
- Allocate frequencies to minimize spectral crowding
- Measure crosstalk via simultaneous RB
- Calibrate high-fidelity readout with TWPA
- Implement surface code stabilizer circuits

**✓ Done Criteria:**
- [✓] All-to-all crosstalk < 1% degradation
- [✓] Readout fidelity > 99%
- [✓] Logical error rate below threshold (p < p_th)

**✗ Fail Criteria:**
- [✗] Crosstalk ratio > 2× — re-plan frequency allocation
- [✗] Readout fidelity < 95% — optimize Purcell filter or TWPA

---
