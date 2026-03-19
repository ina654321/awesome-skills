# Scenario Examples

## 9.1 Common Scenario: Teacher Adoption Barriers

**User:** "Our app is technically excellent but teachers keep dropping off after the first week. How do we improve adoption?"

**Expert:**
> **Adoption Analysis:**
>
> 1. **First-run friction**: Map the teacher onboarding step-by-step. If it takes more than 5 minutes to set up a class, expect 60%+ drop-off.
> 2. **Perceived relevance**: Interview 3-5 churned teachers. Common answer: "It doesn't fit my curriculum flow."
> 3. **LMS integration gap**: If teachers must manually export/import grades, they will abandon the tool.
> 4. **Action plan**: Redesign onboarding to "create your first lesson in 3 minutes." Add pre-built curriculum templates aligned to Common Core or national standards. Integrate with Google Classroom and Microsoft Teams.
> 5. **NPS tracking**: Set up in-app NPS survey at day 7 and day 30; surface detractor feedback weekly.

## 9.2 Complex Scenario: COPPA Compliance for Under-13 Users

**User:** "We want to include under-13 students but our current data collection is too broad. What do we need to change?"

**Expert:**
> **COPPA Remediation Plan:**
>
> 1. **Consent mechanism**: Implement verified parental consent before collecting ANY data from under-13 users. Use email-based consent or payment-verified parents.
> 2. **Data minimization**: Collect only data necessary for the service. Remove optional data fields. Audit all third-party SDKs.
> 3. **Data retention**: Define and enforce a data retention policy. Delete under-13 data within 30 days of account inactivity.
> 4. **Privacy policy update**: Rewrite in plain language (8th-grade reading level). Include exact list of data collected, how it's used, and how parents can delete it.
> 5. **Legal review**: Engage a COPPA-specialized attorney before launch. Consider FTC Safe Harbor program participation (PRIVO, iKeepSafe).

## 9.3 Edge Case: Learning Loss Disparity Detected in Data

**User:** "Our analytics show students from lower-income households are scoring 25% lower. How should we respond?"

**Expert:**
> **Equity-First Response:**
>
> 1. **Do not patch without understanding root cause**: Conduct qualitative follow-up with affected families. Is it device access? Internet connectivity? Language barrier? Time at home?
> 2. **Design accessible alternatives**: Offline mode, low-bandwidth version, downloadable content. Assume 30% of users have limited connectivity.
> 3. **Multilingual support**: Add at minimum the top 3 languages spoken by your user base.
> 4. **Accessibility for low-literacy parents**: Video tutorials in parents' native language for home setup.
> 5. **Track equity metrics separately**: Do not let overall averages mask disparate outcomes. Build equity dashboards from day one.
