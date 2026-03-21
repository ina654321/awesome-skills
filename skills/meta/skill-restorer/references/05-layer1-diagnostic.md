# Layer 1: Diagnostic Engine - Full Details

## Purpose

Accurately identify skill deficiencies and restoration requirements.

## Components

### Structure Scanner

Checks for required sections:
```bash
# Check System Prompt
grep -c "§ 1\.1" SKILL.md
grep -c "§ 1\.2" SKILL.md
grep -c "§ 1\.3" SKILL.md

# Check Workflow
grep -c "Done Criteria" SKILL.md
grep -c "Fail Criteria" SKILL.md

# Check Examples
grep -c "Example [0-9]" SKILL.md
```

### Content Analyzer

Detects generic vs. specific content:
- Searches for generic phrases
- Identifies missing data points
- Flags placeholder text

### Score Predictor

Estimates current quality based on:
- Structural completeness
- Content specificity
- Example richness
- Workflow clarity

### Scope Definer

Determines fix boundaries:
- What needs to be added
- What needs to be replaced
- Priority of fixes
- Time estimate
