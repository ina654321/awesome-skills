# Common Pitfalls & Anti-Patterns

## 10.1 Coding Mistakes

| # | Mistake | Severity | Prevention |
|---|---------|----------|------------|
| 1 | **SQL injection** | 🔴 High | Parameterized queries |
| 2 | **Hardcoded secrets** | 🔴 High | Environment variables |
| 3 | **No error handling** | 🔴 High | Try-catch, fallbacks |
| 4 | **Memory leaks** | 🟡 Medium | Proper resource cleanup |
| 5 | **N+1 queries** | 🟡 Medium | Eager loading |

## 10.2 Security Checklist

- [ ] Input validation
- [ ] Output encoding
- [ ] Authentication + Authorization
- [ ] Secure headers
- [ ] Rate limiting
- [ ] Logging/monitoring
