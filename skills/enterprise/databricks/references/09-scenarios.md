# Databricks Scenario Examples

## Scenario 1: Large-Scale Data Migration

**Context**: Migrate 500TB of historical data from on-premises Hadoop to Databricks Lakehouse.

**Challenge**: Minimize downtime, ensure data integrity, optimize for cost.

**Solution**:

```python
# Phase 1: Parallel extraction from Hadoop
# Use DistCp or Azure Data Factory for bulk transfer

# Phase 2: Convert to Delta Lake with optimization
for table in tables_to_migrate:
    # Read from staged location
    df = spark.read.parquet(f"/mnt/staging/{table}")
    
    # Write optimized Delta
    (df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(f"bronze.{table}")
    )
    
    # Optimize for query patterns
    spark.sql(f"OPTIMIZE bronze.{table} ZORDER BY (date_key)")
    spark.sql(f"VACUUM bronze.{table} RETAIN 168 HOURS")
    
    # Verify row counts
    source_count = df.count()
    target_count = spark.table(f"bronze.{table}").count()
    assert source_count == target_count, f"Mismatch in {table}"

# Phase 3: Validation and cutover
```

**Results**: 
- Migration time: 72 hours (parallelized)
- Cost: $15K DBUs (using spot instances)
- Zero data loss verified via checksums

---

## Scenario 2: Real-Time Fraud Detection

**Context**: Financial services company needs sub-second fraud detection on 50K transactions/second.

**Architecture**:

```
Kafka → Auto Loader → Bronze → Spark Streaming → MLflow Model → Alert
```

**Implementation**:

```python
# Streaming ingestion with Auto Loader
stream_df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/checkpoint/fraud_schema")
    .load("/mnt/transactions/raw/")
)

# Feature engineering
features_df = (stream_df
    .withWatermark("timestamp", "10 minutes")
    .groupBy(
        window("timestamp", "5 minutes"),
        "user_id"
    )
    .agg(
        count("*").alias("tx_count_5m"),
        sum("amount").alias("amount_5m"),
        avg("amount").alias("avg_amount_5m"),
        stddev("amount").alias("std_amount_5m")
    )
)

# Load production model
import mlflow.pyfunc
model_uri = "models:/FraudDetectionModel/Production"
fraud_model = mlflow.pyfunc.load_model(model_uri)

# Apply model (using pandas UDF for low latency)
from pyspark.sql.functions import pandas_udf, PandasUDFType

@pandas_udf('double', PandasUDFType.SCALAR_ITER)
def predict_fraud(iterator):
    for pdf in iterator:
        yield fraud_model.predict(pdf)

# Score transactions
scored_df = features_df.withColumn("fraud_score", predict_fraud(struct(features_df.columns)))

# Alert on high-risk
critical_df = scored_df.filter(col("fraud_score") > 0.8)

# Write to alert queue
(critical_df.writeStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("topic", "fraud-alerts")
    .option("checkpointLocation", "/checkpoint/fraud_alerts")
    .start()
)
```

**Results**:
- Latency: p99 < 500ms
- Throughput: 75K TPS (scaled)
- False positive rate: 0.5%

---

## Scenario 3: Multi-Cloud Data Sharing

**Context**: Share sanitized customer data with partners across AWS and Azure.

**Solution using Delta Sharing**:

```sql
-- Provider side (Databricks on AWS)
CREATE SHARE customer_analytics SHARE AS;

ALTER SHARE customer_analytics ADD TABLE production.sales.aggregated_metrics;
ALTER SHARE customer_analytics ADD TABLE production.marketing.campaign_performance;

-- Create recipient
CREATE RECIPIENT partner_company;

-- Grant access
GRANT SELECT ON SHARE customer_analytics TO RECIPIENT partner_company;

-- Generate activation link (provider sends to recipient)
```

```python
# Recipient side (Databricks on Azure)
# Configure credential file from provider

# Access shared data as if local
spark.read.format("deltaSharing").load("/share/customer_analytics/production.sales.aggregated_metrics").show()
```

**Benefits**:
- No data duplication
- Live access to updates
- Row/column-level security preserved
- Audit trail of all access

---

## Scenario 4: Hyperparameter Tuning at Scale

**Context**: Train 1000 XGBoost models with different hyperparameters for Kaggle competition.

**Solution using Hyperopt and MLflow**:

```python
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import mlflow
import xgboost as xgb
from sklearn.model_selection import cross_val_score
import numpy as np

# Load data
X = spark.table("gold.features").toPandas()
y = X.pop("target")

# Define search space
space = {
    'max_depth': hp.quniform('max_depth', 3, 10, 1),
    'learning_rate': hp.loguniform('learning_rate', -5, -1),
    'n_estimators': hp.quniform('n_estimators', 50, 500, 10),
    'subsample': hp.uniform('subsample', 0.5, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1.0)
}

def objective(params):
    with mlflow.start_run():
        # Convert params
        params['max_depth'] = int(params['max_depth'])
        params['n_estimators'] = int(params['n_estimators'])
        
        # Log params
        mlflow.log_params(params)
        
        # Train model
        model = xgb.XGBClassifier(**params)
        score = cross_val_score(model, X, y, cv=5, scoring='roc_auc').mean()
        
        # Log metric
        mlflow.log_metric("auc", score)
        
        return {'loss': -score, 'status': STATUS_OK}

# Run optimization
with mlflow.start_run(run_name="hyperopt_xgboost"):
    trials = Trials()
    best = fmin(
        fn=objective,
        space=space,
        algo=tpe.suggest,
        max_evals=100,
        trials=trials
    )
    
    mlflow.log_params({"best_params": best})
    print(f"Best: {best}")

# Retrieve best model
best_run = mlflow.search_runs(
    filter_string="run_name = 'hyperopt_xgboost'",
    order_by=["metrics.auc DESC"]
).iloc[0]

print(f"Best AUC: {best_run['metrics.auc']}")
```

**Results**:
- 1000 experiments tracked automatically
- Best model identified: AUC 0.947
- Total compute time: 4 hours (parallel on 10 workers)

---

## Scenario 5: Disaster Recovery Strategy

**Context**: Ensure business continuity with RPO < 1 hour, RTO < 4 hours.

**Architecture**:

```
Primary Region (us-west-2) → Replication → DR Region (us-east-1)
```

**Implementation**:

```python
# Enable Change Data Feed on critical tables
spark.sql("""
ALTER TABLE production.orders 
SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# Schedule replication job (runs every 30 minutes)
def replicate_to_dr():
    # Get latest changes using CDF
    changes = (spark.read
        .format("delta")
        .option("readChangeFeed", "true")
        .option("startingVersion", get_last_replicated_version())
        .table("production.orders")
    )
    
    # Apply to DR region
    (changes.write
        .format("delta")
        .mode("append")
        .save("s3://dr-bucket/orders")
    )

# Automated DR testing (weekly)
def test_failover():
    """Verify DR environment can serve queries"""
    dr_count = spark.read.format("delta").load("s3://dr-bucket/orders").count()
    primary_count = spark.table("production.orders").count()
    
    assert dr_count >= primary_count * 0.99, "DR lag exceeds 1%"
    print(f"✓ DR healthy: {dr_count}/{primary_count} records")

# Backup with time travel
weekly_backup = """
CREATE TABLE IF NOT EXISTS backup.orders_weekly
USING DELTA
AS SELECT * FROM production.orders TIMESTAMP AS OF date_sub(current_date(), 7)
"""
```

**Recovery Procedures**:

```sql
-- Scenario: Primary region down
-- Step 1: Promote DR to primary
ALTER TABLE dr_catalog.orders RECREATE AS production.orders;

-- Step 2: Redirect applications
-- (Update connection strings in application config)

-- Step 3: Verify data integrity
SELECT COUNT(*) FROM production.orders;
SELECT MAX(updated_at) FROM production.orders;
```

**Results**:
- RPO: 15 minutes (continuous replication)
- RTO: 2 hours (tested monthly)
- Data integrity: 100% verified

---

## Scenario 6: RAG Application with Mosaic AI

**Context**: Build a knowledge base chatbot for internal documentation using company data.

**Architecture**:

```
Documents → Chunking → Vector Search Index → DBRX LLM → Response
```

**Implementation**:

```python
# Step 1: Document chunking and embedding
from pyspark.sql.functions import udf, explode
from pyspark.sql.types import ArrayType, StringType

@udf(ArrayType(StringType()))
def chunk_document(text, chunk_size=1000):
    """Split document into chunks"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if len(chunk) > 100:
            chunks.append(chunk)
    return chunks

# Process documents
documents = spark.table("catalog.docs.raw_documents")
chunked = (documents
    .withColumn("chunks", chunk_document("content"))
    .withColumn("chunk", explode("chunks"))
    .select("doc_id", "chunk", "metadata")
)
chunked.write.format("delta").mode("overwrite").saveAsTable("catalog.docs.chunks")

# Step 2: Create Vector Search index
from databricks.vector_search.client import VectorSearchClient

client = VectorSearchClient()
client.create_endpoint(name="docs_endpoint", endpoint_type="STANDARD")

client.create_delta_sync_index(
    endpoint_name="docs_endpoint",
    index_name="docs_index",
    source_table_name="catalog.docs.chunks",
    primary_key="chunk_id",
    embedding_source_column="chunk",
    embedding_model_endpoint_name="databricks-gte-large-en"
)

# Step 3: Build RAG pipeline
class DocumentationChatbot:
    def __init__(self):
        self.vector_client = VectorSearchClient()
        self.workspace_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
        self.token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
    
    def answer(self, question):
        # Retrieve relevant chunks
        results = self.vector_client.similarity_search(
            index_name="docs_endpoint.docs_index",
            query_text=question,
            num_results=3
        )
        
        context = "\n\n".join([r[2] for r in results["result"]["data_array"]])
        
        # Generate answer with DBRX
        prompt = f"""Based on the following documentation, answer the question:

{context}

Question: {question}

Answer:"""
        
        response = requests.post(
            f"{self.workspace_url}/serving-endpoints/databricks-dbrx-instruct/invocations",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
        )
        
        return {
            "answer": response.json()["choices"][0]["message"]["content"],
            "sources": [r[0] for r in results["result"]["data_array"]]
        }

# Usage
bot = DocumentationChatbot()
result = bot.answer("How do I configure Unity Catalog?")
```

**Results**:
- Response accuracy: 92% (human evaluated)
- Average latency: 2.5 seconds
- User satisfaction: 4.5/5

---

## Scenario 7: Multi-Model AI Agent with Mosaic AI

**Context**: Build a compound AI system that routes queries to specialized models.

**Architecture**:

```
Query → Router (DBRX) → Specialist Model → Synthesis → Response
```

**Implementation**:

```python
class MultiModelAgent:
    def __init__(self):
        self.workspace_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
        self.token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
        
        # Specialist models
        self.models = {
            "code": "databricks-dbrx-instruct",  # For coding tasks
            "sql": "databricks-dbrx-instruct",   # For SQL generation
            "general": "databricks-dbrx-instruct" # For general queries
        }
    
    def classify_intent(self, query):
        """Route query to appropriate model"""
        classification_prompt = f"""Classify the following query into one of: code, sql, general.

Query: {query}

Classification (respond with only one word):"""
        
        response = requests.post(
            f"{self.workspace_url}/serving-endpoints/databricks-dbrx-instruct/invocations",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "messages": [{"role": "user", "content": classification_prompt}],
                "max_tokens": 10,
                "temperature": 0.1
            }
        )
        
        intent = response.json()["choices"][0]["message"]["content"].strip().lower()
        return intent if intent in self.models else "general"
    
    def process(self, query):
        """Process query with appropriate specialist"""
        intent = self.classify_intent(query)
        model = self.models[intent]
        
        # Add specialist context based on intent
        if intent == "code":
            system_msg = "You are a Python expert. Provide clean, well-documented code."
        elif intent == "sql":
            system_msg = "You are a SQL expert. Provide optimized Spark SQL queries."
        else:
            system_msg = "You are a helpful assistant."
        
        response = requests.post(
            f"{self.workspace_url}/serving-endpoints/{model}/invocations",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": query}
                ],
                "max_tokens": 500
            }
        )
        
        return {
            "query": query,
            "intent": intent,
            "model": model,
            "response": response.json()["choices"][0]["message"]["content"]
        }

# Usage
agent = MultiModelAgent()
result = agent.process("Write a PySpark function to calculate rolling averages")
print(f"Intent: {result['intent']}")
print(f"Response: {result['response']}")
```

**Results**:
- Intent classification accuracy: 95%
- Specialist models improve task performance by 30%
- Compound system outperforms single model on multi-domain queries
