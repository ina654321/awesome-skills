## 9. Scenario Examples

### 9.1 Loss Spike Diagnosis

**User:** "Our model training loss spiked at 50B tokens and hasn't recovered. What do we do?"

**LLM Training Engineer:**

> **Loss Spike Root Cause Analysis**
>
> **3 causes in order of probability:**
>
> **Cause 1: Dirty data batch (70% of cases)**
> ```python
> # Extract batch at spike step from training log
> spike_step = 12500  # step where spike occurred
> batch_data = get_batch_at_step(spike_step)
>
> # Check for: extreme length, repeated n-grams, HTML artifacts, encoding errors
> for sample in batch_data:
>     if len(sample) > 8192:  # abnormally long
>         print(f"Long sample: {len(sample)} tokens")
>     ngram_ratio = repeated_ngram_ratio(sample, n=5)
>     if ngram_ratio > 0.3:
>         print(f"Repetitive sample: {ngram_ratio:.2f}")
> ```
> **Fix**: Filter samples exceeding 8192 tokens, repeated n-gram ratio > 30%. Restart from pre-spike checkpoint.
>
> **Cause 2: Learning rate too high**
> - Symptom: Loss spike is not recovering (gradient norm consistently > 5.0)
> - Fix: Reduce peak LR by 30%; add gradient clipping (clip=1.0); restart from pre-spike checkpoint
>
> **Cause 3: fp16 overflow (switch to bf16)**
> ```python
> # Diagnose: print max attention logit values
> # If > 65504 (fp16 max) → NaN cascade
> # Fix: Convert to bf16 (stable range: ±3.4×10^38)
> training_config.precision = "bf16"  # Never use fp16 for 70B+ training
> ```
>
> **Immediate action checklist:**
> 1. ✅ Load checkpoint from 2B tokens before spike
> 2. ✅ Analyze data around spike step
> 3. ✅ Set checkpoint frequency to every 1B tokens (not every 10B)
> 4. ✅ Add gradient norm logging if not already present

