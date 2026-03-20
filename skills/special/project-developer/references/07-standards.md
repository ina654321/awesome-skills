# Standards & Reference

## 7.1 Repository Structure

### Directory Layout
```
/awesome-skills
├── skills/                    # All skill directories
│   ├── [category]/           # Category folders
│   │   └── [skill-name]/    # Individual skill
│   │       ├── SKILL.md     # Main skill file
│   │       └── references/  # Reference materials
│   └── _template/           # Skill template
├── .github/                  # GitHub workflows
├── CONTRIBUTING.md           # Contribution guidelines
├── README.md                # Repository readme
└── docs/                    # Documentation
```

### Skill Naming Convention
- Lowercase with hyphens: `agent-persona-designer`
- Alphanumeric and hyphens only
- Max 40 characters
- Unique within repository

## 7.2 Git Workflow Standards

### Branch Naming
| Branch Type | Pattern | Example |
|------------|---------|---------|
| Feature | `feature/[skill-name]` | `feature/new-music-skill` |
| Bugfix | `fix/[issue-description]` | `fix/readme-broken-link` |
| Documentation | `docs/[topic]` | `docs/api-reference` |

### Commit Message Format
```
type(scope): description

Types: feat, fix, docs, refactor, test, chore
Scope: skill name, infrastructure, docs

Examples:
feat(skills): add new music composition skill
fix(agent-persona-designer): correct typo in workflow
docs(readme): update installation instructions
```

### Pull Request Requirements
- Title: Clear, descriptive, references issue
- Description: What changed, why, how to test
- Checklist: All items from PR template completed
- Reviews: Minimum 1 approval for skills
- CI: All checks must pass

## 7.3 Skill Quality Gates

### Gate 1: Metadata
- [ ] YAML frontmatter complete (name, description, tags, author, version)
- [ ] Display name matches directory name convention
- [ ] Description is 50-500 characters
- [ ] Tags follow approved taxonomy

### Gate 2: Structure
- [ ] SKILL.md follows 16-section template
- [ ] All required H2 sections present
- [ ] System prompt properly formatted
- [ ] References directory exists with files

### Gate 3: Content
- [ ] No placeholder content (e.g., "example.com")
- [ ] Real resources referenced (no fake URLs)
- [ ] Domain-specific terminology used correctly
- [ ] Quality score self-assessed honestly

### Gate 4: Automation
- [ ] Links verified (no broken links)
- [ ] Images use relative paths or absolute URLs
- [ ] No HTML in YAML blocks
- [ ] Proper markdown formatting

## 7.4 Resources

### Documentation
- **Contributing Guide**: CONTRIBUTING.md
- **Skill Template**: `skills/_template/SKILL.md`
- **Quality Rubric**: See quality scoring guidelines
- **Platform Support Matrix**: Supported AI assistant platforms

### Tools
- **Markdown Linting**: markdownlint for formatting
- **Link Checking**: verify-links workflow
- **Spell Check**: cspell for technical terms
- **YAML Validation**: yamllint for frontmatter