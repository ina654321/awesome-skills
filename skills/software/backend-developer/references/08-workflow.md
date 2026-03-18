# Standard Workflow

## 8.1 Feature Development

```
Phase 1: Requirements
├── User story creation
├── Acceptance criteria definition
├── Technical feasibility review
└── Estimation (story points)

Phase 2: Design
├── Architecture decision (ADR if needed)
├── Database schema changes
├── API contract definition
└── Security review

Phase 3: Implementation
├── TDD: Red-Green-Refactor
├── Feature flags for risky changes
├── Documentation updates
└── Code review

Phase 4: Deployment
├── CI/CD pipeline
├── Staging verification
├── Production rollout (canary/blue-green)
└── Monitoring setup
```

## 8.2 Code Review Checklist

1. Does it solve the problem?
2. Is the code readable?
3. Are there tests?
4. Any security concerns?
5. Performance implications?
6. Breaking changes?
