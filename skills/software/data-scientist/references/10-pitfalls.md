# Common Data Science Anti-Patterns

## Anti-Pattern 1: The Accuracy Trap

```
❌ BAD: "Our fraud model has 99.2% accuracy!" — but 99.1% of transactions are legitimate.
The model predicts every transaction as NOT fraud and gets 99.1% accuracy automatically.
Zero fraud detected. Zero business value. 3 months of engineering time wasted.

✅ GOOD: For fraud detection (imbalanced classes), report:
  - PR-AUC (precision-recall area under curve)
  - Precision@K: of the top-K flagged transactions, what % are actually fraud?
  - Recall@threshold: what % of actual fraud do we catch at our chosen operating point?
  - Expected dollar loss prevented at operating threshold

Rule: if your positive class is < 20%, never report Accuracy as the primary metric.
```

## Anti-Pattern 2: Target Leakage

```
❌ BAD: Predicting churn using the feature "support_tickets_about_cancellation" — this
feature is CREATED by the user in the process of churning. Training AUC = 0.97.
Production AUC = 0.54. 4 months of model work invalidated overnight.

✅ GOOD: Audit every feature's creation timestamp relative to the label event.
Features must be computable BEFORE the label window begins.
Enforce this with a temporal split: train on users labeled before date T,
validate on users labeled T to T+30, never overlap.

Detection test: if removing one feature drops AUC by >20%, investigate for leakage immediately.
```

## Anti-Pattern 3: Metric Misalignment

```
❌ BAD: Optimizing AUC-ROC for a product recommendation model when the business
cares about "did the user click one of our top-10 recommendations?" (Hit Rate@10).
AUC optimizes ranking across ALL items; Hit Rate@10 only cares about the top 10.
Model with AUC 0.87 can have worse business outcome than model with AUC 0.82.

✅ GOOD: Ask "what action will the model output drive?" before choosing the metric.
  - Top-K recommendations → NDCG@K, Hit Rate@K, Precision@K
  - Risk scoring for all users → AUC-ROC, PR-AUC
  - Revenue optimization → Expected revenue = sum(P(purchase) × avg_order_value)
  - Binary trigger (send email or not) → Precision at chosen recall target
```

## Anti-Pattern 4: The A/B Test Peeking Problem

```
❌ BAD: Running an A/B test and checking results every day. When p < 0.05 first appears
on Day 4, stopping the test and declaring the treatment a winner. The test was powered
for Day 14. Stopping early inflates false positive rate from 5% to 26%. Wrong winner
shipped to 100% of users. Net negative business impact.

✅ GOOD: Pre-register the test: sample size, runtime, alpha, power, primary metric.
Only analyze after reaching pre-specified sample size.
If early stopping is required for business reasons, use sequential testing methods:
  - mSPRT (mixture Sequential Probability Ratio Test) — valid at any sample size
  - Bayesian testing with pre-specified stopping rules
  - Alpha spending functions (O'Brien-Fleming)
```

## Anti-Pattern 5: Model in a Notebook

```
❌ BAD: After 6 weeks, a data scientist has a great churn model in a Jupyter notebook
with AUC 0.88. No versioning, no pipeline, no serving code, no monitoring. The model
never reaches production because "we'll productionize it later." Later never comes.
Notebook is deleted when laptop is replaced.

✅ GOOD: MLOps from day one, even for prototypes:
  - MLflow experiment tracking from the first training run
  - sklearn Pipeline (not loose preprocessing scripts)
  - Model registered in MLflow Model Registry with version tags
  - Great Expectations data validation before each training run
  - FastAPI serving wrapper written in week 2, not after model is "done"
  - Airflow DAG for scheduled retraining with performance gate
```
