# Skill Manager

> Create · Evaluate · Restore · Tune — the complete AI skill lifecycle.

## Quick Start

```bash
# 1. Ensure dependencies are installed
which jq bc curl git

# 2. Set API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Create a new skill
skill-manager "create a skill for extracting product prices from URLs"
skill-manager "write skill quick"        # Lite tier (50-150 lines, ~15 min)
skill-manager "start standard"           # Standard tier (150-400 lines)
skill-manager "start expert"             # Enterprise tier (400+ lines)

# 4. Evaluate existing skill
skill-manager "evaluate skills/my-skill"
skill-manager "score my skill at skills/my-skill"

# 5. Restore underperforming skill
skill-manager "restore skills/underperforming/SKILL.md target 9.5"

# 6. Autotune (autonomous optimization)
skill-manager "autotune skills/moderate/SKILL.md --rounds 10"
```

## Dependencies

| Tool | Purpose | Install |
|------|---------|---------|
| `jq` | JSON parsing | `brew install jq` |
| `bc` | Calculator | `brew install bc` |
| `curl` | HTTP requests | Pre-installed |
| `git` | Version control | `brew install git` |

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | LLM scoring & evaluation |
| `ANTHROPIC_API_KEY` | Yes | Alternative LLM for scoring |

```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Mode Examples

### CREATE — Build a new skill from scratch

```bash
# Lite tier (quick, single function)
skill-manager "write skill quick"
# → Creates: skills/[name]/SKILL.md (50-150 lines, ~15 min)

# Standard tier
skill-manager "start standard"
# → Creates: skills/[name]/SKILL.md + references/ (150-400 lines)

# Example conversation:
# Input: "I need a skill that extracts product prices from URLs. start quick"
# Output: skills/price-extractor/SKILL.md (87 lines, score 8.4)
```

### EVALUATE — Score and find gaps

```bash
skill-manager "score my skill at skills/my-skill"
skill-manager "evaluate skills/my-skill"
skill-manager "certify skills/my-skill"

# Example output:
# Text Score: 7.8/10 (System Prompt 7, Domain 6, Workflow 8, Error 7, Examples 5, Meta 10)
# Runtime Score: 7.2/10 (Immersion 7, Framework 6, Actionability 8, Accuracy 7, Stability 8, Resilience 7)
# Variance: 0.6
#
# Top 3 Gaps:
# 1. Missing §1.3 constraints → System Prompt 7→9
# 2. Generic "McKinsey model" → Domain 6→8
# 3. Only 2 scenarios → Examples 5→8
```

### RESTORE — Fix low-scoring skills (5-7 → 9.5)

```bash
skill-manager "restore skills/underperforming/SKILL.md"
skill-manager "restore skills/underperforming/SKILL.md target 9.5"

# Example improvement:
# Original: 6.5/10 → After RESTORE: 9.2/10 ✓
# - §1.1/§1.2/§1.3 added → System Prompt 5→8 (+3)
# - Specific benchmarks added → Domain 6→8 (+2)
# - Done/Fail in 5 phases → Workflow 5→9 (+4)
# - 5 detailed scenarios → Examples 5→9 (+4)
```

### TUNE — Autonomous optimization (no permission needed)

```bash
skill-manager "autotune skills/moderate/SKILL.md --rounds 10"
skill-manager "optimize skills/my-skill --target 9.5"

# Runs autonomously: read → improve → score → keep/discard → repeat
# Logs to: results.tsv
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `jq: command not found` | `brew install jq` |
| Score stuck below 8.0 | Check System Prompt (§1.1/1.2/1.3) — it's 20% weight |
| High variance (>2.0) | Text and runtime disagree — fix the weaker track |
| Generic content detected | Add specific benchmarks: "McKinsey 7-S", "94% accuracy" |
| SKILL.md > 400 lines | Move details to `references/` |
| TUNE keeps discarding | Try different approach; 10 consecutive discards = give up |
| API key errors | Verify `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are set |

## Quick Command Reference

```bash
# Validation
./scripts/validate.sh my-skill/SKILL.md      # 5 sec - spec compliance

# Scoring
./scripts/score.sh my-skill/SKILL.md         # 5 sec - quick check
./scripts/score-v2.sh my-skill/SKILL.md       # 5 sec - deep analysis
./scripts/score-secure.sh my-skill/SKILL.md   # 15-30 sec - LLM evaluation

# Evaluation
./scripts/eval.sh my-skill/SKILL.md standard  # 5-60 min - dual-track
./scripts/certify.sh my-skill/SKILL.md       # ~2 hrs - production

# Autotune
./scripts/tune.sh my-skill/SKILL.md 100       # N rounds
```

## Certification Thresholds

| Metric | Target |
|--------|--------|
| Text Score | ≥ 8.0 |
| Runtime Score | ≥ 8.0 |
| Variance | < 1.0 |
| **Overall** | **≥ 9.0** |

## Mode Routing

| First Verb | Mode | Notes |
|------------|------|-------|
| write/create/make/build | **CREATE** | No existing skill |
| evaluate/test/score/certify | **EVALUATE** | Has skill, wants score |
| restore/fix/repair | **RESTORE** | Low-scoring skill |
| optimize/tune/autotune | **TUNE** | Autonomous improvement |

> **Tip:** "improve score" → TUNE; "improve quality" → RESTORE

## Links

- [SKILL.md](./SKILL.md) — Full skill specification
- [references/tools.md](./references/tools.md) — Tool documentation
