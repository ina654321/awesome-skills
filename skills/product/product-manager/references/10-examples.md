# Product Manager — Real-World Scenarios

## Scenario 1: Onboarding Activation Problem

**Context:** SaaS product with 60% trial users never completing setup. Free-to-paid conversion at 8%. User interviews reveal confusion at API integration step.

**Discovery findings:**
- 8 users who didn't activate interviewed
- 5/8 stuck at API key setup
- 6/8 said "wasn't sure what to do after signup"
- Session recordings: 45% abandonment at API integration step

**Root cause hypothesis:** Onboarding assumes technical knowledge that new users don't have.

**Solutions considered:**
- Option A: Guided setup wizard with progress tracking
- Option B: "Demo account" to delay integration requirement
- Option C: Video walkthrough embedded at drop-off points

**Decision: Option A**
- Build progressive onboarding wizard
- Key metrics: Activation rate (defined as complete setup + first core action)
- Target: 40% → 60% activation within 90 days

**PRD includes:**
- Success metric: Activation rate 60% at 90 days post-launch
- Guardrail: P95 latency <500ms (don't degrade performance)
- Non-goals: Mobile optimization (web first only)

## Scenario 2: Roadmap Prioritization Dispute

**Context:** Three items competing for Q3 sprint (2 engineers, 1 designer, 1 PM). Sales committed a date for one item without consulting product.

**Items and RICE scores:**

| Feature | Reach/qtr | Impact | Confidence | Effort (wks) | RICE |
|---------|-----------|--------|-----------|-------------|------|
| Bulk export | 800 | 1 | 80% | 3 | 213 |
| AI summary | 1200 | 2 | 50% | 8 | 150 |
| Team permissions | 500 | 3 | 80% | 6 | 200 |

**RICE ranking:** Bulk export (213) > Team permissions (200) > AI summary (150)

**Complicating factor:** Sales promised Team permissions to enterprise customer by Q3.

**Resolution:**
1. Present RICE analysis to leadership
2. Explain trade-off: Bulk export has highest score but enterprise needs Team permissions
3. Propose: Team permissions first (satisfies sales commitment), Bulk export second
4. AI summary deferred to Q4 (lowest score, highest effort)

**Key principle:** Don't let RICE override business judgment — use it to inform, not decide.

## Scenario 3: Feature Success Review

**Context:** Three months ago, shipped "Saved Searches" feature. Goal: Increase retention by 5%. Now reviewing results.

**Data available:**
- Feature adoption: 22% of active users have used it
- Retention: No measurable change (within noise)
- NPS: Feature NPS is +35 (positive)

**Analysis:**
- Feature is used by ~20% of users — decent for new feature
- Retention not improved — but retention is hard to move with single feature
- NPS is positive — users who use it like it

**Assessment:** Feature is moderately successful, not transformative.

**Learnings:**
- Retention goal was too ambitious for single feature
- Should have measured more proximate metric (usage of saved searches)
- For next release: Define leading indicators, not just lagging

**Decisions:**
- Keep feature (positive NPS, some usage)
- Invest in promoting feature (email to dormant saved-search users)
- Don't over-invest in expansion until retention link is proven

## Scenario 4: Customer Escalation vs. Roadmap

**Context:** Your largest customer (15% of revenue) requests a custom integration with their legacy system. Engineering estimates 8 weeks. It doesn't fit your product direction.

**Assessment:**
- 15% of revenue = significant business risk
- Custom integration could open similar enterprise deals
- But: Sets precedent for custom work, splits engineering focus

**Options:**

**Option A: Say no**
- Clear product direction communication
- Risk: Customer churns or threatens to
- Pros: Maintains product integrity

**Option B: Yes, full custom**
- Satisfies customer
- Risk: 8 weeks off roadmap, precedent for others
- Cost: Engineering time + support burden

**Option C: Hybrid — Partial + Direction change**
- Build simplified version (2 weeks) that addresses 80% of need
- Use learnings to inform future API investments
- Negotiate: Customer gets partial now, full later

**Recommended: Option C**
- Protects roadmap while addressing urgent customer need
- Opens door to enterprise market with learnings
- Sets precedent: We listen and respond, but don't overpromise

## Scenario 5: PRD Review — Edge Cases

**Context:** Engineering comes back during development saying the search feature as specced will take 12 weeks instead of 4 weeks. What's in the PRD needs to be cut.

**Original PRD scope:**
- Full-text search across all content
- Filter by date, type, author
- Sort by relevance, date
- Mobile optimization
- Search analytics dashboard

**Engineering constraints:**
- Can deliver: Full-text search + basic filters + sort
- Cannot deliver: Mobile optimization + analytics in 4 weeks

**Decision framework:**
1. What is the CORE value? — Finding content quickly
2. What enables the core value? — Search + filters + sort
3. What enhances but isn't essential? — Analytics dashboard
4. What is nice-to-have? — Mobile optimization

**Revised scope:**
- Phase 1 (4 weeks): Search + basic filters + sort ✅
- Phase 2 (4 weeks): Mobile optimization
- Phase 3 (4 weeks): Search analytics dashboard

**Communication:**
- Update PRD with phased approach
- Communicate to stakeholders: What we're shipping, what's deferred
- Measure: Search completion rate in Phase 1

## Scenario 6: Market Shift Response

**Context:** A well-funded competitor just launched a product that directly competes with your core offering. Your differentiation is now at risk.

**Initial assessment:**
- Competitor has more features, but worse UX
- Your product: Simpler, more intuitive
- Customer feedback: They love you but worried about "who will win"

**Strategic options:**

**Option A: Feature parity sprint**
- Copy key competitor features
- Risk: Playing defense, chasing, losing simplicity advantage

**Option B: Double down on differentiation**
- Invest heavily in what makes you unique
- Lean into simplicity, speed, ease of use
- Risk: Some customers may leave for feature-rich competitor

**Option C: Reposition to different segment**
- If competitor targets enterprise, move upmarket or downmarket
- Find segment where your strengths matter more

**Recommended: Option B + C hybrid**
- Double down on simplicity and ease (core strength)
- Add the 2-3 most-requested features that address real needs
- Target underserved segment (e.g., small teams vs. enterprise)

**Execution:**
- Pause roadmap items that don't strengthen differentiation
- Launch "Simpler, Faster, Better" messaging campaign
- 90-day sprint to address top 3 feature gaps
- Customer communication: We're doubling down on your success
