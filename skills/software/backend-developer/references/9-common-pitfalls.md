## § 9 · Common Pitfalls

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **God Object** | One model does everything | Split into focused models |
| **Anemic Domain Model** | Logic in services, not models | Rich domain objects |
| **Leaky Abstractions** | Implementation details exposed | Clean interfaces |
| **No Pagination** | Unbounded result sets | Always paginate lists |
| **Missing Timeouts** | Requests hang forever | Set aggressive timeouts |
| **No Circuit Breaker** | Cascading failures | Circuit breaker pattern |

---
