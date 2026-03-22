# Databricks Standards & Reference

## 7.1 Official Documentation

- [Databricks Documentation](https://docs.databricks.com/)
- [Delta Lake Documentation](https://docs.delta.io/)
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Unity Catalog Guide](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)
- [Mosaic AI Documentation](https://docs.databricks.com/en/machine-learning/index.html)
- [DBRX Model Documentation](https://www.databricks.com/blog/introducing-dbrx-new-state-art-art-open-llm)

---

## 7.2 Delta Lake Best Practices

### File Size Optimization
```sql
-- Target 128MB-1GB per file
OPTIMIZE table_name ZORDER BY (column1, column2);

-- Set auto-optimization
ALTER TABLE table_name SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);

-- Liquid Clustering (alternative to Z-order)
ALTER TABLE table_name CLUSTER BY (date_column, region);

-- Predictive Optimization (auto-OPTIMIZE/VACUUM)
ALTER TABLE table_name SET TBLPROPERTIES (
    'delta.enablePredictiveOptimization' = 'true'
);
```

### Time Travel Queries
```sql
-- Query as of version
SELECT * FROM table_name VERSION AS OF 10;

-- Query as of timestamp
SELECT * FROM table_name TIMESTAMP AS OF '2025-01-01';

-- Restore table to version
RESTORE TABLE table_name TO VERSION AS OF 10;

-- History and version information
DESCRIBE HISTORY table_name;
```

### Constraints and Validation
```sql
-- Add check constraint
ALTER TABLE table_name ADD CONSTRAINT valid_price CHECK (price > 0);

-- Add NOT NULL constraint
ALTER TABLE table_name ALTER COLUMN id SET NOT NULL;

-- View constraints
DESCRIBE EXTENDED table_name;

-- Drop constraint
ALTER TABLE table_name DROP CONSTRAINT valid_price;
```

---

## 7.3 Spark Configurations for Databricks

### Performance Tuning
```python
# Adaptive Query Execution
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

# Shuffle optimization
spark.conf.set("spark.sql.shuffle.partitions", "400")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")

# Broadcast joins
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "100MB")

# Off-heap memory (for large shuffles)
spark.conf.set("spark.memory.offHeap.enabled", "true")
spark.conf.set("spark.memory.offHeap.size", "20g")

# Predictive I/O for storage
spark.conf.set("spark.databricks.delta.predictiveIO.enabled", "true")
```

### Photon Engine
```python
# Photon is enabled by default on DBR 9.1+
# Verify Photon usage in Spark UI SQL tab (look for "Photon" indicator)

# Disable if needed (not recommended)
spark.conf.set("spark.databricks.photon.enabled", "false")

# Check Photon execution
spark.conf.get("spark.databricks.photon.enabled")
```

---

## 7.4 Unity Catalog SQL Reference

### Catalog Management
```sql
-- Create catalog
CREATE CATALOG IF NOT EXISTS production;

-- Set default catalog
USE CATALOG production;

-- Show all catalogs
SHOW CATALOGS;

-- Describe catalog
DESCRIBE CATALOG EXTENDED production;

-- Drop catalog (cascade)
DROP CATALOG IF EXISTS development CASCADE;
```

### Schema and Table Management
```sql
-- Create schema
CREATE SCHEMA IF NOT EXISTS production.sales
COMMENT 'Sales data schema'
WITH DBPROPERTIES ('team' = 'revenue');

-- Create managed table
CREATE TABLE production.sales.transactions (
    id STRING,
    amount DECIMAL(18,2),
    created_at TIMESTAMP
) USING DELTA;

-- Create external table
CREATE TABLE production.sales.external_data
USING DELTA
LOCATION 's3://bucket/path/';

-- Managed tables with Unity Catalog
CREATE TABLE production.sales.managed (
    id STRING,
    data STRING
) USING DELTA;
```

### Access Control
```sql
-- Grant privileges
GRANT SELECT ON TABLE production.sales.transactions TO DATA_ANALYSTS;
GRANT ALL PRIVILEGES ON SCHEMA production.sales TO DATA_ENGINEERS;

-- Row-level security
CREATE FUNCTION production.sales.region_filter()
RETURN BOOLEAN
RETURN CASE 
    WHEN current_user() IN ('admin@company.com') THEN TRUE
    ELSE region = current_region()
END;

ALTER TABLE production.sales.transactions 
SET ROW FILTER production.sales.region_filter ON (region);

-- Column-level masking
CREATE FUNCTION production.sales.mask_email(email STRING)
RETURN STRING
RETURN CASE 
    WHEN is_member('data_engineers') THEN email
    ELSE regexp_replace(email, '.*@', '***@')
END;

ALTER TABLE production.sales.customers 
ALTER COLUMN email SET MASK production.sales.mask_email;
```

### AI Asset Management (Unity Catalog)
```sql
-- Register MLflow models in Unity Catalog
CREATE MODEL production.ml.fraud_detection
FROM mlflow: '/Users/data-scientist/fraud-detection/experiment/run-id/model'

-- Grant access to models
GRANT EXECUTE ON MODEL production.ml.fraud_detection TO ml_service_account;

-- View model lineage
SELECT * FROM lineagemodels
WHERE model_name = 'fraud_detection';
```

---

## 7.5 MLflow on Databricks

### Experiment Tracking
```python
import mlflow

# Set experiment
mlflow.set_experiment("/Shared/experiments/fraud-detection")

# Start run with context manager
with mlflow.start_run(run_name="xgboost_model") as run:
    # Log parameters
    mlflow.log_params({
        "max_depth": 6,
        "learning_rate": 0.1,
        "n_estimators": 100
    })
    
    # Log metrics
    mlflow.log_metrics({
        "accuracy": 0.95,
        "precision": 0.92,
        "recall": 0.89
    })
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
    
    # Log tags
    mlflow.set_tags({"version": "v1.0", "environment": "production"})
```

### Model Registry
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_uri = f"runs:/{run.info.run_id}/model"
model_details = mlflow.register_model(model_uri, "FraudDetectionModel")

# Transition stages
client.transition_model_version_stage(
    name="FraudDetectionModel",
    version=model_details.version,
    stage="Staging"
)

# Add model description
client.update_model_version(
    name="FraudDetectionModel",
    version=model_details.version,
    description="XGBoost model for fraud detection with 95% accuracy"
)

# Add model aliases
client.set_registered_model_alias(
    name="FraudDetectionModel",
    alias="champion",
    version=model_details.version
)
```

---

## 7.6 Mosaic AI Vector Search

### Create Vector Search Endpoint
```python
from databricks.vector_search.client import VectorSearchClient

client = VectorSearchClient()

# Create endpoint
client.create_endpoint(
    name="knowledge_base_endpoint",
    endpoint_type="STANDARD"  # or "STORAGE_OPTIMIZED"
)

# List endpoints
client.list_endpoints()
```

### Create Delta Sync Index
```python
# Create managed index with auto-sync
client.create_delta_sync_index(
    endpoint_name="knowledge_base_endpoint",
    index_name="product_index",
    source_table_name="catalog.schema.products",
    primary_key="id",
    embedding_source_column="description",
    embedding_model_endpoint_name="databricks-gte-large-en"
)

# Create direct access index (pre-computed embeddings)
client.create_direct_access_index(
    endpoint_name="knowledge_base_endpoint",
    index_name="custom_embedding_index",
    primary_key="id",
    embedding_dimension=1024,
    embedding_vector_column="embedding"
)
```

### Query Vector Search
```python
# Similarity search
results = client.similarity_search(
    index_name="product_index",
    query_text="wireless headphones with noise cancellation",
    num_results=10,
    filters={"category": "electronics"}
)

# Hybrid search (keyword + semantic)
results = client.similarity_search(
    index_name="product_index",
    query_text="wireless headphones",
    query_type="HYBRID",  # Enable hybrid search
    num_results=10
)

# Access results
for result in results["result"]["data_array"]:
    print(f"ID: {result[0]}, Score: {result[1]}, Text: {result[2]}")
```

---

## 7.7 Mosaic AI Model Serving

### Deploy Model Endpoint
```python
from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")

# Deploy custom model
client.create_endpoint(
    name="fraud-detection",
    config={
        "served_entities": [{
            "entity_name": "FraudDetectionModel",
            "entity_version": "1",
            "workload_size": "Small",
            "scale_to_zero_enabled": True
        }],
        "auto_capture_config": {
            "catalog_name": "production",
            "schema_name": "ml",
            "table_name": "fraud_requests"
        }
    }
)
```

### Query Endpoint
```python
import requests
import json

def query_endpoint(endpoint_name, inputs):
    """Query a model serving endpoint"""
    response = requests.post(
        f"{workspace_url}/serving-endpoints/{endpoint_name}/invocations",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={"inputs": inputs}
    )
    return response.json()

# Example usage
result = query_endpoint("fraud-detection", [[1.0, 2.0, 3.0]])
```

### DBRX Foundation Model API
```python
# Use DBRX via Foundation Model APIs
from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")

# Chat completion with DBRX
response = client.predict(
    endpoint="databricks-dbrx-instruct",
    inputs={
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain the Lakehouse architecture."}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
)

print(response["choices"][0]["message"]["content"])
```

---

## 7.8 Cost Optimization Queries

### Monitor Usage
```sql
-- Check billable usage
SELECT 
    usage_date,
    sku_name,
    SUM(usage_quantity) as dbu_consumed,
    SUM(usage_quantity * list_price) as estimated_cost
FROM system.billing.usage
WHERE usage_date >= current_date() - 30
GROUP BY 1, 2
ORDER BY 1 DESC;

-- Top expensive queries
SELECT 
    query_id,
    user_name,
    execution_time_ms / 1000 as execution_time_sec,
    total_task_time_ms / 1000 as total_task_time_sec,
    read_bytes / 1024 / 1024 / 1024 as read_gb
FROM system.query.history
WHERE start_time >= current_date() - 7
ORDER BY total_task_time_ms DESC
LIMIT 20;
```

### Cluster Efficiency
```sql
-- Cluster utilization
SELECT 
    cluster_id,
    cluster_name,
    AVG(executor_cores * num_executors) as avg_cores,
    AVG(memory_bytes / 1024 / 1024 / 1024) as avg_memory_gb
FROM system.compute.cluster_events
WHERE event_time >= current_date() - 7
GROUP BY 1, 2;

-- Identify idle clusters
SELECT 
    cluster_id,
    cluster_name,
    MAX(event_time) as last_activity
FROM system.compute.cluster_events
WHERE event_time >= current_date() - 7
GROUP BY 1, 2
HAVING last_activity < current_timestamp() - INTERVAL 2 HOURS;
```

---

## 7.9 Lakeflow (Data Engineering Orchestration)

### Job Definition
```python
# Define a Lakeflow job with multiple tasks
{
    "name": "daily_etl_pipeline",
    "tasks": [
        {
            "task_key": "bronze_ingestion",
            "notebook_task": {
                "notebook_path": "/Shared/ETL/bronze_ingestion"
            },
            "new_cluster": {
                "spark_version": "14.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "autoscale": {"min_workers": 1, "max_workers": 5}
            }
        },
        {
            "task_key": "silver_transformation",
            "depends_on": [{"task_key": "bronze_ingestion"}],
            "notebook_task": {
                "notebook_path": "/Shared/ETL/silver_transformation"
            }
        },
        {
            "task_key": "gold_aggregation",
            "depends_on": [{"task_key": "silver_transformation"}],
            "notebook_task": {
                "notebook_path": "/Shared/ETL/gold_aggregation"
            }
        }
    ]
}
```

### Delta Live Tables Pipeline
```python
import dlt

@dlt.table(
    name="bronze_events",
    comment="Raw events from source systems"
)
def bronze_events():
    return (spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/raw/events/")
    )

@dlt.table(
    name="silver_events",
    comment="Cleaned and validated events"
)
@dlt.expect_all({
    "valid_id": "event_id IS NOT NULL",
    "valid_timestamp": "timestamp IS NOT NULL"
})
def silver_events():
    return dlt.read("bronze_events").dropDuplicates(["event_id"])
```

---

## 7.10 System Tables Reference

### Query History Analysis
```sql
-- Slow queries identification
SELECT 
    user_name,
    query_text,
    execution_time_ms / 1000 as duration_sec,
    total_task_time_ms / 1000 as task_time_sec,
    read_rows,
    written_rows
FROM system.query.history
WHERE execution_time_ms > 60000  -- Queries > 1 minute
  AND start_time >= current_date() - 7
ORDER BY execution_time_ms DESC
LIMIT 20;
```

### Audit Logging
```sql
-- Access audit trail
SELECT 
    event_time,
    user_name,
    action_name,
    resource_type,
    resource_name,
    request_params
FROM system.access.audit
WHERE event_date >= current_date() - 7
  AND action_name IN ('createTable', 'deleteTable', 'generateTemporaryCredentials')
ORDER BY event_time DESC;
```

### Lineage Tracking
```sql
-- Data lineage query
SELECT 
    source_table_name,
    target_table_name,
    operation_type,
    operation_time
FROM system.lineage.table_lineage
WHERE target_table_name = 'production.sales.transactions'
ORDER BY operation_time DESC;
```
