# QA Engineer — Standards & Reference

## 7.1 Testing Standards

### Test Pyramid — Proportional Investment Model

The test pyramid is a strategy guide, not a strict law. The ratios represent the **cost and maintenance burden** of each test type, not the importance.

```
                                    ┌─────────────────────────┐
                                    │     E2E / System         │  < 10%
                                    │  Full user journeys       │  Slow, expensive
                           ┌────────┴─────────────────────────┴────────┐
                           │         Integration / Contract             │  ~20%
                           │  Service boundaries, DB, message queues    │
              ┌────────────┴───────────────────────────────────────────┴─┐
              │                    Unit / Component                       │  ~70%
              │  Isolated functions, classes, pure logic                   │
              │  Fast (<1ms each), cheap to run, reliable                 │
──────────────┴───────────────────────────────────────────────────────────┘

Target ratio (by execution time and maintenance cost):
  Unit: 70% of total test investment
  Integration: 20%
  E2E: 10% or less

Anti-patterns to avoid:
  - Ice cream cone: Many E2E, few unit tests → expensive, slow, flaky
  - Hourglass: Many unit + E2E, no integration → misses service boundary bugs
```

### ISO/IEC 25010 — Software Quality Model

The SQuaRE standard defines quality characteristics that tests should validate:

| Characteristic | Sub-characteristics | Test Coverage |
|---------------|---------------------|---------------|
| **Functional Suitability** | Completeness, correctness, appropriateness | Happy path, edge cases, error handling |
| **Performance Efficiency** | Time behavior, resource utilization | Load tests, stress tests, performance benchmarks |
| **Compatibility** | Co-existence, interoperability | Multi-version, cross-browser, API contract |
| **Usability** | Operability, user error protection | UX testing, accessibility (WCAG 2.1) |
| **Reliability** | Maturity, availability, fault tolerance | Resilience tests, chaos testing |
| **Security** | Confidentiality, integrity, non-repudiation | SAST, DAST, penetration testing |
| **Maintainability** | Modularity, reusability, analysability | Code quality, complexity metrics, mutation testing |
| **Portability** | Adaptability, installability | Cross-platform testing, migration testing |

**Reference:** [ISO/IEC 25010:2011](https://www.iso.org/standard/35733.html)

### IEEE 829 — Software Test Documentation Standard

The canonical standard for test documentation artifacts:

| Document | Purpose | Contents |
|---------|---------|----------|
| **Test Plan** | Scope, approach, resources, schedule | Test strategy, environment, roles, risk assessment |
| **Test Case Specification** | Detailed test steps | Pre-conditions, inputs, expected results, test data |
| **Test Procedure** | Executable steps | How to execute each test case |
| **Test Log** | Execution record | Actual results, anomalies, tester ID, timestamp |
| **Test Summary Report** | Post-execution evaluation | Metrics, coverage, defects, recommendations |

---

## 7.2 API Testing Standards

### REST API Testing Checklist

For every REST endpoint, test these dimensions:

| Test Category | What to Test |
|--------------|-------------|
| **Happy path** | Valid inputs → expected 200/201, correct response schema |
| **Input validation** | Invalid types, missing required fields, out-of-range values → 400 |
| **Authentication** | Missing token → 401; invalid token → 401; expired token → 401 |
| **Authorization** | Valid auth, wrong scope → 403; resource belongs to another user → 403 |
| **Not found** | Valid ID format, non-existent resource → 404 |
| **Conflict** | Duplicate create → 409 (e.g., duplicate email) |
| **Rate limiting** | Exceed quota → 429 with Retry-After header |
| **Payload limits** | Oversized request body → 413 |
| **Error schema** | All error responses conform to documented error schema |

### GraphQL API Testing

| Test Dimension | Approach |
|---------------|----------|
| **Query execution** | Valid queries return expected data shape |
| **Variable validation** | Invalid types/missing required vars → 400 with specific error |
| **Authorization** | User A cannot query User B's private fields |
| **Rate limiting** | Query complexity limit enforced |
| **Introspection** | Introspection disabled in production (security) |
| **Error responses** | Partial success (some fields error) handled gracefully |

### Contract Testing — Pact & Spring Cloud Contract

For microservices, contract testing prevents integration breakage:

```
Consumer (Test)                    Provider (Test)
     │                                   │
     │  ──── Pact file published ────▶  │
     │     (exposes expectations)         │
     │                                   │
     │                                   │  Validates against real implementation
     │                                   │  Returns: can I satisfy your contract?
     │  ◀─── Pact Broker ◀───────────  │
     │     (shared contract results)     │
```

**Pact Broker workflow:**
```bash
# Consumer side — write consumer tests
npx pact-broker publish ./pacts \
  --broker-base-url=https://pact-broker.example.com \
  --consumer-version=1.0.0

# Provider side — verify against consumer contracts
npx pact-provider-verifier \
  --provider-base-url=https://provider-api.example.com \
  --pact-broker-url=https://pact-broker.example.com
```

---

## 7.3 Performance Testing Standards

### The k6 Performance Testing Hierarchy

k6 is the modern choice for scriptable, developer-friendly load testing.

```
Test Types:
  ┌──────────────────────────────────────────────────┐
  │ SMOKE TEST (pre-deploy)                          │
  │ - 1-5 VUs, 1-5 minutes                          │
  │ - Is the system basically working under load?    │
  │ - Pass criteria: p95 < 2× SLO, error rate < 1% │
  └──────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────────────────────────────────────────────┐
  │ LOAD TEST (SLO validation)                       │
  │ - Ramp to expected peak: 10-30 minutes          │
  │ - Validate SLOs at normal load                  │
  │ - Pass criteria: p95 < SLO, error rate < 0.1%   │
  └──────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────────────────────────────────────────────┐
  │ STRESS TEST (find breaking point)               │
  │ - Ramp 2-5× above peak                          │
  │ - Find where system degrades or fails           │
  │ - Document capacity ceiling                      │
  └──────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────────────────────────────────────────────┐
  │ SOAK TEST (reliability validation)              │
  │ - Sustained load at 80% of peak for 1-4 hours   │
  │ - Find memory leaks, connection pool exhaustion │
  │ - Monitor for gradual error rate increase        │
  └──────────────────────────────────────────────────┘
```

### SLO-Based Load Test Targets

Define SLOs before writing load tests. These are your pass/fail gates:

| Metric | Measurement Point | Target | Alert Threshold |
|--------|------------------|--------|----------------|
| **Availability** | All endpoints | ≥ 99.9% | < 99.9% = page |
| **Latency (p50)** | All endpoints | < 100ms | > 200ms = page |
| **Latency (p95)** | All endpoints | < 500ms | > 1s = page |
| **Latency (p99)** | All endpoints | < 2s | > 5s = page |
| **Error rate** | All endpoints | < 0.1% | > 1% = page |
| **Throughput** | Key endpoints | ≥ N RPS | < 50% expected = warn |

### Gatling vs k6 vs Locust — Tool Selection Guide

| Tool | Best For | Pros | Cons |
|------|---------|------|------|
| **k6** | Modern teams, CI/CD | Scriptable in JS/Go, Grafana native, cloud results | Less enterprise reporting than JMeter |
| **Gatling** | Complex scenarios, Scala/Java teams | Powerful DSL, excellent reports, enterprise support | Scala DSL; harder to pick up |
| **Locust** | Python teams | Python scripting, distributed testing | UI-centric; not CI-friendly |
| **JMeter** | Enterprise, legacy teams | GUI, extensive plugins, broad protocol support | Memory-intensive, hard to maintain |
| **Artillery** | Node.js teams | Simple YAML, real-time metrics | Limited scripting compared to k6 |

---

## 7.4 Mobile Testing Standards

### Platform-Specific Testing Requirements

| Platform | Framework | What to Test |
|---------|-----------|-------------|
| **iOS** | XCTest + XCUITest | UI testing, accessibility (VoiceOver), notch/pill safe areas, Dark Mode |
| **Android** | Espresso + UIAutomator | UI testing, accessibility, various screen sizes/densities |
| **React Native** | Detox | Cross-platform, native bridge, JS bundle loading |
| **Flutter** | Flutter Driver / Integration Test | Cross-platform widget tests, platform channels |
| **Both** | Appium | Cross-platform WebView, hybrid apps |

### Mobile-Specific Test Cases

- **Offline behavior:** App handles network loss gracefully (shows offline indicator, queues actions)
- **Background/foreground transitions:** State preserved on backgrounding
- **Push notification permissions:** App requests correctly; handles opt-out
- **Biometric auth fallback:** Face ID/Touch ID → PIN fallback works
- **Deep links:** Universal links open correct app screen
- **Memory pressure:** App handles low memory gracefully; no crashes when backgrounded
- **OTA updates:** App handles version mismatch gracefully

---

## 7.5 Accessibility (A11y) Testing Standards

### WCAG 2.1 Level AA — Required for Most Products

| Principle | Guideline | Test Method |
|-----------|----------|-------------|
| **Perceivable** | Text alternatives for images (alt text) | axe-core automated + manual review |
| **Perceivable** | Captions for video (WCAG 2.1 AA) | Manual review + axe-core |
| **Perceivable** | Color contrast ≥ 4.5:1 (text), ≥ 3:1 (large text) | axe-core contrast check, Colour Contrast Analyser |
| **Operable** | Keyboard navigable (no trap) | Manual keyboard-only testing |
| **Operable** | Focus order is logical | Manual tab navigation test |
| **Operable** | No keyboard traps (Tab/Escape works) | Manual testing |
| **Operable** | Skip navigation links | Manual review |
| **Understandable** | Language declared in HTML | Automated |
| **Understandable** | Error identification + suggestion | Manual |
| **Robust** | Valid HTML | W3C validator |
| **Robust** | ARIA used correctly | axe-core, manual ARIA review |

**Reference:** [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)

### Automated Accessibility Testing

```typescript
// Playwright — axe-core integration
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('accessibility scan on homepage', async ({ page }) => {
  const violations = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  expect(violations.length).toBe(0);
  // If violations exist, log them:
  violations.forEach(v => {
    console.log(`${v.id}: ${v.description} (${v.impact})`);
    console.log(`  Help: ${v.helpUrl}`);
    console.log(`  Elements: ${v.nodes.map(n => n.html).join(', ')}`);
  });
});
```

---

## 7.6 Security Testing Standards

### OWASP ZAP Integration in CI/CD

| Test Type | When | Tool | Pass Criteria |
|-----------|------|------|---------------|
| **DAST baseline scan** | Every PR → staging | OWASP ZAP baseline | No HIGH/CRITICAL |
| **DAST full scan** | Weekly / before release | OWASP ZAP full | No HIGH/CRITICAL |
| **SAST** | Every PR | Semgrep, SonarQube | No HIGH/CRITICAL in new code |
| **Dependency scan** | Every PR | npm audit, Snyk, Dependabot | No HIGH/CRITICAL CVEs |
| **Secrets scan** | Every PR | Gitleaks, TruffleHog | Zero new secrets |
| **Infrastructure scan** | Every apply | tfsec, Checkov | No HIGH/CRITICAL |

```yaml
# GitHub Actions — ZAP baseline scan
- name: OWASP ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.9.0
  with:
    target: 'https://staging.example.com'
    rules: '-category:browser'
    cmdline: 'zap-baseline.py -t {target}'
  continue-on-error: false
```

---

## 7.7 Quality Metrics & Targets

| Metric | Definition | Target | Measurement |
|--------|-----------|--------|-------------|
| **Code Coverage** | Lines executed / total executable lines | ≥ 80% (new code), ≥ 70% (legacy) | jest --coverage, pytest --cov |
| **Mutation Score** | Surviving mutations / total | ≥ 65% (indicates tests catch real bugs) | Stryker, PITest |
| **Defect Escape Rate** | Production bugs / total bugs | < 5% | Bug tracker + prod monitoring |
| **Flakiness Rate** | Flaky test runs / total test runs | < 0.5% | CI retry analytics |
| **MTTR (Test Fix)** | Mean time to repair broken test | < 4 hours | CI analytics |
| **Test Execution Time** | Full suite runtime | < 15 minutes (E2E < 30min) | CI pipeline |
| **API Coverage** | Documented endpoints with test coverage | 100% | OpenAPI coverage check |
| **Automated Pass Rate** | % PRs passing automated gates | > 95% | CI dashboard |
| **Accessibility Violations** | Critical/Major WCAG issues | 0 critical, < 5 major | axe-core in CI |
| **Performance Regression** | p95 latency delta vs baseline | < 10% regression | k6 comparison |

---

## 7.8 Professional QA Standards & Certifications

| Standard/Certification | Body | Focus |
|-----------------------|------|-------|
| **ISTQB Foundation Level** | ISTQB | Test design, techniques, lifecycle |
| **ISTQB Agile Tester** | ISTQB | Agile testing practices, ATDD |
| **Certified Selenium Professional** | Bread Runner | Selenium WebDriver automation |
| **AWS Certified Cloud Practitioner** | AWS | Cloud fundamentals for cloud-based testing |
| **Google Testing Blog** | Google | Internal testing philosophy (Set Phasers on STC) |
| **Microsoft Engineering Pipeline** | Microsoft | SDL + testing integration |

---

## 7.9 Key QA Reference Standards Index

| Standard | Version | Body | URL |
|---------|---------|------|-----|
| ISO/IEC 25010 | 2011 | ISO | iso.org/standard/35733 |
| IEEE 829 | 2008 | IEEE | standards.ieee.org/standard/829 |
| WCAG | 2.1 | W3C | w3.org/TR/WCAG21 |
| ISTQB Syllabus | 2018 | ISTQB | istqb.org |
| OWASP Testing Guide | v4.2 | OWASP | owasp.org/www-project-web-security-testing-guide |
| Google Testing Blog | — | Google | testing.googleblog.com |
| Microsoft SDL | — | Microsoft | docs.microsoft.com/en-us/windows/security/threat-protection |
| NIST SP 800-137 | — | NIST | csrc.nist.gov/publications/detail/sp/800-137/final |
