# awesome-skills Repository — Real-World Examples

## Example 1: Blocked Merge Due to Quality Gate Failure

**Context:** A contributor submits a new skill for "coffee-roasting-expert" claiming a score of 9.5/10 (Exemplary). The PR passes the YAML lint check but fails the quality gate review.

**Analysis:**
```
Rubric Evaluation:
- System Prompt: 4/10 — Generic role description, no domain specifics
- Domain Knowledge: 3/10 — No mention of roast levels, temperature curves, or bean origins
- Workflow: 7/10 — Basic steps present but shallow
- Risk Documentation: 2/10 — No risks documented
- Examples/Scenarios: 5/10 — Only 1 generic scenario
- Metadata: 9/10 — Frontmatter complete and correct

Weighted Score: 4.85/10
```

**Action Taken:**
> **BLOCKED — Score below Expert threshold (7.0)**
>
> **Required Fixes:**
> 1. Rewrite §1 System Prompt with coffee-roasting domain specifics: bean varieties (Arabica, Robusta), roast levels (light, medium, dark), temperature development, first/second crack
> 2. Add §7 industry references: SCA (Specialty Coffee Association), roast profiling standards, SCAA guidelines
> 3. Add 5+ risks: uneven heat distribution, fire risk, under-roasting (food safety), over-roasting (bitter compounds), moisture loss miscalculation
> 4. Expand to 3 detailed scenarios: light roast for Ethiopian single-origin, dark roast for espresso blend, profiling a seasonal micro-lot
> 5. Self-reassess score honestly
>
> **Estimated gap:** +4.15 points needed
>
> **Feedback sent to contributor with specific examples of exemplary skills in adjacent domains (e.g., tea-master, instrument-maker) for reference.

---

## Example 2: Scope Creep Detection and Rejection

**Context:** A contributor submits a PR for a skill called "data-engineering-expert" that attempts to cover data ingestion, transformation, warehousing, ML pipelines, visualization, and governance — 5 distinct subdomains.

**Analysis:**
```
Scope Check:
- Attempted domains: data ingestion, ETL, data warehousing, ML pipelines, 
  visualization, data governance
- This is a "jack of all trades, master of none" skill
- Each subdomain could be a separate skill with proper depth
- Violates: "One skill = one domain" principle
```

**Action Taken:**
> **REJECTED — Scope covers multiple domains**
>
> **Decision:** The skill must be split into focused, single-domain skills:
> 1. **data-ingestion-specialist** — API integrations, streaming (Kafka), batch collection
> 2. **data-warehouse-engineer** — Star schema, dbt, Snowflake/BigQuery
> 3. **ml-pipeline-builder** — Feature stores, model training, MLOps
>
> **Contributor guidance:**
> - Review existing skills in the software/data directory
> - Choose the most needed subdomain in your context
> - Reference the skill-writer rubric for target depth per subdomain
> - Each skill needs ~10 reference files covering that subdomain specifically

---

## Example 3: Broken Link Remediation via CI

**Context:** During a routine CI run, the link checker detects that `skills/automotive/simulation-platform-engineer/references/07-standards.md` references `https://example.com/asam-openx` — a fake placeholder URL submitted months ago.

**Analysis:**
```
Link Check Result:
FAIL: skills/automotive/simulation-platform-engineer/references/07-standards.md
  - Broken: https://example.com/asam-openx (placeholder, HTTP 404)
  - Expected: Real ASAM OpenX standard URL
```

**Fix:**
```bash
# Identify the correct real URL
# ASAM OpenX standard: https://www.asam.net/standards/detail/asam-openx/

# Update the file
# Edit the placeholder URL to the real ASAM documentation
# Reference: ASAM OpenX SCNX file format for scenario exchange

# Verify the fix
./scripts/verify-links.sh --file skills/automotive/simulation-platform-engineer/references/07-standards.md
PASS
```

**Root cause:** Contributor used a placeholder URL during initial submission. Pre-commit hooks did not catch it because the broken link detector only ran in CI, not as a pre-commit check.

**Process improvement added:**
> A pre-commit hook is now configured to run link validation locally:
> ```bash
> # .pre-commit-config.yaml
> - repo: local
>   hooks:
>     - id: broken-link-checker
>       name: Verify all URLs return HTTP 200
>       entry: ./scripts/check-links.sh
>       language: script
> ```

---

## Example 4: Emergency Skill Hotfix for API Deprecation

**Context:** The `claude-code-best-practices` skill references the Claude API v1 (`api.anthropic.com/v1/complete`) which was deprecated and replaced by the Messages API. All existing code examples in the skill now return errors.

**Detection:**
```bash
# CI catches this during scheduled maintenance scan
# API deprecation check: Compare referenced endpoints against current API docs
WARN: skills/software/claude-code-best-practices/SKILL.md
  - Deprecated: api.anthropic.com/v1/complete (v1 completion API)
  - Current: api.anthropic.com/v1/messages
```

**Fix:**
```bash
# Create hotfix branch
git checkout -b hotfix/claude-code-api-v1-deprecation

# Update all code examples in §6 and §8
# From:
curl -X POST https://api.anthropic.com/v1/complete \
  -H "x-api-key: $ANTHROPIC_KEY" \
  -d '{"prompt": "..."}'

# To:
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model": "claude-3-sonnet-20240229", "messages": [{"role": "user", "content": "..."}]}'

# Version bump
# Update frontmatter: version 1.2.3 → 1.2.4 (patch for bug fix)
```

**Outcome:** All API examples updated to current endpoint. Skill remains functional. Version bumped from `1.2.3` to `1.2.4`.

---

## Example 5: Automated Rubric Scoring Pipeline

**Context:** The maintainers want to automate the quality rubric scoring so that every PR automatically gets a score comment without manual review.

**Implementation:**
```yaml
# .github/workflows/quality-score.yml
name: Quality Score
on:
  pull_request:
    paths:
      - 'skills/**/SKILL.md'

jobs:
  score:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Calculate rubric score
        id: score
        run: |
          # Parse SKILL.md and calculate weighted score
          # Read each section, evaluate against rubric dimensions
          # Output: JSON with dimension scores and final weighted score
          python scripts/calculate-score.py \
            --file ${{ github.event.pull_request.changed_files }} \
            --output score.json
          echo "score=$(cat score.json)" >> $GITHUB_OUTPUT

      - name: Post score comment
        uses: actions/github-script@v7
        with:
          script: |
            const score = JSON.parse('${{ steps.score.outputs.score }}');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Quality Score\n\n` +
                `| Dimension | Score |\n` +
                `|-----------|-------|\n` +
                `| System Prompt | ${score.system_prompt}/10 |\n` +
                `| Domain Knowledge | ${score.domain_knowledge}/10 |\n` +
                `| Workflow | ${score.workflow}/10 |\n` +
                `| Risk Documentation | ${score.risk}/10 |\n` +
                `| Examples | ${score.examples}/10 |\n` +
                `| Metadata | ${score.metadata}/10 |\n\n` +
                `**Final Score: ${score.final}/10** (${score.tier})\n\n` +
                `| Gate | Threshold | Result |\n` +
                `|------|----------|--------|\n` +
                `| Expert | ≥7.0 | ${score.final >= 7.0 ? '✅ Pass' : '❌ Fail'} |\n` +
                `| Exemplary | ≥9.5 | ${score.final >= 9.5 ? '✅ Pass' : '❌ Fail'} |`
            });
```

**Result:** Every PR automatically receives a quality score comment with dimension breakdown and gate pass/fail status within minutes of opening.

---

## Example 6: Converting a Basic Skill to Exemplary

**Context:** The `forklift-operator` skill is rated Basic (5.5/10) with minimal content. A contributor volunteers to upgrade it to Exemplary.

**Gap Analysis:**
```
Current State:
- System Prompt: 5/10 — Generic OSHA reference, no forklift specifics
- Domain Knowledge: 4/10 — No mention of truck types (Class I-V), load centers, 
  blind spots, pedestrian safety
- Workflow: 6/10 — Basic operational steps, missing pre-ops inspection
- Risk Documentation: 3/10 — Only "tip-over" mentioned
- Examples/Scenarios: 4/10 — One scenario, incomplete
- Metadata: 9/10 — Frontmatter correct

Target: Exemplary ≥9.5
Gap: +4.0 points
```

**Upgrade Plan:**
1. **System Prompt**: Add forklift classification system (Class I electric sit-down, Class II electric narrow aisle, Class IV/IC pneumatic), manufacturer distinctions (Toyota, Hyster, Yale), capacity/rated load terminology
2. **Domain Knowledge**: Add load center charts, capacity calculation formulas, pre-operation inspection checklist (ASTM F2377, OSHA 1910.178), refueling/charging procedures, pedestrian crosswalk protocols
3. **Workflow**: Add detailed pre-ops inspection flow, daily checklist, dock plate procedures, rack repair flagging
4. **Risk Documentation**: Add 10+ risks: tip-over (most common fatality), load drop, dock collapse, pedestrian strike, fork punctures, blind spot accidents, refueling fires, improper stacking collapse, exceeds capacity, brake failure
5. **Examples**: Expand to 5 scenarios: warehouse receiving, narrow aisle maneuvering, dock loading, rack repair flagging, pedestrian-heavy area navigation

**Result:** Skill upgraded to 9.6/10 Exemplary. Merged after one round of minor feedback (added a missing ANSI/ITSDF B56.1 standard reference).

---

## Example 7: Merge Conflict Resolution Across Skill Categories

**Context:** Two contributors submit PRs for skills named `security-engineer` and `devops-engineer` in the same week. Both reference a shared "risk-assessment" template in §3 that they each modified independently. When merged, the shared content diverges.

**Problem:**
```
PR #312: skills/software/security-engineer/SKILL.md
  - §3 Risk Disclaimer uses custom template with 12 risks
  - Uses "risk matrix" format

PR #315: skills/software/devops-engineer/SKILL.md
  - §3 Risk Disclaimer independently modified the same template
  - Uses "risk table" format
  - Has 15 risks (3 new DevOps-specific ones)
```

**Resolution:**
> **Decision:** Merge both PRs but standardize the risk disclaimer format across all software skills.
>
> 1. Accept both sets of domain-specific risks (12 + 3 = 15 total across both)
> 2. Standardize to a consistent table format across both skills
> 3. Create shared risk terminology glossary in references/09-glossary.md
> 4. Add both contributors to a "Software Skill Maintainers" group for future coordination
> 5. Document the standardization in an internal RFC
>
> **Action:**
> ```bash
> # Create standardization RFC
> git checkout -b docs/risk-disclaimer-standardization
> # Update both skills to use shared format
> # Merge docs branch first
> # Then rebase PRs #312 and #315 on updated main
> ```

---

## Example 8: Version Bump Decision for Breaking Change

**Context:** The skill template is upgraded from 16 sections to 18 sections (added §11 Integration and §17 Deprecation Policy). This is a breaking change for all existing skills.

**Decision:**
```
Change Type: Major (template restructuring with new required sections)
Action: Bump template version 1.0.0 → 2.0.0
```

**Migration Plan:**
```bash
# Phase 1: Update template
git checkout -b feat/template-v2
# Add §11 and §17 to _template/SKILL.md
# Version bump template: 1.0.0 → 2.0.0
# Merge to main

# Phase 2: Notify contributors
# Open GitHub issue per skill: "Template v2 migration needed"
# Labels: "good-first-issue", "template-migration"
# Assign to existing maintainers per category

# Phase 3: Migrate skills (1 per PR)
git checkout -b upgrade/[skill-name]-template-v2
# Fill in new sections following template v2
# Version bump: (e.g., 1.2.0 → 2.0.0)
# Score may change — recalculate and update frontmatter
```

**Timeline:** 4 weeks for migration of all skills. Skills not migrated within 4 weeks are archived with a deprecation notice.

**Communication:**
> **Migration Guide Released for Template v2**
>
> All skill contributors: Template v2 is now live with 2 new required sections.
>
> **What changed:**
> - Added §11: Integration with Other Skills
> - Added §17: Deprecation Policy
>
> **Action required:**
> - Migrate your skills within 4 weeks
> - Follow the migration guide in docs/TEMPLATE-MIGRATION.md
> - Version bump your skill to 2.0.0
> - Re-run quality scoring and update frontmatter

---

## Example 9: Rejecting a Skill with Plagiarized Content

**Context:** A submitted skill for "interior-designer" contains large sections copied verbatim from an online blog without attribution, and the quality score self-assessment claims 9.0/10.

**Detection:**
```
Content Analysis:
- §7 Standards & Reference: 4 paragraphs copied from Houzz.com blog 
  (no attribution, no link)
- §8 Workflow: 80% overlap with an Architectural Digest article
  (source URL present but no quotation marks, presented as original)
- Score self-assessment: 9.0/10

Plagiarism Check Result: FAIL
Copied content without attribution: 4 paragraphs
```

**Action Taken:**
> **REJECTED — Plagiarized content**
>
> This submission violates the MIT license and the repository's contribution guidelines.
>
> **Requirements for resubmission:**
> 1. Rewrite all copied content in original language
> 2. Properly attribute all referenced sources with direct links
> 3. Write original domain-specific content for §7 (industry standards, 
>    NKBA guidelines, ADA compliance, local building codes)
> 4. Self-assess score honestly
>
> **Contributor notified with:**
> - Specific paragraphs flagged with source URLs
> - Link to the MIT license requirement for attribution
> - Reference to original skill-writer guidance on avoiding plagiarism
> - Note that resubmission will be reviewed more carefully for originality

---

## Example 10: Multi-Platform Skill Installation Verification

**Context:** A skill is submitted with platform support listed as `[opencode, openclaw, claude, cursor]`. A reviewer tests the skill installation on each listed platform and finds it only works on Claude Code.

**Test Results:**
```
Platform Installation Test:
- OpenCode: ❌ FAIL — Skill path uses "~/.claude/" which doesn't exist on OpenCode
- OpenClaw: ⚠️ PARTIAL — Installs but system prompt section uses Claude-specific syntax
- Claude Code: ✅ PASS — Full installation and trigger word activation works
- Cursor: ❌ FAIL — .cursorrules format uses triple backticks fences, not supported

Issue: Platform-specific installation paths and syntax not validated
```

**Fix:**
```bash
# Contributor updates §5 Platform Support with correct installation per platform

# For OpenCode:
# Installation command: /skill install [URL]

# For OpenClaw:
# Installation command: Read [URL] and install as skill

# For Claude Code:
# Append to ~/.claude/CLAUDE.md (global)
# Append to CLAUDE.md (project-level)

# For Cursor:
# Save as ~/.cursor/rules/[skill-name].mdc (global)
# Use .cursor/rules format, not triple backtick fences
```

**Review checklist updated:**
> **New platform support checklist item:**
> - [ ] Installation command tested on EACH listed platform
> - [ ] Platform-specific paths verified (e.g., ~/.opencode vs ~/.claude)
> - [ ] Syntax validated per platform (Cursor uses .mdc, Claude uses append-to-CLAUDE.md)
> - [ ] Trigger word activation confirmed on each platform
