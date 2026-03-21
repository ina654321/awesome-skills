# Skill Writer — Anti-Patterns

Full anti-pattern catalog for §10. Load this file when reviewing a skill for quality issues or when the user asks about common mistakes.

---

## 🔴 High Severity

**#1 Scope Sprawl**
```
❌ "This skill covers: software architecture, DevOps, cloud engineering,
    database design, security, and AI/ML systems..."

✅ "This skill focuses on software architecture. For DevOps, see
    devops-engineer.md. For security, see security-engineer.md."
```

**#2 Shallow Depth**
```
❌ ## Core Philosophy
   1. Write clean code
   2. Follow best practices
   3. Test your code

✅ ## Core Philosophy
   1. Separation of Concerns: Each module has one reason to change
      - Apply at: function (SRP), module (package), service (bounded context)
   2. Fail Fast: Detect errors at compile > startup > request > runtime
      - Use types over runtime checks: `UserId` not `string`
```

**#3 Self-Inconsistency**
```
❌ A skill that teaches "all skills must have complete metadata"
   but its own metadata is missing fields.
   A skill that defines a 16-section checklist but uses a different structure.

✅ The skill is the best exemplar of everything it teaches.
   Run the 16-section checklist against skill-writer itself before each release.
```

---

## 🟡 Medium Severity

**#4 Token Waste**
```
❌ Full 57-category directory tree (50+ lines of static reference)

✅ Compact domain-grouped table (8 lines) + "browse /skills/ if unsure"
   + heavy reference tables → references/ files (on-demand loading)
```

**#5 Generic Risk Table**
```
❌ | Risk       | Mitigation   |
   | Accuracy   | Verify outputs |

✅ | Risk                         | Mitigation |
   | Hallucinated Drug Interaction | Cross-reference FDA database; never prescribe without pharmacist review |
```

**#6 HTML Comments in YAML**
```
❌ description: >
     Expert skill for X.
     
✅ description: >
     Expert skill for X. Use when [trigger conditions].
     Triggers: "keyword1", "keyword2"
   # Bilingual content belongs in the Markdown body only
```

**#9 Platform Coverage Miss**
```
❌ ## 5. Platform Support
   | Platform  | Installation             |
   | Claude Code | Read URL and install   |
   | Cursor    | Copy §1 into .cursorrules |
   (Missing: OpenCode, OpenClaw, Codex, Cline, Kimi)
   (No persistent install options for any platform)

✅ ## 5. Platform Support
   | Platform      | Session Install              | Persistent Config               |
   | OpenCode      | /skill install [name]        | Auto-saved to ~/.opencode/skills/ |
   | OpenClaw      | Read [URL] and install       | Auto-saved to ~/.openclaw/...   |
   | Claude Code   | Read [URL] and install       | Append to ~/.claude/CLAUDE.md   |
   | Cursor        | Paste §1 into .cursorrules   | ~/.cursor/rules/[skill].mdc     |
   | OpenAI Codex  | Paste §1 into system prompt  | ~/.codex/config.yaml            |
   | Cline         | Paste §1 into Custom Instr.  | Append §1 to .clinerules        |
   | Kimi Code     | Read [URL] and install       | Append to .kimi-rules           |
   [URL]: https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/[category]/[skill-name].md
   (Rule: §7.11 — all 7 platforms; session + persistent; [URL] defined once)
```

**#10 Pattern Absence**
```
❌ ## § 8 · Standard Workflow
   1. Understand the request
   2. Think about the domain
   3. Generate the output
   (No structural pattern; all logic crammed into §1 system prompt prose)

✅ Select a design pattern first (references/design-patterns.md §DP.0):
   - Tool Wrapper → if Claude uses this domain wrong
   - Generator    → if output consistency is the problem
   - Reviewer     → if the task is auditing against a checklist
   - Inversion    → if acting without info gathering wastes effort
   - Pipeline     → if step order is safety-critical
   Then build §8 around that pattern's structure.
```

**#11 Pattern Mismatch**
```
❌ Using Generator pattern (template fill) for a deployment workflow:
   "Fill in this deploy template with the target environment and version"
   → Steps can be skipped; no safety gates; "complete-looking" output masks missing prereqs

✅ Switch to Pipeline pattern for sequential safety-critical workflows:
   Step 1: Smoke test [PREREQ: test suite passes] [✓ DONE: all green]
   Step 2: Stage deploy [PREREQ: smoke test confirmed] [✓ DONE: stage healthy]
   Step 3: Prod rollout [PREREQ: stage confirmed] [BLOCK: error rate >1%]
```

---

## 🟢 Low Severity

**#7 Literal Translation**
```
❌ "Think outside the box" → "想象在盒子外"
✅ "Think outside the box" → "突破常规思维"
```

**#8 Prose Wall**
```
❌ ## Core Philosophy
   As a senior software architect, you should always consider scalability when
   designing systems. It is important to think about performance and make sure
   that the code is clean and maintainable...

✅ ## Core Philosophy
   | Principle           | Rule                         | Litmus Test                          |
   |---------------------|------------------------------|--------------------------------------|
   | Scalability-First   | Design for 10× current load  | Can this fail under peak?            |
   | Security by Default | Auth at every layer boundary | Is any endpoint unauthenticated?     |
   | Fail Fast           | Compile > startup > runtime  | Where does this fail silently?       |
```

---

## 🔴 Enterprise Practice Skills — High Severity

**#EP1 Culture as Buzzwords**
```
❌ ## Core Philosophy
   At Tesla, we value innovation, collaboration, and excellence.
   We strive to be the best and push boundaries every day.
   (Empty phrases — no actionable meaning)

✅ ## Core Philosophy  
   ### 4.2 The Five-Step Algorithm
   | Step | Action | Key Question | Rule |
   |------|--------|--------------|------|
   | 1 | Question | Why does this exist? | Attach name to every requirement |
   | 2 | Delete | What can we remove? | Delete > feels comfortable |
   | 3 | Simplify | How to make elegant? | Optimize AFTER deleting |
   (Specific framework with concrete steps)
```

**#EP2 Missing Dual-Perspective**
```
❌ ## 2. What This Skill Does
   This skill teaches Tesla engineering culture.
   (Single audience; unclear who it's for)

✅ ## 2. What This Skill Does
   1. **For Job Seekers** — Prepare for Tesla interviews:
      - Behavioral frameworks (STAR format adapted to Tesla)
      - "Evidence of Excellence" templates
   
   2. **For Practitioners** — Operate at Tesla:
      - Decision frameworks for daily work
      - Cross-functional collaboration protocols
   (Explicit dual-audience design)
```

**#EP3 Undocumented Source**
```
❌ ## 1. System Prompt
   At Tesla, engineers use the "Five-Step Algorithm" for decisions...
   (No indication of how this information was obtained)

✅ ## 1. System Prompt
   At Tesla, engineers use the "Five-Step Algorithm"...
   
   **Source:** Based on analysis of publicly available information 
   including job postings, earnings calls, and published interviews.
   (Clear attribution; no internal confidential claims)
```

**#EP4 Missing Three-Layer Architecture**
```
❌ ## 4. Core Philosophy
   Tesla values first principles thinking and moving fast.
   
   ### Tools
   - Five-Step Algorithm
   - Direct communication
   (Missing: Culture layer, Methodology layer)

✅ ## 4. Core Philosophy
   
   ### 4.1 Culture Layer — Mission
   "Accelerate the world's transition to sustainable energy"
   
   ### 4.2 Methodology Layer — First Principles
   | Step | Action | Key Question |
   |------|--------|--------------|
   | 1 | Deconstruct | What are the fundamental truths? |
   
   ### 4.3 Tool Layer — Five-Step Algorithm
   | Step | Name | Rule |
   |------|------|------|
   | 1 | Question | Attach name to requirement |
   (Complete architecture: Culture → Methodology → Tools)
```

---

## 🟡 Enterprise Practice Skills — Medium Severity

**#EP5 Generic Interview Advice**
```
❌ ## 9. Scenario Examples
   **User:** "Tell me about yourself"
   
   **Response:** Start with your background, then discuss relevant 
   experience, and end with why you're interested in the role.
   (Generic advice applicable to any company)

✅ ## 9. Scenario Examples
   **User:** "Tell me about a time you disagreed with your manager"
   
   **Tesla Candidate:**
   > **Situation:** Manager wanted established vendor...
   > **Task:** I needed to reduce latency for Autopilot...
   > **Action:** Built prototype in 3 days, showed data...
   > **Result:** Shipped 2 months ahead, 10M events/day...
   > **Values:** First principles (prototyped), Ownership (end-to-end)
   (Tesla-specific response demonstrating values)
```

**#EP6 No Behavioral Examples**
```
❌ ## 9. Scenario Examples
   **Scenario:** How to optimize a manufacturing process
   
   **Solution:** Apply the Five-Step Algorithm...
   (Technical scenario; no interview prep value)

✅ ## 9. Scenario Examples
   **9.1 Scenario:** Manufacturing optimization
   **9.2 Scenario:** Interview behavioral question
   **9.3 Scenario:** Cross-team conflict resolution
   (Mix of workplace + interview scenarios)
```

---

## 🟢 Enterprise Practice Skills — Low Severity

**#EP7 Missing Evidence Framework**
```
❌ ## 8. Interview Preparation
   Prepare examples of your work to discuss in interviews.
   (Vague guidance)

✅ ## 8. Interview Preparation
   **Evidence of Excellence Document:**
   - 3-5 projects with quantified impact
   - Your specific contribution (not "the team")
   - Before/after metrics
   - Technical depth visible in artifacts
   (Concrete, actionable template)
```

**#EP8 Low Structure Density**
```
❌ ## Core Philosophy
   Tesla's approach to manufacturing involves questioning every 
   requirement, removing unnecessary steps, simplifying the remaining 
   processes, accelerating cycle times, and automating last.
   (Paragraph format; low scanability)

✅ ## Core Philosophy
   | Step | Action | Key Rule | Example |
   |------|--------|----------|---------|
   | 1 | Question | Attach name to requirement | Why 18650 cells? |
   | 2 | Delete | Remove > feels comfortable | 171 parts → 1 |
   | 3 | Simplify | Optimize AFTER deleting | Unified compute |
   (Table format; high information density)
```

---

*Anti-Pattern Reference Complete*
