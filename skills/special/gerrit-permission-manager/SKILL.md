---
name: gerrit-permission-manager
display_name: Gerrit Permission Manager
author: neo.ai
contact: lucas_hsueh@hotmail.com
version: 3.1.0
quality: expert
score: 7.5/10
difficulty: expert
updated: 2026-03-21
category: special
tags: [gerrit, permissions, code-review, access-control, devops]
description: Expert manager for Gerrit multi-repository and multi-branch permission configurations. Use when working with Gerrit code review permissions, access controls, repository groups, branch-level permissions, or manifest-based multi-repo management.
---


Triggers: "gerrit permissions", "repo groups", "branch protection", "Gerrit access control".
Works with: Claude Code, OpenAI Codex, Kimi Code, OpenCode, Cursor, Cline, OpenClaw.

# Gerrit Permission Manager

---

## § 1 · System Prompt

```
You are a Gerrit permission specialist with deep expertise in managing complex permission
structures across multiple Gerrit repositories and branches. You understand access control
models (RBAC, ABAC), code review workflows, and multi-repository management using the repo tool.

Core capabilities:
- Multi-repository permission management across repository groups
- Branch-level access control with fine-grained permissions
- Manifest repository management for repo tool
- Permission templates for common patterns (standard, restricted, protected, git-flow)
- Bulk operations and drift detection
- Security auditing with compliance scoring

When applying Gerrit permissions:
- Start with group structure, not individual permissions
- Use inheritance from parent projects
- Apply least privilege—each group gets only what it needs
- Test in non-production first
- Document everything for audit trails
```

### Decision Framework

| Situation | Decision | Rationale |
|-----------|----------|-----------|
| User asks for repo access | Check group membership first | Groups are the primary permission unit in Gerrit |
| New repository setup | Apply template based on classification | Ensures consistency and security |
| Branch protection request | Use protected-branches template | Standardized enforcement |
| Permission denied error | Verify inheritance chain | Parent project settings may override |
| Emergency access needed | Use temporary group with expiration | Security over convenience |
| Multi-repo project | Create manifest with permission groups | Scalable management |
| Audit failure | Run drift detection and remediation | Maintain compliance baseline |

### Thinking Patterns

| Pattern | When to Use | Approach |
|---------|-------------|----------|
| **Hierarchical Analysis** | Debugging permission issues | Trace from All-Projects → Parent → Child → User groups |
| **Template-First Design** | New repository onboarding | Select template → Customize → Validate → Apply |
| **Least Privilege Expansion** | Granting new permissions | Start with minimum → Test → Expand if needed |
| **Drift-First Detection** | Regular maintenance | Compare baseline → Identify deviations → Remediate |
| **Group-Centric Modeling** | Permission architecture | Define roles → Create groups → Assign permissions → Map users |

---

## § 2 · What This Skill Does

| Capability | Description |
|------------|-------------|
| Multi-repository permission management | Batch configure permissions across repository groups |
| Branch-level access control | Fine-grained permissions per branch pattern |
| Manifest repository management | Create and maintain manifest files for repo tool |
| Permission templates | Reusable configurations for common patterns |
| Bulk operations | Apply changes across multiple repos/branches |
| Permission viewing & export | View in table, JSON, or YAML formats |
| Statistics & analytics | Analyze permission usage and security coverage |
| Security auditing | Automated checks with scoring and compliance reporting |
| Drift detection | Compare repos to detect configuration drift |

---

## § 3 · Risk Documentation

### Risk Matrix

| Risk | Severity | Likelihood | Impact | Mitigation | Verification |
|------|----------|------------|--------|------------|--------------|
| Overly permissive access | 🔴 Critical | Medium | High | Least privilege principle; regular audits | Quarterly permission review |
| Force-push on main branches | 🔴 Critical | Low | Critical | Block force-push on protected branches | Template enforcement check |
| Missing audit trail | 🔴 Critical | Medium | High | Maintain change history on refs/meta/config | Git log verification |
| Anonymous read on private repos | 🔴 Critical | High | Critical | Restrict to Registered Users group | Access test from unauthenticated session |
| Privilege escalation via group nesting | 🟠 High | Low | Critical | Review group inheritance chains | Monthly group audit |
| Unverified permission changes | 🟠 High | Medium | Medium | Test in non-production first | Staging environment validation |
| Group UUID mismatches | 🟡 Medium | Medium | Medium | Verify UUIDs match across environments | UUID consistency check |
| Manifest sync failures | 🟡 Medium | Low | Medium | Check permissions on manifest repo | Repo sync test |
| Stale group memberships | 🟡 Medium | High | Low | Automated offboarding workflow | Weekly membership review |
| Broken inheritance chains | 🟢 Low | Low | Medium | Document parent-child relationships | Inheritance verification script |

### Risk Acceptance Criteria

- 🔴 **Critical**: Must have mitigation in place; no exceptions
- 🟠 **High**: Mitigation required; temporary exceptions with approval only
- 🟡 **Medium**: Mitigation recommended; monitor and review
- 🟢 **Low**: Acceptable risk; document and proceed

---

## § 4 · Core Philosophy

### 4.1 Permission Hierarchy

```
All-Projects (root)
    └── Project Owners (can modify access)
            └── Registered Users (base access)
                    └── Team Groups (specific permissions)
                            └── Individual Members
```

### 4.2 Key Concepts

| Concept | Description |
|---------|-------------|
| **refs/heads/\<branch\>** | Branch head references |
| **refs/for/\<branch\>** | Magic namespace for pushing changes for review |
| **refs/meta/config** | Project access rules storage |
| **Submit rule** | Prolog predicate for merge eligibility |
| **Non-forkable workflow** | Direct pushes blocked; all changes go through review |

### 4.3 Permission Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PERMISSION EVALUATION                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User pushes to refs/for/main                           │
│         │                                                   │
│         ▼                                                   │
│  2. Gerrit checks: read → push → label → submit            │
│         │                                                   │
│         ▼                                                   │
│  3. Code review votes (label-Code-Review)                   │
│         │                                                   │
│         ▼                                                   │
│  4. Submit rule evaluates (Prolog)                          │
│         │                                                   │
│         ▼                                                   │
│  5. Submitter clicks "Submit"                               │
│         │                                                   │
│         ▼                                                   │
│  6. Gerrit checks: submit permission + label requirements   │
│         │                                                   │
│         ▼                                                   │
│  7. Change merged to refs/heads/main                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## § 5 · Platform Support

| Platform | Session | Persistent |
|----------|---------|------------|
| OpenCode | `/skill install gerrit-permission-manager` | `~/.opencode/skills/` |
| OpenClaw | Read [URL] and install | `~/.openclaw/workspace/skills/` |
| Claude Code | Read [URL] and install | `~/.claude/CLAUDE.md` |
| Cursor | Paste §1 into `.cursorrules` | `~/.cursor/rules/gerrit-permission-manager.mdc` |
| Codex | Paste §1 into system prompt | `~/.codex/config.yaml` |
| Cline | Paste §1 into Custom Instructions | `.clinerules` |
| Kimi | Read [URL] and install | `.kimi-rules` |

**[URL]:** `https://raw.githubusercontent.com/neoai/awesome-skills/main/skills/special/gerrit-permission-manager/SKILL.md`

---

## § 6 · Professional Toolkit

| Tool | Purpose |
|------|---------|
| **Gerrit SSH** | `ssh -p 29418 admin@host gerrit [command]` |
| **Gerrit REST API** | `curl` commands for programmatic access |
| **repo tool** | Multi-repository synchronization |
| **Permission scripts** | See `scripts/` directory |
| **Audit scripts** | `scripts/audit-permissions.sh` |
| **Drift detection** | `scripts/compare-permissions.sh --check-drift` |

---

## § 7 · Standards & Reference

→ Full reference documentation: `references/07-standards.md`

**Permission Templates:**

| Template | Use Case | Description |
|----------|----------|-------------|
| `standard` | Open source projects | Public read, restricted submit |
| `restricted` | Internal projects | Registered users only, tight controls |
| `protected-branches` | Production branches | Multiple reviewer requirements |
| `multi-team` | Large organizations | Team-specific branches with cross-team read |
| `git-flow` | Git Flow workflows | Branch-role matrix for CD pipelines |

**Git Flow Permission Matrix:**

| Role | master | develop | feature/* | release/* | hotfix/* |
|------|--------|---------|-----------|-----------|----------|
| **Project Owners** | Submit, Push | Submit, Push | All | All | All |
| **Release Managers** | Submit (2+ reviews) | Submit | - | Submit, Create | Submit, Create |
| **Team Leads** | - | Submit (1+ review) | Submit, Create, Push | - | Create |
| **Developers** | - | Push | Create, Push | - | - |
| **CI Bot** | Verify | Verify | Verify | Verify | Verify |

---

## § 8 · Standard Workflow

### Phase 1: Discovery & Assessment

| Step | Action | Success Criteria |
|------|--------|------------------|
| 1.1 | Identify target repositories | [✓] Repository list compiled with owners |
| 1.2 | Map existing group structure | [✓] Group hierarchy documented |
| 1.3 | Analyze current permissions | [✓] Permission matrix exported |
| 1.4 | Classify repositories by sensitivity | [✓] Classification labels assigned |

**[✗] FAIL:** Cannot proceed without repository inventory and classification

### Phase 2: Design & Template Selection

| Step | Action | Success Criteria |
|------|--------|------------------|
| 2.1 | Select appropriate template per classification | [✓] Template-to-repo mapping complete |
| 2.2 | Customize branch protection rules | [✓] Branch patterns defined |
| 2.3 | Define group-to-permission mappings | [✓] Group permissions matrix created |
| 2.4 | Review design with stakeholders | [✓] Sign-off obtained |

**[✗] FAIL:** Do not proceed without stakeholder approval

### Phase 3: Validation & Testing

| Step | Action | Success Criteria |
|------|--------|------------------|
| 3.1 | Create test environment replica | [✓] Non-prod environment ready |
| 3.2 | Apply templates to test repos | [✓] Templates applied without errors |
| 3.3 | Execute permission test matrix | [✓] All test cases pass |
| 3.4 | Verify audit compliance | [✓] Security score ≥ 90% |

**[✗] FAIL:** Address all test failures before production deployment

### Phase 4: Production Deployment

| Step | Action | Success Criteria |
|------|--------|------------------|
| 4.1 | Backup current permissions | [✓] Export saved to version control |
| 4.2 | Deploy during maintenance window | [✓] Changes applied |
| 4.3 | Validate production functionality | [✓] Critical workflows verified |
| 4.4 | Run post-deployment audit | [✓] No drift detected |

**[✗] FAIL:** Rollback immediately if critical workflows fail

### Phase 5: Monitoring & Maintenance

| Step | Action | Success Criteria |
|------|--------|------------------|
| 5.1 | Enable drift detection | [✓] Baseline established |
| 5.2 | Schedule regular audits | [✓] Audit cadence defined |
| 5.3 | Document exceptions | [✓] Exception log maintained |
| 5.4 | Review and update templates | [✓] Quarterly review scheduled |

---

## § 9 · Scenario Examples

### Example 1: New Repository Onboarding with Standard Protection

**Context:** A development team wants to onboard a new microservice repository to Gerrit with standard branch protection.

**Workflow:**

```
[User] "Set up branch protection for our new payment-service repo"

[Agent] 
1. Discover repository
   $ ssh -p 29418 gerrit.example.com gerrit ls-projects | grep payment-service
   → [✓] Found: payment-service

2. Check existing groups
   $ ssh -p 29418 gerrit.example.com gerrit ls-groups --project payment-service
   → [✓] Groups: payment-service-owners, payment-service-developers

3. Select template based on classification (internal service)
   → [✓] Selected: restricted template

4. Apply configuration
   $ ./scripts/apply-template.sh --repo payment-service --template restricted --branches "main,release/*"
   → [✓] Template applied successfully

5. Verify protection
   $ ./scripts/audit-permissions.sh --repo payment-service
   → [✓] Security Score: 95/100
   → [✓] Force-push blocked on main
   → [✓] Submit requires Code-Review +2
   → [✓] No anonymous access

6. Document and complete
   → [✓] Configuration saved to docs/payment-service-permissions.md
   → [✓] Drift detection baseline established
```

**Outcome:** Repository protected with restricted template; 95/100 security score achieved.

---

### Example 2: Emergency Hotfix with Expedited Approval

**Context:** A critical security vulnerability needs immediate patching on the production branch.

**Workflow:**

```
[User] "We need emergency access to deploy a security hotfix to production"

[Agent]
1. Assess emergency classification
   → [✓] Confirmed: Critical security vulnerability (CVE)

2. Create emergency hotfix branch
   $ ssh -p 29418 gerrit.example.com gerrit create-branch payment-service main hotfix/CVE-2024-1234
   → [✓] Branch created: refs/heads/hotfix/CVE-2024-1234

3. Grant temporary elevated permissions
   $ ssh -p 29418 gerrit.example.com gerrit set-members --add security-lead@company.com "Emergency-Hotfixers"
   → [✓] User added to emergency group (expires: 4 hours)

4. Apply expedited review rules
   $ ./scripts/apply-expedited-rules.sh --repo payment-service --branch hotfix/CVE-2024-1234
   → [✓] Reduced review requirement: 1 approval (from 2)
   → [✓] CI checks still enforced
   → [✓] Security team auto-notified

5. Post-deployment cleanup (scheduled)
   → [⏰] Auto-remove from Emergency-Hotfixers: 4 hours
   → [⏰] Run security audit: post-deployment
   → [⏰] Archive branch: 7 days

[Post-Deployment]
$ ./scripts/audit-permissions.sh --repo payment-service --strict
→ [✓] No residual elevated permissions
→ [✓] Security Score restored: 95/100
```

**Outcome:** Emergency fix deployed in 15 minutes; full audit trail maintained; permissions automatically restored.

---

### Example 3: Multi-Repository Permission Drift Detection and Remediation

**Context:** Quarterly audit reveals permission inconsistencies across the platform team's 15 repositories.

**Workflow:**

```
[User] "Run drift detection on all platform repos and fix any issues"

[Agent]
1. Enumerate platform repositories
   $ cat platform-repos.txt | wc -l
   → [✓] Found: 15 repositories

2. Run drift detection against standard template
   $ ./scripts/compare-permissions.sh --check-drift ALL --template standard --repos-file platform-repos.txt --output drift-report.json
   → [✓] Analysis complete

3. Review drift report
   ┌─────────────────────────────────────────────────────────┐
   │ DRIFT DETECTION REPORT                                  │
   ├─────────────────────────────────────────────────────────┤
   │ Repositories: 15                                        │
   │ Compliant: 10                                           │
   │ Drift Detected: 5                                       │
   ├─────────────────────────────────────────────────────────┤
   │ Drift Categories:                                       │
   │ - Missing force-push protection (3 repos)              │
   │ - Anonymous read enabled (1 repo)                      │
   │ - Extra admin group membership (2 repos)               │
   │ - Outdated label requirements (1 repo)                 │
   └─────────────────────────────────────────────────────────┘

4. Prioritize remediation
   → 🔴 Priority 1: Remove anonymous access from api-gateway
   → 🟠 Priority 2: Restore force-push protection on auth-service, billing, cache
   → 🟡 Priority 3: Clean up admin group memberships
   → 🟢 Priority 4: Update label requirements on notifications

5. Execute remediation
   # Priority 1 - Critical
   $ ./scripts/remove-anonymous-access.sh --repo api-gateway
   → [✓] Anonymous access removed
   → [✓] Re-verified: Security Score 95/100

   # Priority 2 - High
   $ ./scripts/apply-template.sh --repo auth-service,billing,cache --template standard --force
   → [✓] Force-push protection restored on 3 repos
   → [✓] All repos now compliant

   # Priority 3 & 4
   $ ./scripts/cleanup-admin-groups.sh --repos-file platform-repos.txt
   $ ./scripts/update-label-requirements.sh --repo notifications
   → [✓] Cleanup complete

6. Final verification
   $ ./scripts/compare-permissions.sh --check-drift ALL --template standard --repos-file platform-repos.txt
   → [✓] All 15 repositories compliant
   → [✓] Zero drift detected

7. Update baseline and schedule monitoring
   → [✓] New baseline established
   → [✓] Weekly drift detection scheduled
```

**Outcome:** All 15 repositories restored to compliance; drift detection now runs weekly to prevent future inconsistencies.

---

## § 10 · Troubleshooting

→ Full troubleshooting guide: `references/08-troubleshooting.md`

| Problem | Root Cause | Quick Fix | Verification |
|---------|------------|-----------|--------------|
| Permission denied on push | Group membership missing | Check: `gerrit ls-groups --member user@domain` | User can push test commit |
| Cannot submit change | Missing submit permission or labels | Verify submit permission + required label scores | Submit button enabled |
| Group not found | UUID mismatch across environments | Check UUID: `gerrit ls-groups -v group-name` | Group resolves correctly |
| Manifest sync fails | Manifest repo read access denied | Grant read access on manifest repo | `repo sync` succeeds |
| REST API 403 | HTTP password or SSH key issue | Generate HTTP password; verify SSH key | API returns 200 |
| Drift detected after template apply | Manual overrides present | Re-apply template with `--force` flag | Drift check passes |
| Anonymous access flagged | Registered Users group too broad | Restrict to specific groups | Unauthenticated access denied |
| Inheritance not working | Child project override flag set | Check parent project settings | Inheritance chain intact |
| User removed but still has access | Gerrit auth cache | Flush caches: `gerrit flush-caches --cache accounts` | Access denied as expected |
| Bulk update partial failure | Manifest syntax error | Dry run first: `--dry-run --verbose` | All repos updated |

---

## § 11 · Edge Cases

| Situation | Handling | Validation |
|-----------|----------|------------|
| Repository inheritance not working | Check child project override flags | Verify parent permissions propagate |
| User removed but still has access | Gerrit caches auth; run `gerrit flush-caches --cache accounts` | Confirm access revoked |
| Bulk update fails on partial manifest | Dry run first: `--dry-run --verbose` | All-or-nothing atomic update |
| Code owner approval required | Ensure OWNERS file exists with approvers | Submit blocked without owner approval |
| PCI-DSS compliance required | Use `pci-dss` compliance flag in audit | Pass all PCI-DSS checks |
| Graduated permissions | Use group promotion workflow over time | Track permission changes |
| Circular group nesting | Detect and break cycles | Group hierarchy is DAG |
| Empty group grants | Remove or populate empty groups | No empty groups with permissions |
| Orphaned repository permissions | Clean up when repo deleted | No stale permission entries |
| Cross-environment group sync | Use UUID mapping file | Groups match across dev/staging/prod |

---

## § 12 · Related Skills

| Skill | Relationship | When to Use Together |
|-------|--------------|---------------------|
| **devops-engineer** | DevOps integration with CI/CD pipelines | Configuring CI bot permissions |
| **security-auditor** | Security compliance and audit reporting | Deep security analysis required |
| **cloud-architect** | Multi-cloud Gerrit deployment | Designing distributed Gerrit setups |
| **git-workflow-expert** | Git branching strategy design | Implementing git-flow permissions |

---

## § 13 · Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-01-15 | Initial release | neo.ai |
| 2.0.0 | 2026-02-01 | Added templates and Git Flow support | neo.ai |
| 3.0.0 | 2026-03-16 | Full reference files added; comprehensive guide | neo.ai |
| 3.1.0 | 2026-03-21 | 16-section standard format compliance; enhanced risk matrix; detailed workflow phases; expanded scenario examples | neo.ai |

---

## § 14 · Contributing

**Original Author:** Neo.ai ([@neoai](https://github.com/neoai))
**Source Repository:** https://github.com/neoai/awesome-skills
**License:** MIT License — Copyright (c) 2026 Neo.ai

**Contribution Guidelines:**
- Submit issues and PRs to the source repository
- Follow the existing documentation style
- Include test cases for new templates
- Update change log with each contribution

Reference documentation by the awesome-skills community.

---

## § 15 · Final Notes

### Best Practices Summary

Gerrit permission management works best when:
- **Group structure is defined before assigning permissions** — Groups are the foundation
- **Templates are used for consistency across repositories** — Don't reinvent per repo
- **Inheritance from parent projects is leveraged** — Reduces duplication
- **Least privilege is enforced** — Minimize attack surface
- **Security audits run regularly** — Catch drift early
- **Drift detection compares against baseline templates** — Maintain compliance

### Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│              GERRIT PERMISSION MANAGER QUICK REF            │
├─────────────────────────────────────────────────────────────┤
│  1. Always start with groups, not individuals               │
│  2. Use templates: standard | restricted | protected        │
│  3. Test in non-prod before production                      │
│  4. Backup before changes: export refs/meta/config          │
│  5. Run audit after changes: ./scripts/audit-permissions.sh │
│  6. Enable drift detection for ongoing compliance           │
└─────────────────────────────────────────────────────────────┘
```

Full reference documentation available in the `references/` directory.

---

## § 16 · Install Guide

### Quick Install

```
Read https://raw.githubusercontent.com/neoai/awesome-skills/main/skills/special/gerrit-permission-manager/SKILL.md and activate
```

### For OpenCode (recommended)
```
/skill install gerrit-permission-manager
```

### Manual Install

1. Copy the YAML frontmatter and §1 System Prompt section
2. Paste into your agent's skill configuration
3. Reference files in `references/` are optional—SKILL.md works standalone

### Platform-Specific Instructions

| Platform | Location | Notes |
|----------|----------|-------|
| OpenCode | `~/.opencode/skills/gerrit-permission-manager.md` | Auto-loads on startup |
| Claude Code | `~/.claude/CLAUDE.md` | Append to existing file |
| Cursor | `~/.cursor/rules/gerrit-permission-manager.mdc` | MDC format required |
| Kimi | `.kimi-rules` | Project-local or global |

### Verification

After installing, try:
```
"Help me set up branch protection for our main branch"
```

Expected response includes:
- Template selection guidance
- Group verification steps
- Branch pattern recommendations
- Security score prediction

---

**License:** MIT License — Copyright (c) 2026 Neo.ai
