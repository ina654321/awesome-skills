## § 9 · Common Pitfalls & Anti-Patterns

| Anti-Pattern | Symptom | Solution |
|--------------|---------|----------|
| **Distributed Monolith** | Services share database; coordinated deploys | Database per service; async communication |
| **Premature Microservices** | 5-person team with 20 services | Start modular monolith; extract when team grows |
| **API Gateway Bloat** | Gateway contains business logic | Gateway only for routing, auth, rate limiting |
| **Synchronous Chains** | 5-service deep call chains | Async events; sagas for transactions |
| **Shared Libraries** | Common code changes break all services | Versioned libraries; copy over share |
| **Database per Service (Overapplied)** | 50 databases for 50 services | Shared read replicas OK; write isolation required |

📄 **Full Anti-Patterns**: [references/anti-patterns.md](references/anti-patterns.md)

---
