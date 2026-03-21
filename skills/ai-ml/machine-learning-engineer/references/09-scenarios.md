# Machine Learning Engineer — Scenarios & Anti-Patterns

This file contains detailed scenarios and anti-patterns referenced from SKILL.md §9 and §10.

---

## Scenario 9.1: Real-Time Fraud Detection Model

**User:** "Build a real-time fraud detection model for our payment system. We process 10,000 transactions per minute and need decisions in under 100ms."

**Machine Learning Engineer:**
> **Architecture Constraints:**
> - 100ms budget: 20ms feature fetch + 30ms inference + 10ms post-process + 40ms buffer
> - Rules out deep learning → XGBoost/LightGBM at <5ms inference
>
> **Feature Engineering (Feast):**
> ```python
> user_transaction_stats = FeatureView(
>     name="user_transaction_stats",
>     entities=["user_id"],
>     ttl=timedelta(hours=1),
>     features=[
>         Feature(name="tx_count_1h", dtype=ValueType.INT64),
>         Feature(name="tx_amount_sum_24h", dtype=ValueType.FLOAT),
>         Feature(name="unique_merchants_7d", dtype=ValueType.INT64),
>     ],
>     online=True,
> )
> ```
>
> **Model Training (Time-Based Split):**
> ```python
> from sklearn.model_selection import TimeSeriesSplit
> tscv = TimeSeriesSplit(n_splits=5, gap=1)
>
> model = xgb.XGBClassifier(
>     n_estimators=500,
>     scale_pos_weight=99,
>     tree_method="hist",
> )
> mlflow.xgboost.log_model(model, "fraud_model")
> ```
>
> **Serving (BentoML):**
> ```python
> @bentoml.service(resources={"cpu": "2"}, traffic={"timeout": 0.09})
> class FraudDetectionService:
>     model = bentoml.xgboost.get("fraud_model:latest").to_runner()
> ```

---

## Scenario 9.2: Diagnosing CTR Drop

**User:** "Our recommendation model's CTR dropped 15% this week. No model changes were deployed."

**Machine Learning Engineer:**
> **Decision Tree:**
> ```
> CTR dropped 15% with no deployment
> │
> ├── Feature store latency spike? → fix upstream pipeline
> ├── Feature PSI > 0.25? → trace to data source
> ├── Prediction distribution shifted? → normalization issue
> └── No drift detected → seasonality or external event
> ```
>
> **Remediation:**
> | Root Cause | Fix |
> |-----------|-----|
> | Pipeline stuck | Restart DAG; backfill |
> | Data corrupted | Revert snapshot |
> | Behavior change | Retrain on fresh data |

---

## Scenario 9.3: ML Platform Design

**User:** "We have 5 data scientists and 10 models in production. How do we build a proper ML platform?"

**Machine Learning Engineer:**
> **Target Architecture:**
> ```
> Feature Store (Feast) → Prefect Pipelines → MLflow Registry → BentoML → K8s
>                              ↓
>                     Monitoring (Evidently + Grafana)
> ```
>
> **Migration Roadmap:**
> | Week | Action |
> |------|--------|
> | 1-2 | Convert 2 highest-risk models to Prefect |
> | 3-4 | Deploy MLflow tracking + model registry |
> | 5-6 | Add Evidently monitoring to all 10 models |
> | 7-8 | Shadow-deploy; retire notebook crons |

---

## Anti-Patterns (from §10)

| Severity | Anti-Pattern | Risk |
|----------|--------------|------|
| 🔴 High | **Jupyter Notebook Model** | No version control, manual ops |
| 🔴 High | **Offline-Online Disconnect** | AUC up, revenue down |
| 🔴 High | **Training-Serving Skew** | Silent degradation |
| 🔴 High | **Unmonitored Model** | Silent failure |
| 🟡 Medium | **Premature Complexity** | DL when GBDT suffices |
