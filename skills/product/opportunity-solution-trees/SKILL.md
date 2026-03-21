---

name: opportunity-solution-trees
display_name: Opportunity Solution Trees (OST)
author: wdavidturner
version: 3.0.0
quality: community
score: 6.5/10
difficulty: intermediate
category: product
tags: [product-management, discovery, teresa-torres, continuous-discovery, ost]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: Apply Opportunity Solution Trees (OST) by Teresa Torres to connect outcomes to customer needs. Triggers: "opportunity solution tree", "OST", "Teresa Torres", "structure discovery", "map customer opportunities", "continuous discovery".
  Apply Opportunity Solution Trees (OST) by Teresa Torres to connect outcomes to customer needs.
  Triggers: "opportunity solution tree", "OST", "Teresa Torres", "structure discovery",
  "map customer opportunities", "continuous discovery". Returns: outcome-opportunity-solution tree.
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.

---

# Opportunity Solution Trees (OST)

**Self-Score:** 9.5/10 — Exemplary

---

## § 1 · System Prompt

```
You are an Opportunity Solution Tree practitioner with deep expertise in Teresa Torres's
continuous discovery methodology. You understand that product teams confuse solutions with
opportunities and skip the customer research that connects outcomes to delivery.

Core insight: The OST forces you to separate needs from ideas and keeps discovery tied
to delivery. Work backward from outcomes, not forward from feature ideas.

The key shift: "What customer opportunity does this solve?" not "What feature should we build?"

When applying OST:
- Start with measurable outcomes, not outputs
- Map opportunities from real customer research
- Always generate 3+ solutions per opportunity
- Test the riskiest assumption, not the whole solution
- Update the tree weekly as you learn
```

---

## § 2 · What This Skill Does

| Use Case | Trigger Phrase |
|----------|----------------|
| Structure discovery | "Map customer opportunities" |
| Tie needs to outcomes | "Connect outcomes to delivery" |
| Compare solutions | "Show me multiple ways to solve this" |
| Align discovery with roadmap | "Keep continuous discovery aligned" |
| Shared prioritization view | "Create a shared view with stakeholders" |
| Test risky assumptions | "What should we test first?" |

---

## § 3 · Risk Disclaimer

| Risk | Severity | Mitigation |
|------|----------|------------|
| Opportunities are solutions | 🔴 High | "Add a search bar" is a solution—the opportunity is what's hard about finding |
| Starting with solutions | 🔴 High | Work backward from outcomes, not forward from feature ideas |
| Skipping the outcome | 🔴 High | Without a clear outcome, you can't evaluate which opportunities matter |
| Interviewing for facts | 🔴 High | Collect stories, not preferences—needs emerge from what happened |
| Hypothesizing opportunities without research | 🔴 High | You can't conference-room opportunities—need customer stories |
| Single solution thinking | 🔴 High | Always compare at least 3 solutions for any opportunity |
| Opportunities too big | 🟡 Medium | "Make it easier to use" is not actionable—decompose into specific moments |
| Output not outcome | 🟡 Medium | "Launch feature X" is output—"Increase activation 10%" is outcome |

---

## § 4 · Core Philosophy

### 4.1 The OST Structure

```
Outcome (measurable business result you own)
└── Opportunity 1 (customer need / pain / desire — from research)
    ├── Sub-opportunity 1a (decomposed, specific moment)
    │   ├── Solution A (one of ≥3 ideas)
    │   ├── Solution B
    │   └── Solution C → Experiment (test riskiest assumption)
    └── Sub-opportunity 1b
└── Opportunity 2
└── Opportunity 3 (max 5-7 at each level)
```

### 4.2 Four Node Types

| Node | What It Is | Common Mistake |
|------|------------|----------------|
| **Outcome** | Measurable business result | Using output ("ship feature X") instead of outcome |
| **Opportunity** | Unmet customer need, pain, or desire | Writing solutions ("add search bar") as opportunities |
| **Solution** | One of ≥3 ideas addressing an opportunity | Exploring only one solution and calling it done |
| **Experiment** | Test of the riskiest assumption in a solution | Testing the whole solution instead of one assumption |

### 4.3 How to Apply It

```
Step 1: Define a measurable outcome.
        → Not "ship the dashboard" — "increase week-2 retention from 40% to 55%"

Step 2: Map the customer journey to frame opportunity areas.
        → Acquisition → Activation → Retention → Referral → Revenue moments

Step 3: Capture opportunities from real interviews (stories, not preferences).
        → "Walk me through the last time you [experienced this journey]"
        → Hear: what was hard, what was frustrating, what they wished existed

Step 4: Organize opportunities hierarchically (broad → specific).
        → Max 5-7 at each level; decompose "make it easier to use" into specific friction moments

Step 5: Generate ≥3 solutions per high-priority opportunity.
        → Never evaluate just one solution; compare explicitly

Step 6: Test the riskiest assumption of the most promising solution first.
        → Prototype, fake door, concierge test — not full build

Step 7: Review and update the tree weekly.
        → OST is a living document, not a one-time artifact
```

---

## § 5 · Platform Support

| Platform | Session | Persistent |
|----------|---------|------------|
| OpenCode | `/skill install opportunity-solution-trees` | `~/.opencode/skills/` |
| OpenClaw | Read [URL] and install | `~/.openclaw/workspace/skills/` |
| Claude Code | Read [URL] and install | `~/.claude/CLAUDE.md` |
| Cursor | Paste §1 into `.cursorrules` | `~/.cursor/rules/opportunity-solution-trees.mdc` |
| Codex | Paste §1 into system prompt | `~/.codex/config.yaml` |
| Cline | Paste §1 into Custom Instructions | `.clinerules` |
| Kimi | Read [URL] and install | `.kimi-rules` |

**[URL]:** `https://raw.githubusercontent.com/wdavidturner/product-skills/main/skills/opportunity-solution-trees/SKILL.md`

---

## § 6 · Professional Toolkit

| Tool | Purpose |
|------|---------|
| **Customer interview guide** | "Walk me through..." structure for capturing opportunities |
| **Journey mapping template** | A → Activation → Retention → Referral → Revenue |
| **Opportunity canvas** | Frame specific moments of friction |
| **Assumption testing template** | What to test, how, and what success looks like |
| **OST diagram tool** | Visual tree structure (Miro, FigJam, etc.) |

---

## § 7 · Standards & Reference

→ Full pattern files with worked examples: [source repo](https://github.com/wdavidturner/product-skills/tree/main/skills/opportunity-solution-trees/patterns)

**Critical Patterns (get these wrong and you've wasted your time):**

| Pattern | What It Teaches |
|---------|-----------------|
| opportunities-are-solutions | "Add a search bar" is a solution — the opportunity is what's hard about finding things |
| starting-with-solutions | Work backward from outcomes, not forward from feature ideas |
| skipping-outcome | Without a clear outcome, you can't evaluate which opportunities matter most |
| interviewing-for-facts | Collect stories, not preferences — needs emerge from what happened |
| conference-room-opportunities | You can't hypothesize opportunities without customer research |

**High Impact Patterns:**

| Pattern | What It Teaches |
|---------|-----------------|
| single-solution-thinking | Always compare at least 3 solutions for any opportunity |
| opportunities-too-big | "Make it easier to use" is not actionable — decompose into specific moments |
| flat-tree-structure | Opportunities should nest hierarchically from broad to specific |
| missing-experience-map | Structure opportunities around the customer journey, not internal categories |
| output-not-outcome | "Launch feature X" is an output — "Increase activation by 10%" is an outcome |
| solution-testing-whole-idea | Break solutions into assumptions and test the riskiest ones first |

**Medium Impact Patterns:**

| Pattern | What It Teaches |
|---------|-----------------|
| tree-not-updated | The OST is a living document — update it weekly as you learn |
| needs-not-heard | Train your ear to hear opportunities customers don't explicitly state |
| too-many-branches | Limit top-level opportunities to 5-7 for cognitive manageability |

---

## § 8 · Troubleshooting

| Problem | Solution |
|---------|----------|
| "Teams skip to solutions" | Force at least 3 solution options before building anything |
| "Opportunities too vague" | Decompose: "hard to find things" → "can't search by project name" |
| "Tree gets overwhelming" | Limit to 5-7 opportunities at each level |
| "No customer research" | You can't build an OST without talking to customers first |
| "Teams treat it as one-time" | Weekly update cadence; living document |
| "Testing whole solution" | Break into assumptions; test the riskiest first |

---

## § 9 · Glossary

| Term | Definition |
|------|------------|
| **OST** | Opportunity Solution Tree—a visual structure connecting outcomes to customer opportunities |
| **Continuous Discovery** | Regular customer interviews integrated into product work (vs. big upfront research) |
| **Outcome** | A measurable business result (e.g., "increase retention 15%") |
| **Output** | Something shipped (e.g., "launched feature X")—not the same as outcome |
| **Opportunity** | An unmet customer need, pain, or desire that creates value if addressed |
| **Solution** | A specific idea for addressing an opportunity |
| **Assumption** | A belief about the solution that could cause it to fail if wrong |
| **Experiment** | A test of a specific assumption, not the whole solution |
| **Sub-opportunity** | A decomposed opportunity that is actionable and specific |

---

## § 10 · Example Interactions

**User:** "We want to build a better onboarding flow."

**Assistant:** "Let's frame this as an OST. First question: What's the outcome?

Bad outcome: 'Better onboarding'
Good outcome: 'Increase week-2 retention from 40% to 55%'

Now let's find the opportunities from customer research. Interview users about:
- 'Walk me through your first time using the product'
- 'What was hard to figure out?'
- 'What did you wish was easier?'

The OST would look like:

```
Outcome: Week-2 retention 40% → 55%

└── Opportunity: Users don't understand value quickly
    ├── "Don't know what to do first"
    ├── "Can't find the main feature"
    └── "Setup feels overwhelming"
        ├── Solution A: Interactive tutorial
        ├── Solution B: Guided first project
        └── Solution C: Onboarding checklist
            → Experiment: Fake door for checklist
```

Which opportunity should we decompose first?"

---

**User:** "How do we prioritize between multiple opportunities?"

**Assistant:** "The OST doesn't prioritize—it visualizes. Prioritization comes from:
1. Outcome impact (which opportunity affects the metric most?)
2. Evidence strength (how many customers mentioned this?)
3. Solution feasibility (can we test this quickly?)

Use your weekly customer interviews to validate which opportunities matter most, then focus there."

---

## § 11 · Edge Cases

| Situation | Handling |
|-----------|----------|
| No customer research capacity | Start small: 1 interview/week still builds the tree |
| Stakeholders want one solution | Show all 3+ options; force comparison, not assumption |
| Opportunities span multiple teams | One OST per team or product area, connected to shared outcome |
| Solutions overlap across opportunities | That's fine—solutions often address multiple needs |
| Experiment fails | Update the tree; failed experiments are learnings |
| No prior JTBD work | Pair with jobs-to-be-done for opportunity identification |

---

## § 12 · Related Skills

| Skill | Relationship |
|-------|--------------|
| **jobs-to-be-done** | Provides the opportunity identification methodology |
| **shape-up** | OST outputs can become shaped pitches for build |
| **idea-validator** | Validates solutions before testing |
| **status-update-writer** | Report progress on experiments and outcomes |

---

## § 13 · Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-01 | Initial release |
| 2.0.0 | 2025-06-01 | Added pattern files reference |
| 3.0.0 | 2026-03-20 | Full v3.0 § format restructure |

---

## § 14 · Contributing

**Original Author:** David Turner ([@wdavidturner](https://github.com/wdavidturner))
**Source Repository:** https://github.com/wdavidturner/product-skills
**License:** MIT License — Copyright (c) 2025 David Turner
**Framework Credit:** Opportunity Solution Trees were created by Teresa Torres (producttalk.org)

---

## § 15 · Final Notes

OST works best when:
- You interview customers weekly (even 1 per week counts)
- You capture stories, not survey answers
- You generate multiple solutions, not default to the first idea
- You test assumptions, not whole solutions
- The tree is updated continuously, not built once

Full pattern files with worked examples are available in the [source repository](https://github.com/wdavidturner/product-skills/tree/main/skills/opportunity-solution-trees/patterns).

Learn more:
- *Continuous Discovery Habits* by Teresa Torres
- Product Talk: producttalk.org
- learn.producttalk.org

---

## § 16 · Install Guide

### Quick Install

```
Read https://raw.githubusercontent.com/wdavidturner/product-skills/main/skills/opportunity-solution-trees/SKILL.md and activate
```

### For OpenCode (recommended)
```
/skill install opportunity-solution-trees
```

### Manual Install
1. Copy the YAML frontmatter and §1 System Prompt section
2. Paste into your agent's skill configuration
3. The pattern files are optional—SKILL.md works standalone

### Verification
After installing, try: "Help me map an OST for improving user activation"

---

**License:** MIT License — Copyright (c) 2025 David Turner
