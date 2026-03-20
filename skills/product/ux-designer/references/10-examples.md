# UX Designer — Real-World Scenarios

## Scenario 1: Onboarding Usability Audit

**Context:** Mobile app onboarding has 38% completion rate. Product team wants to redesign.

**Heuristic evaluation findings:**

| Issue | Heuristic | Severity | Finding |
|-------|-----------|----------|---------|
| No progress indicator | #1 System status | 4 (Catastrophic) | Users don't know how many steps remain |
| Technical jargon | #2 Real-world match | 3 (Major) | "Configure webhook endpoint" — users don't understand |
| No skip option | #3 User control | 3 (Major) | Users forced through 8 steps |
| Form errors on submit | #5 Error prevention | 3 (Major) | Should validate inline |
| 12 form fields | #8 Minimalist design | 3 (Major) | Ask only essential fields |

**Usability test (5 participants):**
- 4/5 abandoned at API configuration step
- Average time on this step: 4.2 minutes
- Quote: "I don't know what any of this means"

**Design recommendations:**
1. Add progress bar: "Step 2 of 4 — 2 minutes"
2. Replace technical terms with plain English + optional tooltip
3. Make all non-essential steps skippable
4. Reduce required fields to 4; defer the rest
5. Inline validation: show green check when valid

**Expected outcome:** Based on similar redesigns, expect 38% → 65%+ completion.

## Scenario 2: Dashboard Redesign

**Context:** Enterprise analytics dashboard is overwhelming. 47 widgets on screen. Users report they can't find what they need.

**Audit findings:**
- Users look at average of 3-4 widgets before giving up
- 22 widgets have <5% interaction rate
- Most-used widgets are buried below fold

**Information architecture redesign:**

**Approach:**
1. Card sorting with 8 users: What do you think these sections are?
2. Analytics show top 10 most-used widgets
3. Remote contextual inquiry: What do you check daily?

**New structure:**
- **Daily Dashboard**: Top 5 widgets users check every day (configurable)
- **Reports**: Scheduled and saved analyses
- **Explore**: Ad-hoc analysis tools
- **Settings**: User and account preferences

**Design principles for new dashboard:**
- Maximum 12 widgets visible without scrolling
- User-configurable: Users choose their 5 "daily" widgets
- Progressive disclosure: Advanced features behind "View more"
- Search: Users expect to search for metrics

**Results after launch:**
- Daily active dashboard users: +34%
- Time to find information: -60%
- Support tickets about dashboard: -70%

## Scenario 3: Mobile Checkout Accessibility Remediation

**Context:** Legal compliance review flags checkout flow as inaccessible. Primary issues: form labels missing, contrast failures, tap targets too small.

**Accessibility audit findings:**

| Issue | WCAG Criterion | Impact |
|-------|---------------|--------|
| Form inputs have no labels | 3.3.2 | Screen reader users can't identify fields |
| Button text 12px | 1.4.4 | Low vision users can't read |
| Tap targets 32×32px | 2.5.5 | Motor impaired users struggle |
| Error messages vague | 3.3.1 | Users don't know what to fix |
| Color-only status indicators | 1.4.1 | Colorblind users miss status |

**Remediation plan:**

**Week 1: Forms**
- Add visible labels above all inputs
- Add aria-label for screen readers
- Error messages: "Email address is required" not "Required field"

**Week 2: Typography & Color**
- Increase body text to 16px minimum
- Fix contrast: Change secondary text from #999 to #666
- Add icon + text for status, not color alone

**Week 3: Touch Targets**
- Increase all buttons to minimum 48×48px
- Increase padding around interactive elements
- Add spacing between tap targets

**Week 4: Testing**
- Screen reader testing (VoiceOver, NVDA)
- Keyboard-only navigation test
- Color blindness simulation test

## Scenario 4: Enterprise Dashboard User Research

**Context:** B2B SaaS product. Enterprise customers saying the dashboard is "confusing" but can't specify why.

**Research approach:**
1. 5 contextual inquiry sessions: Watch users perform real tasks
2. 3-day diary study: Daily check-ins about dashboard use
3. Survey: 150 users on dashboard satisfaction

**Key insights from contextual inquiry:**

**Finding 1: Mental model mismatch**
- Product organizes by data type (Revenue, Users, Performance)
- Users think by workflow (Acquire, Engage, Retain)
- Gap: Users can't find data because they search by job, not by data type

**Finding 2: Context loss**
- User opens specific report
- Leaves to check email
- Returns 30 minutes later
- Can't find the report they had open
- "Where did my thing go?"

**Finding 3: Notification fatigue**
- 47 notification emails per week from product
- Users ignore or unsubscribe from all
- Missing critical alerts

**Design implications:**
- Offer workflow-based view as alternative to data-type view
- Persist user's recent reports and current working context
- Reduce notifications to 1-2 per week maximum; make them actionable

## Scenario 5: Error Message Redesign

**Context:** User testing reveals that error messages throughout the app are unhelpful. Users don't know what to do when errors occur.

**Current error message audit:**

| Location | Current Message | Problem |
|----------|----------------|---------|
| Form submission | "Error occurred" | What error? |
| Network failure | "Something went wrong" | What happened? |
| Invalid input | "Invalid" | Which field? Why? |
| Session timeout | "Please log in again" | Lost my work? |

**Error message redesign framework:**

**Good error message = 4 components:**
1. What happened (clear, specific)
2. Why it happened (if known)
3. What to do about it (actionable)
4. How to prevent in future (if applicable)

**Redesigned messages:**

| Location | Redesigned Message |
|----------|--------------------|
| Form submission | "We couldn't save your changes. Your internet connection appears offline. Check your connection and click Save again." |
| Network failure | "Connection lost. We've saved your work locally. You'll sync automatically when you're back online." |
| Invalid input | "Email address must include @ and a domain (example: name@company.com)" |
| Session timeout | "Your session expired after 30 minutes of inactivity. Your work is saved. Sign in to continue." |

## Scenario 6: Search Feature Redesign

**Context:** Enterprise search has 15% search-to-no-result rate. Users report search doesn't find things they know are there.

**Research:**
1. Analytics: What do users search for?
2. 8 user interviews: How do you use search?
3. Log analysis: What no-result queries exist?

**Findings:**

**Finding 1: Synonym problem**
- Users search "profit" → system searches "revenue"
- Users search "customers" → system searches "clients"
- Result: Zero matches, no results

**Finding 2: Filter complexity**
- Users don't know filters exist
- Filters are hidden in dropdown
- Users could find results with filters, but don't know to use them

**Finding 3: Results ranking**
- Most relevant results buried on page 2
- Users rarely go past page 1
- Top results are "recently updated" not "best match"

**Design recommendations:**
1. Add "Did you mean?" with synonyms
2. Show filter suggestions on no-result page
3. Improve results ranking algorithm
4. Add "Search tips" accessible from search bar
5. Pagination → infinite scroll to reduce barrier to page 2
