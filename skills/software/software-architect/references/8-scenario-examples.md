## § 8 · Scenario Examples

### Example 1: E-commerce Platform Design

**Context**: Design an e-commerce platform for 10M daily active users, $1B GMV/year.

**User**: "Design the architecture for our e-commerce platform launching in 6 months."

**Architect Response**:

```
Architecture Overview:
├── Order Service (CQRS)
│   ├── Command side: PostgreSQL for ACID order creation
│   ├── Query side: Elasticsearch for order search
│   └── Event sourcing for audit trail
├── Inventory Service
│   ├── Redis for real-time stock checks (< 10ms)
│   ├── PostgreSQL for inventory records
│   └── Outbox pattern for reservation events
├── Payment Service
│   ├── PCI-compliant isolated deployment
│   ├── Stripe integration via webhook events
│   └── Idempotency keys for duplicate prevention
└── Notification Service (Event-driven)
    ├── Kafka for event consumption
    ├── Template engine for email/SMS
    └── Dead letter queue for failed notifications

SLOs:
- Availability: 99.95% (order placement)
- Latency: p99 < 200ms (product page), < 500ms (checkout)
- Throughput: 10K orders/minute peak

ADRs Required:
1. Database choice (PostgreSQL vs. DynamoDB)
2. Event streaming (Kafka vs. AWS SNS)
3. Payment isolation strategy
```

---

### Example 2: Monolith-to-Microservices Migration

**Context**: 50-engineer team with Rails monolith experiencing 2-day deploy cycles.

**User**: "Our monolith is slowing us down. Should we migrate to microservices?"

**Architect Response**:

```
Assessment:
├── Current State
│   ├── Deploy frequency: 2x/week (target: 10x/day)
│   ├── Test suite: 4 hours (blocking deploys)
│   └── Team coordination: 15 teams, constant conflicts
├── Migration Strategy: Strangler Fig
│   ├── Phase 1: Extract user service (low risk, high value)
│   ├── Phase 2: Extract inventory (bounded context clear)
│   ├── Phase 3: Extract recommendations (ML team autonomy)
│   └── Phase 4: Gradual strangulation over 18 months
├── Risk Mitigation
│   ├── Feature flags for instant rollback
│   ├── Data consistency: Saga pattern for transactions
│   └── Performance: Load test each extraction
└── Success Metrics
    ├── Deploy frequency: 10x/day within 12 months
    ├── Lead time: < 1 hour (from commit to deploy)
    └── Failure rate: < 5% (change failure rate)

⚠️ Warning: Microservices require DevOps maturity.
Current SRE practice assessment needed before proceeding.
```

---

### Example 3: Real-time Analytics Platform

**Context**: Ad tech platform requiring real-time bid optimization with < 50ms latency.

**User**: "We need to process 1M events/second for real-time bidding decisions."

**Architect Response**:

```
High-Throughput Architecture:
├── Ingestion Layer
│   ├── Kafka (100+ partitions for parallelism)
│   ├── Protobuf for serialization (compact, fast)
│   └── Schema registry for evolution
├── Stream Processing
│   ├── Flink for stateful processing
│   ├── 50ms p99 SLA via memory-state stores
│   └── Exactly-once semantics for billing accuracy
├── Feature Store
│   ├── Redis Cluster for low-latency features
│   ├── TTL-based eviction (24hr default)
│   └── Pre-aggregated counters for speed
├── Model Serving
│   ├── Triton Inference Server
│   ├── GPU batching for throughput
│   └── A/B testing framework built-in
└── Data Lake
    ├── S3 for raw event storage
    ├── Iceberg for time-travel queries
    └── Athena for ad-hoc analytics

Trade-offs Documented:
- Latency vs. Accuracy: 50ms SLA requires approximate aggregates
- Cost vs. Freshness: Feature freshness 30s (not real-time)
- Complexity vs. Scale: Flink adds ops overhead, enables scale
```

---

### Example 4: Architecture Review

**Context**: Review existing microservices architecture for anti-patterns.

**User**: "Can you review our architecture and identify issues?"

**Architect Response**:

```
Architecture Review Findings:

🔴 CRITICAL Issues:
├── Distributed Monolith Detected
│   ├── 5 services share single PostgreSQL database
│   ├── Direct table access across service boundaries
│   └── Impact: Tight coupling, schema change coordination
│   └── Remediation: Database per service; synchronous → async
├── Missing Circuit Breakers
│   ├── Service A calls Service B with no timeout
│   ├── Cascading failure risk during outages
│   └── Remediation: Hystrix/Resilience4j implementation

🟠 HIGH Issues:
├── Shared Library Anti-Pattern
│   ├── "Common" library imported by all services
│   ├── Change requires coordinated deployment
│   └── Remediation: Versioned libraries; async patterns
├── No Distributed Tracing
│   ├── 5-minute mean time to identify failing service
│   └── Remediation: OpenTelemetry + Jaeger

🟡 MEDIUM Issues:
├── API Versioning Strategy Missing
├── Secrets in environment variables (not vault)
└── No chaos engineering practice

Remediation Roadmap:
- Month 1: Circuit breakers, tracing
- Month 2: Database isolation (highest-traffic service)
- Month 3-6: Gradual decoupling
```

---

### Example 5: Multi-Region Active-Active Design

**Context**: Financial platform requiring global availability with < 100ms latency worldwide.

**User**: "Design a globally distributed system with strong consistency for transactions."

**Architect Response**:

```
Global Architecture:
├── Region Setup (us-east, eu-west, ap-south)
│   ├── Active-active deployment
│   ├── Traffic routed via GeoDNS
│   └── Local read replicas for < 50ms reads
├── Data Consistency Strategy
│   ├── CRDTs for shopping cart (eventual consistency OK)
│   ├── Paxos/Raft for inventory (strong consistency required)
│   └── Saga pattern for cross-region transactions
├── Conflict Resolution
│   ├── Last-write-wins for non-critical data
│   ├── Business rules for inventory conflicts
│   └── Manual reconciliation queue for edge cases
└── Failover Design
    ├── RTO: 30 seconds (automated failover)
    ├── RPO: 0 (synchronous replication for critical data)
    └── Circuit breakers prevent split-brain

Critical Design Decisions:
1. Inventory is CP (availability sacrificed during partition)
2. Product catalog is AP (stale reads acceptable)
3. Orders use Saga (eventual consistency with compensation)

Trade-offs:
- Write latency: 150ms (cross-region coordination)
- Read latency: < 50ms (local serving)
- Complexity: High (conflict resolution required)
```

---
