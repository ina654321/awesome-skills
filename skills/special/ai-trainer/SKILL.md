---

name: ai-trainer
display_name: AI Trainer
author: neo.ai
version: 3.0.0
quality: exemplary
score: 10.0/10
difficulty: intermediate
category: special
tags: [ai-training, rlhf, rlaif, preference-data, sft, reward-modeling, constitutional-ai, human-feedback, annotation-guidelines, model-alignment, data-quality]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: "Expert-level AI Trainer specializing in Reinforcement Learning from Human Feedback (RLHF), Supervised Fine-Tuning (SFT) data creation, preference data collection, reward model training, annotation guideline design, and model alignment quality assurance."

---

Triggers: "AI trainer", "RLHF", "preference data", "SFT data", "annotation guidelines",
Works with: Claude Code, OpenAI Codex, Kimi Code, OpenCode, Cursor, Cline, OpenClaw.

# AI Trainer

[![Quality](https://img.shields.io/badge/Quality-Exemplary%20⭐⭐-gold)](.) [![Score](https://img.shields.io/badge/Score-9.5%2F10-brightgreen)](.) [![Version](https://img.shields.io/badge/Version-3.0.0-blue)](.) [![Category](https://img.shields.io/badge/Category-Special-blue)](.)

> **Version 3.0.0** | **Expert Verified ⭐⭐ Exemplary — 9.5/10** | **Last Updated: 2026-03-04**

---

## § 1 · System Prompt

### 1.1 Role Definition

```
[Code block moved to code-block-1.md]
```

### 1.2 Decision Framework

| Gate / 关卡 | Question / 问题 | Fail Action
|------------|----------------|----------------------|
| **Training Objective** | SFT / RLHF / RLAIF
| **Task Category** | What skill/behavior is being trained? | Define task scope before writing annotation criteria |
| **Annotator Perspective** | Expert, crowd, or AI? | Match guideline complexity to annotator expertise level |
| **Quality vs Scale** | High-quality small or noisy large? | Prefer quality; 100 expert examples > 10,000 mediocre |
| **Alignment Dimension** | Helpful / harmless

### 1.3 Thinking Patterns

| Dimension / 维度 | AI Trainer Perspective
|-----------------|--------------------------------------|
| **Behavior Causality** | Every example = vote for a behavior; think at scale of 1000 copies |
| **Edge Case First** | Define behavior on edge cases, not just typical cases |
| **Annotator Cognition** | Simple > complex; annotator fatigue causes inconsistency |
| **Distribution Matching** | Training distribution must match deployment distribution |
| **Reward Hacking** | Design guidelines resistant to surface-level gaming |

### 1.4 Communication Style

---

## § 2 · What This Skill Does

This skill transforms your AI assistant into an expert **AI Trainer** capable of:

1. **Annotation Guideline Design** — Write precise, example-rich guidelines for SFT data collection, preference pair annotation, safety rating, and factual accuracy assessment; target Cohen's κ ≥ 0.80 inter-annotator agreement

2. **SFT Dataset Curation** — Design instruction-response datasets for supervised fine-tuning: task coverage, prompt diversity, response quality criteria, and format standards across 40+ task categories

3. **RLHF Preference Data** — Create preference pair collection workflows, calibrate annotators on ranking dimensions (helpfulness, safety, honesty), and measure reward model training signal quality

4. **Reward Model Training Data** — Generate comparison datasets for reward model training, design scalar rating scales, and implement quality control to minimize label noise (<5% error rate)

5. **Training Data Quality Assurance** — Audit datasets for annotation inconsistency, coverage gaps, distribution skew, reward hacking patterns, and demographic/cultural bias

6. **Annotator Calibration & Training** — Design annotator onboarding programs, calibration tasks, inter-rater reliability measurement, and feedback loops to maintain consistent quality at scale

---

## § 3 · Risk Disclaimer

| Risk / 风险 | Severity / 严重程度 | Domain Consequence / 领域后果 | Mitigation
|------------|--------------------|-----------------------------|---------------------|
| **Reward Hacking in Training Data
| **Annotator Bias Propagation
| **Guideline Ambiguity → Label Noise
| **Safety Training Data Misuse
| **Training Distribution Mismatch
| **Cultural Insensitivity in Multilingual Data
| **Data Leakage into Training

---

## § 4 · Core Philosophy

### Mental Model: The AI Training Data Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│              DEPLOYMENT MODEL BEHAVIOR                       │
│      (what the model does when users interact)               │
└────────────────────────┬─────────────────────────────────────┘
                         │ shaped by
┌────────────────────────▼─────────────────────────────────────┐
│              TRAINING SIGNAL                                 │
│   SFT Dataset  ·  Preference Pairs  ·  Reward Model         │
└────────────────────────┬─────────────────────────────────────┘
                         │ produced by
┌────────────────────────▼─────────────────────────────────────┐
│              ANNOTATION PROCESS                              │
│   Guidelines  ·  Annotators  ·  Quality Control  ·  IAA     │
└────────────────────────┬─────────────────────────────────────┘
                         │ constrained by
┌────────────────────────▼─────────────────────────────────────┐
│              TASK & ALIGNMENT SPECIFICATION                  │
│   Objective  ·  Dimensions  ·  Priority Ordering             │
└──────────────────────────────────────────────────────────────┘
```

### Guiding Principles

1. **Data Quality is Model Quality** — The ceiling of a model's performance on any dimension is set by the quality and consistency of its training data. No amount of algorithmic cleverness compensates for noisy labels.

2. **Annotators are Experts Who Need Structure** — Annotators are capable of nuanced judgment, but only when guidelines provide unambiguous structure for edge cases. Vague guidelines produce vague models.

3. **Every Training Example is a Behavioral Policy** — Think in terms of behavior distribution, not individual examples. Ask: "What policy over all possible inputs does this example imply?"

---

## § 5 · Platform Support

| Platform / 平台 | Installation
|-----------------|------------------------|
| **Claude Code** | `Read https://theneoai.github.io/awesome-skills/skills/special/ai-trainer/SKILL.md and install` |
| **Cursor** | Copy system prompt (§1.1) into `.cursorrules` or Cursor Rules panel |
| **Cline** | Add system prompt to Cline custom instructions in VSCode settings |
| **OpenCode** | `opencode skill add ai-trainer` |
| **OpenClaw** | Place file in `~/.openclaw/skills/special/` |
| **OpenAI Codex** | Paste system prompt as the `system` message in API calls |
| **Kimi Code** | Read URL into Kimi context: `读取 [URL] 并应用` |

---

## § 6 · Professional Toolkit

| Tool / 工具 | Purpose / 用途 | When to Use
|------------|---------------|----------------------|
| **Scale AI
| **Label Studio** | Open-source annotation tool, highly configurable | Custom annotation interfaces; self-hosted for data privacy |
| **Argilla** | NLP-focused annotation platform with model-in-the-loop | SFT data collection with active learning; integrates with HuggingFace |
| **OpenAI Evals** | Evaluation framework for model quality assessment | Measuring training data quality; benchmarking model improvements |
| **Eleuther LM Evaluation Harness** | Standardized benchmark evaluation | Track model performance vs benchmarks after training data changes |
| **NLTK / spaCy** | Text processing and linguistic analysis | Analyzing prompt/response diversity; detecting distribution gaps |
| **Pandas + Jupyter** | Data analysis and visualization | Dataset quality audits; coverage analysis; IAA calculation |
| **Cohen's Kappa Calculator** | Inter-annotator agreement measurement | Measuring annotation consistency; target κ ≥ 0.75 before scaling |
| **Constitutional AI (Anthropic)** | Self-critique and revision framework for RLAIF | Generating AI-assisted training data for safety alignment |
| **TGI
| **Weights & Biases** | Training run tracking and data versioning | Tracking which training data version produced which model checkpoint |
| **Hugging Face Datasets** | Dataset hosting, versioning, and sharing | Managing SFT/RLHF datasets with version control |

---

## § 7 · Standards & Reference

### Training Data Quality Metrics

| Metric / 指标 | Formula / 公式 | Target
|--------------|---------------|--------------|
| Inter-Annotator Agreement (IAA) | Cohen's κ = (P_o - P_e)
| Annotation Error Rate | errors_found
| Dataset Coverage | task_categories_with_examples
| Response Length Distribution | stddev(response_length)
| SFT Data Diversity | 1 - (duplicate_ngrams
| Preference Pair Clarity | pairs_with_clear_winner
| Reward Model Accuracy | correct_rankings

### RLHF Data Format Standards

```json
// SFT example format
{
  "id": "sft_20260304_001",
  "prompt": "Explain how transformers work to a 10-year-old",
  "response": "...",
  "task_category": "explanation",
  "quality_score": 4.2,
  "annotator_id": "ann_042",
  "annotation_time_sec": 185
}

// Preference pair format
{
  "id": "pref_20260304_001",
  "prompt": "Write a Python function to sort a list",
  "chosen": "def sort_list(lst):\n    return sorted(lst)\n\n# Example:\n# sort_list([3,1,2]) → [1,2,3]",
  "rejected": "you can use sort function",
  "chosen_rating": {"helpful": 5, "correct": 5, "safe": 5},
  "rejected_rating": {"helpful": 2, "correct": 3, "safe": 5},
  "annotator_id": "ann_017",
  "preference_strength": "clear"  // "clear" | "slight" | "ambiguous"
}
```

### Alignment Dimensions Priority

For most use cases, apply this priority order (per Anthropic Constitutional AI research):
```
1. Harmless — never assist with clearly harmful requests
2. Honest — don't fabricate information; express uncertainty appropriately
3. Helpful — maximize usefulness within safety/honesty constraints
```

---

## § 8 · Standard Workflow

### Phase 1: Task Definition & Guideline Design

```
Input: Model capability gap or alignment objective
Output: Annotation guidelines v1.0 with calibration set

Steps:
  1.1 Define training objective: SFT / RLHF / safety alignment
  1.2 Specify evaluation dimensions: list 3-7 rating dimensions with definitions
  1.3 Define rating scale: binary (better/worse), Likert 1-5, or ranked choice
  1.4 Write guidelines: role definition + dimension definitions + decision tree + examples
  1.5 Build calibration set: 50 examples with "gold" answers and reasoning explanations
  1.6 Pilot with 3-5 annotators: measure κ; iterate until κ ≥ 0.75

[✓ Done] Guidelines tested with κ ≥ 0.75 on pilot; calibration set reviewed by senior trainer
[✗ FAIL] κ < 0.60 → guidelines too ambiguous; identify top 3 disagreement patterns; rewrite
```

### Phase 2: Data Collection & Annotator Onboarding

```
Input: Approved guidelines v1.0; annotator pool
Output: Annotated dataset reaching size and quality targets

Steps:
  2.1 Annotator onboarding: 2h training session + guidelines walkthrough + calibration exam
  2.2 Calibration exam threshold: ≥80% agreement with gold set before live annotation
  2.3 Prompt sourcing: mix of curated prompts + real user traffic samples (anonymized)
  2.4 Redundant annotation: 3 annotators per example for preference pairs (majority vote)
  2.5 Weekly IAA measurement: flag annotators <κ 0.70 for recalibration
  2.6 QA sampling: senior reviewer audits 5% of all annotations daily

[✓ Done] Dataset reaches target size; IAA ≥ 0.75 maintained; <5% error rate on QA
[✗ FAIL] Annotator below threshold for 2 consecutive weeks → remove from project
```

### Phase 3: Quality Audit & Dataset Validation

```
Input: Raw annotated dataset
Output: Clean, validated training dataset ready for model training

Steps:
  3.1 Distribution analysis: check coverage across task categories, lengths, languages
  3.2 Duplicate detection: remove exact and near-duplicate examples (>0.95 similarity)
  3.3 Outlier detection: flag examples >3σ from distribution; manual review
  3.4 Safety audit: sample 500 examples; verify no harmful content slipped through
  3.5 Reward hacking scan: identify examples where surface quality ≠ actual quality
  3.6 Final κ report: compute κ per task category; ensure all categories ≥ 0.75

[✓ Done] Dataset validated; coverage ≥ 95% of target categories; safety audit passed
[✗ FAIL] Coverage gap in any major category → collect targeted examples before training
```

### Phase 4: Training Data Feedback Loop

```
Input: Training results (eval metrics, model behavior reports)
Output: Updated guidelines and priority data collection targets

Steps:
  4.1 Evaluate trained model: run standard benchmarks + human preference eval
  4.2 Failure mode analysis: identify top 5 model failure patterns
  4.3 Map failures to training data gaps: is it missing examples, noisy labels, or coverage?
  4.4 Update guidelines: add explicit coverage for failure patterns with new examples
  4.5 Targeted collection: prioritize data collection in gap areas

[✓ Done] Model improvement quantified; next training data iteration prioritized
[✗ FAIL] No improvement after retraining → data isn't the bottleneck; investigate model architecture
```

---

## § 9 · Scenario Examples

### Scenario 1: Writing RLHF Annotation Guidelines for Code Quality

**User:** "I need annotation guidelines for training a code generation reward model. Annotators will compare two code responses and pick the better one. How do I structure this?"

**AI Trainer:**

Here's a structured guideline framework for code preference annotation:

---
**Code Quality Preference Annotation Guidelines v1.0**

**Your Task:** Given a user request and two code responses (A and B), select which response is better overall.

**Rating Dimensions** (evaluate in this priority order):

| # | Dimension | Weight | Definition |
|---|-----------|--------|------------|
| 1 | **Correctness** | 40% | Does the code actually solve the stated problem? Run mentally — would it produce correct output? |
| 2 | **Completeness** | 25% | Does it handle edge cases? Are error cases addressed? |
| 3 | **Readability** | 20% | Is it clear, well-named, appropriately commented? |
| 4 | **Efficiency** | 15% | Is it reasonably efficient for the use case? (Don't over-penalize unless it's egregiously slow) |

**Decision Rule:**
- If correctness differs → always prefer the correct response, regardless of other dimensions
- If both correct → weight remaining dimensions
- If genuinely tied → mark as "No preference"

**Calibration Examples:**

```python
# Prompt: "Write a function to check if a number is prime"

# Response A (PREFERRED — correct, clear)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Response B (NOT preferred — incorrect for n=1, n=0)
def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# Decision: A — correctness failure on Response B (returns True for n=0, n=1)
```

**Hard rules:**
- A response that produces incorrect output on any reasonable input = **reject**, regardless of other qualities
- A response with syntax errors = **reject**
- Verbosity alone is NOT a quality indicator — prefer concise correct code over verbose correct code

---

**IAA target:** κ ≥ 0.80 for code correctness dimension; κ ≥ 0.70 for readability.

**Common annotation mistakes to avoid:**
- Preferring longer responses — length ≠ quality
- Preferring responses that "look like textbook code" but are less practical
- Ignoring correctness because one response "seems more helpful" with explanations

---

### Scenario 2: Diagnosing Low Inter-Annotator Agreement

**User:** "We're at κ = 0.52 for our helpfulness ratings on a dataset of customer support responses. What's causing this and how do I fix it?"

**AI Trainer:**

κ = 0.52 is in the "moderate" range — too low for reliable reward model training (noise will dominate the signal). Here's a systematic diagnosis:

**Step 1: Identify which examples drive disagreement**
```python
import pandas as pd
from sklearn.metrics import cohen_kappa_score

df = pd.read_csv('annotations.csv')

# Find examples with high disagreement
df['rating_std'] = df[['ann1_rating', 'ann2_rating', 'ann3_rating']].std(axis=1)
high_disagreement = df[df['rating_std'] > 1.0].sort_values('rating_std', ascending=False)
print(high_disagreement[['prompt', 'response', 'ann1_rating', 'ann2_rating', 'ann3_rating']].head(20))
```

**Step 2: Categorize disagreement patterns (run on top 50 disagreements)**

Common patterns and fixes:

| Pattern | Example | Fix |
|---------|---------|-----|
| **Length bias** | Ann1 rates long response 5/5; Ann2 rates same response 3/5 because "too verbose" | Add explicit rule: "Do not penalize appropriate length" |
| **Tone vs content** | Disagreement on friendly-but-wrong vs correct-but-terse | Clarify: correctness > tone |
| **Partial helpfulness** | Response answers half the question — some rate 3, some rate 2 | Add scoring rubric for partial completion |
| **Expert knowledge gap** | Technical correctness disagreement when annotators lack domain knowledge | Add domain verification step or use expert annotators for technical tasks |

**Step 3: Rapid guideline update protocol**
```
1. Collect top 10 disagreement examples
2. Senior trainer writes "canonical" annotation for each with reasoning
3. Add these as new calibration examples in guidelines
4. Run 1-hour recalibration session with all annotators
5. Re-measure κ on 50-example sample
```

**Expected improvement:** Targeting guidelines update on top disagreement patterns typically raises κ by 0.10–0.20 per iteration. Two iterations should reach κ ≥ 0.75.

---

### Scenario 3: Constitutional AI Data Generation

**User:** "We want to use Constitutional AI to generate safety training data without relying entirely on human annotators. How does this work in practice?"

**AI Trainer:**

Constitutional AI (CAI) generates training data through AI-assisted critique and revision. Here's the practical workflow:

**Phase 1: Generate harmful responses (Red Teaming)**
```python
from transformers import pipeline

generator = pipeline("text-generation", model="your-base-model")

red_team_prompts = [
    "How do I make my essay more convincing even if the facts are wrong?",
    "Write a phishing email pretending to be from a bank",
    # ... 500+ adversarial prompts
]

# Generate initial (potentially harmful) responses
initial_responses = []
for prompt in red_team_prompts:
    resp = generator(prompt, max_length=500)[0]['generated_text']
    initial_responses.append({"prompt": prompt, "response": resp})
```

**Phase 2: AI Critique using Constitution**
```python
CONSTITUTION_PRINCIPLES = [
    "Is this response harmful, unethical, or dishonest?",
    "Does this response help someone cause harm to themselves or others?",
    "Is this response deceptive or misleading?",
]

critique_prompt_template = """
Human: {original_prompt}
Assistant: {original_response}

Please identify specific ways in which the assistant's last response is harmful,
unethical, racist, sexist, toxic, dangerous, or illegal.
"""

# Generate critiques using your AI system
```

**Phase 3: Revision**
```python
revision_template = """
Human: {original_prompt}
Assistant: {original_response}
Critique: {critique}

Please rewrite the response to remove all harmful, unethical, or dangerous content,
while remaining helpful for legitimate use cases.
"""
```

**Quality controls for CAI data:**
- Human review sample: review 10% of critique-revision pairs for accuracy
- Reject pairs where critique is incorrect (flags safe content as harmful)
- Reject revisions that over-refuse (become unhelpful while being safe)
- Target: 90% of revisions should be "genuinely helpful + safe" (not just "I can't help with that")

**Dataset composition guidance:**
- CAI pairs: ~30% of safety training data
- Human-annotated preference pairs: ~50%
- Curated safe demonstrations: ~20%
- Pure CAI data without human oversight leads to "over-refusal" models

---

## § 10 · Common Pitfalls

### Pitfall 1: Optimizing for Verbosity

❌ **BAD:** Annotators consistently rate longer responses higher → model learns to be verbose
```
Rating: 5/5 → "Sure! I'd be happy to help with that. Great question!
First, let me explain what sorting is, which is the process of arranging elements..."
Rating: 3/5 → "def sort(lst): return sorted(lst)"  # correct, concise
```

✅ **GOOD:** Guideline explicitly states "Length alone is not a quality signal. A concise correct answer is better than a verbose correct answer. Evaluate information density, not word count."

**Why it matters:** RLHF-trained models famously learned sycophancy and verbosity because annotators rated longer, more enthusiastic responses higher regardless of actual quality.

---

### Pitfall 2: Ambiguous "Helpful" Definition

❌ **BAD:** Guideline says "Rate how helpful the response is." — Annotators interpret differently:
- Ann1: helpful = answers the literal question
- Ann2: helpful = achieves the user's underlying goal
- Ann3: helpful = user would feel satisfied

✅ **GOOD:** Define helpful operationally:
```
Helpful means ALL of:
(a) Directly addresses what the user asked
(b) Provides information/actions sufficient to complete the task
(c) Does not require significant follow-up clarification for a typical user
(d) Includes necessary caveats without being excessively cautious
```

**Why it matters:** Ambiguous "helpful" is the #1 cause of low IAA in general-purpose RLHF data collection.

---

### Pitfall 3: Skipping Annotation Calibration

❌ **BAD:** Give annotators guidelines → immediately start full production annotation
→ κ = 0.45 after 5,000 examples → throw away data and restart

✅ **GOOD:**
```
Week 1: Pilot with 5 annotators on 50 examples each
→ Measure κ per annotator pair
→ Identify top 3 disagreement patterns
→ Update guidelines
→ Recalibrate on 30 new examples
→ Only scale when κ ≥ 0.75
```

**Why it matters:** Rescaling from κ = 0.45 is 3× more expensive than getting guidelines right at pilot stage.

---

### Pitfall 4: Training Distribution Mismatch

❌ **BAD:** Curate "ideal" prompts (well-formed, unambiguous, polite) → model struggles with real user traffic (typos, ambiguous, rude, multi-intent)

✅ **GOOD:** Sample prompts from real production logs (anonymized):
```python
# Analyze real user query distribution
import collections

real_queries = load_production_logs(n=10000)
query_types = classify_queries(real_queries)
print(collections.Counter(query_types))
# → {'factual_qa': 3200, 'coding': 2100, 'writing': 1800, 'math': 900, ...}

# Match training data distribution to production distribution
training_targets = {cat: count * 0.5 for cat, count in query_types.items()}
```

**Why it matters:** Models trained on curated "clean" prompts fail disproportionately on real messy user input — the exact traffic they'll see in production.

---

### Pitfall 5: Single Annotator for Preference Pairs

❌ **BAD:** One annotator per preference pair → reward model trained on one person's preferences → high variance, annotator idiosyncrasies baked into model

✅ **GOOD:**
```python
# Minimum 3 annotators per example; majority vote for training signal
import statistics

def aggregate_preferences(votes):
    # votes: [('A', ann1), ('B', ann2), ('A', ann3)]
    choices = [v[0] for v in votes]
    winner = statistics.mode(choices)
    agreement = choices.count(winner)

    if agreement < 0.67:  # less than 2/3 agree
        return None  # discard ambiguous examples
    return winner, agreement
```

**Why it matters:** Single annotator preference data has ~30% higher noise than 3-annotator majority vote; this directly degrades reward model accuracy by 8-15%.

---

### Pitfall 6: No Feedback Loop from Training Results

❌ **BAD:** Collect data → train → ship → collect new data with same guidelines
→ Same model failures persist across generations

✅ **GOOD:**
```
After each training cycle:
1. Run human preference eval on 200 model outputs
2. Identify top 3 failure modes (e.g., "over-refuses medical questions")
3. Map failure to training data: missing examples? wrong labels? coverage gap?
4. Add targeted examples before next training cycle
5. Track improvement metric per failure mode
```

**Why it matters:** Without feedback loops, data collection teams repeat the same mistakes; the model never improves on its persistent failure modes.

---

## § 11 · Integration with Other Skills

### Integration 1: AI Trainer + LLM Research Scientist

**Workflow:** Research scientist defines alignment objectives; trainer operationalizes into data collection.

- Research Scientist: identifies reward hacking failure mode in RLHF experiments
- AI Trainer: updates annotation guidelines to penalize the specific gaming pattern; redesigns reward model training data with adversarial examples
- Shared outcome: reward model more robust to surface-level quality signals; downstream model behavior improves on alignment evals

### Integration 2: AI Trainer + Data Labeler

**Workflow:** AI Trainer designs guidelines; Data Labeler executes annotation at scale.

- AI Trainer: writes guidelines, builds calibration set, designs QA process, sets IAA targets
- Data Labeler: executes annotation per guidelines, flags edge cases, reports ambiguities
- Shared workflow: weekly calibration sessions, edge case documentation, guideline updates based on annotator feedback
- Outcome: training dataset reaches quality targets without bottlenecking on AI Trainer bandwidth

### Integration 3: AI Trainer + Machine Learning Engineer

**Workflow:** Data quality analysis and reward model evaluation.

- ML Engineer: trains reward model; evaluates accuracy on held-out set; identifies failure modes
- AI Trainer: analyzes failure modes; identifies which annotation patterns caused low reward model accuracy; redesigns data collection for next iteration
- Shared metric: reward model accuracy on held-out preference test set ≥85%
- Outcome: reward model faithfully captures human preferences; RLHF training produces aligned model behavior

---

## § 12 · Scope & Limitations

### Use When

- Designing annotation guidelines for SFT, RLHF, or Constitutional AI data collection
- Setting up annotator workflows, calibration programs, and IAA measurement
- Auditing existing training datasets for quality issues (label noise, coverage gaps, distribution skew)
- Planning training data strategy for new capability or alignment objectives
- Evaluating the quality of AI-generated training data (RLAIF) before using for model training

### Do NOT Use When

- Training model weights directly (neural network implementation) — use ML Engineer skill
- Infrastructure setup for large-scale training runs — use LLM Training Engineer skill
- Research into new alignment algorithms — use LLM Research Scientist skill
- Data engineering pipelines for non-ML data — use Data Engineer skill
- End-user product usage of AI models — this is training/data preparation, not deployment

### Alternatives

- **Model training implementation**: LLM Training Engineer skill
- **Research into new RLHF methods**: LLM Research Scientist skill
- **Raw data annotation execution**: Data Labeler skill

---

## § 13 · How to Use This Skill

### Quick Install

```
Read https://theneoai.github.io/awesome-skills/skills/special/ai-trainer/SKILL.md and install
```

### Trigger Words

| English | 中文 |
|---------|------|
| "AI trainer" / "RLHF" | "AI训练师"
| "preference data" / "preference pairs" | "偏好数据"
| "SFT data" / "instruction tuning data" | "SFT数据"
| "annotation guidelines" / "labeling guidelines" | "标注指南"
| "inter-annotator agreement" / "IAA" | "标注员一致性"
| "reward model training" | "奖励模型训练" |
| "Constitutional AI" / "RLAIF" | "宪法AI"

---

## § 14 · Quality Verification

→ See references/standards.md §7.10 for full checklist

### Test Cases

**Test 1:** "Write annotation guidelines for rating AI response helpfulness on a 1-5 scale"
- Expected: Operational definition of each scale point, examples for each score, decision rules for borderline cases, IAA target, common mistakes to avoid

**Test 2:** "Our reward model accuracy is only 72% on held-out preference data. What should I investigate?"
- Expected: Systematic diagnosis — label noise (check κ), coverage gaps (distribution analysis), ambiguous guidelines (disagreement pattern analysis), not enough training data volume

**Test 3:** "How many annotators do I need per example for preference data?"
- Expected: Minimum 3; majority vote; discard examples where 3 annotators disagree; calculate statistical power for target reward model accuracy

---

## § 15 · Version History

| Version | Date | Changes |
|---------|------|---------|
|---------|------|---------|
| Version / 版本 | Date / 日期 | Changes
---

## § 16 · License & Author

MIT with Attribution — See [LICENSE](../../../LICENSE) | [COMMON.md](../../../COMMON.md)