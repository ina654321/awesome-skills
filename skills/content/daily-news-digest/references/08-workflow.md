## 8. Standard Workflow

### 8.1 Full Daily Digest Generation

```
Phase 1: Signal Collection (5–10 min)
├── Fetch geopolitics: search "[today's date] -1 day site:reuters.com OR apnews.com"
│   Focus: elections, sanctions, trade policy, military escalation, regulatory rulings
├── Fetch financial: pull end-of-day data for S&P 500, Nasdaq, USD/CNY, gold, BTC,
│   10Y Treasury; scan earnings releases and central bank statements
├── Fetch AI/Tech: search "[today] AI model release OR AI funding OR AI regulation"
│   Cross-reference with arXiv (cs.AI, cs.LG last 48h), Hugging Face blog, vendor blogs
└── Fetch GitHub: pull trending repos (24h daily, 7-day weekly); filter by language/topic
    if user requested specific domains (e.g., "AI tools", "Rust ecosystem")

Phase 2: Editorial Filtering (3–5 min)
├── Apply 5-Gate Filter to every candidate item
├── Score materiality: High (phase transition) / Medium (incremental)
├── Corroborate: reject single-source items unless flagged 🔮 Speculative
└── Prune to max 5 items per section to enforce signal density

Phase 3: Deep Analysis (10–15 min)
├── Write verdict for each item (1 sentence, bold)
├── List 2–4 evidence bullets with quantified data where possible
├── Craft "Analyst's Take": first-order impact → second-order implication → recommendation
└── Identify cross-domain connections for the Synthesis section

Phase 4: Digest Assembly
├── Header: date, market snapshot table, 3-word tone descriptor (e.g., "Risk-On | Cautious | Pivotal")
├── Section 1: Geopolitics & Policy
├── Section 2: Financial Markets & Macro
├── Section 3: AI & Technology
├── Section 4: GitHub & Open Source
├── Section 5: Cross-Domain Synthesis (the analyst's edge)
└── Footer: "Watch in the Next 48h" with 3–5 upcoming catalysts
```

### 8.2 Quick Briefing (On-Demand)

```
Step 1: Identify the user's domain focus (all domains / specific sector
Step 2: Apply Phase 1 signal collection for requested domains only
Step 3: Apply 5-Gate Filter; write BLUF-format summary (no full digest structure)
Step 4: Close with 2 watch items for the requested domain
Expected output: 300–500 words, 3–5 minutes to read
```

