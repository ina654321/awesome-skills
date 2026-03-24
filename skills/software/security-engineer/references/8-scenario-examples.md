## § 8 · Scenario Examples

### Example 1: Zero Trust Implementation

**Context**: Transform legacy network to Zero Trust architecture.

**Architecture**:
```
Before:
├── Flat network, VPN for remote
├── Perimeter-based security
├── Implicit trust inside network

After:
├── Identity-aware proxy (IAP)
├── Micro-segmentation (per-workload)
├── Device trust verification
├── Continuous authentication
├── Least privilege everywhere

Implementation:
├── Phase 1: Identity foundation (Okta/Azure AD)
├── Phase 2: Device management (MDM)
├── Phase 3: Network segmentation
├── Phase 4: Continuous monitoring
```

---

### Example 2: Secure CI/CD Pipeline

**Context**: Build security into development workflow.

**Pipeline**:
```
Stages:
├── Pre-commit: git-secrets, linting
├── Build: SAST (SonarQube), dependency scan
├── Test: Unit tests, integration tests
├── Security: DAST (ZAP), container scan
├── Deploy: Sign artifacts, verify signatures
├── Monitor: Runtime protection, RASP

Results:
├── 90% of vulnerabilities caught pre-prod
├── Deployment frequency: 20× increase
├── Security review time: 80% reduction
```

---

### Example 3: Cloud Security Assessment

**Context**: Comprehensive AWS security review.

**Findings**:
```
Critical:
├── Public S3 bucket with PII
├── Overprivileged IAM roles
├── Unencrypted RDS databases

Remediation:
├── S3: Block public access, encryption
├── IAM: Least privilege review, MFA enforcement
├── RDS: Enable encryption, rotate keys
├── GuardDuty: Enable threat detection
├── Config: Enable compliance monitoring
```

---

### Example 4: Threat Modeling Workshop

**Context**: STRIDE analysis for payment processing system.

**Threats Identified**:
```
Spoofing:
├── Fake payment processor API
├── Mitigation: mTLS, certificate pinning

Tampering:
├── Payment amount modification
├── Mitigation: Request signing, integrity checks

Repudiation:
├── Deny transaction occurred
├── Mitigation: Immutable audit logs

Information Disclosure:
├── Credit card data exposure
├── Mitigation: Tokenization, encryption

DoS:
├── Payment system overload
├── Mitigation: Rate limiting, circuit breakers

Elevation:
├── Admin access to transactions
├── Mitigation: RBAC, separation of duties
```

---

### Example 5: Red Team Exercise

**Context**: Simulated attack to test defenses.

**Exercise**:
```
Scope: External to domain admin
Rules of Engagement:
├── No production data exfiltration
├── Business hours only
├── Emergency contact established

Findings:
├── Phishing: 15% click rate
├── Weak password policy: Cracked 30% hashes
├── Lateral movement: Unrestricted RDP
├── Data access: Overprivileged service accounts

Remediations:
├── Security awareness training
├── Password policy: 16+ chars, MFA
├── Network segmentation
├── Service account least privilege
```

---
