## § 9 · Scenario Examples

### Scenario 1: T1 Degradation Diagnosis

**User:**
"Our transmon T1 dropped from 80 μs to 12 μs after chip remounting. How do I diagnose this?"

**Expert Response:**
> **Diagnostic Framework — Trace the signal chain:**

| Check | Method | Expected | If Fail |
|-------|--------|----------|---------|
| Thermal photons | Add 20 dB cold attenuation, remeasure | T1 recovers | Attenuation insufficient |
| TLS resonance | Frequency-dependent T1 sweep | T1 varies with ωq | TLS at qubit frequency |
| Quasiparticle | Temperature dependence T1(T) | T1 ∝ 1/√T | QP poisoning |
| Wiring change | Compare pre/post attenuation | Same | Attenuators shifted |

**Executable diagnostic code:**
```python
import numpy as np
from scipy.optimize import curve_fit

def diagnose_t1_drop(T1_before_us, T1_after_us, freq_ghz, temp_mk):
    """Diagnose T1 drop post-handling."""
    print(f"T1 before: {T1_before_us} μs → after: {T1_after_us} μs")
    print(f"Qubit frequency: {freq_ghz} GHz, Temperature: {temp_mk} mK")
    
    # Thermal photon limit at temperature T
    n_thermal = 1 / (np.exp(freq_ghz * 1e9 * 6.582e-16 / (1.38e-23 * temp_mk / 1000)) - 1)
    T1_thermal = 1 / (n_thermal + 0.5)  # Thermal photon induced loss
    
    print(f"Thermal photon occupancy at {temp_mk} mK: n_th = {n_thermal:.2f}")
    print(f"Thermal-limited T1max: {T1_thermal/1e-6:.1f} μs")
    
    # Calculate ratio
    ratio = T1_before_us / T1_after_us
    if ratio > 3:
        print(f"⚠️ T1 dropped {ratio:.1f}× → Likely TLS or QP issue")
        print("→ Next: Check qubit frequency stability, run temperature sweep")
    else:
        print(f"✓ T1 drop within 3× → may be normal variation")

diagnose_t1_drop(T1_before_us=80, T1_after_us=12, freq_ghz=5.0, temp_mk=15)
```
**Next I need:** What were the attenuation settings before and after remounting?

---

### Scenario 2: DRAG Calibration for Target Fidelity

**User:**
"How do I calibrate DRAG pulses to achieve < 0.1% single-qubit gate error?"

**Expert Response:**
> **DRAG Calibration Protocol — 3-step sequence:**

1. **Rabi calibration** → Find ΩR (Rabi frequency)
2. **ALLXY optimization** → Minimize error across all XY combinations
3. **Leakage verification** → Run leakage-sensitive RB with β sweep

**Executable calibration code:**
```python
import numpy as np

def calibrate_drag(qubit, max_rabi_amp=0.5, n_amps=21):
    """Calibrate DRAG pulse to achieve < 0.1% error."""
    # Step 1: Rabi oscillation - find Ω_R
    t_pulse = np.linspace(0, 100, n_amps)  # ns
    amplitudes = np.linspace(0, max_rabi_amp, n_amps)
    rabi_data = run_rabi_oscillation(qubit, t_pulse, amplitudes)
    Omega_R = fit_rabi_frequency(rabi_data)  # MHz
    
    # Step 2: Set π/2 and π amplitudes
    amp_pi_2 = np.pi / (4 * Omega_R * 40)  # 40ns pulse
    amp_pi = 2 * amp_pi_2
    
    # Step 3: ALLXY with β sweep
    beta_range = np.linspace(-0.5, 0.5, 11)
    allxy_fidelities = []
    for beta in beta_range:
        pulses = generate_drag_pulses(beta=beta, amp=amp_pi_2, width=40)
        fidelity = run_allxy(qubit, pulses)
        allxy_fidelities.append(fidelity)
    
    beta_optimal = beta_range[np.argmax(allxy_fidelities)]
    print(f"Optimal DRAG β = {beta_optimal:.3f}")
    
    # Step 4: Leakage verification
    L1 = run_leakage_rb(qubit, beta=beta_optimal)
    print(f"Leakage L1 = {L1*100:.3f}%")
    
    if L1 < 0.001:
        print("✓ DRAG calibrated: EPC < 0.1%")
    else:
        print("⚠️ Reduce gate speed or re-optimize β")

calibrate_drag(qubit="Q1")
```

---

### Scenario 3: Surface Code Threshold Verification

**User:**
"What two-qubit gate fidelity do I need to run the surface code below threshold?"

**Expert Response:**
> **Surface Code Threshold Analysis:**

| Parameter | Threshold | Rationale |
|-----------|-----------|-----------|
| Single-qubit EPC | < 0.1% | p < p_th/10 |
| Two-qubit EPC | < 0.5% | p < p_th for depolarizing |
| Readout fidelity | > 99% | Syndrome extraction reliability |
| Cycle time | < 1 μs | Error correction speed |

**Threshold calculation:**
```python
import numpy as np

def surface_code_threshold(d=5, l=1):
    """
    Calculate logical error rate for distance-d surface code.
    d: code distance, l: error suppression target
    """
    # Physical error rates (typical for transmon)
    p1q = 0.0001   # 0.01% single-qubit gate
    p2q = 0.005    # 0.5% two-qubit gate  
    pMeas = 0.01   # 1% measurement error
    
    # Total error per gate + measurement
    p = (p1q + p2q + pMeas) / 3
    
    # Threshold for depolarizing noise: p_th ≈ 1%
    p_th = 0.01
    
    if p < p_th:
        # Logical error suppressed by (p/p_th)^((d+1)/2)
        p_L = p * (p / p_th) ** ((d+1)/2 - 1)
        print(f"Physical error rate p = {p*100:.2f}% < p_th = {p_th*100}%")
        print(f"Distance-{d} code: logical error p_L ≈ {p_L*1e6:.1f} ppm")
        print("✓ Below threshold — error correction effective")
    else:
        print(f"⚠️ p = {p*100:.2f}% > p_th = {p_th*100}%")
        print("→ Improve hardware fidelity before running QEC")

surface_code_threshold(d=5)
```

---

### Scenario 4: Simultaneous RB Crosstalk Detection

**User:**
"Our individual qubit RB passes < 0.1% but algorithms fail. How do I check for crosstalk?"

**Expert Response:**
> **Crosstalk Detection — Simultaneous RB Protocol:**

| Step | Action | Pass Criteria |
|------|--------|---------------|
| 1 | Run individual RB per qubit | All < 0.1% |
| 2 | Run simultaneous RB (all qubits) | Ratio < 1.5× |
| 3 | Map culprit pairs | Identify ZZ coupling |

**Crosstalk diagnostic:**
```python
def detect_crosstalk(epc_individual, epc_simultaneous):
    """Flag crosstalk from simultaneous vs individual RB."""
    print("Individual RB → Simultaneous RB (ratio):")
    for q, (epc_ind, epc_sim) in enumerate(zip(epc_individual, epc_simultaneous)):
        ratio = epc_sim / epc_ind if epc_ind > 0 else 0
        status = "⚠️ CROSSTALK" if ratio > 1.5 else "✓"
        print(f"  Q{q}: {epc_ind*100:.3f}% → {epc_sim*100:.3f}% ({ratio:.2f}×) {status}")
        
    # Identify frequency collision pairs
    if any(ratio > 1.5 for ratio in [epc_sim/epc_ind for epc_ind in epc_individual]):
        print("→ Recommendation: Reallocate qubit frequencies")

# Example: 5-qubit device
epc_ind = {"Q0": 0.0008, "Q1": 0.0007, "Q2": 0.0009, "Q3": 0.0006, "Q4": 0.0008}
epc_sim = {"Q0": 0.0015, "Q1": 0.0012, "Q2": 0.0018, "Q3": 0.0011, "Q4": 0.0014}
detect_crosstalk(list(epc_ind.values()), list(epc_sim.values()))
```

**Next I need:** Do you have the frequency allocation map for all qubits?

---
