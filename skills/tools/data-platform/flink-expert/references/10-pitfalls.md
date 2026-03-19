# Common Pitfalls & Anti-Patterns

## 10.1 Common Mistakes

| # | Mistake | Severity | Impact | Fix |
|---|---------|----------|--------|-----|
| 1 | **Using EVENT_TIME without WatermarkStrategy** | 🔴 High | Out-of-order data processed incorrectly, late data silently dropped | Always define `WatermarkStrategy.forBoundedOutOfOrderness()` with appropriate grace period |
| 2 | **Stateful operator without proper `open()` initialization** | 🔴 High | State lost on restart, NullPointerException | Use `RichFunction.open(Configuration)` for state initialization |
| 3 | **Parallelism mismatch between source and sink** | 🔴 High | Data skew, bottlenecks, backpressure propagation | Explicitly set `sink.parallelism` and `INSERT INTO` with consistent key distribution |
| 4 | **Checkpointing disabled in streaming mode** | 🔴 High | No fault tolerance, state lost on failure | Always enable: `execution.checkpointing.interval: 60s` |
| 5 | **Using collect()/print() in production DataStream** | 🟡 Medium | Memory leak, blocking call in distributed pipeline | Use `writeAsText()`, Kafka sink, or async I/O pattern |
| 6 | **Ignoring `minimizeMemories()` for state** | 🟡 Medium | OOM on large state, RocksDB compaction overhead | Use RocksDB backend, enable incremental checkpoints |
| 7 | **Not handling exceptions in `flatMap()`** | 🟡 Medium | Task failure, job restart cascade | Wrap in try-catch, emit to dead-letter topic or side output |
| 8 | **Over-partitioning (parallelism too high)** | 🟡 Medium | Excessive network shuffle, increased latency | Benchmark with realistic data; parallelism = TM slots × TM count |
| 9 | **Kafka offset commit disabled** | 🟡 Medium | Duplicates or missed records on restart | Use Flink's checkpointing as offset strategy, disable `enable.auto.commit` |
| 10 | **Timestamp assignment after keyBy()** | 🟡 Medium | Watermarks don't propagate correctly | Assign timestamps and watermarks **before** keyBy() |

## 10.2 Anti-Patterns

### Anti-Pattern: Global Window Without Eviction

```java
// BAD: Global window that never fires
DataStream<Tuple2<String, Integer>> stream = ...
stream.windowAll(SlidingEventTimeWindows.of(Time.hours(1), Time.minutes(5)));

// WHY IT'S BAD: Every event is held in state forever until the job is cancelled.
// Solution: Use session windows or incremental aggregation
```

### Anti-Pattern: Blocking I/O in ProcessFunction

```java
// BAD
@Override
public void processElement(String value, Context ctx, Collector<String> out) {
    String result = httpClient.get("http://api.example.com/lookup/" + value); // BLOCKING
    out.collect(result);
}

// GOOD: Async I/O
DataStream<String> result = AsyncDataStream.unorderedWait(env, new AsyncHttpRequest(), 1000, TimeUnit.MILLISECONDS, 10);
```

### Anti-Pattern: Processing Time for Business Logic

```java
// BAD: Business metrics depend on ProcessingTime
public class BadAggregator extends KeyedProcessFunction<String, Event, Aggregated> {
    @Override
    public void processElement(Event e, Context ctx, Collector<Aggregated> out) {
        if (System.currentTimeMillis() % 24 == 0) { // WRONG: Non-deterministic
            out.collect(new Aggregated(e.getKey(), e.getValue()));
        }
    }
}

// GOOD: Use EventTime + Timers for deterministic business logic
public class GoodAggregator extends KeyedProcessFunction<String, Event, Aggregated> {
    @Override
    public void processElement(Event e, Context ctx, Collector<Aggregated> out) {
        ctx.timerService().registerEventTimeTimer(
            ctx.timestamp() + Time.minutes(5).toMilliseconds()
        );
    }
}
```

### Anti-Pattern: Using DataStream for Complex SQL Workloads

```java
// BAD: Complex joins and aggregations in DataStream API
DataStream<Tuple3<...>> result = input1
    .join(input2).where(...).equalTo(...)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .process(new ComplexJoinProcess());

// GOOD: Use Table API / SQL for relational operations
Table result = tEnv.sqlQuery(
    "SELECT a.id, b.value FROM table_a a JOIN table_b b ON a.id = b.id"
);
```

### Anti-Pattern: No Dead Letter Queue for Flinks

```java
// BAD: Fail silently on parse errors
public void map(String json) {
    MyEvent event = objectMapper.readValue(json); // throws on malformed JSON
}

// GOOD: Side output for unparseable records
OutputTag<FailedRecord> deadLetterTag = new OutputTag<FailedRecord>("dlq"){};
DataStream<MyEvent> main = stream
    .process(new ParseWithDlq(deadLetterTag));
DataStream<FailedRecord> dlq = main.getSideOutput(deadLetterTag);
dlq.addSink(new KafkaSink<>("dlq-topic"));
```

### Anti-Pattern: Neglecting Serialization

```java
// BAD: Using non-serializable object in state
public class BadState extends KeyedProcessFunction<String, Event, Result> {
    ObjectMapper mapper = new ObjectMapper(); // NOT serializable!

    @Override
    public void processElement(Event e, Context ctx, Collector<Result> out) {
        // Fails at checkpoint time
    }
}

// GOOD: Initialize in open() or use Avro/Protobuf
public class GoodState extends KeyedProcessFunction<String, Event, Result> {
    transient ObjectMapper mapper;

    @Override
    public void open(Configuration parameters) {
        mapper = new ObjectMapper(); // Initialized on each TM
    }
}
```

## 10.3 Performance Pitfalls

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| **Small RocksDB write buffer** | High compaction overhead, slow throughput | Set `state.backend.rocksdb.writebuffer.size: 64mb`, `writebuffer.count: 4` |
| **Excessive keyBy cardinality** | State explosion, OOM | Pre-aggregate before high-cardinality keyBy; use `ValueState` instead of `MapState` |
| **No network buffer tuning** | Backpressure, checkpoint alignment delays | Set `taskmanager.network.memory.fraction: 0.15`, `taskmanager.network.memory.min: 64mb` |
| **Micro-batching too small** | Excessive overhead per record | Increase `table.exec.source.cdc-events-per-packet: 1000` for CDC sources |
| **Synchronous I/O in sink** | TM thread blocking, low throughput | Use `AsyncSinkBase` or `GenericWriteAheadSink` |
