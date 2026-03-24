## § 9 · Common Pitfalls

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Snowflake Servers** | Unique manual configuration | Immutable infrastructure, cattle not pets |
| **ClickOps** | Manual console changes | Everything as code, drift detection |
| **Secrets in Repo** | Credentials exposed | Vault, Sealed Secrets, SOPS |
| **Over-Engineering** | Complex solutions for simple needs | Start simple, evolve as needed |
| **No Rollback Plan** | Stuck with failed deployment | Automated rollback, blue-green |
| **Alert Fatigue** | Too many alerts, ignored | Alert on symptoms, page sparingly |

---
