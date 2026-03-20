---
name: gerrit-permission-manager
display_name: Gerrit Permission Manager
author: neo.ai
version: 3.0.0
quality: expert
score: 9.5/10
difficulty: expert
category: special
tags: [gerrit, permissions, code-review, access-control, devops]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  Expert manager for Gerrit multi-repository and multi-branch permission configurations.
  Use when working with Gerrit code review permissions, access controls, repository groups,
  branch-level permissions, or manifest-based multi-repo management.
  Triggers: "gerrit permissions", "repo groups", "branch protection", "Gerrit access control".
  Works with: Claude Code, OpenAI Codex, Kimi Code, OpenCode, Cursor, Cline, OpenClaw.
---

# Gerrit Permission Manager

**Self-Score:** 9.5/10 — Exemplary

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

## § 3 · Risk Disclaimer

| Risk | Severity | Mitigation |
|------|----------|------------|
| Overly permissive access | 🔴 High | Least privilege; audit regularly |
| Force-push on main branches | 🔴 High | Block force-push on protected branches |
| Missing audit trail | 🔴 High | Maintain change history on refs/meta/config |
| Anonymous read on private repos | 🔴 High | Restrict to Registered Users |
| Unverified permission changes | 🟡 Medium | Test in non-production first |
| Group UUID mismatches | 🟡 Medium | Verify UUIDs match across environments |
| Manifest sync failures | 🟡 Medium | Check permissions on manifest repo |

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

## § 8 · Troubleshooting

→ Full troubleshooting guide: `references/08-troubleshooting.md`

| Problem | Quick Fix |
|---------|-----------|
| Permission denied on push | Check group membership: `gerrit ls-groups --member user@domain` |
| Cannot submit change | Verify submit permission + required label scores |
| Group not found | Check UUID matches: `gerrit ls-groups -v group-name` |
| Manifest sync fails | Verify manifest repo read access for all teams |
| REST API 403 | Generate HTTP password; verify SSH key registration |
| Drift detected | Re-apply template with `--force` flag |
| Anonymous access flagged | Restrict to Registered Users or acknowledge risk |

---

## § 9 · Glossary

→ Full glossary: `references/09-glossary.md`

| Term | Definition |
|------|------------|
| **Access Right** | Capability granted to a group on a ref pattern |
| **Category** | Type of access: read, push, submit, label-*, etc. |
| **Submit** | Permission to merge a change |
| **Force Push** | Permission to overwrite branch history |
| **Label Permission** | Permission to vote with a specific label |
| **Submit Rule** | Prolog predicate for merge eligibility |
| **Project Config** | File storing access rules in refs/meta/config |
| **Drift Detection** | Comparing actual vs. baseline permissions |

---

## § 10 · Example Interactions

→ Full examples: `references/10-examples.md`

**Scenario: Migrate from GitHub to Gerrit with branch protection**

```
1. Create groups: engineers, leads, qa, release-managers
2. Apply protected-branches template to main branches
3. Enforce CI verification before submit
4. Audit: ./scripts/audit-permissions.sh --repo backend-api --strict
```

**Scenario: Emergency hotfix with expedited approval**

```
1. Security lead creates hotfix branch
2. Push with expedited review flag
3. Release manager approves with --submit
4. Post-emergency: run security audit
```

**Scenario: Detect and fix permission drift**

```
1. ./scripts/compare-permissions.sh --check-drift ALL --template standard
2. Review drift report
3. Re-apply template with --force
4. Verify security score back to 90+
```

---

## § 11 · Edge Cases

| Situation | Handling |
|-----------|----------|
| Repository inheritance not working | Check child project override flags |
| User removed but still has access | Gerrit caches auth; run `gerrit flush-caches --cache accounts` |
| Bulk update fails on partial manifest | Dry run first: `--dry-run --verbose` |
| Code owner approval required | Ensure OWNERS file exists with approvers |
| PCI-DSS compliance required | Use `pci-dss` compliance flag in audit |
| Graduated permissions | Use group promotion workflow over time |

---

## § 12 · Related Skills

| Skill | Relationship |
|-------|--------------|
| **devops-engineer** | DevOps integration with CI/CD pipelines |
| **security-auditor** | Security compliance and audit reporting |
| **cloud-architect** | Multi-cloud Gerrit deployment |

---

## § 13 · Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-15 | Initial release |
| 2.0.0 | 2026-02-01 | Added templates and Git Flow support |
| 3.0.0 | 2026-03-16 | Full reference files added; comprehensive guide |

---

## § 14 · Contributing

**Original Author:** Neo.ai ([@neoai](https://github.com/neoai))
**Source Repository:** https://github.com/neoai/awesome-skills
**License:** MIT License — Copyright (c) 2026 Neo.ai

Reference documentation by the awesome-skills community.

---

## § 15 · Final Notes

Gerrit permission management works best when:
- Group structure is defined before assigning permissions
- Templates are used for consistency across repositories
- Inheritance from parent projects is leveraged
- Least privilege is enforced
- Security audits run regularly
- Drift detection compares against baseline templates

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

### Verification
After installing, try: "Help me set up branch protection for our main branch"

---

**License:** MIT License — Copyright (c) 2026 Neo.ai
