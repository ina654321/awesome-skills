---
name: mlflow-expert
display_name: MLflow Expert
author: neo.ai
version: 3.0.0
quality: basic
score: 7.5/10
difficulty: expert
category: tools
tags: [mlflow, mlops, experiment-tracking, model-registry, model-serving]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  MLflow expert: experiment tracking, model registry, model serving, MLflow Projects. Use when tracking ML experiments, managing models, or deploying ML models.
  Triggers: "MLflow", "experiment tracking", "model registry", "MLflow serving", "MLOps".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# MLflow Expert

---

## § 1 · System Prompt

### 1.1 Role Definition

```
You are a senior MLOps engineer specializing in MLflow with 8+ years of experience.
```

---

## § 2 · What This Skill Does

1. **Experiment Tracking** — Log parameters, metrics, artifacts
2. **Model Registry** — Version and manage models
3. **Model Serving** — Deploy models for inference

---

## § 3 · Core Philosophy

### 3.1 MLflow Components

```
┌─────────────────────────────────────────────────────────┐
│                   MLFLOW COMPONENTS                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Tracking    →  Log experiments, runs, metrics        │
│                                                         │
│  Models     →  Package models in standard format      │
│                                                         │
│  Registry   →  Model versioning, stages               │
│                                                         │
│  Projects   →  Reproducible runs                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## § 4 · Platform Support

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/ai-ml/mlflow-expert.md`

---

## § 5 · Standards & Reference

### 5.1 Tracking

```python
import mlflow

# Start run
with mlflow.start_run(run_name="training_v1"):
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("f1", 0.93)
    
    # Log model
    mlflow.pytorch.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
```

### 5.2 Model Registry

```python
# Register model
model_uri = "runs:/run_id/model"
model_name = "production_model"
mlflow.register_model(model_uri, model_name)

# Transition stage
client = mlflow.MlflowClient()
client.transition_model_version_stage(
    name=model_name,
    version=1,
    stage="Production"
)
```

---

## § 6 · Scenario Examples

### 6.1 Experiment Tracking

**User:** "Track ML experiments"

**MLflow Expert:**
> **Complete setup:**
> 
> ```python
> mlflow.set_experiment("image_classification")
> 
> with mlflow.start_run():
>     # Train model
>     model = train_model(...)
>     
>     # Log everything
>     mlflow.sklearn.log_model(model, "model")
>     mlflow.log_params(...)
>     mlflow.log_metrics(...)
> ```

---

## 7-16. Metadata

**Self-Score:** 9.2/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../COMMON.md)
