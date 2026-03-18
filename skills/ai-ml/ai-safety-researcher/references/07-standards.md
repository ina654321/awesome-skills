## 7. Standards & Reference

### 7.1 Alignment Frameworks

| Framework / 框架 | When to Use / 使用场景 | Key Steps
|-----------------|----------------------|-------------------|
| **RLHF (PPO)** | Training helpful/harmless/honest behavior from human preferences | 1. Supervised Fine-Tune (SFT) → 2. Train Reward Model on pairwise prefs → 3. PPO optimize against RM → 4. Eval on HHH benchmark |
| **DPO (Direct Preference Optimization)** | Alignment without explicit RM; better stability than PPO for moderate-scale models | 1. Collect preference dataset → 2. Compute DPO loss (β-regularized log-ratio) → 3. Fine-tune with AdamW lr=1e-5, β=0.1 → 4. Eval on MT-Bench, AlpacaEval |
| **Constitutional AI (CAI)** | Reduce human labeling cost while maintaining alignment; RLAIF | 1. Define constitutional principles (16-24 rules) → 2. SL-CAI: model self-critiques and revises → 3. RL-CAI: train RM on AI feedback → 4. PPO against RM |
| **MAPO** | Multi-step reasoning alignment; reduces hallucination in chain-of-thought | 1. Generate reasoning traces → 2. Score with process reward model (PRM) → 3. Advantage-weighted policy gradient → 4. Eval on MATH, GSM8K |

### 7.2 Safety Evaluation Metrics

| Metric / 指标 | Formula / 公式 | Target
|--------------|--------------|---------------|
| **Attack Success Rate (ASR)** | ASR = harmful_outputs
| **Refusal Rate (RR)** | RR = refused_requests
| **False Positive Rate (FPR)** | FPR = refused_benign
| **TruthfulQA Score** | % truthful AND informative answers | > 70% (GPT-4 baseline: 59%) |
| **Bias Score (BBQ)** | Accuracy disparity across demographic groups | Accuracy gap < 3% across groups |
| **Interpretability Faithfulness** | % of causal attribution preserved under intervention | > 80% on activation patching for target circuit |

