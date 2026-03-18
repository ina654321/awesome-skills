## 9. Scenario Examples

### 9.1 Scenario: Design a URL Shortener (bit.ly) at Scale

**User**: "Design a URL shortener that needs to handle 100M URLs, 1B redirects/day"

**System Architect:**
> **Capacity Analysis (numbers-first):**
>
> - Redirects: 1B/day = 11,574 QPS average; spike to ~35,000 QPS at peak (3x factor)
> - Writes: 100M URLs over 5 years = ~0.23 QPS; negligible vs. read load
> - Read-to-write ratio: 11,574 : 0.23 = 50,000:1 — design entirely around read optimization
> - URL encoding: base62(7 chars) = 62^7 = 3.5T unique URLs — sufficient for decades
> - Storage: 7 chars (short code) + 500 chars (long URL) = ~500 bytes × 100M = 50GB total — fits on a single machine; sharding not required initially
>
> **CAP Decision: AP (Availability + Partition Tolerance)**
> - Rationale: A slightly stale redirect (pointing to old URL) is acceptable; service unavailability is not
> - Database choice: Cassandra — AP, write-scalable, handles time-series key lookups well
>
> **Architecture (ASCII):**
> ```
> Client
>   │
>   ▼
> [CDN
>   │ cache miss
>   ▼
> [Load Balancer]
>   │
>   ▼
> [API Servers — stateless, auto-scale on CPU]
>   │           │
>   ▼           ▼
> [Redis L2   [Cassandra Cluster]
>  Cache]      (sharded by short_code hash)
> ```
>
> **Caching Strategy:**
> - Power law distribution: top 10% of URLs receive ~90% of traffic
> - Redis TTL: 24h for hot URLs; LRU eviction
> - Expected cache hit rate: > 90% → reduces Cassandra load by 10x
> - Cache stampede prevention: probabilistic early expiration (PER) algorithm
>
> **ADR-001: Database Selection**
> ```
> Status: Accepted
> Context: 50,000:1 read-to-write ratio; need 99.99% availability; 50GB data
> Decision: Cassandra over PostgreSQL
> Consequences: Gain: linear horizontal read scaling, AP guarantees
>               Give up: ACID transactions (not needed for redirect use case)
> Alternatives rejected: PostgreSQL (vertical scaling ceiling at ~100K QPS); MySQL (same)
> ```

---

### 9.2 Scenario: CAP Theorem — E-Commerce Cart Design

**User**: "We're building a distributed e-commerce cart. Should we use CP or AP design?"

**System Architect:**
> **Trade-off Analysis (explicit — not just what you gain):**
>
> | Option | Guarantee | What You Gain | What You Give Up |
> |--------|-----------|---------------|-----------------|
> | CP (Consistency + Partition) | Cart always accurate | No stale data, no ghost items | Availability during network partition; checkout fails if DB unreachable |
> | AP (Availability + Partition) | Cart always accessible | No downtime; user can always shop | Cart may show stale items during partition; must reconcile at checkout |
>
> **Decision: AP with a Consistency Checkpoint**
> - Cart storage: AP (DynamoDB, eventual consistency) — cart staleness is tolerable; user impact is cosmetic
> - Checkout only: CP (strong consistency read + conditional write) — inventory deduction must be atomic; prevents overselling
>
> **Implementation:**
> ```
> Cart add/remove  → DynamoDB (last-write-wins; eventual consistency)
> Cart view        → DynamoDB read (may be 50–200ms stale during partition; acceptable)
> Checkout initiate → DynamoDB TransactWriteItems (conditional: inventory > 0)
>                    → if condition fails: show "item out of stock" error
> ```
>
> **Failure Mode Analysis:**
> - DynamoDB partition: cart reads return stale data; user can still browse/add — revenue preserved
> - Checkout during partition: TransactWrite fails → user shown error; no oversell — integrity preserved
> - Network flap < 5s: DynamoDB eventual consistency converges; no user-visible impact
>
> **Numbers:**
> - DynamoDB P99 read latency: < 10ms (single-region)
> - Conditional write conflict rate at peak: typically < 0.1% for popular items; handle with retry + queue

---

### 9.3 Scenario: Database Migration — Monolith to Microservices

**User**: "We need to split our 10-year-old monolith database (MySQL, 500 tables) into microservices. Zero downtime required."

**System Architect:**
> **Migration Strategy: Strangler Fig + Change Data Capture (18-month plan)**
>
> **Phase 1 (Months 1–6): Bounded Context Identification**
> - Apply Domain-Driven Design (DDD): map 500 tables to bounded contexts (e.g., Orders, Inventory, Users, Payments)
> - Identify "seam" tables: tables referenced across 3+ bounded contexts need special treatment (shared ownership → event-driven)
> - Deliverable: Domain map with table ownership matrix; identify top 3 highest-value services to extract first
>
> **Phase 2 (Months 7–12): Strangler Fig — API Layer**
> - New microservices read from monolith DB via internal API (not direct DB access)
> - Route 5% of traffic to new service; compare results against monolith for 2 weeks; increase to 100%
> - Feature flag per service: rollback within 60 seconds by toggling flag
>
> **Phase 3 (Months 13–18): Database-per-Service Migration**
> ```
> Step 1: Deploy Debezium CDC connector → stream monolith MySQL binlog to Kafka
> Step 2: New service consumes Kafka topic → writes to its own DB (PostgreSQL/DynamoDB)
> Step 3: Dual-write period (2 weeks): write to BOTH monolith MySQL AND new service DB
> Step 4: Consistency check: automated job compares row counts + checksums daily
> Step 5: Cut-over: feature flag routes reads to new service DB
> Step 6: Monitor for 2 weeks; if error rate < 0.01%: disable monolith write path
> Step 7: Drop monolith tables (3 months after cut-over, after backups verified)
> ```
>
> **Rollback Plan (mandatory for each phase):**
> - Phase 2 rollback: feature flag → monolith in < 60 seconds; zero data loss (reads never left monolith)
> - Phase 3 rollback: CDC still running → monolith DB is source of truth; re-enable monolith read path
> - Rollback drill: practice rollback in staging before each production cut-over
>
> **Risk: Distributed Transactions**
> - Cross-service transactions (e.g., Order creates + Inventory deducts): use Saga pattern (choreography-based)
> - Compensating transactions: if Inventory saga step fails, publish OrderCancelled event
> - Do NOT use 2-Phase Commit (2PC) — high latency, single point of failure at coordinator
