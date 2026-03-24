## § 8 · Scenario Examples

### Example 1: Multi-Region Kubernetes Platform

**Context**: Build global platform across 3 AWS regions.

**Architecture**:
```
Components:
├── EKS clusters in us-east, eu-west, ap-south
├── Global load balancer (Route53 latency-based)
├── RDS PostgreSQL with cross-region read replicas
├── ElastiCache Redis (cluster mode)
├── S3 with cross-region replication

GitOps:
├── ArgoCD in each region
├── ApplicationSet for multi-region deploy
├── Automated failover capability

Disaster Recovery:
├── RPO: 1 hour
├── RTO: 30 minutes
├── Quarterly DR drills
```

---

### Example 2: Cost Optimization Initiative

**Context**: Reduce AWS spend by 40%.

**Actions**:
```
Before: $100K/month
├── Overprovisioned EC2 instances
├── Unused RDS instances
├── Unattached EBS volumes
├── No Spot instance usage

After: $60K/month
├── Rightsized based on CloudWatch metrics
├── Reserved Instances for baseline
├── Spot instances for batch workloads
├── Automated cleanup of unused resources
├── Cost allocation tags and dashboards
```

---

### Example 3: Zero-Downtime Migration

**Context**: Migrate monolith to microservices without downtime.

**Strategy**:
```
Approach: Strangler Fig with feature flags
├── Step 1: Deploy microservices alongside monolith
├── Step 2: Route traffic gradually (feature flags)
├── Step 3: Migrate data with dual-write
├── Step 4: Remove monolith components
├── Step 5: Decommission monolith

Safety:
├── Automated rollback on error rate spike
├── Database replication for instant fallback
├── Feature flags for instant revert
```

---

### Example 4: Security Incident Response

**Context**: Container vulnerability discovered in production.

**Response**:
```
Timeline:
├── T+0: Vulnerability disclosed
├── T+1h: Scan all running containers
├── T+2h: Identify affected services
├── T+4h: Patch base image, rebuild
├── T+6h: Rolling update to production
├── T+12h: Verify all containers updated

Prevention:
├── Trivy/Clair scanning in CI/CD
├── Distroless base images
├── Snyk monitoring for new CVEs
├── 24-hour patch SLA for critical CVEs
```

---

### Example 5: Developer Platform Build

**Context**: Build internal platform for 500 developers.

**Platform**:
```
Services:
├── Self-service namespace provisioning
├── Template library (golden paths)
├── Secrets management (Vault integration)
├── Preview environments per PR
├── Observability stack (metrics, logs, traces)

Adoption:
├── 90% of new services use platform
├── Developer NPS: 45 (was -10)
├── Deployment frequency: 10× increase
```

---
