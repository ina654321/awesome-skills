# Databricks Standard Workflows

## 8.1 Medallion Architecture Implementation

### Bronze Layer (Raw Ingestion)

```python
# Auto Loader for cloud file ingestion
bronze_df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/checkpoint/bronze_schema")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaEvolutionMode", "rescue")
    .load("/mnt/raw/events/")
    .withColumn("_ingestion_timestamp", current_timestamp())
    .withColumn("_source_filename", input_file_name())
)

# Write to Bronze Delta table
(bronze_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/checkpoint/bronze_events")
    .trigger(availableNow=True)
    .table("bronze.events")
)
```

### Silver Layer (Cleaned & Validated)

```python
from pyspark.sql.functions import *
from delta.tables import DeltaTable

# Read Bronze
bronze_df = spark.readStream.table("bronze.events")

# Clean and validate
silver_df = (bronze_df
    .filter(col("user_id").isNotNull())  # Remove invalid records
    .withColumn("event_date", to_date(col("timestamp")))
    .withColumn("cleaned_json", from_json(col("payload"), schema))
    .dropDuplicates(["event_id"])  # Deduplication
    .select(
        "event_id",
        "user_id",
        "event_type",
        "event_date",
        "timestamp",
        "cleaned_json.*",
        "_ingestion_timestamp"
    )
)

# Merge to Silver (CDC pattern)
def upsert_to_silver(microBatchDF, batchId):
    microBatchDF.createOrReplaceTempView("silver_updates")
    
    microBatchDF._jdf.sparkSession().sql("""
        MERGE INTO silver.events t
        USING silver_updates s
        ON t.event_id = s.event_id
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)

(silver_df.writeStream
    .foreachBatch(upsert_to_silver)
    .option("checkpointLocation", "/checkpoint/silver_events")
    .trigger(availableNow=True)
    .start()
)
```

### Gold Layer (Business Aggregates)

```python
# Daily user activity summary
daily_summary = (spark.table("silver.events")
    .groupBy(
        col("user_id"),
        col("event_date")
    )
    .agg(
        count("*").alias("event_count"),
        countDistinct("event_type").alias("unique_event_types"),
        sum(when(col("event_type") == "purchase", 1).otherwise(0)).alias("purchases"),
        max("timestamp").alias("last_activity")
    )
)

# Write to Gold with OPTIMIZE
(daily_summary.write
    .format("delta")
    .mode("overwrite")
    .partitionBy("event_date")
    .saveAsTable("gold.daily_user_activity")
)

# Z-order for query performance
spark.sql("OPTIMIZE gold.daily_user_activity ZORDER BY (user_id)")
```

---

## 8.2 Delta Live Tables Pipeline

```python
import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Bronze layer with DLT
@dlt.table(
    name="bronze_orders",
    comment="Raw orders from source systems"
)
@dlt.expect("valid_order_id", "order_id IS NOT NULL")
def bronze_orders():
    return (spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/raw/orders/")
        .withColumn("_ingestion_time", current_timestamp())
    )

# Silver layer with quality expectations
@dlt.table(
    name="silver_orders",
    comment="Cleaned and validated orders"
)
@dlt.expect_all({
    "valid_amount": "amount > 0",
    "valid_customer": "customer_id IS NOT NULL",
    "valid_status": "status IN ('pending', 'completed', 'cancelled')"
})
def silver_orders():
    return (dlt.read("bronze_orders")
        .filter(col("_ingestion_time") > current_date() - 30)
        .dropDuplicates(["order_id"])
        .select(
            "order_id",
            "customer_id",
            "amount",
            "status",
            "created_at",
            "_ingestion_time"
        )
    )

# Gold layer aggregation
@dlt.table(
    name="gold_daily_revenue",
    comment="Daily revenue summary"
)
def gold_daily_revenue():
    return (dlt.read("silver_orders")
        .groupBy(
            date_trunc("day", "created_at").alias("date")
        )
        .agg(
            sum("amount").alias("total_revenue"),
            count("*").alias("order_count"),
            countDistinct("customer_id").alias("unique_customers")
        )
    )
```

---

## 8.3 MLflow Model Development Workflow

```python
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd

# Load feature data
features_df = spark.table("gold.customer_features").toPandas()
X = features_df.drop("churned", axis=1)
y = features_df["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Set experiment
mlflow.set_experiment("/Shared/churn-prediction")

# Start run
with mlflow.start_run(run_name="rf_baseline") as run:
    # Log parameters
    params = {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": 42
    }
    mlflow.log_params(params)
    
    # Train model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "f1_score": f1_score(y_test, predictions)
    }
    mlflow.log_metrics(metrics)
    
    # Log feature importance
    importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    
    importance_df.to_csv("feature_importance.csv", index=False)
    mlflow.log_artifact("feature_importance.csv")
    
    # Log model with signature
    from mlflow.models.signature import infer_signature
    signature = infer_signature(X_train, model.predict(X_train))
    
    mlflow.sklearn.log_model(
        model,
        "model",
        signature=signature,
        input_example=X_train.iloc[:5],
        registered_model_name="ChurnPredictionModel"
    )
    
    print(f"Run ID: {run.info.run_id}")
    print(f"Metrics: {metrics}")
```

---

## 8.4 Unity Catalog Migration Workflow

### Step 1: Discovery
```python
# List all tables in Hive metastore
tables = spark.catalog.listTables("default")
for table in tables:
    print(f"Table: {table.name}, Type: {table.tableType}")

# Analyze table sizes
for table in tables:
    df = spark.table(f"default.{table.name}")
    size_gb = df.count() * len(df.columns) * 100 / 1024**3  # Rough estimate
    print(f"{table.name}: ~{size_gb:.2f} GB")
```

### Step 2: Create Catalog Structure
```sql
-- Create environment catalogs
CREATE CATALOG IF NOT EXISTS production COMMENT 'Production workloads';
CREATE CATALOG IF NOT EXISTS staging COMMENT 'Pre-production testing';
CREATE CATALOG IF NOT EXISTS development COMMENT 'Development and experimentation';

-- Create schemas
CREATE SCHEMA IF NOT EXISTS production.sales;
CREATE SCHEMA IF NOT EXISTS production.marketing;
CREATE SCHEMA IF NOT EXISTS production.operations;
```

### Step 3: Sync External Tables
```sql
-- Create external table pointing to existing Delta files
CREATE TABLE IF NOT EXISTS production.sales.transactions
USING DELTA
LOCATION 's3://company-data-lake/production/sales/transactions/';

-- Verify data
SELECT COUNT(*) FROM production.sales.transactions;
```

### Step 4: Set Up Governance
```sql
-- Create groups (via admin console or API)
-- Apply access controls

GRANT USAGE ON CATALOG production TO GROUP data_analysts;
GRANT SELECT ON SCHEMA production.sales TO GROUP data_analysts;

GRANT ALL PRIVILEGES ON CATALOG production TO GROUP data_engineers;

-- Row-level security for sensitive data
CREATE FUNCTION production.sales.region_access()
RETURN BOOLEAN
RETURN CASE 
    WHEN is_member('global_admins') THEN TRUE
    ELSE region = current_region()
END;

ALTER TABLE production.sales.transactions 
SET ROW FILTER production.sales.region_access ON (region);
```

---

## 8.5 RAG Application Workflow with Mosaic AI

### Step 1: Prepare Data for Vector Search
```python
# Load and chunk documents
documents_df = spark.table("catalog.schema.documents")

# Create chunks for RAG
from pyspark.sql.functions import udf, explode, lit, col
from pyspark.sql.types import ArrayType, StringType

@udf(ArrayType(StringType()))
def chunk_text(text, chunk_size=1000, overlap=100):
    """Split text into overlapping chunks"""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if len(chunk) > 100:  # Filter tiny chunks
            chunks.append(chunk)
    return chunks

chunked_df = (documents_df
    .withColumn("chunks", chunk_text(col("content")))
    .withColumn("chunk", explode("chunks"))
    .select(
        concat(col("doc_id"), lit("_"), col("chunk")).alias("id"),
        col("doc_id"),
        col("chunk").alias("content"),
        col("metadata")
    )
)

# Save chunked data
chunked_df.write.format("delta").mode("overwrite").saveAsTable("catalog.schema.document_chunks")
```

### Step 2: Create Vector Search Index
```python
from databricks.vector_search.client import VectorSearchClient

client = VectorSearchClient()

# Create vector search endpoint
client.create_endpoint(
    name="rag_knowledge_base",
    endpoint_type="STANDARD"
)

# Create delta sync index
client.create_delta_sync_index(
    endpoint_name="rag_knowledge_base",
    index_name="document_chunks_index",
    source_table_name="catalog.schema.document_chunks",
    primary_key="id",
    embedding_source_column="content",
    embedding_model_endpoint_name="databricks-gte-large-en"
)
```

### Step 3: Build RAG Chain
```python
import requests
import json

class RAGPipeline:
    def __init__(self, vector_endpoint, model_endpoint="databricks-dbrx-instruct"):
        self.vector_client = VectorSearchClient()
        self.vector_endpoint = vector_endpoint
        self.model_endpoint = model_endpoint
        self.workspace_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
        self.token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
    
    def retrieve(self, query, k=5):
        """Retrieve relevant documents"""
        results = self.vector_client.similarity_search(
            index_name=f"{self.vector_endpoint}.document_chunks_index",
            query_text=query,
            num_results=k
        )
        
        contexts = []
        for result in results["result"]["data_array"]:
            contexts.append({
                "content": result[2],
                "score": result[1],
                "doc_id": result[0].split("_")[0]
            })
        return contexts
    
    def generate(self, query, contexts):
        """Generate response using DBRX"""
        context_text = "\n\n".join([c["content"] for c in contexts])
        
        prompt = f"""Based on the following context, answer the question. If the answer is not in the context, say "I don't have enough information."

Context:
{context_text}

Question: {query}

Answer:"""
        
        response = requests.post(
            f"{self.workspace_url}/serving-endpoints/{self.model_endpoint}/invocations",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
        )
        
        return response.json()["choices"][0]["message"]["content"]
    
    def query(self, query, k=5):
        """End-to-end RAG query"""
        contexts = self.retrieve(query, k)
        answer = self.generate(query, contexts)
        return {
            "query": query,
            "answer": answer,
            "sources": contexts
        }

# Usage
rag = RAGPipeline("rag_knowledge_base")
result = rag.query("What is the Lakehouse architecture?")
print(result["answer"])
```

---

## 8.6 Cost Monitoring Workflow

```python
# Weekly cost report
weekly_costs = spark.sql("""
SELECT 
    date_trunc('week', usage_date) as week,
    sku_name,
    SUM(usage_quantity) as dbu_consumed,
    SUM(usage_quantity * list_price) as estimated_cost_usd
FROM system.billing.usage
WHERE usage_date >= current_date() - 90
GROUP BY 1, 2
ORDER BY 1 DESC, 4 DESC
""")

weekly_costs.display()

# Alert on anomalous spend
anomalies = spark.sql("""
WITH daily_costs AS (
    SELECT 
        usage_date,
        SUM(usage_quantity * list_price) as daily_cost
    FROM system.billing.usage
    WHERE usage_date >= current_date() - 30
    GROUP BY 1
),
stats AS (
    SELECT 
        AVG(daily_cost) as avg_cost,
        STDDEV(daily_cost) as stddev_cost
    FROM daily_costs
)
SELECT 
    d.*,
    s.avg_cost,
    (d.daily_cost - s.avg_cost) / s.stddev_cost as z_score
FROM daily_costs d
CROSS JOIN stats s
WHERE d.daily_cost > s.avg_cost + 2 * s.stddev_cost
ORDER BY d.usage_date DESC
""")

if anomalies.count() > 0:
    print("⚠️ Anomalous spend detected!")
    anomalies.display()
```

---

## 8.7 DBRX Fine-tuning Workflow

### Prepare Training Data
```python
# Format data for DBRX fine-tuning
from pyspark.sql.functions import to_json, struct, lit

training_data = spark.table("catalog.schema.instruction_data")

# Convert to chat completion format
formatted_data = training_data.select(
    to_json(struct(
        lit("system").alias("role"),
        col("system_prompt").alias("content")
    )).alias("system_message"),
    to_json(struct(
        lit("user").alias("role"),
        col("instruction").alias("content")
    )).alias("user_message"),
    to_json(struct(
        lit("assistant").alias("role"),
        col("response").alias("content")
    )).alias("assistant_message")
)

# Save as JSONL for Mosaic AI training
formatted_data.write.format("json").mode("overwrite").save("/mnt/training/dbrx_finetune")
```

### Launch Fine-tuning Job
```python
# Use Mosaic AI Model Training (MPT) for DBRX fine-tuning
# This requires access to Mosaic AI training infrastructure

from databricks.model_training import create_training_run

run = create_training_run(
    model="databricks-dbrx-instruct",
    training_data="/mnt/training/dbrx_finetune",
    output_model_name="my-finetuned-dbrx",
    hyperparameters={
        "learning_rate": 1e-5,
        "num_epochs": 3,
        "batch_size": 32
    }
)

# Monitor training
print(f"Training run ID: {run.id}")
```

### Deploy Fine-tuned Model
```python
from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")

# Deploy fine-tuned model
client.create_endpoint(
    name="my-finetuned-dbrx-endpoint",
    config={
        "served_entities": [{
            "entity_name": "my-finetuned-dbrx",
            "entity_version": "1",
            "workload_size": "Medium"
        }]
    }
)
```
