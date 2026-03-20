# Gerrit Permission Management — Standards & References

## Official Documentation

- [Gerrit Code Review — Access Control](https://gerrit.googlesource.com/gerrit/Documentation/2.16/access-control.html)
- [Gerrit Code Review — Project Configuration](https://gerrit.googlesource.com/gerrit/Documentation/2.16/config-project-config.html)
- [Gerrit Code Review — prolog-rules](https://gerrit.googlesource.com/gerrit/Documentation/2.16/prolog-cookbook.html)
- [Gerrit Code Review — REST API](https://gerrit.googlesource.com/gerrit/Documentation/2.16/rest-api.html)
- [Gerrit Code Review — sshd Command Index](https://gerrit.googlesource.com/gerrit/Documentation/2.16/cmd-index.html)
- [Gerrit Code Review — Project Owner Guide](https://gerrit.googlesource.com/gerrit/Documentation/2.16/project-setup.html)

## Industry Standards

### Source Code Access Control Models

- **RBAC (Role-Based Access Control)** — NIST IR 7874, "Guide to Role-Based Access Control" (National Institute of Standards and Technology). Gerrit groups map directly to RBAC roles.
- **ABAC (Attribute-Based Access Control)** — NIST SP 800-162. Used for fine-grained permission inheritance in large Gerrit deployments.
- **Separation of Duties (SoD)** — Enforced in Gerrit through distinct submit, label, and push permissions per branch.
- **Least Privilege Principle** — Each group should have only the permissions required for its function; avoid granting broad `forge identity` or `push` to large groups.

### Code Review Standards

- **ISO/IEC 25010 (SQuaRE)** — Software product quality model relevant to code review quality gates (correctness, security, maintainability).
- **SEI CERT C/C++/Java** — Secure coding standards. Code review labels can enforce security gate scores.
- **OWASP Code Review Guide** — Security-focused review practices; can be integrated into Gerrit label rules.
- **Google Engineering Practices** — Google's internal code review guidelines heavily influenced the Gerrit workflow model.

### Supply Chain & Provenance

- **SLSA (Supply-chain Levels for Software Artifacts)** — Framework for software supply chain integrity. Gerrit's code review trail provides non-forkable provenance; `pushSignedTag` and `require-signed-off-by` support SLSA Level 3+.
- **SBOM (Software Bill of Materials)** — SPDX/cyclonedx. While not directly enforced by Gerrit, permission audits support SBOM provenance tracking.

## Regulatory & Compliance Frameworks

### SOC 2 Type II

- Requires change management controls (CC6.1, CC7.2). Gerrit's review trail provides audit evidence for:
  - Who approved each change
  - Minimum reviewer counts enforced via label rules
  - Branch protection preventing direct pushes to production branches

### ISO/IEC 27001

- **A.12.1.1** — Documented change management procedures. Gerrit access rules serve as the technical implementation of change control.
- **A.14.1.1** — Change request requirements. Submit permissions enforce approval workflows.

### NIST SP 800-53 (FedRAMP)

- **SA-10** — Developer contribution restrictions. Enforced via Gerrit's `allowed-contributor` rules and review score requirements.
- **CM-2** — Baseline configuration. Repository access rules define the baseline for code contribution.
- **AC-17** — Remote access. SSH/HTTP authentication in Gerrit satisfies access control requirements.

### PCI DSS v4.0

- **Requirement 6.2** — Unauthorized software changes must be documented and approved. Gerrit submit rules provide approval records.
- **Requirement 6.3.2** — Code review before release for public-facing applications.

## Professional Associations

- **OWASP (Open Web Application Security Project)** — Security code review standards and tooling integrations.
- **Cloud Native Computing Foundation (CNCF)** — Gerrit is a CNCF project; SLSA compliance guidance applies.
- **ISPE (International Society for Pharmaceutical Engineering)** — GAMP guidelines for validated change management in regulated environments (GxP).
- **IIBA (International Institute of Business Analysis)** — BABOK alignment for requirements change control workflows.

## Reference Specifications

### Gerrit-Specific

- [Project Configuration File Format](https://gerrit.googlesource.com/gerrit/Documentation/2.16/config-project-config.html) — `project.config` and `groups` file specifications.
- [Prolog Rules Cookbook](https://gerrit.googlesource.com/gerrit/Documentation/2.16/prolog-cookbook.html) — Programmatic submit rules.
- [Access Categories Reference](https://gerrit.googlesource.com/gerrit/Documentation/2.16/access-control.html#access_categories) — Complete list of all permission categories.
- [Account Groups API](https://gerrit.googlesource.com/gerrit/Documentation/2.16/rest-api-groups.html) — Group management via REST.

### Related Tooling

- [Repo Manifest Format](https://source.android.com/docs/setup/create/manifest) — Android manifest XML schema for multi-repository management.
- [git-repo tool](https://gerrit.googlesource.com/git-repo/) — Gerrit-managed repo tool for multi-repo synchronization.
- [Jenkins Gerrit Trigger Plugin](https://plugins.jenkins.io/gerrit-trigger/) — CI integration with review score requirements.
- [Zuul CI Gate](https://zuul-ci.org/docs/zuul/gating.html) — Distributed CI gating with Gerrit integration.

## Security Benchmarks

- **CIS Benchmark for Git Servers** — Configuration hardening guidelines applicable to Gerrit deployments.
- **OWASP ASVS (Application Security Verification Standard)** — V4.0 access control verification requirements align with Gerrit label-based review gates.
- **CWE (Common Weakness Enumeration)** — CWE-284 (Improper Access Control) and CWE-285 (Improper Authorization) are directly mitigated by proper Gerrit permission configuration.
