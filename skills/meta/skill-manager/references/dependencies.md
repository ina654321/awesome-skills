# Skill Dependencies & Versioning

> How to manage skill relationships, dependencies, and versions.

---

## Why Dependencies Matter

In enterprise environments, skills aren't isolated:

```
code-review-skill
  └── requires: security-analysis-skill
                  └── requires: language-model-skill

document-creation-skill
  └── requires: template-engine-skill
  └── conflicts: plain-text-only-mode
```

Without dependency management:
- Silent breakage when a dependency changes
- Version drift causes subtle bugs
- No way to know if a skill can be used standalone

---

## Dependency Declaration

### In SKILL.md Frontmatter

```yaml
---
name: code-reviewer
description: Automated code review with security focus
metadata:
  version: "1.2.0"
  requires:
    - skill: security-analysis
      version: ">=1.0.0"
    - skill: language-model
      version: ">=2.1.0"
  provides:
    - code-review
    - security-feedback
  conflicts:
    - plain-text-mode
---
```

### Dependency Types

| Type | Meaning | Example |
|------|---------|---------|
| `requires` | Must be present | security-analysis |
| `provides` | Capability this skill adds | code-review |
| `conflicts` | Cannot coexist with | plain-text-mode |

### Version Specification

| Format | Meaning | Example |
|--------|---------|---------|
| `>=1.0.0` | Minimum version | Must have at least 1.0.0 |
| `^1.0.0` | Compatible | 1.x.x, not 2.0.0 |
| `~1.0.0` | Patch compatible | 1.0.x, not 1.1.0 |
| `1.0.0` | Exact version | Only 1.0.0 |

---

## Semantic Versioning for Skills

### Version Number Meaning

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ Bug fixes, no new features
  │     └─────── New features, backward compatible
  └───────────── Breaking changes
```

### Versioning Rules

| Change | Version Bump |
|--------|-------------|
| Add new capability | 1.0.0 → 1.1.0 |
| Deprecate a feature | 1.0.0 → 1.1.0 (note deprecation) |
| Remove a feature | 1.0.0 → 2.0.0 |
| Change output format | 1.0.0 → 2.0.0 |
| Fix bug | 1.0.0 → 1.0.1 |
| Improve performance | 1.0.0 → 1.0.1 |

### Changelog

```markdown
# Changelog

## [1.2.0] - 2026-03-25
### Added
- Security analysis integration

### Changed
- Improved output format for JSON responses

## [1.1.0] - 2026-02-15
### Added
- Support for GitHub Enterprise

## [2.0.0] - 2026-01-01
### Removed
- Legacy API support (breaking)
```

---

## Dependency Resolution

### Simple Case

```
skill-a requires: skill-b

User has: skill-b@1.0.0
Result: OK (1.0.0 >= 1.0.0)
```

### Complex Case

```
skill-a requires: skill-b@>=1.0.0
skill-b@2.0.0 is installed

Check: 2.0.0 >= 1.0.0? YES
Result: OK
```

### Conflict Case

```
skill-a conflicts: plain-text-mode
skill-b provides: plain-text-mode

Result: ERROR - Cannot use together
```

---

## Best Practices

### Do

- ✅ Declare dependencies explicitly
- ✅ Use semantic versioning
- ✅ Test with minimum required versions
- ✅ Document what your skill provides

### Don't

- ❌ Don't assume skills exist
- ❌ Don't use exact versions unless necessary
- ❌ Don't create circular dependencies
- ❌ Don't hide implicit dependencies

---

## Tool Support

### Validation

```bash
# Check dependencies
skills-ref deps ./my-skill

# Check circular dependencies
skills-ref deps --check-circular

# Visualize dependency graph
skills-ref deps --graph
```

---

## Enterprise Considerations

### Skill Portfolio

In enterprise, maintain a skill portfolio:

```yaml
# skills.yaml
skills:
  - name: code-reviewer
    version: 1.2.0
    owner: platform-team
  
  - name: security-analysis  
    version: 2.1.0
    owner: security-team
    
  - name: document-generator
    version: 1.0.0
    owner: productivity-team
```

### Approval Workflow

Before adding a new dependency:
1. Review dependency's security
2. Check dependency's maintenance status
3. Verify version compatibility
4. Add to skill portfolio
