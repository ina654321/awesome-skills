## 7. Standards & Reference

### Architecture Design Reference

| Component / 组件 | Options / 选项 | Trade-off / 权衡 | Current Best Practice
|----------------|--------------|----------------|-----------------------------------|
| **Attention** | MHA / MQA / GQA
| **Positional Encoding** | RoPE / ALiBi
| **Normalization** | Pre-LN / Post-LN
| **Activation** | GeLU / SwiGLU
| **Tokenizer** | BPE / SentencePiece

### Scaling Laws Reference

```
Chinchilla Optimal (Hoffmann et al., 2022):
  N_opt ≈ C
  - N = model parameters, D = training tokens, C = compute budget (FLOPs)
  - Rule of thumb: ~20 tokens per parameter for compute-optimal training
  - Example: 7B model → ~140B tokens optimal (LLaMA used 1T+ for inference efficiency)

Inference-Optimal Regime (Touvron et al., LLaMA):
  When inference cost >> training cost:
  - Train smaller model for longer (more tokens)
  - LLaMA/Mistral approach: smaller N, much larger D
  - Trade-off: higher training cost → lower per-inference cost
```

### Alignment Methods Comparison

| Method | Data Required | Complexity | Best For |
|--------|--------------|-----------|----------|
| **SFT** | High-quality instruction pairs | Low | Instruction following baseline |
| **RLHF (PPO)** | Preference pairs + RM | High | Large-scale alignment |
| **DPO** | Preference pairs | Low | Medium-scale, stable training |
| **GRPO** | Verifiable reward signal | Medium | Math, code (DeepSeek-R1) |

