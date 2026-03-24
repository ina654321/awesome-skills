## § 7 · Standard Workflow

### Phase 1: Requirements & Design (Days 1-3)

```
├── Gather application requirements
├── Design infrastructure architecture
├── Define security and compliance needs
├── Plan observability strategy
└── [✓ Done]: Architecture diagram, tech stack chosen
    [✗ FAIL]: Unclear requirements → continue discovery
```

### Phase 2: Infrastructure Setup (Days 4-10)

```
├── Set up Terraform/Pulumi project structure
├── Create core infrastructure (VPC, networking)
├── Deploy Kubernetes cluster
├── Configure access control and security
└── [✓ Done]: Infrastructure provisioned, accessible
    [✗ FAIL]: Security scan failures → remediate
```

### Phase 3: CI/CD Pipeline (Days 11-15)

```
├── Build containerization strategy
├── Create CI pipeline (build, test, scan)
├── Set up GitOps deployment
├── Configure progressive delivery
└── [✓ Done]: End-to-end automation working
    [✗ FAIL]: Pipeline failures → debug and fix
```

### Phase 4: Observability & Hardening (Days 16-20)

```
├── Deploy monitoring stack
├── Configure alerting rules
├── Set up log aggregation
├── Perform security hardening
└── [✓ Done]: Production-ready, monitored
    [✗ FAIL]: Monitoring gaps → fill before launch
```

---
