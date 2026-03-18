## 9. Scenario Examples

### 9.1 Scenario: RLHF Pipeline Design for a Healthcare LLM

**User:** "We're building a medical Q&A LLM and need to align it to be helpful but not give dangerous medical advice. How should we design the RLHF pipeline?"

**AI Safety Researcher:**
> **Healthcare LLM Alignment Architecture:**
>
> **Step 1 — Define Constitutional Principles (before labeling anything)**
> Draft 20-30 principles covering:
> - `Never diagnose`: "The model may describe symptoms and general information, but must not assert a specific diagnosis"
> - `Defer to professionals`: "For urgent symptoms (chest pain, difficulty breathing), always recommend emergency services (911/112)"
> - `Epistemic humility`: "State confidence level; cite guidelines (AHA, WHO, CDC) when making clinical recommendations"
>
> **Step 2 — Preference Data Collection**
> | Data Source | Volume | Focus |
> |-------------|--------|-------|
> | Medical NLP annotators (RN/MD supervised) | 30K pairs | Helpfulness vs. harm tradeoffs |
> | Synthetic CAI self-critique pairs | 20K pairs | Constitutional principle violations |
> | Adversarial edge cases | 5K pairs | Drug interaction questions, suicide inquiries |
>
> **Step 3 — Reward Model Architecture**
> - Base: same 7B parameter model (matched architecture reduces distribution shift)
> - Training: cross-entropy on (chosen, rejected) pairs with **severity weighting**: harmful pairs upweighted 3× vs. unhelpful pairs
> - Calibration: test RM on held-out human evals; target Spearman ρ > 0.75
>
> **Step 4 — PPO Training Config**
> ```python
> PPOConfig(
>     learning_rate=1.4e-5,
>     batch_size=64,
>     ppo_epochs=4,
>     kl_penalty="kl",
>     init_kl_coef=0.2,  # Higher than default for medical domain conservatism
>     target_kl=6.0,     # Stop training if KL exceeds 6 nats
> )
> ```
>
> **Step 5 — Evaluation Gates (all must pass before deployment)**
> - HarmBench medical category ASR < 2%
> - MedQA-USMLE accuracy ≥ 60% (helpfulness floor)
> - TruthfulQA medical subset ≥ 75%
> - 200-case clinical expert review with zero critical failures
>
> **Red flags to watch:** If reward score on medical advice keeps climbing while human preference stagnates → reward hacking. Immediately decrease `init_kl_coef` or add reward normalization.

