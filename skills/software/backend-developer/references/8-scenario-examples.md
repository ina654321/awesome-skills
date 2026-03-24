## § 8 · Scenario Examples

### Example 1: E-commerce API Design

**Context**: Design API for online store.

**API Structure**:
```
GET    /v1/products              # List with filters
GET    /v1/products/{id}         # Get product details
POST   /v1/cart/items            # Add to cart
GET    /v1/orders                # List user orders
POST   /v1/orders                # Create order
PATCH  /v1/orders/{id}/cancel    # Cancel order

Optimizations:
├── Pagination: Cursor-based for performance
├── Caching: Redis for product catalog
├── Rate limiting: 100 req/min per user
└── Webhooks: Order status updates
```

---

### Example 2: Database Performance Issue

**Context**: API response time degraded from 50ms to 2s.

**Diagnosis**:
```
Investigation:
├── Query analysis: Missing index on user_id
├── N+1 problem: Order items loaded individually
├── No caching: Same queries repeated

Fixes:
├── Added composite index (user_id, created_at)
├── Implemented DataLoader for batch loading
├── Redis cache for user profiles

Result:
├── p99 latency: 50ms → 30ms
├── Database CPU: 80% → 20%
```

---

### Example 3: Microservices Migration

**Context**: Split monolith into services.

**Migration**:
```
Services:
├── User Service: Authentication, profiles
├── Catalog Service: Products, inventory
├── Order Service: Orders, payments
├── Notification Service: Email, push

Communication:
├── Synchronous: gRPC for critical paths
├── Asynchronous: Kafka for events
├── Saga: Distributed order processing

Challenges:
├── Data consistency: Eventual consistency
├── Service discovery: Kubernetes DNS
├── Observability: Distributed tracing
```

---

### Example 4: High-Throughput Service

**Context**: Build notification service (1M notifications/minute).

**Architecture**:
```
Components:
├── API: Accept notification requests
├── Queue: Kafka for buffering
├── Workers: Process and send
├── Providers: SMS, email, push

Scaling:
├── Horizontal pod autoscaling
├── Database connection pooling
├── Circuit breakers for providers
└── Dead letter queue for failures
```

---

### Example 5: GraphQL API Implementation

**Context**: Replace REST with GraphQL for mobile clients.

**Benefits**:
```
Before (REST):
├── 5 API calls to load screen
├── Over-fetching: Unused fields
├── Versioning complexity

After (GraphQL):
├── Single query for all data
├── Exact field selection
├── Strong typing, introspection
├── No versioning needed

Implementation:
├── Schema-first design
├── Resolver optimization
├── Query complexity limits
├── persisted queries for mobile
```

---
