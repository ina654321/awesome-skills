# Evals Templates

> Ready-to-use templates for skill evaluation.

---

## What Are Evals?

Evals (evaluations) are test cases that verify your skill works correctly. They serve two purposes:

1. **Validation** — Does the skill do what it claims?
2. **Regression** — Does the skill still work after changes?

---

## Basic Template: evals.json

```json
{
  "skill_name": "your-skill-name",
  "version": "1.0.0",
  "description": "What this skill does",
  "assertions": [
    {
      "id": "assertion-1",
      "query": "Example query that should trigger this skill",
      "expected_behavior": "What the skill should do",
      "should_trigger": true,
      "pass_criteria": [
        "criterion 1",
        "criterion 2"
      ]
    }
  ]
}
```

---

## Full Template

```json
{
  "skill_name": "code-reviewer",
  "version": "1.2.0",
  "description": "Automated code review with security focus",
  "created": "2026-03-25",
  "maintainer": "your@email.com",
  
  "assertions": [
    {
      "id": "security-scan",
      "query": "Review this PR for security vulnerabilities",
      "expected_behavior": "Skill activates and provides security analysis",
      "should_trigger": true,
      "pass_criteria": [
        "Mentions OWASP",
        "Identifies at least one vulnerability",
        "Provides severity rating"
      ]
    },
    {
      "id": "non-security-query",
      "query": "What's the weather today?",
      "expected_behavior": "Skill does NOT activate",
      "should_trigger": false,
      "pass_criteria": [
        "Skill remains inactive",
        "Normal response given"
      ]
    }
  ],
  
  "baseline": {
    "enabled": true,
    "description": "Compare skill output vs baseline (no skill)"
  },
  
  "thresholds": {
    "min_pass_rate": 0.8,
    "max_tokens": 5000,
    "max_duration_ms": 30000
  }
}
```

---

## Query Template: eval-queries.json

```json
{
  "skill_name": "your-skill-name",
  "version": "1.0.0",
  "description": "Test queries for trigger rate validation",
  
  "train_split": 15,
  "validation_split": 5,
  
  "queries": [
    {
      "id": "q01",
      "query": "What a user would actually type",
      "should_trigger": true,
      "category": "core-functionality",
      "expected_output": "Description of expected output"
    }
  ]
}
```

---

## Categories for Queries

| Category | Description |
|----------|-------------|
| `core-functionality` | Primary use case |
| `edge-case` | Boundary conditions |
| `error-handling` | What happens on bad input |
| `negative` | Should NOT trigger |
| `ambiguous` | Unclear if should trigger |

---

## Example: Security Code Review Skill

### evals.json

```json
{
  "skill_name": "security-code-review",
  "version": "1.0.0",
  "assertions": [
    {
      "id": "sql-injection",
      "query": "Review this Python code for SQL injection",
      "expected_behavior": "Identifies SQL injection vulnerability",
      "should_trigger": true,
      "pass_criteria": [
        "Detects string concatenation for SQL",
        "Suggests parameterized queries",
        "Rates severity as high"
      ]
    },
    {
      "id": "weather-query",
      "query": "What's the weather in Tokyo?",
      "expected_behavior": "Skill does not trigger",
      "should_trigger": false,
      "pass_criteria": [
        "Normal response",
        "No code review performed"
      ]
    }
  ]
}
```

### eval-queries.json

```json
{
  "skill_name": "security-code-review",
  "queries": [
    {
      "id": "q01",
      "query": "Review my PR for security issues",
      "should_trigger": true,
      "category": "core-functionality"
    },
    {
      "id": "q02", 
      "query": "Check this Go code for vulnerabilities",
      "should_trigger": true,
      "category": "core-functionality"
    },
    {
      "id": "q03",
      "query": "Find XSS bugs in this JavaScript",
      "should_trigger": true,
      "category": "core-functionality"
    },
    {
      "id": "q04",
      "query": "Analyze this code for crypto issues",
      "should_trigger": true,
      "category": "edge-case"
    },
    {
      "id": "q05",
      "query": "What is 2+2?",
      "should_trigger": false,
      "category": "negative"
    }
  ]
}
```

---

## Running Evals

### Manual Testing

```bash
# For each assertion
# 1. Run the query with skill active
# 2. Check if output matches pass_criteria
# 3. Record PASS/FAIL
```

### Automated (if you have API access)

```bash
# skill-creator style
./scripts/run_eval.py --skill ./my-skill --evals ./evals.json
```

---

## Best Practices

### Do

- ✅ Test both positive (should trigger) and negative (shouldn't)
- ✅ Cover core functionality
- ✅ Include edge cases
- ✅ Update evals when skill changes

### Don't

- ❌ Don't test trivial cases only
- ❌ Don't skip negative cases
- ❌ Don't hard-code expected outputs (be flexible)
- ❌ Don't forget to run evals before publishing

---

## Integration with skill-manager

### In EVALUATE Mode

After running dual-track scoring, **generate evals**:

```
1. Review failed queries
2. Add to evals.json assertions
3. Document pass criteria
4. Re-test after fixes
```

### In CREATE Mode

After Phase 3 (Testing), **formalize evals**:

```
1. Capture 3-5 test queries from real usage
2. Add to eval-queries.json
3. Define pass criteria
4. Use for regression testing
```
