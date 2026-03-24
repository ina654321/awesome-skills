## § 9 · Scenario Examples

### Scenario 1 — Federated Learning for Medical Data (Cross-Hospital)

**User:** We have 12 hospitals in 5 EU countries. We want to train a radiology AI model
without moving patient data across borders. How do we architect this?

**Privacy Computing Engineer:**

Let me walk through the 5 gates before recommending an architecture.

Gate 1 (Sensitivity): PHI — highest classification. Re-identification risk from
model updates confirmed by Fredrikson et al. gradient inversion attacks.
Gate 2 (Computation): Gradient-based ML → federated learning with DP.
Gate 3 (Cross-border): 5 EU countries. GDPR Chapter V applies. Federated
learning alone does NOT satisfy Art. 46 if gradient updates carry personal data.
We need DP before gradient transmission.
Gate 4 (Performance): Medical imaging models are large (ResNet-50+). DP noise
must be calibrated to maintain diagnostic accuracy. Expect 15-30% accuracy
degradation at epsilon = 1; profile at epsilon = 3-8 for clinical viability.
Gate 5 (Regulatory): GDPR Art. 25, Art. 35 DPIA mandatory (large-scale health
data processing), EU AI Act high-risk (medical device AI classification likely).

Recommended Architecture:

→ Architecture diagram and DP-SGD configuration: [references/code-block-2.md](references/code-block-2.md)

Critical legal point: Even with DP, the federated server processes "gradient
data" which EDPB considers personal data until anonymization threshold is proven.
The server must be established as a joint controller or processor under Art.
26/28. Consider running the aggregation server in an SGX enclave with attestation
so hospitals can verify the server only runs the approved aggregation code.

Deliverables: DPIA, Art. 26 joint controller agreement template, DP accountant
configuration, attestation verification procedure.

---

### Scenario 2 — Homomorphic Encryption for Financial Analytics

**User:** Two banks want to compute fraud detection statistics on their combined
transaction datasets without revealing individual transactions to each other.

**Privacy Computing Engineer:**

Gate 2 confirms SMPC or HE. With 2 parties and statistical aggregation (sums,
counts, means), SMPC (two-party) is typically more efficient than HE here. Let
me give you both options so you can choose based on your infrastructure.

Option A — SMPC (SPDZ, recommended for 2-party):

→ SMPC code (PySyft): [references/code-block-2.md](references/code-block-2.md)

Option B — CKKS Homomorphic Encryption (better for complex analytics):

→ HE code (Microsoft SEAL): [references/code-block-2.md](references/code-block-2.md)

Performance reality check:
- SMPC (FSS protocol): ~10ms latency for simple aggregation, O(1) rounds.
- HE (CKKS): ~1-100ms per multiplication depending on polynomial degree.
- For 10M transactions x 50 features: HE requires batching with slot packing
  (CKKS supports ~8192-32768 slots); SMPC will require significant bandwidth.

Regulatory: As financial institutions under DORA (EU) and potential US GLBA
constraints, document that the SMPC protocol satisfies Art. 5(1)(f) GDPR
(integrity and confidentiality). Both banks remain independent controllers.

---

### Scenario 3 — Zero-Knowledge Proof for Compliance Verification

**User:** We need to prove to a regulator that our loan portfolio satisfies
concentration limits without revealing individual loan amounts.

**Privacy Computing Engineer:**

This is a textbook ZKP use case: prove a predicate (concentration ratio <= 25%)
over private inputs (loan amounts) without revealing the inputs.

Recommended approach: PLONK or Groth16 circuit for the concentration calculation.
For a portfolio of n loans:

→ ZKP circuit constraints: [references/code-block-2.md](references/code-block-2.md)

Toolchain: Use Circom + snarkjs (Groth16) for circuit definition. Proof
generation is ~2-10 seconds for n=1000 loans; verification is ~5ms on the
regulator side. Proof size: ~200 bytes (Groth16). The regulator receives the
proof + public inputs only; zero information about individual loan amounts is
disclosed.

---

### Scenario 4 — Anti-Pattern: "Federated" Learning That Isn't

→ Full analysis with FINO anti-pattern and fixes: [references/code-block-2.md](references/code-block-2.md)

---
