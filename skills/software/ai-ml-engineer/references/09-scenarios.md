# AI/ML Engineer — Scenario Examples & Anti-Patterns

This file contains detailed scenario examples and anti-patterns referenced from SKILL.md §9 and §10.

---

## Scenario 9.1: Diagnosing and Fixing AUC Drop in Production

**User:** "Our recommendation model AUC dropped from 0.87 to 0.81 in production. Diagnose and fix."

**ML Engineer:**
> **Production AUC Drop: Diagnosis Protocol**
>
> A drop from 0.87 to 0.81 (6 absolute points) is severe. Systematic diagnosis before any fix:
>
> **Step 1 — Isolate the Cause (Day 1)**
>
> Run these checks in order; stop at the first confirmed failure:
>
> | Check | Tool | Signal |
> |-------|------|--------|
> | Feature data drift | Evidently AI PSI report | PSI > 0.2 on any feature → data pipeline issue |
> | Label distribution shift | Compare label histograms | Positive rate change > 10% → concept drift |
> | Feature serving skew | KS test on online vs offline | p-value < 0.05 → training-serving skew |
> | Model version | Triton model registry | Wrong version deployed → rollback |
> | Data pipeline freshness | Feast timestamps | Stale features (> 24h) → pipeline failure |
>
> **Step 2 — Feature Drift Analysis:**
> ```python
> from evidently.report import Report
> from evidently.metric_preset import DataDriftPreset
>
> report = Report(metrics=[DataDriftPreset(stattest="psi", stattest_threshold=0.2)])
> report.run(reference_data=training_df, current_data=production_df_last_7d)
> report.save_html("drift_report.html")
> ```
>
> **Step 3 — Rollback and Retrain:**
> ```bash
> # Rollback to previous version
> cp -r /models/recommender/v3 /models/recommender/active
> curl -X POST http://triton:8000/v2/repository/models/recommender/load
> ```
>
> **Step 4 — Validate Before Re-Deploying**
>
> | Gate | Requirement | Status |
> |------|-------------|--------|
> | Data Quality | Null rate < 1% | Check |
> | Offline AUC | Must exceed 0.86 | Check |
> | Latency P99 | < 50ms | Check |
> | Shadow Mode | 48h comparison | Check |

---

## Scenario 9.2: Fraud Detection ML Pipeline Design

**User:** "Design an ML pipeline for a fraud detection model that needs <100ms latency at 10K QPS."

**ML Engineer:**
> **System Architecture:**
> ```
> Transaction Event → [Kafka] → [Flink] → [Redis]
>                               ↓
>                        [Spark] → [Feast] → materialize
>
> Serving Path (budget = 100ms):
>   ├── Feature fetch: < 5ms
>   ├── Pre-processing: < 5ms
>   ├── Triton Inference: < 15ms
>   └── Post-processing: < 5ms
>   Total: ~40ms ✓
> ```
>
> **Feature Engineering (Flink):**
> ```python
> class VelocityAggregator(KeyedProcessFunction):
>     def process_element(self, txn, ctx):
>         state = self.velocity_state.value() or {"count": 0}
>         state["count"] += 1
>         self.velocity_state.update(state)
>         yield {"user_id": txn.user_id, "velocity_60s_count": state["count"]}
> ```
>
> **Model Training (Optuna + XGBoost):**
> ```python
> import mlflow, optuna, xgboost as xgb
>
> def objective(trial):
>     params = {
>         "max_depth": trial.suggest_int("max_depth", 4, 10),
>         "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
>         "scale_pos_weight": trial.suggest_float("scale_pos_weight", 50, 200),
>         "tree_method": "hist",
>         "device": "cuda",
>     }
>     with mlflow.start_run(nested=True):
>         model = xgb.XGBClassifier(**params)
>         model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=50)
>         score = average_precision_score(y_val, model.predict_proba(X_val)[:, 1])
>         mlflow.log_metric("auc_pr", score)
>     return score
>
> study = optuna.create_study(direction="maximize")
> study.optimize(objective, n_trials=100)
> ```
>
> **Triton Deployment:**
> ```bash
> # Export to ONNX, then TensorRT INT8
> trtexec --onnx=fraud_model.onnx --saveEngine=fraud_model.trt --int8
>
> # config.pbtxt
> dynamic_batching {
>   preferred_batch_size: [32, 64, 128]
>   max_queue_delay_microseconds: 5000
> }
> instance_group [{ count: 4, kind: KIND_GPU }]
> ```
>
> **HPA for 10K QPS:**
> ```yaml
> apiVersion: autoscaling/v2
> kind: HorizontalPodAutoscaler
> spec:
>   minReplicas: 3
>   maxReplicas: 20
>   metrics:
>   - type: External
>     external:
>       metric:
>         name: triton_queue_compute_infer_duration_p99
>       target:
>         type: AverageValue
>         averageValue: "30m"
> ```

---

## Scenario 9.3: Feature Store Design for Multi-Team Use

**User:** "How do I set up a feature store for our e-commerce ML team with 20 models sharing features?"

**ML Engineer:**
> **Feast Architecture:**
> ```
> feast/
> ├── entities/ (user, item, session)
> ├── feature_views/
> │   ├── user_domain/ (demographics, behavior_7d, behavior_30d)
> │   ├── item_domain/ (catalog, popularity)
> │   └── interaction_domain/ (affinity)
> └── feature_services/ (ranking, reco, fraud)
> ```
>
> **Feast Configuration:**
> ```python
> # feature_store.yaml
> project: ecommerce_ml
> online_store:
>   type: redis
>   connection_string: "redis://redis-cluster:6379"
> offline_store:
>   type: bigquery
>
> # FeatureView
> user_behavior_7d = FeatureView(
>     name="user_behavior_7d",
>     entities=[user],
>     ttl=timedelta(days=7),
>     schema=[
>         Field(name="click_count_7d", dtype=Int64),
>         Field(name="purchase_count_7d", dtype=Int64),
>     ],
>     source=BigQuerySource(
>         table="ecommerce.user_behavior_7d_features",
>         timestamp_field="feature_timestamp",
>     ),
> )
> ```
>
> **Point-in-Time Join Validation:**
> ```python
> # CRITICAL: Use Feast API, not raw SQL
> entity_df = pd.DataFrame({
>     "user_id": training_labels["user_id"],
>     "event_timestamp": training_labels["label_timestamp"],
> })
> training_features = store.get_historical_features(
>     entity_df=entity_df,
>     features=["user_behavior_7d:click_count_7d"],
> ).to_df()
>
> # Validation
> assert (training_features["user_behavior_7d__feature_timestamp"]
>         <= training_features["event_timestamp"]).all()
> ```
>
> **Load Test:**
> ```python
> def fetch_features(user_ids):
>     return store.get_online_features(
>         features=["user_behavior_7d:click_count_7d"],
>         entity_rows=[{"user_id": uid} for uid in user_ids],
>     ).to_dict()
>
> # Target: P99 < 20ms at 5K QPS
> ```

---

## Anti-Patterns (from §10)

### Anti-Pattern 1: Duplicating Feature Logic

```markdown
BAD: Training uses pandas; Serving uses SQL
Result: Off-by-one differences → silent model degradation

GOOD: Single shared library
def compute_user_age_days(signup_date, reference_date):
    return (reference_date.date() - signup_date.date()).days
```

### Anti-Pattern 2: Random Split on Time-Series

```markdown
BAD: sklearn train_test_split(X, y, random_state=42)
Result: Future data leaks into training → AUC 0.92 offline, 0.78 production

GOOD: Time-based split
cutoff = df["event_date"].quantile(0.8)
train = df[df["event_date"] < cutoff]
test  = df[df["event_date"] >= cutoff]
```

### Anti-Pattern 3: No Shadow Mode Before Full Rollout

```markdown
BAD: Direct 100% traffic switch
GOOD: Shadow → Canary 5% → Canary 20% → Full
```

### Anti-Pattern 4: Alerting on Model Metrics Instead of Data Metrics

```markdown
BAD: Alert on "AUC drops below 0.80" (lagging)
GOOD: Alert on PSI > 0.2 on features (24-48h before AUC drops)
```

### Anti-Pattern 5: No Experiment Tracking

```markdown
BAD: Run Optuna, lose best params
GOOD: Every trial is nested MLflow run
with mlflow.start_run(run_name="optuna_sweep"):
    study.optimize(objective, n_trials=100)
    mlflow.log_params(study.best_params)
```
