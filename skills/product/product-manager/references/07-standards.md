# Product Manager — Standards & Reference

## Frameworks & Methodologies

### RICE Prioritization Framework

```
RICE Score = (Reach × Impact × Confidence) / Effort

Components:
- Reach: How many users/customers will this affect per quarter?
  Estimate the number of users who will benefit. Be specific.

- Impact: How much will this move your key metric?
  3 = Massive (>5% change in target metric)
  2 = High (1-5% change)
  1 = Medium (0.5-1% change)
  0.5 = Low (0.1-0.5% change)
  0.25 = Minimal (<0.1% change)

- Confidence: How confident are you in these estimates?
  100% = Based on strong research data
  80% = Based on some research or good analogies
  50% = Rough guess based on assumption

- Effort: Person-weeks across entire team (eng + design + PM)

Score interpretation:
> 100 = Must-do (high impact, low effort, high reach)
50-100 = Should-do
20-50 = Consider
< 20 = Defer or reject
```

### Jobs-to-be-Done (JTBD) Framework

**Format:**
> "When [situation/trigger], I want to [motivation/aspiration], so I can [expected outcome]."

**Types of jobs:**
- **Functional**: Accomplish a specific task
- **Emotional**: Feel a certain way
- **Social**: Belong or be perceived in a certain way

**Examples:**
- "When I'm coordinating a team across time zones, I want to know what everyone is working on, so I can avoid duplicate effort." (functional)
- "When I'm planning a trip, I want to feel like an expert, so my family thinks I'm organized." (emotional/social)

### Opportunity Scoring Framework

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| Satisfaction | 25% | Current satisfaction in job (1-5) |
| Importance | 25% | How important is this job (1-5) |
| Underserved | 25% | How underserved is this job (1-5) |
| Growth | 25% | Job growth/trend (1-5) |

Higher score = more valuable opportunity to address.

## Product Frameworks

### HEART Framework (Google)

| Dimension | Metric | Purpose |
|----------|--------|---------|
| **Happiness** | Satisfaction, NPS, CSAT | How do users feel about the product? |
| **Engagement** | DAU/MAU, session depth | Are users engaged? |
| **Adoption** | New user activation, feature adoption | Are users starting successfully? |
| **Retention** | Churn rate, returning users | Do users come back? |
| **Task Success** | Completion rate, time on task | Can users accomplish their goals? |

### Pirate Metrics (AARRR)

- **Acquisition**: How do users find you?
- **Activation**: Do users have a great first experience?
- **Retention**: Do users come back?
- **Referral**: Do users tell others?
- **Revenue**: Do users pay?

## Professional Certifications & Resources

**Product Management Associations:**
- **Product-Led Alliance** — Resources for PLG product managers. Website: productled.org
- **Product Management Festival** — Annual conference and community. Website: productmanagementfestival.com
- **Mind the Product** — Community and events for product managers. Website: mindtheproduct.com

**Certifications:**
- **Pragmatic Marketing** — Product management certification courses. Website: pragmaticinstitute.com
- **Product School** — Product management certifications. Website: productschool.com
- **Scrum.org** — Professional Scrum certifications including PSD (Product Owner). Website: scrum.org

## Roadmapping Standards

### Roadmap Types

| Type | Description | When to Use |
|------|-------------|-------------|
| **Theme-based** | Organized by strategic themes, not features | Most common; strategy-driven |
| **Outcome-based** | Focused on measurable outcomes, not outputs | When you want flexibility in solutions |
| **Feature-based** | Lists specific features with dates | When stakeholders demand specifics |
| **Time-based** | Time-boxed milestones with dates | When sales has committed dates |
| **Opportunity-based** | Driven by opportunity assessment | Discovery-led teams |

### OKR Framework

**Format:**
```
Objective: [Inspirational, qualitative goal]

Key Result 1: [Measurable outcome] — Baseline → Target
Key Result 2: [Measurable outcome] — Baseline → Target
Key Result 3: [Measurable outcome] — Baseline → Target
```

**Rules:**
- 3-5 KRs per Objective
- KRs must be measurable (not activities)
- 70% achievement is success, not failure
- Review quarterly; mid-quarter check-ins

## Analytics Reference

### Key Metrics by Product Stage

| Stage | North Star | Supporting Metrics |
|-------|-----------|-------------------|
| **Pre-launch** | Waitlist signups, wait time engagement | Conversion rate, social shares |
| **Launch** | Activation rate | Time to value, feature adoption |
| **Growth** | Monthly active users, DAU/MAU | Churn, referral rate |
| **Maturity** | Revenue per user, LTV | Engagement depth, expansion MRR |
| **Retention** | Churn rate, returning users | NRR, CSAT |

### Cohort Analysis Framework

- Group users by acquisition date
- Track behavior over time (week 1, 2, 3, 4...)
- Identify when users drop off
- Compare cohorts to measure impact of changes

### A/B Test Statistical Significance

**Minimum requirements:**
- 95% statistical significance
- Minimum 7-day run time (avoid weekly seasonality)
- Calculate sample size before running
- Account for multiple comparisons

**Sample size formula (approximate):**
```
n ≈ (1.96 + 0.84)² × [p1(1-p1) + p2(1-p2)] / (p2 - p1)²
```
Where p1 = baseline conversion, p2 = expected conversion.
