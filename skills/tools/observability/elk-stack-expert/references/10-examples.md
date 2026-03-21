# ELK Stack Expert — Example Interactions

This file contains detailed example implementations referenced from SKILL.md §10.

---

## Example 1: Set Up Application Log Pipeline

**User:** "I need to ship JSON logs from our Node.js app to Elasticsearch. Help me design the pipeline."

**ELK Expert:**

> **Architecture:**
> ```
> Node.js App (JSON logs)
>   → Filebeat (harvest)
>     → Logstash (parse, enrich)
>       → Elasticsearch (app-logs-*)
>         → Kibana (visualize)
> ```
>
> **Step 1: Node.js logging to JSON**
> ```javascript
> const winston = require('winston');
> const logger = winston.createLogger({
>   level: 'info',
>   format: winston.format.combine(
>     winston.format.timestamp(),
>     winston.format.json()
>   ),
>   transports: [
>     new winston.transports.File({ filename: '/var/log/app/application.log' }),
>     new winston.transports.Console()
>   ]
> });
> ```
>
> **Step 2: Filebeat config**
> ```yaml
> filebeat.inputs:
>   - type: log
>     paths: ["/var/log/app/application.log"]
>     json.keys_under_root: true
>     json.add_error_key: true
>     fields:
>       application: my-node-app
>       environment: production
>     fields_under_root: true
>
> output.logstash:
>   hosts: ["logstash:5044"]
> ```
>
> **Step 3: Logstash filter**
> ```ruby
> filter {
>   if [application] == "my-node-app" {
>     mutate {
>       add_field => { "[@metadata][index_prefix]" => "app-logs" }
>     }
>     if [level] == "error" {
>       mutate {
>         add_tag => ["error"]
>       }
>     }
>   }
> }
> ```
>
> **Step 4: Elasticsearch index template**
> ```json
> PUT _index_template/app-logs-template
> {
>   "index_patterns": ["app-logs-*"],
>   "template": {
>     "settings": {
>       "number_of_shards": 1,
>       "index.lifecycle.name": "app-logs-policy"
>     },
>     "mappings": {
>       "properties": {
>         "@timestamp": { "type": "date" },
>         "level": { "type": "keyword" },
>         "message": { "type": "text" },
>         "service": { "type": "keyword" },
>         "trace_id": { "type": "keyword" },
>         "user_id": { "type": "keyword" }
>       }
>     }
>   }
> }
> ```
>
> **Step 5: Create ILM policy**
> ```json
> PUT _ilm/policy/app-logs-policy
> { "policy": { "phases": { "hot": { "min_age": "0ms", "actions": { "rollover": { "max_age": "7d" } } } } } }
> ```
>
> **Step 6: Create initial write index**
> ```json
> PUT app-logs-000001
> {
>   "aliases": {
>     "app-logs": { "is_write_index": true }
>   }
> }
> ```

---

## Example 2: Build Kibana Dashboard for Error Monitoring

**User:** "Create a dashboard showing error rate, error types, and top errors for the last 24 hours"

**ELK Expert:**

> **Dashboard Components:**
>
> | Component | Visualization | Key Config |
> |-----------|--------------|-----------|
> | Time Range Filter | Top bar | Last 24 hours, auto-refresh 5m |
> | Error Rate Over Time | Line Chart | Date Histogram on @timestamp (1h) |
> | Error Rate KPI | Metric | % errors, thresholds: >5% Red |
> | Errors by Service | Pie Chart | Terms on service.name |
> | Top 10 Errors | Data Table | Message + count + last_seen |
> | Error Distribution Map | Coordinate Map | geoip.location heatmap |
>
> **Error Rate Calculation:**
> ```
> count(log.level:ERROR) / count(*) * 100
> ```
>
> **Top Errors Table Columns:**
> - message (keyword, first 100 chars)
> - count (Document count)
> - last_seen (@timestamp, last occurrence)

---

## Example 3: Use ML for Anomaly Detection on Response Times

**User:** "I want to automatically detect unusual response times in our API logs"

> **Step 1: Create index pattern in Kibana**
> ```
> Stack Management → Index Patterns → Create index pattern
> Pattern: apm-traces-*
> Time field: @timestamp
> ```
>
> **Step 2: Create ML Job (Single Metric)**
> ```
> Machine Learning → Anomaly Detection → Create Job
> Select: app-logs-*
>
> Job Configuration:
>   - Job ID: api-latency-anomaly
>   - Description: Detect unusual API latency
>
> Analysis Configuration:
>   - Detector: High mean of http.response.latency_ms
>   - Partition: service.name
>   - Bucket span: 15m
>
> Datafeed:
>   - Indices: app-logs-*
>   - Query: match phrase: span.type = "external"
>
> Job Settings:
>   - Model memory: 200MB
>   - Dedup: enabled
> ```
>
> **Step 3: Create alert rule**
> ```
> Machine Learning → Anomaly Detection → Jobs
> Select: api-latency-anomaly
> Create Alert:
>   - Trigger: Anomaly score > 75
>   - Action: Send to Slack #alerts
>   - Summary: Include top influencers
> ```

---

## Example 4: (Reference §11)

See SKILL.md §11 for edge case scenarios including:
- Multi-line stack traces (multiline pattern in Filebeat)
- High cardinality from request IDs (doc_values:false)
- TLS/SSL handshake failures
- Timezone mismatch in logs
- Log rotation causing data loss
- Shard too large (>50GB)
- Slow log queries
- Cluster-wide shard relocation
