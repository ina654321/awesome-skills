# Security Engineer — Standards & Reference

## 7.1 OWASP Top 10 (2021)

The OWASP Top 10 is the definitive standard for web application security. Every code review and penetration test should map findings to these categories.

| ID | Category | Description | Common Findings |
|----|----------|-------------|-----------------|
| **A01** | Broken Access Control | Restrictions on authenticated users not enforced | IDOR, privilege escalation, CORS misconfiguration, forced browsing |
| **A02** | Cryptographic Failures | Data exposure at rest or in transit | Unencrypted PII, weak hashing (MD5/SHA1), hardcoded secrets, missing TLS |
| **A03** | Injection | Untrusted data interpreted as command | SQLi, NoSQLi, LDAPi, Command Injection, XSS (reflected/stored) |
| **A04** | Insecure Design | Missing/abused security controls | Business logic flaws, rate limiting bypass, authentication flaws |
| **A05** | Security Misconfiguration | Loose defaults, verbose errors, outdated components | Default creds, missing hardening, unnecessary features, debug mode |
| **A06** | Vulnerable Components | Using components with known vulnerabilities | Outdated libraries, abandoned OSS, unpatched server software |
| **A07** | Auth Failures | Broken authentication/session management | Weak passwords, session fixation, JWT alg none, missing MFA |
| **A08** | Data Integrity Failures | Improper code/deploy verification | SSRF, CI/CD injection, unsafe deserialization |
| **A09** | Logging Failures | Insufficient audit trail | No logging of security events, missing breach detection, unparsable logs |
| **A10** | SSRF | Fetching remote resources without validation | File://, http://169.254.169.254, internal API enumeration |

**Reference:** [OWASP Top 10 2021](https://owasp.org/Top10/)

### OWASP Testing Guide v4.2

The companion guide to the Top 10 for conducting structured security tests:
- **Web:** [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- Covers: information gathering, configuration testing, identity management, authentication, authorization, session management, input validation, error handling, cryptography, business logic, client-side testing

### OWASP API Security Top 10 (2023)

For REST/GraphQL API reviews:
- **API1:** Broken Object Level Authorization (BOLA)
- **API2:** Broken Authentication
- **API3:** Broken Object Property Level Authorization
- **API4:** Unrestricted Resource Consumption
- **API5:** Broken Function Level Authorization
- **API6:** Server Side Request Forgery
- **API7:** Security Misconfiguration
- **API8:** Lack of Protection from Automated Threats
- **API9:** Improper Inventory Management
- **API10:** Unsafe Consumption of APIs

**Reference:** [OWASP API Security Top 10](https://owasp.org/API-Security/)

---

## 7.2 NIST Cybersecurity Framework 2.0

The NIST CSF 2.0 (2024) is the primary framework for managing cybersecurity risk in the US and internationally.

### Core Functions

| Function | Purpose | Key Controls |
|----------|---------|-------------|
| **GOVERN (GV)** | Organizational context, risk tolerance, supply chain | GV.OC, GV.RM, GV.SC |
| **IDENTIFY (ID)** | Asset inventory, risk assessment, compliance | ID.AM, ID.RA, ID.GV |
| **PROTECT (PR)** | Access control, data security, awareness | PR.AA, PR.DS, PR.AT |
| **DETECT (DE)** | Anomaly detection, continuous monitoring | DE.CM, DE.AE |
| **RESPOND (RS)** | Incident response planning, communications | RS.RP, RS.CO, RS.IM |
| **RECOVER (RC)** | Recovery planning, improvements | RC.RP, RC.CO, RC.IM |

**Reference:** [NIST CSF 2.0](https://csrc.nist.gov/publications/detail/sp/1271/final)

### NIST SP 800-53 Rev 5 — Security Controls

The comprehensive catalog of security controls for federal systems (widely adopted by enterprise):

| Control Family | Scope | Key Controls |
|---------------|-------|-------------|
| AC (Access Control) | IAM, least privilege, MFA | AC-2, AC-3, AC-6, AC-7 |
| AU (Audit & Accountability) | Logging, monitoring, alerting | AU-2, AU-6, AU-7 |
| CM (Configuration Management) | Baseline configs, change control | CM-2, CM-6, CM-8 |
| IA (Identification & Authentication) | AuthN factors, password policy | IA-2, IA-5 |
| IR (Incident Response) | IR plan, detection, response | IR-4, IR-5, IR-6 |
| SC (System & Communications) | Encryption, network separation | SC-8, SC-12, SC-28 |
| SI (System & Information Integrity) | Patch management, malware | SI-2, SI-3, SI-7 |

**Reference:** [NIST SP 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

### NIST SP 800-63B — Digital Identity Guidelines

Authentication and credential requirements:
- **AAL (Authenticator Assurance Level):** 1 (single factor), 2 (MFA), 3 (phishing-resistant MFA)
- **FAL (Federation Assurance Level):** 1, 2, 3
- **Password requirements:** Minimum 8 chars; check against breach corpuses; no arbitrary complexity rules

**Reference:** [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)

---

## 7.3 CVSS 4.0 — Vulnerability Scoring

CVSS (Common Vulnerability Scoring System) provides a qualitative framework for rating vulnerabilities.

### Base Score Metrics

| Metric | Options | Weight |
|--------|---------|--------|
| **Attack Vector (AV)** | Network (N), Adjacent (A), Local (L), Physical (P) | 0.85, 0.62, 0.55, 0.2 |
| **Attack Complexity (AC)** | Low (L), High (H) | 0.77, 0.62 |
| **Privileges Required (PR)** | None (N), Low (L), High (H) | 0.85, 0.62, 0.27 |
| **User Interaction (UI)** | None (N), Passive (P), Active (A) | 0.85, 0.62, 0.85 |
| **CIA Impact (C/I/A)** | High (H), Low (L), None (N) | 0.56, 0.22, 0 |

### Severity Ratings

| CVSS Score | Severity |
|-----------|----------|
| **0.0** | None |
| **0.1–3.9** | Low |
| **4.0–6.9** | Medium |
| **7.0–8.9** | High |
| **9.0–10.0** | Critical |

### CVSS + EPSS Prioritization

CVSS alone is insufficient. Use **EPSS (Exploit Prediction Scoring System)** to prioritize patching:

| Approach | Formula | Use Case |
|----------|---------|----------|
| **Risk = CVSS × EPSS** | Higher CVSS × Higher exploit probability | Emergency patch prioritization |
| **Patch if EPSS > 0.1** | ~10% probability of exploitation in 30 days | Threshold-based triage |
| **EPSS + Asset Criticality** | Exploit probability × Business impact | Full risk assessment |

**Reference:** [FIRST EPSS](https://www.first.org/epss/), [NVD CVSS](https://nvd.nist.gov/general/nist-processing)

---

## 7.4 Encryption & Cryptographic Standards

| Algorithm | Use Case | Key Size | Standard |
|-----------|----------|----------|----------|
| **AES-256-GCM** | Data at rest (authenticated encryption) | 256 bit | FIPS 197, SP 800-38D |
| **AES-256-CBC** | Legacy at-rest; prefer GCM | 256 bit | FIPS 197 |
| **ChaCha20-Poly1305** | Mobile, high-performance | 256 bit | RFC 7539 |
| **TLS 1.3** | Data in transit (no 1.2 fallback for sensitive) | Ephemeral DH/ECDH | RFC 8446 |
| **TLS 1.2** | Legacy compatibility only | RSA/AES | RFC 5246 |
| **RSA-OAEP** | Key wrapping, digital signatures | 2048 min, 4096 preferred | PKCS#1 v2.2 |
| **Ed25519** | Digital signatures (preferred over RSA) | 256 bit | RFC 8032 |
| **SHA-256** | Integrity, signatures (not for passwords) | 256 bit | FIPS 180-4 |
| **SHA-3** | Integrity (alternative to SHA-2) | 256/512 bit | FIPS 202 |
| **Argon2id** | Password hashing (memory-hard) | t=3, p=1, m=64M | RFC 9106 |
| **bcrypt** | Password hashing (legacy; Argon2 preferred) | Cost factor ≥ 12 | |
| **HKDF** | Key derivation | Variable | RFC 5869 |
| **PBKDF2** | Password-based key derivation | ≥ 310,000 iterations | SP 800-132 |

**Reference:** [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)

---

## 7.5 Compliance Framework Mapping

### SOC 2 Type II — Key Trust Service Criteria

| Trust Principle | Relevant Controls |
|----------------|------------------|
| **CC6.1** — Logical access controls | IAM, MFA, least privilege, access reviews |
| **CC6.6** — Boundary protection | Network segmentation, WAF, VPN, Zero Trust |
| **CC7.1** — Change management | CI/CD security gates, code review, SAST in pipeline |
| **CC7.2** — Incident response | IR plan, MTTD/MTTR metrics, breach notification |
| **CC8.1** — System operations | Monitoring, alerting, capacity management |
| **CC9.9** — Data retention/disposal | Encryption at rest, secure deletion, data classification |

### ISO/IEC 27001:2022 — Annex A Reference

| Domain | Key Controls |
|--------|-------------|
| **A.5** — Information security policies | ISMS policy, review process |
| **A.8** — Asset management | Data classification, asset inventory, ownership |
| **A.9** — Access control | User access, privileged access, access review |
| **A.10** — Cryptography | Encryption policy, key management |
| **A.12** — Operations security | Malware, backup, logging, patch |
| **A.13** — Communications security | Network security, transfer security |
| **A.16** — Incident management | Incident response, reporting |
| **A.18** — Compliance | Privacy, GDPR obligations |

**Reference:** [ISO 27001:2022](https://www.iso.org/standard/27001)

### HIPAA Security Rule — Safeguard Categories

| Category | Standard | Implementation |
|----------|----------|----------------|
| **Administrative** | §164.308 | Risk analysis, workforce training, incident response |
| **Physical** | §164.310 | Facility access, workstation security, device controls |
| **Technical** | §164.312 | Access control, audit controls, integrity, transmission security |

### PCI DSS v4.0 — Key Requirements

| Requirement | Focus | Security-Engineer Role |
|-------------|-------|----------------------|
| **Req 2** | Default credentials, configuration hardening | Cloud/K8s hardening review |
| **Req 3** | Cardholder data protection at rest | Encryption configuration audit |
| **Req 6** | Vulnerability management, secure development | SAST/DAST in CI/CD |
| **Req 7** | Least privilege access | IAM review, RBAC audit |
| **Req 8** | AuthN, MFA, password policy | AuthN implementation review |
| **Req 11** | Regular testing, penetration testing | Annual pentest coordination |

---

## 7.6 Threat Modeling — STRIDE Framework

STRIDE categorizes threats by the security property they violate:

| Threat Category | Violates | Mitigation Examples |
|----------------|----------|---------------------|
| **Spoofing** | Authentication | MFA, certificate pinning, SSH key auth |
| **Tampering** | Integrity | HMAC, digital signatures, code signing |
| **Repudiation** | Non-repudiation | Audit logs, cryptographic log signing |
| **Information Disclosure** | Confidentiality | Encryption, access controls, tokenization |
| **Denial of Service** | Availability | Rate limiting, CDN, autoscaling, DDoS protection |
| **Elevation of Privilege** | Authorization | RBAC, input validation, least privilege |

**STRIDE per Component Worksheet:**

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | EoP |
|-----------|----------|-----------|-------------|----------------|-----|-----|
| Web App | MFA | Input validation | Audit logs | HTTPS | Rate limit | RBAC |
| API Gateway | TLS client cert | JWT validation | Request signing | mTLS | Throttle | OAuth2 |
| Database | IAM auth | Encryption at rest | WAL + audit | Encryption | Connection pool | Row-level security |
| CI/CD | OIDC workload identity | SBOM signing | Immutable pipeline | Secret scanning | — | Pipeline RBAC |

---

## 7.7 Secure Development Standards

### OWASP SAMM (Software Assurance Maturity Model)

A framework for assessing and improving software security maturity across 4 business functions:

| Function | Domains |
|---------|--------|
| **Governance** | Strategy, education, compliance |
| **Design** | Threat assessment, security requirements, architecture |
| **Implementation** | Secure build, secure deployment, defect management |
| **Verification** | Architecture review, testing, security testing |

**Reference:** [OWASP SAMM v2](https://owaspsamm.org/model/)

### SEI CERT Coding Standards

Language-specific secure coding rules:

| Standard | Language | Focus |
|---------|----------|-------|
| **SEI CERT C** | C | Memory safety, integer overflow, concurrency |
| **SEI CERT C++** | C++ | RAII, smart pointers, buffer boundaries |
| **SEI CERT Java** | Java | Serialization, permissions, I/O |
| **SEI CERT Oracle-C** | SQL, Java, Android | Input validation, authentication |

**Reference:** [SEI CERT Standards](https://wiki.sei.cmu.edu/confluence/display/seccode)

### Microsoft SDL (Security Development Lifecycle)

Mandatory security practices for Microsoft product development:

1. Security training
2. Security requirements (Bug Bar)
3. Design review (STRIDE threat modeling)
4. Bug tracking (severity-based triage)
5. Static analysis (SAST)
6. Dynamic analysis (DAST, fuzzing)
7. Penetration testing
8. Security response planning
9. Release review (security sign-off)

---

## 7.8 Cloud Security Reference Architecture

### AWS Security Reference Architecture

| Service | Security Control | Notes |
|---------|----------------|-------|
| **IAM** | Least privilege, SCPs, permission boundaries | Never use `*` in IAM policies |
| **VPC** | Private subnets, NACLs, VPC endpoints | No direct internet for workloads |
| **KMS** | CMK rotation (90 days), grants | Use instead of third-party encryption |
| **GuardDuty** | Always-on threat detection | Enable across all regions |
| **Security Hub** | Centralized findings aggregation | Integrate with Prowler/ScoutSuite |
| **Secrets Manager** | Dynamic secrets, rotation | Never store secrets in SSM or env vars |
| **WAF + Shield** | DDoS protection, OWASP rule sets | Enable on all public-facing endpoints |
| **CloudTrail** | Audit logging, all regions | Enable in ALL regions + GovCloud |

**Reference:** [AWS Well-Architected Framework — Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)

### CIS Benchmarks

| Benchmark | Scope |
|-----------|-------|
| **CIS Kubernetes** | K8s cluster hardening (CIS v1.9) |
| **CIS Docker** | Container runtime hardening |
| **CIS AWS Foundations** | AWS account-level security baseline |
| **CIS Linux** | OS-level hardening (Ubuntu, RHEL, Amazon Linux) |
| **CIS PostgreSQL/MySQL** | Database hardening |

**Reference:** [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)

---

## 7.9 Professional Associations & Certifications

| Organization | Certification | Focus |
|-------------|--------------|-------|
| **ISACA** | CISM, CRISC | Governance, risk, compliance |
| **(ISC)²** | CISSP, CCSP | Broad security, cloud security |
| **Offensive Security** | OSCP, OSED | Penetration testing |
| **SANS Institute** | GIAC (GSEC, GCIH, GCIA) | Technical security |
| **OWASP** | — | Application security |
| **Cloud Security Alliance** | CCSK, CCAK | Cloud security, STAR certification |

---

## 7.10 Key Security Standards Index

| Standard | Body | Version | Scope |
|---------|------|---------|-------|
| OWASP Top 10 | OWASP | 2021 | Web application security |
| OWASP API Security Top 10 | OWASP | 2023 | REST/GraphQL API security |
| OWASP Testing Guide | OWASP | v4.2 | Security testing methodology |
| NIST CSF | NIST | 2.0 (2024) | Enterprise cybersecurity risk |
| NIST SP 800-53 | NIST | Rev 5 | Security and privacy controls |
| NIST SP 800-63B | NIST | 3.0 | Digital identity guidelines |
| CVSS | FIRST | 4.0 | Vulnerability severity scoring |
| EPSS | FIRST | — | Exploit likelihood prediction |
| ISO 27001 | ISO | 2022 | ISMS requirements |
| ISO 27002 | ISO | 2022 | ISMS controls implementation |
| SOC 2 Type II | AICPA | 2017 | Trust service criteria |
| PCI DSS | PCI SSC | v4.0 | Payment card data security |
| HIPAA Security Rule | HHS | — | US healthcare data protection |
| NISTIR 8374 (Cybersecurity Framework for 5G) | NIST | 2022 | 5G security |
| CIS Benchmarks | CIS | Annual | Configuration hardening |
| SLSA | Open Source | v1.0 | Software supply chain integrity |
| OWASP SAMM | OWASP | v2 | Software security maturity |
| MITRE ATT&CK | MITRE | v14 | Adversary tactics and techniques |
| MITRE CWE | MITRE | v3.13 | Weakness enumeration |
| MITRE CAPEC | MITRE | v3.9 | Attack pattern classification |
