# CI/CD Automation Guide

This document describes the continuous integration and quality assurance pipeline for the Awesome Skills repository.

## Overview

The CI/CD pipeline consists of multiple automated workflows:

1. **Skill Quality Gate** - Runs on every PR to check skill quality
2. **Daily Optimization Scan** - Daily comprehensive quality analysis
3. **PR Skill Review** - Automated review comments on skill changes
4. **Runtime Validation** - Validates skill runtime performance

## Workflows

### 1. Skill Quality Gate (`skill-quality-gate.yml`)

**Triggers:**
- Pull requests modifying skills
- Daily scheduled runs
- Manual dispatch

**Jobs:**
- **Quality Analysis**: Scores skills on 8 dimensions
- **Structure Validation**: Validates 16-section format
- **Anti-Pattern Scan**: Detects common mistakes

**Usage:**
```bash
# Manual trigger via GitHub UI
# Or run locally:
python -m tools.skill_analyzer.cli score --all
```

### 2. Daily Optimization Scan (`daily-optimization-scan.yml`)

**Triggers:**
- Daily at 3 AM UTC
- Manual dispatch

**Output:**
- `reports/daily_analysis.json` - Full analysis data
- `reports/OPTIMIZATION_REPORT.md` - Human-readable summary
- `reports/optimization_recommendations.json` - Action items

**Creates GitHub Issues for:**
- P6+ priority skills needing immediate attention

### 3. PR Skill Review (`pr-skill-check.yml`)

**Triggers:**
- Pull requests modifying skill files

**Features:**
- Posts quality check results as PR comment
- Blocks merge if score < 4.0
- Shows dimension breakdown

### 4. Runtime Validation (`runtime_validator.py`)

**Purpose:**
Validates that skills perform as documented in real-world scenarios.

**Usage:**
```bash
# Test specific skill
python -m tools.skill_analyzer.runtime_validator --skill skills/software/devops-engineer/SKILL.md

# Test entire category
python -m tools.skill_analyzer.runtime_validator --category software
```

## Quality Dimensions

Skills are evaluated on 8 dimensions:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| System Prompt | 18% | Role definition, decision framework, thinking patterns |
| Domain Knowledge | 22% | Professional expertise, frameworks, terminology |
| Workflow | 13% | Clear process, actionable steps, completion criteria |
| Risk Documentation | 9% | Risk identification, severity, mitigation |
| Example Quality | 17% | Practical scenarios, code examples, conversation flows |
| Metadata | 8% | Complete YAML frontmatter |
| Content Efficiency | 8% | Signal-to-noise ratio, structure clarity |
| Token Cost Efficiency | 5% | Description/body token budget compliance |

## Score Tiers

| Tier | Score | Description |
|------|-------|-------------|
| Exemplary | 8.0+ | Production-ready, comprehensive |
| Expert | 7.0-7.9 | High quality, minor improvements needed |
| Community | 5.0-6.9 | Usable but needs work |
| Basic | <5.0 | Significant improvements required |

## Local Development

### Running Quality Checks Locally

```bash
# Analyze all skills
python scripts/batch_optimize_skills.py --analyze

# Analyze specific category
python scripts/batch_optimize_skills.py --analyze --category software

# Score specific skill
python -m tools.skill_analyzer.cli score --path skills/software/devops-engineer/SKILL.md

# Run all analyzers
python -m tools.skill_analyzer.cli all
```

### Continuous Optimization

```bash
# Show optimization dashboard
python scripts/continuous_optimization.py --dashboard

# Run full scan
python scripts/continuous_optimization.py --scan

# Analyze trends
python scripts/continuous_optimization.py --trend --days 30

# Generate optimization plan
python scripts/continuous_optimization.py --suggest --priority 5
```

### Fixing Skill Format

```bash
# Fix specific skill
python scripts/fix_skill_format.py --path skills/category/skill-name/SKILL.md

# Fix all skills in category
python scripts/fix_skill_format.py --category software

# Fix all skills
python scripts/fix_skill_format.py --all
```

## Automation Schedule

| Workflow | Frequency | Time (UTC) |
|----------|-----------|------------|
| Skill Quality Gate | On PR + Daily | 2:00 AM |
| Daily Optimization Scan | Daily | 3:00 AM |
| Runtime Validation | Weekly | Sunday 4:00 AM |

## Reports

Generated reports are stored in `reports/`:

- `daily_analysis_YYYYMMDD.json` - Daily quality snapshot
- `optimization_recommendations.json` - Action items
- `OPTIMIZATION_REPORT.md` - Human-readable summary
- `trend_analysis_*.json` - Historical trends
- `ci_quality_report.json` - CI/CD quality results

## GitHub Integration

### Issue Labels

The automation uses these labels:
- `optimization` - Skills needing improvement
- `automated` - Auto-generated issues
- `high-priority` - P6+ priority items

### Branch Protection

Recommended branch protection rules:
- Require "Skill Quality Gate" check to pass
- Require "Validate 16-Section Structure" check to pass
- Require "Scan Anti-Patterns" check to pass

## Customization

### Adjusting Score Thresholds

Edit `.github/workflows/skill-quality-gate.yml`:

```yaml
--min-score "5.0"  # Change from default 4.0
```

### Adding New Checks

1. Create check script in `tools/skill_analyzer/`
2. Add job to workflow YAML
3. Update this documentation

## Troubleshooting

### Common Issues

**Issue:** CI fails with "Missing YAML frontmatter"
- **Solution:** Ensure skill files start with `---`

**Issue:** Score not improving after edits
- **Solution:** Run `fix_skill_format.py` to ensure correct section format

**Issue:** Anti-pattern scan fails
- **Solution:** Check for duplicate content or missing sections

### Getting Help

- Check `reports/` for detailed analysis
- Review workflow logs in GitHub Actions
- Run checks locally for faster iteration

## Contributing

When adding new skills:

1. Use the [16-section template](TEMPLATE.md)
2. Ensure all required YAML fields are present
3. Run quality checks locally before pushing
4. Address any automated review comments

## See Also

- [Skill Writer Documentation](skills/special/skill-writer/)
- [Skill Evaluator Documentation](skills/special/skill-evaluator/)
- [Quality Improvement Plan](SKILL-IMPROVEMENT-PLAN.md)
