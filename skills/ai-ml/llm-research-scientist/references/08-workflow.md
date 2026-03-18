## 8. Standard Workflow

### Phase 1: Architecture Design & Scaling Analysis

**Objective**: Determine compute-optimal model design before committing to a training run


| Step | Activity | Done Criteria | Fail Criteria |
|------|----------|--------------|---------------|
| 1 | Define compute budget (FLOPs), inference latency target, context length requirement | All 3 constraints documented | Missing any → cannot make optimal design decisions |
| 2 | Apply Chinchilla scaling: N × 20 tokens = compute-optimal; adjust for inference-optimal | Model size and token count determined | Budget inconsistency → revisit constraints |
| 3 | Select attention (GQA if 7B+), positional encoding (RoPE), activation (SwiGLU) | Architecture spec written with justifications | Unjustified choices → require ablation plan |
| 4 | Run 1B proxy experiment to validate architecture choices | 1B proxy matches expected loss curve | Loss divergence at 1B → fix before scaling |
| 5 | Data mix ablation: code %, math %, web %, domain data % | Eval suite shows balanced capability across domains | Any capability gap > 10% from target |

### Phase 2: Alignment Pipeline

**Objective**: Produce aligned model without significant capability regression


| Step | Activity | Done Criteria | Fail Criteria |
|------|----------|--------------|---------------|
| 1 | SFT baseline: train on 50K+ high-quality instruction pairs | MT-Bench > 7.0; IFEval > 0.75 | Scores below → check data quality first |
| 2 | Reward Model training: Bradley-Terry on 50K+ preference pairs | RM accuracy on held-out pairs > 72% | < 65% → reward model is unreliable; collect better data |
| 3 | DPO/PPO alignment: apply chosen method, monitor KL divergence | KL(aligned ‖ SFT) < 10 nats; AlpacaEval Win Rate > baseline | KL > 20 nats → reward hacking; reduce learning rate |
| 4 | Capability preservation check: run MMLU, HumanEval pre/post | Capability regression < 2% on all benchmarks | > 5% regression → KL constraint too loose |
| 5 | Red-team evaluation: 200+ adversarial prompts | Refusal rate > 95% on harmful; helpfulness maintained | Refusal on non-harmful > 5% → over-refusal problem |

