## 8. Standard Workflow

### Phase 1: Pre-training Data + Config

**Objective**: Prepare a validated data pipeline and training configuration before first GPU is allocated


| Step | Activity | Done Criteria | Fail Criteria |
|------|----------|--------------|---------------|
| 1 | Data deduplication: URL-level + MinHash LSH (Jaccard > 0.8 → remove) | Dedup rate reported; data size after dedup documented | No dedup performed → training data contains duplicates (causes overfitting) |
| 2 | Quality filtering: heuristic + ML classifier (FastText/BERT trained on Wikipedia vs. web) | Keep top 25-50% by quality score; distribution by domain validated | Unfiltered web data (garbage in → garbage out) |
| 3 | PII + toxicity: Perspective API or custom classifier; redact emails/SSNs | PII recall > 95% on held-out PII set | PII in training data → legal and security risk |
| 4 | Training config: global_batch=4096, seq_len=4096, LR=3e-4, bf16=true, grad_clip=1.0 | Config reviewed against hardware constraints | Missing grad_clip → risk of loss divergence |
| 5 | 1B proxy run: validate data pipeline, architecture, and config | Loss curve shows expected shape; MFU > 40% | Loss divergence at 1B → fix before scaling |

### Phase 2: Fine-tuning & Alignment

**Objective**: Instruction-tune and align a pre-trained model to production quality


| Step | Activity | Done Criteria | Fail Criteria |
|------|----------|--------------|---------------|
| 1 | SFT on high-quality instruction pairs (10K-500K examples) | MT-Bench > 7.0; IFEval > 0.75 | Scores below → data quality issue; audit examples |
| 2 | Choose alignment: DPO for static preference data; PPO for online/iterative | Method selected with justification | No baseline measurement → can't know if alignment helps |
| 3 | DPO: beta=0.1-0.2, LR=1e-6 to 5e-6, monitor KL divergence | KL(aligned ‖ SFT) < 10 nats; AlpacaEval Win Rate improves | KL > 20 nats → reward hacking; reduce LR |
| 4 | Capability preservation: MMLU, HumanEval pre/post alignment | Regression < 2% on capability benchmarks | > 5% regression → KL constraint too loose |
| 5 | Quantization (if serving): AWQ or GPTQ 4-bit | Benchmark regression < 1% vs. fp16 baseline | > 2% regression → try 8-bit or different quant method |

