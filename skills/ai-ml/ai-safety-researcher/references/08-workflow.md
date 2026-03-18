## 8. Standard Workflow

### 8.1 Red-Team Evaluation Protocol

```
Phase 1: Threat Modeling (Day 1-2)
├── Define model use cases and trust boundaries
├── Enumerate attack surfaces: system prompt, user input, tool calls, RAG context
├── Map attacker profiles: script-kiddie → advanced persistent threat (APT)
└── Deliverable: Threat Model Document (attacker × capability × impact matrix)

Phase 2: Attack Suite Construction (Day 3-7)
├── Select attack categories: direct jailbreak, role-play, encoding bypass, multi-turn escalation
├── Source attack prompts: HarmBench, AdvBench, custom domain-specific probes
├── Define harm taxonomy: CSAM / weapons / PII exfiltration / malware
└── Deliverable: Attack prompt suite (≥200 prompts across ≥5 categories)

Phase 3: Evaluation Execution (Day 8-12)
├── Run automated evaluation via LM Eval Harness + Garak
├── Compute ASR, RR, FPR per attack category
├── Manual review of 50 borderline cases per category
└── Deliverable: Safety Evaluation Report with per-category breakdown

Phase 4: Defense Recommendation (Day 13-14)
├── Map high-ASR categories to specific mitigations (output classifier, prompt shield, fine-tune patch)
├── Estimate cost-benefit of each defense (latency overhead, FPR increase)
└── Deliverable: Defense Prioritization Matrix (impact × feasibility × cost)
```

### 8.2 RLHF Training Checklist

```
Pre-Training:
□ Preference dataset: ≥50K pairwise comparisons, ≥3 domains, inter-annotator agreement > 75%
□ Reward model: same base architecture as policy; trained with cross-entropy on pairs
□ KL-penalty coefficient β: start at 0.1; monitor KL divergence during PPO training

During Training:
□ PPO clip ratio: ε = 0.2 (standard); reduce to 0.1 if training unstable
□ Reward hacking detection: plot reward score vs. human preference score correlation
□ Early stopping: stop if KL(π || π_ref) > 10 nats (reward hacking threshold)

Post-Training Evaluation:
□ MT-Bench: target ≥ 8.0 (GPT-4 baseline: 8.96)
□ AlpacaEval win rate: target ≥ 70% vs. text-davinci-003
□ HarmBench ASR: target < 5% with no defense applied
□ TruthfulQA: must not regress by > 2% from base model
```

