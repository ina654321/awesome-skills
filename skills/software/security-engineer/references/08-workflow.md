# Security Engineer — Standard Workflow

## 8.1 Secure Development Lifecycle (SDL)

The Security Engineer integrates security at every phase of the SDLC.

### Phase 1: Requirements & Design

**Step 1 — Threat Modeling Workshop [✓ Done: STRIDE model complete per component]**

Before any code is written, conduct a threat modeling session for every new service or significant feature:

```
Attendees: Security Engineer + Lead Developer + Architect + Product Owner

Process:
1. Decompose the application: draw data flow diagram (DFD)
   - External entities (users, third-party APIs)
   - Data flows (HTTP, queues, DB queries)
   - Data stores (DB, cache, object storage)
   - Processing boundaries (services, functions)

2. Apply STRIDE per component:
   - For each component, ask: Spoofing / Tampering / Repudiation / 
     Info Disclosure / DoS / Elevation of Privilege?

3. Identify mitigations:
   - Map each threat to a security control
   - Document in the threat model artifact

4. Security requirements extraction:
   - Authentication: what factors? session management?
   - Authorization: what RBAC model? data-level?
   - Data protection: encryption at rest/transit?
   - Logging: what events? retention?
   - Compliance: what frameworks apply?

[✓ Done: Threat model document with mitigations reviewed by Security Owner]
[✗ FAIL: Starting implementation without threat model — too late to change architecture]
```

**Reference:** [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling), [NIST SP 800-154 (DREAD替代)](https://csrc.nist.gov/publications/detail/sp/800-154/draft)

### Phase 2: Implementation

**Step 2 — SAST Integration [✓ Done: Semgrep/SonarQube running in CI on every PR]**

Integrate SAST as a required gate, not a suggestion:

```yaml
# GitHub Actions — SAST in CI
- name: Run Semgrep SAST
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      p/owasp-top-10
      p/nodejs-owasp
      p/rustscanner-best-practices
      p/dockerfile
    # Fail on HIGH and CRITICAL findings
    flags: '--severity=ERROR'
```

**Semgrep Ruleset Priorities:**
1. `p/owasp-top-10` — catches A01-A10
2. `p/security-advisories` — known CVEs in dependencies
3. `p/secrets` — hardcoded credentials, API keys
4. `p/dockerfile` — Docker hardening

**Threshold policy:**
- CRITICAL: Block merge immediately; fix in same PR
- HIGH: Block merge; fix within 24 hours
- MEDIUM: Warning; fix before release
- LOW: Document; fix in next sprint

**[✓ Done: SAST gate blocks all CRITICAL/HIGH findings]**
**[✗ FAIL: SAST runs in advisory mode only — findings ignored in CI**

**Step 3 — Secrets Detection [✓ Done: Gitleaks pre-commit + CI]**

```yaml
# .git/hooks/pre-commit (via Gitleaks)
- name: Detect secrets in staged changes
  run: |
    gitleaks protect --staged --exit-code
    # Block commit if secret detected
```

```yaml
# GitHub Actions — CI secrets scan
- name: Run Gitleaks
  uses: gitleaks/gitleaks-action@v2
  with:
    config-path: .gitleaks.toml
```

**What Gitleaks catches:**
- AWS keys (`AKIA...`)
- Azure keys (`DefaultEndpointsProtocol=https;...`)
- GCP keys (`"type": "service_account"`)
- Private keys (RSA, SSH, GPG)
- Generic secrets (`api_key=`, `password=`, `secret=`)
- JWT tokens
- Database connection strings

**[✓ Done: Zero secrets in git history; pre-commit blocks new commits]**
**[✗ FAIL: Secrets found in git history — requires git filter-branch rewrite + key rotation**

**Step 4 — Dependency Scanning [✓ Done: Snyk/Dependabot blocking vulnerable deps]**

```yaml
# Dependabot configuration
version: 2
updates:
  - package-ecosystem: 'npm'
    directory: '/'
    open-pull-requests-limit: 10
    reviewers:
      - security-team
    commit-message:
      prefix: 'deps'
    security-updates: true
```

**Policy:**
- CRITICAL CVE in direct dependency: block immediately; patch within 4 hours
- HIGH CVE: block; patch within 72 hours
- Use `npm audit --audit-level=high` in CI

**[✓ Done: CVEs patched within SLA; no CRITICAL unpatched in production]**
**[✗ FAIL: Known CVE sitting unpatched — indicates no patch process**

### Phase 3: Verification

**Step 5 — DAST Integration [✓ Done: OWASP ZAP baseline scan in CI against staging]**

```yaml
# GitHub Actions — DAST in staging pipeline
- name: OWASP ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.9.0
  with:
    target: 'https://staging.example.com'
    rules: '-passive scan rules'
    cmdline: 'zap-baseline.py -t {target}'
```

**DAST Scope:**
- Run on staging environment before every production deployment
- Spider the full application surface
- Active scan on the new feature endpoints
- Fail pipeline on HIGH/CRITICAL findings

**[✗ FAIL: DAST only runs manually — not in automated pipeline**

**Step 6 — Penetration Testing [✓ Done: Annual pentest with written scope; results remediated]**

**Pre-engagement (STOP gate — never skip):**
```
□ Written scope document defining in-scope targets (IP ranges, domains, APIs)
□ Written authorization letter signed by legal/ciso
□ Rules of engagement (no DoS testing, no physical testing, timing windows)
□ NDA/confidentiality agreements for findings
□ Emergency contacts and kill switch procedure
□ Bug bounty eligibility (does this scope overlap?)
```

**Engagement phases:**

| Phase | Activities | Deliverable |
|-------|-----------|-------------|
| **Reconnaissance** | Passive (OSINT, Shodan, WHOIS) + Active (port scan, service enumeration) | Target inventory |
| **Vulnerability Discovery** | Burp Suite Pro active scan, nuclei, custom fuzzing | Finding list (unauthenticated + authenticated) |
| **Exploitation** | Metasploit, SQLMap, SSRF兑现 | PoC for each finding (screenshots, logs) |
| **Post-Exploitation** | Lateral movement, privilege escalation, data access | Attack path documentation |
| **Reporting** | Executive summary + technical findings with CVSS | Final pentest report |

**Report structure (per finding):**
1. Title + CVE/CWE if applicable
2. CVSS 3.1 score + vector
3. Description
4. Steps to reproduce
5. Impact assessment
6. Remediation recommendation (with code/config example)
7. Evidence (screenshots, request/response)

**[✓ Done: Written scope, authorization, findings remediated within SLA]**
**[✗ FAIL: Pentest without written authorization — illegal under CFAA, Computer Misuse Act**

**Step 7 — Runtime Security Monitoring [✓ Done: Falco rules deployed in K8s clusters]**

```yaml
# Falco rule example — detect crypto mining
- rule: Detect Crypto Mining
  desc: Detect execution of known cryptocurrency mining tools
  condition: >
    spawned_process and
    (proc.name in (crypto_miners) or
     proc.cmdline contains "stratum+tcp" or
     proc.cmdline contains ".stratum.slushpool.com")
  output: >
    Crypto mining activity detected
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: CRITICAL
  tags: [cryptomining, process]
```

---

## 8.2 Incident Response — NIST SP 800-61 Rev 2

### Preparation [✓ Done: IR plan documented, team trained, tools ready]

```
IR Plan must include:
  - Incident classification (CRITICAL/HIGH/MEDIUM/LOW)
  - Escalation matrix (who is called at what severity + time)
  - Communication templates (internal, customer, regulator)
  - Forensic procedures (evidence preservation, chain of custody)
  - Legal notification requirements (72h GDPR breach notification)
  - Post-incident review template (blameless)
```

### Detection & Analysis

| Signal Type | Tool | Investigation |
|-------------|------|---------------|
| SIEM alert (anomalous login) | Splunk/Elastic | Correlate with CloudTrail/VPC Flow logs |
| GuardDuty alert (credential access) | AWS GuardDuty | Check IAM CloudTrail for API calls |
| Falco alert (runtime anomaly) | Falco | Inspect pod logs, container image |
| DAST finding in prod | ZAP | Scan scope, determine exploitability |
| Bug bounty report | HackerOne/Bugcrowd | Reproduce, validate, prioritize |

### Containment

**Immediate containment (preserve evidence first):**
```bash
# Isolate compromised EC2 instance
aws ec2 modify-instance-attribute \
  --instance-id i-0abc123 \
  --groups sg-00000000000000000  # Restrictive security group (no traffic)

# Snapshot EBS volume before termination (forensics)
aws ec2 create-snapshot \
  --volume-id vol-0abc123 \
  --description "FORENSICS: compromised-instance-$(date +%Y%m%d)"
```

**Credential rotation (HIGH priority):**
- Rotate ALL access keys that existed on the compromised instance
- Rotate ALL database passwords accessed from the instance
- Rotate ALL secrets in Secrets Manager/Vault used by the instance
- Invalidate all sessions for users who had access

### Eradication & Recovery

1. Patch the entry vector (how did attacker get in?)
2. Rebuild affected systems from known-good image (never clean infected systems)
3. Restore from clean backup if system is compromised beyond recovery
4. Re-deploy with security controls hardened
5. Gradual re-entry: monitor closely for 72 hours post-recovery

### Post-Incident Review

| Question | Purpose |
|----------|---------|
| Timeline: when did attacker first gain access? | Detect gaps in detection |
| How was the attacker detected? | Improve detection coverage |
| What was the blast radius? | Understand impact |
| Were existing controls effective? | Improve controls |
| How can we prevent recurrence? | Root cause fix |

---

## 8.3 Cloud Security Configuration Review

### AWS IAM Review Checklist

```bash
# Find overly permissive IAM policies
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:user/username \
  --action-names kms:* \
  --resource-arns "*"

# List all users with console access (no MFA?)
aws iam list-users --query 'Users[?!contains(MFAOptions, `nil`)]'

# Find unused IAM roles
aws iam get-credential-report --query 'CredentialReport[]'

# Check for account-level SCPs preventing privilege escalation
aws organizations describe-stacks --query 'Stacks[*].Outputs'
```

### Kubernetes RBAC Audit

```bash
# Check for overly broad ClusterRoleBindings
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.subjects[].name == "system:authenticated")'

# Find pods running as root
kubectl get pods -A -o json | \
  jq '.items[] | select(.spec.securityContext.runAsUser == 0)'

# Check all ServiceAccount token mounts
kubectl get pods -A -o json | \
  jq '[.items[] | {name: .metadata.name, sa: .spec.serviceAccount, autoMount: .spec.automountServiceAccountToken}]'
```

---

## 8.4 DevSecOps Pipeline Reference

### Complete Shift-Left Security Pipeline

```yaml
name: DevSecOps Pipeline
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  # 1. Pre-commit gates
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gitleaks/gitleaks-action@v2
        # Blocks commit with any detected secret

  # 2. SAST — code analysis
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: p/owasp-top-10 p/security-advisories p/secrets
        # Blocks merge on CRITICAL/HIGH

  # 3. Dependency scan
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high  # or: snyk test
        # Blocks on HIGH/CRITICAL CVEs

  # 4. Container image scan
  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t app:${{ github.sha }} .
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'app:${{ github.sha }}'
          format: 'sarif'
          severity: 'CRITICAL,HIGH'
        # Blocks on CRITICAL/HIGH in base image or app layers

  # 5. IaC scan (Terraform/Kubernetes)
  iac-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/tfsec-action@v1
        with:
          soft_fail: true  # Advisory in PR; mandatory on push to main
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: 'k8s/'
          severity: 'CRITICAL,HIGH'

  # 6. Build and push (only if all gates pass)
  build:
    needs: [secrets-scan, sast, dependency-check, container-scan, iac-scan]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t ghcr.io/org/app:${{ github.sha }} .
      - run: docker push ghcr.io/org/app:${{ github.sha }}
        env:
          DOCKER_PASSWORD: ${{ secrets.GITHUB_TOKEN }}

  # 7. Deploy to staging
  deploy-staging:
    needs: [build]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - deploy to staging cluster

  # 8. DAST on staging
  dast-staging:
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    steps:
      - uses: zaproxy/action-baseline@v0.9.0
        with:
          target: 'https://staging.example.com'
        # Blocks promotion to production

  # 9. Promote to production (manual gate + DAST pass)
  deploy-prod:
    needs: [dast-staging]
    runs-on: ubuntu-latest
    environment: production
    # Requires manual approval
    steps:
      - deploy to production cluster
```
