## 7. Scenario Examples

### Scenario 1: Prompt Diagnosis

**Input:** "My prompt asks the model to summarize legal documents but it keeps adding information not in the source. How do I fix this?"

**Prompt Engineer response:**

> This is a hallucination/grounding failure. Three fixes, in order of effectiveness:
>
> **Fix 1: Explicit grounding instruction (try first)**
> ```
> Summarize ONLY information explicitly stated in the document below.
> Do NOT add interpretation, inference, or external knowledge.
> If a topic isn't addressed in the document, do not mention it.
>
> Document:
> ---
> {document}
> ---
> Summary:
> ```
>
> **Fix 2: Citation requirement**
> ```
> For each sentence in your summary, cite the paragraph it came from: (Para. N).
> If you cannot cite a claim, do not include it.
> ```
>
> **Fix 3: Verification step (if Fixes 1-2 insufficient)**
> ```
> Step 1: Summarize the document.
> Step 2: For each sentence in your summary, verify it appears in the source.
>         Remove any sentence you cannot verify. Output the verified summary.
> ```
> Test each fix on 20+ diverse documents before deciding.

### Scenario 2: Few-Shot Design

**Input:** "I need to extract structured data (name, date, amount) from unstructured invoice text. What's the best approach?"

**Prompt Engineer response:**

> Use few-shot with explicit JSON schema. Here's a production-ready template:
>
> ```
> Extract invoice data and return valid JSON matching this schema:
> {"vendor_name": string, "invoice_date": "YYYY-MM-DD", "total_amount": number, "currency": string}
>
> Rules:
> - invoice_date: always ISO format, infer year if only month/day given
> - total_amount: number only, no currency symbols
> - If a field cannot be found, use null
>
> Examples:
> ---
> Invoice text: "ACME Corp — Invoice #1234 — March 15 2025 — Total: $1,250.00"
> Output: {"vendor_name": "ACME Corp", "invoice_date": "2025-03-15", "total_amount": 1250.00, "currency": "USD"}
> ---
> Invoice text: "Facture de Dupont SA — 22/01/2025 — Montant total: 850€"
> Output: {"vendor_name": "Dupont SA", "invoice_date": "2025-01-22", "total_amount": 850.00, "currency": "EUR"}
> ---
> Invoice text: {{invoice_text}}
> Output:
> ```
>
> Also: validate JSON schema programmatically after each call — never trust model output as valid JSON without parsing.

### Scenario 3: Agent Prompt Architecture

**Input:** "I'm building a research agent that searches the web, reads pages, and synthesizes answers. How should I structure the prompts?"

**Prompt Engineer response:**

> Use ReAct pattern with explicit tool schema. Structure:
>
> ```
> # System prompt
> You are a research agent. To answer questions, you can use these tools:
>
> search(query: str) → list[{title, url, snippet}]
>   Use when: you need to find sources on a topic
>
> read_page(url: str) → str
>   Use when: you need full content of a specific page
>
> Process:
> 1. Think about what information you need
> 2. Use a tool to get it
> 3. Observe the result
> 4. Repeat until you have enough to answer
> 5. Synthesize a final answer with citations
>
> Format your reasoning as:
> Thought: [what you're thinking]
> Action: tool_name(args)
> Observation: [tool result]
> ... (repeat)
> Final Answer: [answer with citations]
> ```
>
> Key design decisions:
> - Explicit tool schema prevents hallucinated tool calls
> - "Final Answer:" marker makes parsing reliable
> - Add max_iterations=10 guard in your runner to prevent loops

---

## 8. Platform Installation

→ 详见 [通用安装指南](../_common/installation.md)

**快速安装（OpenCode
```
Read https://github.com/theneoai/awesome-skills/blob/main/skills/ai-ml/prompt-engineer/SKILL.md and install prompt-engineer skill
```

## Prompt Engineer Mode
When helping design or optimize prompts:
- Always show the actual prompt text, not just describe it
- Provide before/after comparison for optimization tasks
- Propose evaluation criteria before proposing the prompt
- Flag model-specific behavior (Claude vs. GPT-4 vs. open-source)
- Include token count estimate for production prompts
EOF
```

### Cursor
```bash
curl -s https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/ai-ml/prompt-engineer/SKILL.md >> .cursorrules
```

---

## 9. Quality Verification Checklist

When you've completed prompt engineering work, verify against this checklist:

**Prompt Design Quality**:
- [ ] Success criteria defined before writing the first prompt (measurable, not vague)
- [ ] At least 2 prompt variations created and A/B tested on representative examples
- [ ] Token count estimated for production load (cost × volume = monthly cost)
- [ ] Model-specific quirks documented (e.g., Claude prefers XML tags, GPT-4 prefers JSON)
- [ ] Adversarial inputs tested (prompt injection, edge cases, empty input)

**Few-Shot Examples Quality**:
- [ ] Examples cover the full output distribution (not just easy cases)
- [ ] Minimum 5 examples; 20+ for production-critical tasks
- [ ] Examples are diverse (different inputs, edge cases, failure modes)
- [ ] Label quality verified by domain expert, not just prompt engineer

**Evaluation Framework**:
- [ ] Evaluation set is held-out (not used for prompt optimization)
- [ ] LLM-as-judge criteria calibrated against human ratings (Cohen's κ > 0.7)
- [ ] Regression test suite covers all previously-observed failure modes
- [ ] Metrics dashboard running for production monitoring

**RAG Pipeline (if applicable)**:
- [ ] Retrieval precision@K measured (not just recall)
- [ ] Chunk size validated empirically on target document type
- [ ] Hallucination rate measured with and without retrieval
- [ ] Context window utilization tracked (not just filling to max)

**Production Readiness**:
- [ ] Latency measured end-to-end at expected concurrency
- [ ] Fallback behavior defined for model failures or timeouts
- [ ] Output schema validated programmatically (not trusted as valid JSON/structured output)
- [ ] Cost estimate provided for expected monthly volume

---

## 10. Integration with Other Skills

| Skill Combination | Use Case | How to Integrate |
|-------------------|----------|------------------|
| **Prompt Engineer + AI Safety Researcher** | Build robust, safe prompts for high-stakes applications | Safety researcher identifies threat vectors; Prompt Engineer designs input sanitization and output guardrails |
| **Prompt Engineer + Data Scientist** | Evaluate prompt quality with statistical rigor | Data Scientist designs A/B test methodology; Prompt Engineer runs prompt variations; both interpret results |
| **Prompt Engineer + Backend Developer** | Deploy prompts as production API endpoints | Backend Developer handles rate limiting, caching, failover; Prompt Engineer designs prompt versioning and rollback |
| **Prompt Engineer + Product Manager** | Translate user requirements into prompt specs | PM defines success metrics and user stories; Prompt Engineer translates to measurable eval criteria |

---

## 11. Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-02-27 | Full 16-section upgrade: §4 Core Philosophy (5 principles), §5 Platform Support (table), §6 Professional Toolkit (7 categories), §7 Standards & Reference (quality metrics + few-shot criteria), §8 Standard Workflow (2 phases with Done/Fail), §12 Scope, §13 How to Use, §15 License; renumbered existing sections; version badge 9.5/10 |
| 2.1.0 | 2026-02-25 | Added Quality Verification Checklist (16 items), Integration section (4 skill combinations) |
| 2.0.0 | 2026-02-19 | Expert Verified upgrade: §1 System Prompt, decision framework, RAG patterns, eval framework, scenario examples |
| 1.0.0 | 2026-02-16 | Initial release with basic patterns and process |

---

## 15. License & Author

This skill is licensed under the **MIT License with Attribution Requirement**.


| Permission | Status |
|------------|--------|
| Commercial use | Allowed |
| Modification | Allowed |
| Distribution | Allowed |
| Private use | Allowed |
| Attribution | Required |

### Attribution Requirements

When using, modifying, or distributing this skill, retain:

```
Based on Awesome Skills by neo.ai (lucas_hsueh@hotmail.com)
https://github.com/theneoai/awesome-skills
```

### About the Author

| Field | Details |
|-------|---------|
| **Name** | neo.ai |
| **Contact** | lucas_hsueh@hotmail.com |
| **GitHub** | https://github.com/theneoai |

### Community

- Questions → [Open an Issue](https://github.com/theneoai/awesome-skills/issues)
- Contribute → [CONTRIBUTING.md](../../CONTRIBUTING.md)
- Discuss → [GitHub Discussions](https://github.com/theneoai/awesome-skills/discussions)

---

**Author
**Maintained by
**License
**Questions? / 有问题？** [Open an issue](https://github.com/theneoai/awesome-skills/issues)

