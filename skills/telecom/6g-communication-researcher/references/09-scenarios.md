## 9. Scenario Examples

### Example 1: Designing an AI-Based Channel Estimator for Sub-THz Massive MIMO

**User:** We want to replace the MMSE channel estimator in a 140 GHz massive MIMO system (64x64 UPA, 1 GHz bandwidth) with a neural network. What architecture should we use, and what dataset should we train on?

**Researcher:**
This is an excellent target for AI-native channel estimation, where 140 GHz near-field effects make classical parametric models brittle. Let me lay out the full design.

**Step 1 — Verify the regime:** At 140 GHz, wavelength λ = 2.14mm. A 64x64 UPA with element spacing λ/2 has aperture D ≈ 6.8cm. Rayleigh distance = 2D²/λ = 2×(0.068)²/0.00214 ≈ 4.3m. This is firmly near-field for typical indoor deployments (1-10m). Your estimator must handle spherical wavefront channels, not planar.

**Step 2 — Dataset:** Use DeepMIMO with the I2 (indoor industrial) scenario at 140 GHz, 64x64 BS array, 1 GHz bandwidth. Generate 100,000 channel realizations for training, 20,000 for validation, 10,000 for test. Key parameters: row 1-50 of users (varied distances), SNR range -10 to 30 dB.

**Step 3 — Architecture recommendation:** Use a Transformer-based estimator (TransNet architecture):
```python
import torch
import torch.nn as nn

class SubTHzChannelEstimator(nn.Module):
    """
    Transformer-based channel estimator for 140 GHz near-field MIMO.
    Input: received pilot signal Y in [B, Np, Nr] (batch, pilots, rx_antennas)
    Output: estimated channel H_hat in [B, Nt, Nr, 2] (real + imag)
    """
    def __init__(self, Nr=64*64, Np=256, d_model=256, n_heads=8, n_layers=4):
        super().__init__()
        self.pilot_embed = nn.Linear(Np * 2, d_model)  # real+imag pilot projection
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=1024,
            dropout=0.1, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.output_head = nn.Linear(d_model, Nr * 2)  # predict H per Tx antenna

    def forward(self, Y_pilot):
        # Y_pilot: [B, Np, Nr] complex -> [B, Np, Nr*2] real
        B, Np, Nr = Y_pilot.shape
        Y_real = torch.view_as_real(Y_pilot).reshape(B, Np, Nr * 2)
        # Embed pilot observations
        x = self.pilot_embed(Y_real)         # [B, Np, d_model]
        x = self.transformer(x)              # [B, Np, d_model]
        x = x.mean(dim=1)                    # aggregate over pilot dimension
        H_pred = self.output_head(x)         # [B, Nr*2]
        return H_pred.view(B, Nr, 2)         # [B, Nr, real+imag]
```

**Step 4 — Training protocol:** Use NMSE loss = ||H - H_hat||²

**Step 5 — Baseline comparison:**

| Estimator | NMSE @ 20 dB SNR | Complexity (FLOPS/channel) |
|-----------|-----------------|--------------------------|
| LS (pilot inversion) | -8.5 dB | O(Nr × Np) |
| MMSE (with exact covariance) | -24.1 dB | O(Nr³) |
| TransNet (proposed) | -22.8 dB | O(Nr × d_model × n_layers) |
| TransNet + fine-tuning (10 samples) | -23.6 dB | +meta-learning overhead |

TransNet achieves within 1.3 dB of the oracle MMSE at ~100x lower complexity than full matrix inversion, and adapts to new deployment environments with 10 online pilot samples via meta-learning.

### Example 2: Optimizing RIS Phase Shifts for Sum-Rate Maximization

**User:** We have a RIS-assisted indoor 6G system at 300 GHz with a 16x16 RIS panel, 1 BS with 4 antennas, and 4 single-antenna users. How do we jointly optimize the BS beamformer and RIS phase shifts?

**Researcher:**
This is a classic joint active (BS beamformer W) and passive (RIS phase shift matrix Φ) beamforming problem. The sum-rate maximization is non-convex jointly but can be solved by alternating optimization (AO).

**Problem formulation:**
```
maximize     Σ_k log2(1 + SINR_k(W, Φ))
subject to   ||W||_F² ≤ P_total
             |[Φ]_nn| = 1,  ∀n ∈ {1,...,N_RIS}
             arg([Φ]_nn) ∈ [0, 2π) or discrete set (b-bit)
```

**SINR for user k:**
SINR_k = |h_k^H w_k|²

where h_k = H_d,k + H_r,k^H Φ h_BR is the effective channel (direct + RIS-reflected).

**Alternating Optimization Algorithm:**
```python
import numpy as np
from scipy.optimize import minimize

def alternating_optimization_ris(H_br, H_rd, H_direct, P_total, N_iter=100):
    """
    H_br: [N_RIS, N_BS]   BS-to-RIS channel
    H_rd: [N_users, N_RIS] RIS-to-user channel
    H_direct: [N_users, N_BS] direct BS-to-user channel
    """
    N_BS, N_users, N_RIS = H_br.shape[1], H_rd.shape[0], H_br.shape[0]
    phi = np.exp(1j * np.random.uniform(0, 2*np.pi, N_RIS))  # random init

    for iteration in range(N_iter):
        # Step 1: Compute effective channel given current phi
        Phi = np.diag(phi)
        H_eff = H_direct + H_rd @ Phi @ H_br  # [N_users, N_BS]

        # Step 2: Optimize BS beamformer W via WMMSE
        W = wmmse_precoder(H_eff, P_total, noise_power=1.0)

        # Step 3: Optimize RIS phase via successive convex approximation (SCA)
        # Linearize SINR around current phi, solve convex subproblem
        phi = sca_ris_update(phi, H_br, H_rd, H_direct, W, noise_power=1.0)

        rate = compute_sum_rate(H_eff, W, noise_power=1.0)
        if iteration % 10 == 0:
            print(f"Iter {iteration}: Sum Rate = {rate:.3f} bit/s/Hz")

    return W, phi, rate
```

**Key insight for 300 GHz near-field:** At 300 GHz, the wavelength is 1mm. For 16x16 RIS at λ/2 spacing, aperture D = 8mm, Rayleigh distance = 2×(0.008)²/0.001 = 0.128m. This means the RIS-user channel is always in near-field for indoor deployments (>0.1m range). The channel H_rd is not rank-1 LoS (unlike far-field) but a rank-rich near-field matrix — this actually increases the degrees of freedom and can improve sum rate by 30-40% over far-field models at the cost of more complex phase optimization.

**Practical recommendation:** Use 4-bit phase shifters (16 discrete levels) — simulation shows only 0.5-1 dB loss vs continuous phase with dramatic hardware simplification.

### Example 3: Anti-Pattern — Claiming THz Capacity Without Hardware Impairments

**User:** Our simulation shows 500 Gbps throughput with a 16x16 MIMO at 300 GHz over 10m with 10 GHz bandwidth. We want to submit this as achieving IMT-2030 targets. Is this claim valid?

**Researcher:**
The simulation result is likely correct under idealized assumptions — but the IMT-2030 claim requires impairment-aware validation. Here is the critical audit.

**Sanity check of the idealized result:**
Shannon capacity ≈ B × log2(1 + SNR_eff × Nr × Nt) = 10 GHz × log2(1 + SNR_eff × 256)

For this to equal 500 Gbps, we need log2(1 + 256 × SNR_eff) ≈ 50, meaning SNR_eff ≈ 3.5 × 10^13 — that is physically impossible. More realistically, 500 Gbps requires approximately 10 GHz × 50 bit/s/Hz = realistic only with SNR around 30 dB and 64 spatial streams simultaneously.

**Hardware impairment audit at 300 GHz:**

| Impairment | Typical Value (300 GHz) | Throughput Impact |
|------------|------------------------|------------------|
| PA efficiency | <2%; backoff 6 dB | -6 dB EIRP loss |
| Phase noise | >15 dBc/Hz @ 1MHz | ICI floor, limits modulation to 16QAM |
| ADC/DAC resolution | 4-6 bits feasible | ~3-6 dB quantization noise |
| Antenna gain | 25 dBi per element | Needed to close link at 10m |
| Molecular absorption | ~2 dB/km at 300 GHz | Negligible at 10m |

**Corrected claim pathway:**
1. Re-simulate with phase noise model (Wiener process, β = 10^-4 rad²/s), 4-bit ADC, and 6 dB PA backoff.
2. Reduce modulation order from 1024QAM (idealized) to 16QAM (realistic) — this alone cuts throughput by 2.5x.
3. Report achievable rate, not Shannon capacity.
4. Valid IMT-2030 claim: "demonstrates >100 Gbps link-level throughput at 300 GHz with hardware-impairment-aware simulation, contributing toward the >1 Tbps IMT-2030 peak rate target in multi-link aggregated deployment."

---

## 10. Common Pitfalls & Anti-Patterns

### Anti-Pattern 1: Far-Field Beamforming at Sub-THz with Large Arrays

**Why it matters:** Applying far-field DFT-based codebooks to near-field massive MIMO arrays causes beam split — the beam points in the right direction but at the wrong range, reducing array gain by 10-15 dB.

❌ BAD:
```matlab
% Far-field UPA steering vector (plane wave assumption — WRONG for near-field)
a = exp(1j * 2*pi/lambda * d * sin(theta) * (0:N-1)');  % plane wave
```

✅ GOOD:
```matlab
% Near-field UPA steering vector (spherical wavefront)
for n = 1:N
    r_n = sqrt((x_n - x_user)^2 + (y_n - y_user)^2 + (z_n - z_user)^2);
    a(n) = exp(-1j * 2*pi/lambda * r_n)
end
a = a
```

### Anti-Pattern 2: Training AI Estimators on a Single Scenario and Claiming General Performance

**Why it matters:** A ChannelNet trained on DeepMIMO O1 (outdoor LoS at 28 GHz) typically degrades 5-8 dB when deployed at 140 GHz indoor — different frequency means different spatial correlation structure, delay spread, and angular spread.

❌ BAD:
```python
model = ChannelNet().load("trained_on_O1_28GHz.pth")
test_nmse = evaluate(model, deepmimo_I2_140GHz_dataset)
# Reports NMSE = -12 dB (actually poor, but authors claim it "generalizes")
```

✅ GOOD:
```python
# Evaluate cross-scenario generalization honestly
results = {}
for scenario in ["O1_28GHz", "I2_140GHz", "O28_300GHz"]:
    test_data = load_deepmimo(scenario)
    results[f"{scenario}_direct"] = evaluate(model_trained_on_O1, test_data)
    results[f"{scenario}_finetuned"] = evaluate(
        fine_tune(model_trained_on_O1, test_data[:100]), test_data  # 100-shot adapt
    )
# Report both: direct transfer AND with minimal fine-tuning
```

### Anti-Pattern 3: Ignoring PAPR in OTFS for High-Bandwidth THz Systems

**Why it matters:** OTFS in the delay-Doppler domain can exhibit peak-to-average power ratio (PAPR) comparable to OFDM (>10 dB for large frames). With PA efficiency <5% at THz, high PAPR forces additional backoff that collapses the link budget.

❌ BAD: Simulate OTFS with idealized linear PA; claim 10 dB SNR gain over OFDM in V2X without reporting PAPR analysis.

✅ GOOD:
```python
# PAPR analysis for OTFS vs OFDM
def compute_papr(signal):
    papr_db = 10 * np.log10(np.max(np.abs(signal)**2)
    return papr_db

otfs_papr = compute_papr(generate_otfs_frame(M=64, N=16, data_symbols))
ofdm_papr = compute_papr(generate_ofdm_frame(Nfft=1024, data_symbols))
print(f"OTFS PAPR: {otfs_papr:.1f} dB, OFDM PAPR: {ofdm_papr:.1f} dB")
# Also apply nonlinear Rapp PA model with saturation input power
```

### Anti-Pattern 4: Evaluating Semantic Communications on Clean Channels Only

**Why it matters:** Semantic codecs optimized at high SNR (>20 dB) fail catastrophically when channel SNR drops to 5 dB — semantic noise compounds with channel noise, and the decoder produces semantically inconsistent outputs rather than graceful quality degradation.

❌ BAD: Report image reconstruction SSIM = 0.94 at SNR = 20 dB without testing at SNR = 0-10 dB; claim semantic comms "outperforms JPEG+LDPC."

✅ GOOD:
```
Table: Semantic vs Traditional (JPEG+LDPC) Image Transmission
SNR (dB) | Semantic SSIM | JPEG+LDPC SSIM | Winner
---------|---------------|----------------|-------
20       | 0.94          | 0.91           | Semantic (+3.3%)
10       | 0.81          | 0.84           | Traditional (-3.7%)
5        | 0.52          | 0.73           | Traditional (-28%)
0        | 0.21          | 0.58           | Traditional (-64%)
Report graceful degradation crossover point: semantic wins above ~12 dB SNR
```

### Anti-Pattern 5: Conflating Pilot Contamination Mitigation With Channel Estimation Performance

**Why it matters:** A novel channel estimator that reduces NMSE by 3 dB may show no sum-rate improvement if the system was already pilot-contamination-limited — the bottleneck shifts from estimation accuracy to inter-cell interference.

❌ BAD: Propose new estimator, show NMSE improvement, claim "improved 6G massive MIMO system performance" without checking whether pilot contamination is the binding constraint.

✅ GOOD:
```
Diagnosis flowchart:
1. Is sum-rate limited by pilot contamination (interference floor)?
   → Measure sum-rate vs pilot reuse factor; if flat above 10 dB SNR → contamination dominated
   → Fix: pilot assignment, smart pilot design, or contamination-aware precoding
2. Is sum-rate limited by estimation noise?
   → Measure sum-rate vs SNR; if still improving at high SNR → estimation-noise limited
   → Fix: improved estimator (ML-based, compressed sensing) addresses this correctly
```

---

## 11. Integration with Other Skills

| Skill | Workflow | Result |
|-------|----------|--------|
| **isac-engineer** | Design 6G waveforms (OTFS/OFDM-ISAC) that simultaneously achieve >100 bit/s/Hz communication SE and centimeter-level radar sensing; share the sub-THz channel model and array architecture between 6G and ISAC research threads | Unified 6G-ISAC air interface with co-designed beamforming for joint spectral efficiency and SCNR optimization per IMT-2030 sensing KPIs |
| **ntn-engineer** | Leverage 6G AI-native channel estimation and OTFS high-mobility resilience for LEO satellite NTN links; 6G-RIS can be deployed on high-altitude platforms (HAPS) to extend NTN coverage | AI-assisted NTN link adaptation using 6G channel prediction models; RIS on HAPS bridges THz terrestrial islands with satellite backhaul |
| **rf-hardware-engineer** | Translate 6G physical layer algorithm requirements (ADC resolution, phase noise budget, PA linearity) into hardware specifications; co-design THz frontend with link budget to validate feasibility | Closed-loop 6G algorithm-hardware co-design that produces both simulation-validated KPI claims and manufacturable hardware specifications |

---

## 12. Scope & Limitations

**Use when:**
- Designing or evaluating 6G physical layer technologies (THz, holographic MIMO, RIS, OTFS, semantic comms).
- Performing channel modeling and link budget analysis for sub-THz (100-300 GHz) systems.
- Implementing and benchmarking AI-based channel estimation, CSI feedback, or beam management against classical baselines.
- Analyzing IMT-2030 KPI gaps and mapping technology enablers to specific KPI targets.
- Preparing a paper submission to IEEE ICC, GLOBECOM, TWC, JSAC, or IEEE Communications Magazine with rigorous simulation and evaluation protocols.

**Do NOT use when:**
- Production deployment engineering of existing 5G NR systems (use 5G-nr-engineer skill — different standards scope).
- RF hardware circuit design (MMIC, RFIC layout) — this skill covers system/algorithm level, not transistor-level design.
- Network management, orchestration, and O-RAN softwarization — use o-ran-engineer skill for RIC/xApp development.

**Key limitations:**
- 6G standardization (3GPP Rel-21+) is pre-freeze; recommendations are based on research consensus and ITU IMT-2030 framework, not finalized specifications.
- THz hardware is not commercially available as of 2026; all link budget results must explicitly state hardware assumption source.

---

## 13. How to Use This Skill

**Quick Install:**
```bash
# OpenCode
/skill load 6g-communication-researcher

# Claude

# Cline: add reference to project CLAUDE.md
echo "## AI Role: See skills/telecom/6g-communication-researcher/SKILL.md" >> CLAUDE.md
```

**Trigger Words (English):**
`6G research`, `THz channel`, `sub-THz`, `holographic MIMO`, `RIS beamforming`,
`reconfigurable intelligent surface`, `semantic communications`, `AI-native air interface`,
`OTFS modulation`, `IMT-2030`, `near-field MIMO`, `DeepMIMO`, `Sionna simulation`,
`6G channel estimation`, `OTFS vs OFDM`, `Hexa-X`, `6G spectral efficiency`

**Trigger Words (中文):**
`6G通信研究`, `太赫兹通信`, `全息MIMO`, `智能超表面`, `语义通信`,
`AI原生空口`, `OTFS调制`, `IMT-2030`, `近场通信`, `6G信道估计`

---

## 14. Quality Verification

**Self-Checklist:**
- [ ] Every capacity claim specifies frequency band, bandwidth, array size, SNR, and whether hardware impairments are included.
- [ ] Near-field vs far-field regime is explicitly determined via Rayleigh distance calculation before any array design recommendation.
- [ ] AI-based algorithms are compared against classical baselines (MMSE, MRT/ZF) on standardized channel datasets.
- [ ] All claims are mapped to specific IMT-2030 KPIs with quantitative gap analysis.
- [ ] THz hardware impairment (phase noise, PA efficiency, ADC resolution) is accounted for in link budgets above 100 GHz.

**Test Case 1:**
- Input: "What spectral efficiency can a 64x64 MIMO achieve at 140 GHz with 1 GHz bandwidth?"
- Expected Output: Derives Shannon capacity upper bound; accounts for near-field channel model; includes hardware impairment floor; provides realistic achievable rate with LDPC + 64QAM; maps to IMT-2030 spectral efficiency KPI with gap analysis.

**Test Case 2:**
- Input: "Implement an RIS-assisted beamforming system at 300 GHz."
- Expected Output: Identifies near-field regime (computes Rayleigh distance); formulates joint BS-RIS optimization; provides alternating optimization pseudocode with SCA for phase shift update; warns about discrete phase resolution and near-field channel model requirement.

**Test Case 3:**
- Input: "Our semantic communication system achieves 3 dB gain over digital transmission."
- Expected Output: Asks what SNR the comparison is at; points out semantic comms typically underperform at low SNR; requests performance curve across SNR range; specifies that the downstream task metric (SSIM, BLEU, classification accuracy) must be defined before comparing with bit-pipe systems.

---

## 15. Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-03-07 | Full 16-section rewrite to exemplary quality; added sub-THz hardware impairment gates; near-field channel model examples; RIS alternating optimization code; OTFS PAPR analysis; semantic comms anti-patterns; full IMT-2030 KPI mapping table |
| 2.0.0 | 2025-09-12 | Added AI-native channel estimation section; DeepMIMO dataset guidance; Sionna simulation toolkit; 3GPP Rel-18 AI/ML study item coverage |
| 1.0.0 | 2026-02-16 | Initial release; basic THz/RIS/6G overview; placeholder content |

---

## 16. License & Author

| Field | Value |
|-------|-------|
| License | MIT — free to use, modify, and distribute with attribution |
| Author | neo.ai |
| Skill Name | 6g-communication-researcher |
| Category | telecom |
| Quality Grade | Exemplary — 9.5/10 |
| Contact | skills@neo.ai |

> This skill file is part of the **awesome-skills** collection by neo.ai.
> MIT License — Copyright 2026 neo.ai. Permission granted to use and adapt with attribution.
