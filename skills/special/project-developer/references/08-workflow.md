# awesome-skills Repository — Troubleshooting

## Skill Creation Issues

### SKILL.md Not Triggering on Platform

**Symptom:** The skill doesn't activate when using expected trigger words.

**Diagnosis:**
```bash
# Verify the skill file exists in the correct location
ls -la skills/[category]/[skill-name]/SKILL.md

# Check frontmatter for trigger words
grep -A5 'description' skills/[category]/[skill-name]/SKILL.md

# Verify platforms are listed
grep 'platforms' skills/[category]/[skill-name]/SKILL.md
```

**Common causes and fixes:**

| Cause | Fix |
|-------|-----|
| Trigger words not in description | Add clear trigger phrases to frontmatter description and §13 |
| Platform not listed | Add platform to the `platforms` array in frontmatter |
| Wrong directory structure | Ensure SKILL.md is directly in `skills/[category]/[skill-name]/` |
| YAML syntax error in frontmatter | Run `yamllint SKILL.md` to validate |
| Category mismatch | Move to correct category directory |

**Platform-specific installation verification:**
```bash
# OpenCode
# Install via: /skill install [URL]
# Verify: ~/.opencode/skills/ contains the skill

# Claude Code
# Append to: ~/.claude/CLAUDE.md
# Verify: skill appears when trigger word is used

# Cursor
# Save as: ~/.cursor/rules/[skill-name].mdc (not .md)
# Verify: rule loads in Cursor settings

# Cline
# Append to: .clinerules or Custom Instructions
# Verify: trigger activates the skill
```

### YAML Frontmatter Parsing Errors

**Symptom:** `Error: YAML parse error` or skill fails to load.

**Fix:**
```bash
# Validate YAML syntax
yamllint skills/[category]/[skill-name]/SKILL.md

# Common fixes:
# 1. Indentation must be spaces (not tabs)
# 2. Arrays need dash-space format: [- item1, - item2]
# 3. Multi-line strings need proper pipe or > notation
# 4. No HTML tags inside YAML block
```

**Common frontmatter errors:**
```yaml
# WRONG: Tabs used
description: >
	description text here
	more text

# RIGHT: Spaces only
description: >
    description text here
    more text

# WRONG: Missing dash in array
tags: [gerrit, permissions]

# RIGHT: Proper array format
tags:
  - gerrit
  - permissions

# WRONG: Quotes in wrong places
author: "neo.ai <lucas@email.com>"

# RIGHT: Keep it simple
author: neo.ai
```

### Missing Required Sections

**Symptom:** CI fails with "Missing required section: §X"

**Fix:**
```bash
# Check all 16 sections are present
grep -n "^## " SKILL.md

# Compare against template
cp _template/SKILL.md /tmp/template-sections.md
diff <(grep "^## " SKILL.md) <(grep "^## " /tmp/template-sections.md)
```

**Standard 16-section order:**
1. System Prompt / Role Definition
2. What This Skill Does
3. Risk Disclaimer
4. Core Philosophy / Guiding Principles
5. Platform Support
6. Professional Toolkit
7. Standards & Reference
8. Standard Workflow
9. Scenario Examples
10. Common Pitfalls & Anti-Patterns
11. Integration with Other Skills
12. Scope & Limitations
13. How to Use This Skill
14. Quality Verification / Test Cases
15. Version History
16. License & Author

## Quality Gate Failures

### Score Below Threshold

**Symptom:** PR blocked with "Score <7.0 (Expert threshold)" or "Score <9.5 (Exemplary threshold)".

**Diagnosis:**
```bash
# Calculate rubric score manually
# System Prompt × 0.20
# Domain Knowledge × 0.25
# Workflow × 0.15
# Risk Documentation × 0.10
# Examples/Scenarios × 0.20
# Metadata Completeness × 0.10
```

**Common low-scoring sections and fixes:**

| Section | Common Issue | Fix |
|---------|-------------|-----|
| System Prompt | Generic, <200 chars | Add specific role definition, expertise areas, constraints |
| Domain Knowledge | No industry standards | Add §7 with real regulatory bodies, professional associations |
| Workflow | Too shallow | Add detailed step-by-step procedures |
| Risk Documentation | Missing or <3 risks | Document risks with severity, description, mitigation |
| Examples/Scenarios | Only 1 scenario | Add 3-5 detailed real-world scenarios with outcomes |
| Metadata | Missing tags/platforms | Complete frontmatter fully |

### Broken Link Detection

**Symptom:** CI fails with "Broken link detected" on an internal or external URL.

**Fix:**
```bash
# Check which link is broken
# Look at CI output for the specific URL

# Test external URLs
curl -s -o /dev/null -w "%{http_code}" https://example.com/real-url
# Should return 200

# Test internal relative paths
# From skill directory:
ls -la ../../[referenced-path]

# Fix: Replace broken external links
# Use web.archive.org for archived content
# Or remove non-essential links if no replacement exists

# Fix: Correct internal paths
# WRONG: /images/diagram.png
# RIGHT: ../images/diagram.png (relative to SKILL.md location)
```

### markdownlint Failures

**Symptom:** CI fails with markdown formatting errors.

**Fix:**
```bash
# Run markdownlint locally
npx markdownlint skills/[category]/[skill-name]/SKILL.md

# Common issues and fixes:
# 1. Trailing whitespace
sed -i 's/[[:space:]]*$//' SKILL.md

# 2. Missing blank line before lists
# WRONG:
# Header
# - item
# RIGHT:
# Header
#
# - item

# 3. Fenced code blocks without language
# WRONG:
# ```
# code
# ```
# RIGHT:
# ```bash
# code
# ```

# 4. Heading level skipped
# WRONG: ## Section, #### Subsection
# RIGHT: ## Section, ### Subsection, #### Sub-subsection
```

### Token Overflow Warning

**Symptom:** SKILL.md >500 lines triggers a warning. Some platforms may load slowly.

**Fix:**
```bash
# Count lines
wc -l SKILL.md

# Move extended content to references/
# WRONG: SKILL.md has 600 lines of detailed troubleshooting steps
# RIGHT: SKILL.md has brief summary, references/troubleshooting.md has details

# For §7 Standards:
# WRONG: SKILL.md §7 has 50 URLs and paragraphs of details
# RIGHT: references/07-standards.md has the full content

# Keep SKILL.md to core guidance only
# Use references/ for depth and breadth
```

## Git Workflow Issues

### Branch Naming Violation

**Symptom:** CI fails with "Branch name does not follow convention".

**Fix:**
```bash
# Correct branch types:
git checkout -b feature/[skill-name]         # New skill
git checkout -b fix/[issue-description]      # Bug fix
git checkout -b docs/[topic]                 # Documentation
git checkout -b upgrade/[skill-name]         # Skill upgrade
git checkout -b hotfix/[issue-description]   # Emergency fix

# Rename existing branch
git branch -m old-name feature/[correct-name]

# Update remote
git push origin -u feature/[correct-name]
```

### Commit Message Rejected

**Symptom:** Commit rejected with "Commit message format invalid".

**Fix:**
```bash
# Correct format:
# type(scope): subject (50 chars max, no period)
# blank line
# body (explain what and why)
# blank line
# footer (Closes #issue, Refs #issue)

# WRONG:
git commit -m "fixed stuff"

# CORRECT:
git commit -m "fix(security-engineer): add OWASP Top 10 reference section

- Added OWASP Top 10 2021 to §7 standards
- Maps to CWE-284 and CWE-285 risk mitigations
- Closes #142"

# Amend if already committed
git commit --amend -m "fix([scope]): [subject]"
```

### PR Description Incomplete

**Symptom:** PR blocked with "PR description missing required fields".

**Fix:**
```bash
# Ensure PR description includes:
# 1. ## Summary section
# 2. ## Quality Checklist (all items checked)
# 3. ## Changes
# 4. ## Testing

# Template:
# ## Summary
# [1-3 sentence description]
#
# ## Quality Checklist
# - [x] 16 sections present
# - [x] YAML valid
# - [x] Score: X.X/10
# - [ ] ... other items
#
# ## Changes
# [What changed and why]
#
# ## Testing
# [How was this tested]
```

### Merge Conflict Resolution

**Symptom:** PR has merge conflicts with main.

**Fix:**
```bash
# Fetch and rebase on latest main
git fetch origin
git rebase origin/main

# Resolve conflicts:
# 1. Edit conflicting files
# 2. git add [resolved-files]
# 3. git rebase --continue
# 4. Force push if needed
git push --force-with-lease origin feature/[skill-name]
```

## Version & Release Issues

### Semantic Version Confusion

**Symptom:** Version number doesn't reflect change magnitude.

**Fix:**
```bash
# Version format: MAJOR.MINOR.PATCH

# PATCH (1.0.x → 1.0.1):
# - Bug fixes
# - Typo corrections
# - Link fixes
# - Minor documentation improvements

# MINOR (1.0.0 → 1.1.0):
# - New features
# - New reference materials
# - New workflow steps
# - Expanded scenarios
# - Content additions

# MAJOR (1.0.0 → 2.0.0):
# - Breaking changes (template restructure)
# - New required sections
# - Removing functionality
# - Changing workflow fundamentally

# Wrong examples:
# WRONG: Bug fix → version 1.1.0 (should be 1.0.1)
# WRONG: New example added → version 2.0.0 (should be 1.1.0)
```

### Score Mismatch After Changes

**Symptom:** Modifications changed the quality score but frontmatter wasn't updated.

**Fix:**
```bash
# After significant changes, recalculate score
# Compare new score to old score in frontmatter

# If score improved:
# Update frontmatter: score: X.X/10
# Add version note in §15 Version History

# If score dropped (regression):
# Evaluate if changes are necessary
# Fix sections that dropped in score
# Don't merge if score falls below 7.0 Expert threshold
```

## Reference File Issues

### References Directory Missing

**Symptom:** "references/ directory not found" error.

**Fix:**
```bash
# Create references directory
mkdir -p skills/[category]/[skill-name]/references

# Create standard reference files
touch skills/[category]/[skill-name]/references/07-standards.md
touch skills/[category]/[skill-name]/references/08-troubleshooting.md
touch skills/[category]/[skill-name]/references/09-glossary.md
touch skills/[category]/[skill-name]/references/10-examples.md

# Each file should have domain-specific content
# Reference files are NOT optional — they are part of the quality gate
```

### Circular References or Broken Cross-Links

**Symptom:** Skill links to a file that doesn't exist.

**Fix:**
```bash
# Find all internal links
grep -rn '\[.*\](.*\.md)' SKILL.md references/

# Verify each target exists
# WRONG: [Standards](references/07-standards.md) but file is named differently
# RIGHT: Verify exact filename matches the link

# Common naming issues:
# WRONG: references/standards.md
# RIGHT: references/07-standards.md
```

## CI/CD Pipeline Issues

### Local CI Testing

**Symptom:** Want to run CI checks locally before pushing.

**Fix:**
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all checks
pre-commit run --all-files

# Run specific checks
pre-commit run yamllint
pre-commit run markdownlint
pre-commit run broken-links

# Skip certain checks (use sparingly)
git commit --no-verify -m "..."
```

### CI Timeout on Large Repository

**Symptom:** CI runs exceed time limits on the full repository.

**Fix:**
```bash
# Use path filtering in workflow
# Only run checks on changed skills
jobs:
  quality-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Get changed skills
        id: changed
        run: |
          echo "files=$(git diff --name-only ${{ github.event.pull_request.base.sha }} HEAD \
            | grep 'SKILL.md$' \
            | xargs dirname \
            | sort -u \
            | tr '\n' ',')" >> $GITHUB_OUTPUT
      - name: Run checks on changed skills
        run: |
          for skill in ${{ steps.changed.outputs.files }}; do
            ./scripts/check-skill.sh "$skill"
          done
```

### Pre-commit Hook Not Installed

**Symptom:** Pre-commit hooks aren't running.

**Fix:**
```bash
# Install pre-commit
pip install pre-commit

# Verify installation
pre-commit --version

# Install hooks
pre-commit install

# Update hooks to latest version
pre-commit autoupdate

# Run manually to test
pre-commit run --all-files
```
