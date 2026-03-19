# Scenario Examples

## 9.1 Real-World Use Cases

### Streaming Analytics Pipeline

**User:** "I need to compute real-time user session metrics from Kafka events"

**Expert:**
```sql
-- Step 1: Define sessionized source with watermark
CREATE TABLE user_events (
    user_id STRING,
    event_type STRING,
    url STRING,
    ts TIMESTAMP(3),
    WATERMARK FOR ts AS ts - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'user_clickstream',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'json'
);

-- Step 2: Sessionize with gap detection
INSERT INTO session_metrics
SELECT
    user_id,
    TUMBLE_START(ts, INTERVAL '5' MINUTE) AS session_start,
    TUMBLE_END(ts, INTERVAL '5' MINUTE) AS session_end,
    COUNT(*) AS event_count,
    COUNT(DISTINCT url) AS pages_visited,
    COUNT(DISTINCT event_type) AS distinct_actions
FROM user_events
GROUP BY
    user_id,
    TUMBLE(ts, INTERVAL '5' MINUTE);
```

### CDC → Lakehouse Streaming Pipeline

**User:** "Sync PostgreSQL changes to Iceberg in real-time"

**Expert:**
```sql
-- PostgreSQL CDC source using Debezium format
CREATE TABLE pg_orders (
    id STRING,
    order_id STRING,
    customer_id STRING,
    total_amount DECIMAL(10,2),
    status STRING,
    updated_at TIMESTAMP(3),
    WATERMARK FOR updated_at AS updated_at - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'orders_cdc',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-pg-cdc',
    'format' = 'debezium-json',
    'debezium-json.schema-include' = 'true'
);

-- Step 2: Write to Iceberg
CREATE TABLE iceberg_orders (
    id STRING,
    order_id STRING,
    customer_id STRING,
    total_amount DECIMAL(10,2),
    status STRING,
    updated_at TIMESTAMP,
    PRIMARY KEY (id) NOT ENFORCED
) PARTITIONED BY (days(updated_at));

INSERT INTO iceberg_orders
SELECT id, order_id, customer_id, total_amount, status, updated_at
FROM pg_orders;
```

### Real-time Fraud Detection

**User:** "Detect suspicious transactions within a sliding time window"

**Expert:**
```java
DataStream<Transaction> transactions = env
    .fromSource(KafkaSource..., WatermarkStrategy.forMonotonousTimestamps(), "Kafka")
    .keyBy(Transaction::getAccountId)
    .window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(1)))
    .process(new FraudDetectionFunction());

public class FraudDetectionFunction extends KeyedProcessFunction<String, Transaction, Alert> {
    @Override
    public void processElement(Transaction tx, Context ctx, Collector<Alert> out) {
        // Count transactions in window
        // Check velocity thresholds
        // Emit alert if threshold exceeded
    }
}
```

## 9.2 Scaling Scenarios

### Scaling from 1M → 100M events/day

| Dimension | Initial (1M/day) | Scaled (100M/day) |
|-----------|-----------------|-------------------|
| Parallelism | 2 | 64 |
| TaskSlots per TM | 4 | 8 |
| TaskManagers | 2 | 16 |
| Checkpoint interval | 5 min | 1 min |
| State backend | HashMap | RocksDB |
| Network buffer | default | 8192 |
| TM heap | 1024m | 4096m |

```yaml
# Scaled flink-conf.yaml
taskmanager.numberOfTaskSlots: 8
taskmanager.memory.process.size: 6144m
parallelism.default: 64
state.backend: rocksdb
state.backend.rocksdb.memory.managed: true
state.backend.incremental: true
execution.checkpointing.interval: 60s
```

### Dynamic Scaling with Reactive Mode

```bash
# Enable reactive mode for autoscaling
./bin/start-cluster.sh --configmap flink-configmap --reactive-mode
```

```yaml
# kubernetes-deployment.yaml for reactive mode
env:
  - name: FLINK_REACTIVE_MODE
    value: "true"
  - name: FLINK_PLUGINS_DIR
    value: /opt/flink/plugins
resources:
  requests:
    memory: "4Gi"
    cpu: "2"
  limits:
    memory: "8Gi"
    cpu: "4"
```

## 9.3 Integration Scenarios

### Flink + Apache Iceberg (Lakehouse)

```sql
-- Create Iceberg table in SQL
CREATE TABLE iceberg_events (
    event_id STRING,
    event_type STRING,
    user_id STRING,
    payload STRING,
    event_time TIMESTAMP
) PARTITIONED BY (days(event_time), bucket(16, user_id))
TBLPROPERTIES (
    'format-version' = '2',
    'write.distribution-mode' = 'hash',
    'write.metadata.delete-after-commit.enabled' = 'true'
);

-- MERGE into Iceberg (upsert pattern)
MERGE INTO iceberg_events AS target
USING source_events AS source
ON target.event_id = source.event_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

### Flink + dbt (Data Transformation)

```bash
# Flink can read from views created by dbt on Iceberg/Delta tables
# Use Flink SQL to expose dbt-managed tables as streaming sources
CREATE TEMPORARY VIEW user_metrics AS
SELECT * FROM iceberg_catalog.analytics.user_metrics;

-- Flink consumes dbt-transformed data in real-time
INSERT INTO metrics_sink
SELECT user_segment, COUNT(*), SUM(revenue)
FROM user_metrics
GROUP BY user_segment;
```

### Flink + ML Inference

```java
// Online feature store integration
DataStream<PredictionRequest> requests = env
    .addSource(new KafkaSource<>("feature-events"))
    .map(json -> parseRequest(json));

DataStream<PredictionResult> predictions = requests
    .keyBy(req -> req.getUserId())
    .process(new AsyncFunction<PredictionRequest, PredictionResult>() {
        @Override
        public AsyncFunction<PredictionRequest, PredictionResult> {
            // Call ML serving endpoint asynchronously
            // Enrich with features from Redis feature store
        }
    });

predictions.addSink(new KafkaSink<>("predictions"));
```
