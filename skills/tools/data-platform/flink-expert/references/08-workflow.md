# Standard Workflow

## 8.1 Development Workflow (Local → Cluster)

```
Local Development
├── 1. IDE Setup
│   ├── Import flink-quickstarts as Maven/Gradle project
│   ├── Set breakpoints in DataStream/Table API code
│   └── Configure RemoteExecutor for local MiniCluster debugging
│
├── 2. Local Testing with MiniCluster
│   ├── DataStream: EmbeddedExecutionEnvironment
│   ├── Table: TableEnvironment in local mode
│   └── Use test harnesses for stateful operators
│
├── 3. SQL Development (SQL Gateway)
│   ├── Start ./bin/sql-gateway.sh
│   ├── Connect DBeaver/JdbcClient to localhost:8083
│   ├── Iterate DDL/DML queries
│   └── Validate with local Kafka/Postgres docker
│
└── 4. Submit to Cluster
    ├── ./bin/flink run -d ./target/your-job.jar
    └── Monitor via http://jobmanager:8081
```

### Local Development Example

```java
// Debug with MiniCluster
public class LocalDebugTest {
    public static void main(String[] args) throws Exception {
        Configuration config = new Configuration();
        config.setInteger("local.number-taskmanagers", 2);
        config.setInteger("taskmanager.parallelism.default", 2);

        MiniClusterWithClientResource cluster =
            new MiniClusterWithClientResource(new MiniClusterResourceConfiguration.Builder()
                .setConfiguration(config)
                .setNumberTaskManagers(2)
                .setNumberSlotsPerTaskManager(4)
                .build());

        cluster.before();

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        // Your pipeline here...

        env.execute("Debug Pipeline");

        cluster.after();
    }
}
```

## 8.2 Deployment / Production Workflow

```
Production Deployment
├── 1. Build Artifact
│   ├── mvn clean package -DskipTests (JAR with dependencies)
│   ├── Verify flink version in uber-jar manifest
│   └── Upload to S3/GCS/Artifactory
│
├── 2. Pre-deployment Checks
│   ├── Verify savepoint of previous job
│   ├── Validate state.backend = rocksdb
│   ├── Check checkpoint/savepoint bucket accessible
│   └── Confirm parallelism and TM slot counts
│
├── 3. Deploy Job
│   ├── Option A: Flink Dashboard (JAR upload)
│   ├── Option B: CLI: ./bin/flink run -d -p 4 s3://bucket/job.jar
│   └── Option C: SQL Gateway: CREATE JOB AS SELECT ...
│
├── 4. State Migration (if schema change)
│   ├── Take savepoint: ./bin/flink savepoint <job-id> s3://savepoints/
│   ├── Stop old job
│   ├── Deploy new job with -s <savepoint-path>
│   └── Validate state compatibility
│
└── 5. HA Failover
    └── Job restarts automatically on TM failure; JM failover via Kubernetes
```

### CI/CD Pipeline Example (GitHub Actions)

```yaml
# .github/workflows/flink-deploy.yml
- name: Package Flink Job
  run: mvn clean package -DskipTests -B

- name: Upload JAR to S3
  run: aws s3 cp target/my-flink-job.jar s3://$BUCKET/flink-jobs/

- name: Trigger savepoint and deploy
  run: |
    JOB_ID=$(./flink list -r | grep my-job | awk '{print $2}')
    ./flink savepoint $JOB_ID s3://$BUCKET/savepoints/
    # Deploy new version
    ./flink run -d -s s3://$BUCKET/savepoints/latest ./flink-jobs/my-flink-job.jar
```

## 8.3 Monitoring & Observability

```
Monitoring Stack
├── Flink Dashboard (built-in)
│   ├── Job graph visualization
│   ├── Checkpoint statistics
│   ├── TM/JobManager metrics
│   └── Task manager logs
│
├── Metrics Reporter (Prometheus)
│   ├── flink_taskmanager_job_task_numRecordsOutPerSecond
│   ├── flink_taskmanager_status_Heap_Memory_Used
│   ├── flink_jobmanager_job_uptime
│   └── flink_taskmanager_job_task_currentInputWatermark
│
└── Logging
    ├── TaskManager: logs/flink-{user}-taskmanager-{host}.log
    ├── JobManager: logs/flink-{user}-jobmanager-{host}.log
    └── Use log4j.properties to configure log levels
```

### Metrics Configuration

```yaml
# flink-conf.yaml
metrics.reporter.prom.class: org.apache.flink.metrics.prometheus.PrometheusReporter
metrics.reporter.prom.port: 9250
metrics.reporter.prom.interval: 10 SECONDS

# Enable specific metric groups
metrics.reporter.slf4j.class: org.apache.flink.metrics.slf4j.Slf4jReporter
metrics.reporter.slf4j.interval: 1 MINUTES
metrics.reporter.slf4j.scope.variables.include: job_name,task_name
```

### Alerting Rules (Prometheus)

```yaml
# Prometheus alert rules
groups:
  - name: flink
    rules:
      - alert: FlinkJobDown
        expr: flink_jobmanager_job_uptime == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Flink job {{ $labels.job_name }} is down"

      - alert: FlinkCheckpointFailure
        expr: rate(flink_jobmanager_job_numberOfFailedCheckpoints[5m]) > 0
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Checkpoint failures detected for {{ $labels.job_name }}"

      - alert: FlinkHighMemoryUsage
        expr: flink_taskmanager_Status_JVM_Memory_Heap_Used / flink_taskmanager_Status_JVM_Memory_Heap_Max > 0.85
        for: 5m
        labels:
          severity: warning
```
