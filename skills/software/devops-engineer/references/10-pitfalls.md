# Common Pitfalls & Anti-Patterns

## 10.1 High-Severity Anti-Patterns

### 🔴 Anti-Pattern 1: Manual Changes to Production
```
❌ BAD: SSHing into servers to make changes
✅ GOOD: All changes via IaC; if manual change needed, document and reproduce in code
```
**Why it matters**: Manual changes create snowflake servers; impossible to reproduce; no version control.

### 🔴 Anti-Pattern 2: No Backup Strategy
```
❌ BAD: "We'll figure out backups if needed"
✅ GOOD: Automated backups, tested restores, clear ownership
```
**Why it matters**: Data loss is often permanent; backups without testing are unreliable.

### 🔴 Anti-Pattern 3: Secrets in Code
```
❌ BAD: AWS keys, database passwords in GitHub
✅ GOOD: Secret management (Vault, AWS Secrets Manager), environment variables
```
**Why it matters**: Exposed secrets lead to breaches; can't rotate easily; compliance violation.

### 🔴 Anti-Pattern 4: No Monitoring
```
❌ BAD: "We check logs when there's a problem"
✅ GOOD: Proactive monitoring, alerting, dashboards; on-call response procedures
```
**Why it matters**: You find problems before users do; MTTR increases without monitoring.

## 10.2 Medium-Severity Anti-Patterns

### 🟡 Anti-Pattern 5: Long-Lived Branches
```
❌ BAD: Feature branches open for weeks
✅ GOOD: Small PRs, short-lived branches, merge frequently
```

### 🟡 Anti-Pattern 6: No Rollback Plan
```
❌ BAD: "We'll fix forward if deployment fails"
✅ GOOD: Always have rollback procedure; test it before production
```

### 🟡 Anti-Pattern 7: Shared State in Tests
```
❌ BAD: Tests depend on each other; order matters
✅ GOOD: Independent, parallelizable tests with isolated state
```

### 🟡 Anti-Pattern 8: Over-Engineering
```
❌ BAD: Building microservices for 3-person startup
✅ GOOD: Start simple; scale complexity with scale of problem
```

## 10.3 Best Practices Checklist

### Infrastructure
- [ ] All infrastructure as code
- [ ] State management configured
- [ ] Secrets managed securely
- [ ] Backups configured and tested
- [ ] Disaster recovery documented

### Deployment
- [ ] CI/CD pipeline exists
- [ ] Automated tests in pipeline
- [ ] Rollback procedure documented
- [ ] Blue-green or canary capable
- [ ] Smoke tests after deploy

### Monitoring
- [ ] Application metrics collected
- [ ] Infrastructure metrics collected
- [ ] Alerts configured
- [ ] On-call rotation established
- [ ] Runbooks for common issues

## 10.4 Red Flags to Watch For

| Red Flag | Risk Level | Action |
|----------|------------|--------|
| Server unreachable, no alert fired | High | Review monitoring coverage |
| Can't rebuild infrastructure from scratch | High | IaC everything; test regularly |
| Deployment requires 2+ hours | High | Automate; break into smaller parts |
| Frequent prod incidents | Medium | Post-mortem; identify root causes |
| Secrets in version control | High | Immediate rotation; move to secrets manager |