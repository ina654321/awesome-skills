# QA Engineer — Scenario Examples & Anti-Patterns

This file contains detailed scenario implementations and anti-patterns referenced from SKILL.md §9 and §10.

---

## Scenario 1: Building Test Coverage from Near Zero

**Context:** A team has < 10% test coverage on a 2-year-old codebase. The team wants to reach 80% without stopping feature work.

**QA Engineer Approach:**

> **Incremental Coverage Strategy — "Ratchet and Don't Slip"**
>
> **Phase 1: Stop the bleeding (Week 1)**
> - Add coverage threshold to CI: start at current baseline (e.g., 8%), fail if it drops
> - Every new PR must include tests for new code — enforce with coverage diff check
>
> ```yaml
> # .github/workflows/coverage-gate.yml
> - name: Coverage check (new code must be 80%+ covered)
>   run: |
>     npx jest --coverage --coverageThreshold='{"global":{"lines":8}}'
>     git diff origin/main --name-only | grep '\.ts$' > changed_files.txt
>     npx diff-cover coverage/lcov.info --compare-branch=origin/main --fail-under=80
> ```
>
> **Phase 2: Cover the critical paths (Weeks 2-6)**
> - Identify top 10 most business-critical modules (payments, auth, data processing)
> - Write tests for these first — 20% of the code often drives 80% of the risk
> - Use mutation testing to check if existing tests are meaningful
>
> **Phase 3: Raise the bar incrementally (Months 2-6)**
> - Each sprint, raise the global threshold by 2-5%
> - Track coverage trend in Codecov — celebrate improvements in team retros

---

## Scenario 2: Eliminating Flaky E2E Tests

**Context:** The E2E test suite has 30% flakiness rate. Engineers disable failing tests rather than fix them. CI is no longer trusted.

**QA Engineer Approach:**

> **Step 1: Quarantine immediately**
> ```typescript
> test.skip('FLAKY: checkout flow times out on payment step — JIRA QA-234', async ({ page }) => {});
> test('payment flow', { retries: 3 }, async ({ page }) => {});
> ```
>
> **Step 2: Root cause analysis**
> - **Timing issues** → wait for actual conditions, not arbitrary sleeps
> - **Test data collision** → each test creates isolated data
> - **Network instability** → add explicit waits for API responses
> - **Animations** → disable in Playwright config
>
> **Step 3: Measure and prevent regression**
> - Track flakiness rate per test weekly
> - Any test with > 5% flakiness rate gets a fix-or-delete decision

---

## Scenario 3: Performance Testing a New Feature

**Context:** A new search feature is launching. The team has never done performance testing. The product expects 10x traffic growth.

> **Define SLOs first:**
> ```
> - p50 response time < 100ms
> - p95 response time < 500ms
> - p99 response time < 2000ms
> - Error rate < 0.1%
> - Throughput: 1000 RPS sustained, 3000 RPS peak
> ```
>
> **Test pyramid: Smoke → Load → Stress → Soak**
>
> ```javascript
> // k6 smoke test (5 VUs, 1 minute)
> export const options = { vus: 5, duration: '1m',
>   thresholds: { http_req_duration: ['p(99)<2000'] }
> };
>
> // k6 load test (ramp to 1000 RPS)
> export const options = {
>   stages: [
>     { duration: '5m', target: 500 },
>     { duration: '10m', target: 1000 },
>     { duration: '5m', target: 0 },
>   ],
> };
> ```

---

## Scenario 4: Testing Implementation vs Behavior

**❌ Anti-Pattern:**
```typescript
// These tests break on every refactoring, even if behavior is correct
describe('PricingService', () => {
  it('calls applyTierMultiplier with correct rate', () => {
    const spy = jest.spyOn(pricingService, 'applyTierMultiplier');
    pricingService.calculateDiscount(100, 'premium');
    expect(spy).toHaveBeenCalledWith(0.9);
  });
});
```

**✅ Fix — Test behavior, not implementation:**
```typescript
describe('PricingService', () => {
  describe('calculateDiscount', () => {
    it('applies 10% discount for premium tier', () => {
      const result = pricingService.calculateDiscount(100, 'premium');
      expect(result).toBe(90);
    });

    it('applies 0% discount for standard tier', () => {
      const result = pricingService.calculateDiscount(100, 'standard');
      expect(result).toBe(100);
    });

    it('throws on invalid tier', () => {
      expect(() => pricingService.calculateDiscount(100, 'invalid'))
        .toThrow('Unknown tier: invalid');
    });
  });
});
```

---

## Anti-Patterns Quick Reference (§10)

| Pitfall | Bad Pattern | Fix |
|---------|-------------|-----|
| **Arbitrary sleep** | `waitForTimeout(3000)` | Wait for actual condition |
| **Shared mutable state** | Global test user shared across tests | Each test creates isolated data |
| **Coverage as goal** | Test asserts `toBeDefined()` | Mutation testing, meaningful assertions |
| **Skip non-functional** | No perf/security in CI | k6 smoke + ZAP in required stages |
| **Giant test files** | 500-line flat test file | Page Object Model + describe blocks |
