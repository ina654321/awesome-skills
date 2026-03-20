# DevOps Engineer — Standards & Reference

## 7.1 Infrastructure Standards

### Cloud Provider Comparison

| Provider | Best For | Key Services | DevOps Strength |
|----------|----------|-------------|-----------------|
| **AWS** | Enterprise, breadth of services | EKS, ECS, Lambda, RDS, S3, IAM | Largest managed service portfolio, mature tooling |
| **Azure** | Microsoft integration | AKS, Azure DevOps, Cosmos DB, Entra ID | Best for Windows/.NET workloads, enterprise AD |
| **GCP** | Data/ML workloads, startup-friendly | GKE, BigQuery, Cloud Run, Cloud Functions | Best Kubernetes experience, powerful data tools |
| **Multi-cloud** | Vendor independence, resilience | Terraform, Pulumi, Crossplane | Best for: avoiding lock-in, disaster recovery |

**Reference:** [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html), [GCP Architecture Framework](https://cloud.google.com/architecture/framework), [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)

### Container Standards

| Requirement | Standard | Enforcement |
|-------------|----------|-------------|
| **Base image** | Minimal (Alpine, distroless, scratch) | Dockerfile FROM check in CI |
| **Non-root user** | Run as UID 65534 or custom non-privileged | `USER 65534` in Dockerfile |
| **No shell** | Distroless images have no shell | Trivy scan catches shells |
| **Health checks** | Liveness + readiness probes required | K8s manifest validation |
| **Resource limits** | CPU + memory requests and limits | LimitRange in namespace |
| **Image scanning** | No HIGH/CRITICAL CVEs | Trivy in CI gate |
| **Immutable tags** | Use digest-pinned SHA, not `:latest` | CI policy enforcement |

**Reference:** [CIS Docker Benchmark](https://www.cisecurity.org/cis-benchmarks), [Distroless Docker](https://github.com/GoogleContainerTools/distroless)

### Kubernetes Standards (CIS Kubernetes Benchmark v1.9)

| Category | Control | Validation |
|----------|---------|-----------|
| **RBAC** | ServiceAccounts with minimal permissions; no wildcard in rules | `kubectl auth can-i --list` audit |
| **Network Policies** | Default-deny; allowlist egress/ingress per namespace | NetworkPolicy present |
| **Pod Security** | Pod Security Standards: Restricted (or PodSecurityPolicy) | PSA audit |
| **Secrets** | Encryption at rest enabled; no Secret as env var with sensitive data | K8s encryption config |
| **Etcd** | Encryption at rest; TLS; no 0.0.0.0 access | etcd hardening |
| **API Server** | No anonymous auth; RBAC enabled; audit logging | API server flags |
| **Worker nodes** | No privileged containers; read-only root filesystem | PodSecurityPolicy |

**Reference:** [CIS Kubernetes Benchmark](https://www.cisecurity.org/cis-benchmarks)

---

## 7.2 CI/CD Standards

### Pipeline Architecture — GitHub Actions Reference

```
Event → Trigger → Environment → Jobs → Stages → Steps

Trigger Types:
  push (branch, tag, path filter)
  pull_request (opened, synchronize, closed)
  workflow_dispatch (manual)
  schedule (cron: '0 2 * * *')
  repository_dispatch (custom event from CI trigger)
```

### Complete Production CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yaml
name: Production CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main, develop]

env:
  IMAGE_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ══════════════════════════════════════════════
  # Stage 1: Pre-flight — fast feedback
  # ══════════════════════════════════════════════
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linters
        run: |
          yamllint .
          shellcheck .
          tflint .

  test-unit:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests
        run: go test -race -coverprofile=coverage.out ./...
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage.out

  # ══════════════════════════════════════════════
  # Stage 2: Security — shift-left gates
  # ══════════════════════════════════════════════
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
      - name: SAST — Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: p/owasp-top-10 p/security-advisories

  # ══════════════════════════════════════════════
  # Stage 3: Build — container image
  # ══════════════════════════════════════════════
  build:
    runs-on: ubuntu-latest
    needs: [lint, test-unit, security]
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}
      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - name: Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta.outputs.tags }}
          format: 'sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail on CRITICAL
          upload-results: true

  # ══════════════════════════════════════════════
  # Stage 4: Deploy to Staging
  # ══════════════════════════════════════════════
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build]
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: |
          kubectl set image deployment/app \
            app=${{ needs.build.outputs.image-tag }} \
            --namespace=staging
          kubectl rollout status deployment/app \
            --namespace=staging \
            --timeout=300s
      - name: Smoke tests
        run: |
          k6 run tests/load/smoke.js \
            --env BASE_URL=https://staging.example.com
```

### GitOps Principles (ArgoCD Reference)

GitOps is the operational framework using Git as the single source of truth for declarative infrastructure:

```
Developer → Commit to Git → ArgoCD detects drift → Syncs cluster to Git state

Core principles:
  1. DECLARATIVE: Everything expressed as code (K8s YAML, Helm, Kustomize)
  2. VERSIONED: Git history provides full audit trail of every change
  3. PULL-BASED: Operator pulls from Git, not push from CI
  4. IMMUTABLE: Running systems are never modified manually; changes go through Git
```

**Reference:** [ArgoCD Documentation](https://argo-cd.readthedocs.io/), [GitOps Principles](https://opengitops.dev/)

### Deployment Strategies

| Strategy | Description | Risk | Time | When to Use |
|----------|-------------|------|------|-------------|
| **Rolling** | Gradually replace pods (25% maxUnavailable) | Medium | Medium | Stateless services, canary precursor |
| **Blue-Green** | Parallel environment; instant switch | Low | Fast switch | Database schema changes; instant rollback |
| **Canary** | Route N% of traffic to new version | Low | Slow | High-risk changes; gradual traffic shift |
| **Argo Rollouts** | Progressive delivery with automated analysis | Lowest | Gradual | Production with metric-based promotion |
| **Direct** | Deploy directly to production | High | Instant | Dev/test only |

```yaml
# Argo Rollouts — canary with automated analysis
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app-rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 5
        - pause: {duration: 10m}
        - analysis:
            templates:
              - templateName: success-rate
            args:
              - name: service-name
                value: app-rollout
      canaryService: app-canary
      trafficRouting:
        istio:
          virtualService:
            name: app-vs
            routes:
              - primary
```

---

## 7.3 Observability Standards

### The Four Golden Signals (Google SRE Handbook)

Every service must expose these signals for monitoring:

| Signal | What It Measures | How to Query | Alert When |
|--------|----------------|-------------|-----------|
| **Latency** | Time to process requests | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` | p95 > 500ms |
| **Traffic** | Requests per second | `sum(rate(http_requests_total[5m]))` | Drops > 50% unexpectedly |
| **Errors** | Rate of failed requests (5xx, not 4xx) | `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` | Error rate > 1% |
| **Saturation** | How "full" is the service (CPU%, memory%, disk I/O) | `node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes` | Any resource > 90% |

**Reference:** [Google SRE Handbook — Monitoring Distributed Systems](https://sre.google/solutions/book/monitoring-distributed-systems/)

### USE Method (Per-Resource Utilization)

```
For every resource, check:
  U = Utilization %       → Is the resource busy?
  S = Saturation          → Is the resource queuing?
  E = Errors              → Are there errors on this resource?

Resources to check per host:
  - CPU: mpstat, top, /proc/stat
  - Memory: free, vmstat
  - Disk I/O: iostat -x 2
  - Network: netstat -s, /proc/net/dev
  - Kubernetes: kubectl top nodes, kubectl top pods
```

### RED Method (Per-Service Request Rate)

```
For every service, check:
  R = Request rate     → How many requests/second? rate(request_total[1m])
  E = Error rate       → How many errors? rate(request_errors_total[1m])
  D = Duration         → How long do requests take? histogram_quantile(0.99, rate(request_duration_seconds_bucket[5m]))
```

### Alerting Standards

| Severity | Response | SLA | Examples |
|----------|----------|-----|---------|
| **P1 / CRITICAL** | Immediate (< 5 min) | 15 min resolution | Service down, data loss, security breach |
| **P2 / HIGH** | < 15 min | 1 hour | Latency spike > SLO, partial outage |
| **P3 / MEDIUM** | < 1 hour | Next business day | Resource > 80%, error rate rising |
| **P4 / LOW** | Next business day | 1 week | Non-critical anomalies, cleanup |

**Golden rules:**
- Every alert must have a corresponding runbook URL
- Error budget alerts (SLO burn rate) > threshold-based alerts
- No alert should page for something that auto-heals
- Alert on symptoms (is service slow?), not causes (is CPU high?)

---

## 7.4 Terraform & IaC Standards

### Terraform State Management

```
NEVER:
  ❌ terraform apply on developer laptop with local state
  ❌ Share .tfstate file via git or network share
  ❌ Edit .tfstate manually

ALWAYS:
  ✅ Remote backend (S3 + DynamoDB for locking)
  ✅ State versioning enabled
  ✅ State encryption at rest (AES-256)
  ✅ Separate workspace per environment
  ✅ State locked during apply (DynamoDB TTL or Terraform Cloud)
```

```hcl
# Production backend
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/networking/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    versioning     = true
  }
}
```

### Terraform Module Structure

```
modules/
  └── networking/
      ├── main.tf          # Resource definitions
      ├── variables.tf     # Input variables with descriptions
      ├── outputs.tf        # Output values
      ├── versions.tf       # Provider and version constraints
      ├── data.tf           # Data sources
      └── README.md         # Module documentation

Anti-patterns:
  - Monolithic module (one module for entire infrastructure)
  - No version constraints (provider drift)
  - Hardcoded values instead of variables
  - State not isolated between environments
```

### Security Scanning for IaC

| Tool | What It Scans | CI Integration |
|------|-------------|----------------|
| **tfsec** | Terraform HCL | GitHub Actions, pre-merge |
| **Checkov** | Terraform, K8s, Docker, CloudFormation | GitHub Actions, pre-merge |
| **Terrascan** | Terraform, K8s, serverless | CI/CD, Atlantis |
| **Snyk Infrastructure as Code** | Terraform, CloudFormation, K8s | GitHub Actions, IDE |
| **KICS** | Terraform, K8s, Dockerfile | CI/CD, VS Code |

---

## 7.5 SRE & Incident Response Standards

### Error Budget Policy

```
Error Budget = (1 - SLO) × total time in window

Example:
  Availability SLO: 99.9%
  Monthly window: 43,200 minutes
  Allowable downtime: 43.2 minutes/month

  If actual downtime: 20 minutes → 0% error budget used → deploy freely
  If actual downtime: 50 minutes → 117% budget consumed → STOP feature work
  Policy: Stop feature work when error budget is < 50% remaining
```

### Blameless Postmortem Template

```markdown
## Incident: [Brief Description]
**Date:** YYYY-MM-DD | **Duration:** Xh Ym | **Severity:** P1/P2

### Timeline
- HH:MM — Alert fired
- HH:MM — Engineer responded
- HH:MM — Root cause identified
- HH:MM — Fix deployed
- HH:MM — Service restored

### Impact
- X users affected, Y% error rate, Z minutes of downtime
- Revenue impact: ~$X

### Root Cause
[Technical explanation — what was the underlying failure?]

### Contributing Factors
[What conditions enabled the root cause?]

### Detection
[How was this detected? What failed in detection?]

### Response
[What went well? What was slow?]

### Action Items
| Action | Owner | Due Date |
|--------|-------|---------|
| [Specific action] | @name | YYYY-MM-DD |
```

---

## 7.6 Key DevOps Standards Index

| Standard | Body | URL |
|---------|------|-----|
| 12-Factor App | Adam Wiggins | 12factor.net |
| Google SRE Handbook | Google | sre.google/solutions/book.html |
| Site Reliability Engineering | O'Reilly | sre.google/solutions/book.html |
| Kubernetes Documentation | CNCF | kubernetes.io/docs |
| CNCF Cloud Native Trail Map | CNCF | cncf.io/trailmap |
| CIS Kubernetes Benchmark | CIS | cisecurity.org/cis-benchmarks |
| NIST SP 800-190 (Container Security) | NIST | csrc.nist.gov/publications/detail/sp/800-190/final |
| ArgoCD Documentation | Argo Project | argo-cd.readthedocs.io |
| Terraform Best Practices | HashiCorp | developer.hashicorp.com/terraform |
| OpenTelemetry | CNCF | opentelemetry.io/docs |
| AWS Well-Architected Framework | AWS | docs.aws.amazon.com/wellarchitected |
| GitOps Principles | OpenGitOps | opengitops.dev |
| SLSA Framework | OpenSSF | slsa.dev |
