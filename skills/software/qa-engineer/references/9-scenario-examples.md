## § 9 · Scenario Examples

### Scenario 1: E-Commerce Checkout Flow Testing

**Context:** An e-commerce platform needs comprehensive test coverage for checkout, spanning cart management, payment processing, inventory validation, and order confirmation across multiple microservices.

**Challenge:** Previous releases had bugs in payment calculation, inventory overselling, and race conditions. The team needs a test strategy that prevents regressions while maintaining fast feedback.

**Test Implementation:**

```typescript
// tests/unit/payment/calculation.spec.ts
import { describe, it, expect } from 'vitest';
import { calculateOrderTotal } from '@/services/payment/calculation';

describe('Order Total Calculation', () => {
  describe('with single item', () => {
    it('should calculate total without discount', () => {
      const items = [{ price: 99.99, quantity: 1 }];
      expect(calculateOrderTotal(items)).toBe(99.99);
    });
  });

  describe('with multiple items', () => {
    it('should sum all item prices', () => {
      const items = [
        { price: 50.00, quantity: 2 },
        { price: 25.00, quantity: 1 }
      ];
      expect(calculateOrderTotal(items)).toBe(125.00);
    });
  });

  describe('with discount codes', () => {
    it('should apply percentage discount correctly', () => {
      const items = [{ price: 100.00, quantity: 1 }];
      expect(calculateOrderTotal(items, { code: 'SAVE20', type: 'percent', value: 20 }))
        .toBe(80.00);
    });

    it('should not apply expired discount', () => {
      const items = [{ price: 100.00, quantity: 1 }];
      const expiredDiscount = { 
        code: 'EXPIRED', 
        type: 'percent', 
        value: 20,
        expiresAt: new Date('2020-01-01')
      };
      expect(calculateOrderTotal(items, expiredDiscount)).toBe(100.00);
    });
  });

  describe('boundary values', () => {
    it('should handle zero quantity', () => {
      const items = [{ price: 99.99, quantity: 0 }];
      expect(calculateOrderTotal(items)).toBe(0);
    });

    it('should handle very large quantities', () => {
      const items = [{ price: 0.01, quantity: 1000000 }];
      expect(calculateOrderTotal(items)).toBe(10000.00);
    });
  });
});
```

```typescript
// tests/integration/checkout/checkout.flow.spec.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestDatabase } from '@test/infrastructure/TestDatabase';
import { CartService } from '@/services/cart/CartService';
import { InventoryService } from '@/services/inventory/InventoryService';
import { PaymentService } from '@/services/payment/PaymentService';
import { CheckoutService } from '@/services/checkout/CheckoutService';
import { testDataFactory } from '@test/factories';

describe('Checkout Flow Integration', () => {
  let db: TestDatabase;
  let checkoutService: CheckoutService;

  beforeEach(async () => {
    db = await TestDatabase.create();
    await testDataFactory.cleanDatabase();
    checkoutService = new CheckoutService(db);
  });

  afterEach(async () => {
    await db.destroy();
  });

  describe('Happy Path', () => {
    it('completes purchase with sufficient inventory', async () => {
      // Arrange
      const product = await testDataFactory.createProduct({ 
        price: 99.99, 
        inventory: 100 
      });
      const user = await testDataFactory.createUser({ 
        email: 'test@example.com',
        balance: 200.00 
      });
      
      // Act
      await checkoutService.addToCart(user.id, product.id, 2);
      const order = await checkoutService.processCheckout({
        userId: user.id,
        shippingAddress: testDataFactory.validAddress()
      });
      
      // Assert
      expect(order.status).toBe('confirmed');
      expect(order.total).toBe(199.98);
      expect(await db.inventory.getStock(product.id)).toBe(98);
      expect(await db.users.getBalance(user.id)).toBe(0.02);
    });
  });

  describe('Race Condition Handling', () => {
    it('prevents overselling when two users buy last item', async () => {
      const product = await testDataFactory.createProduct({ inventory: 1 });
      const user1 = await testDataFactory.createUser({ balance: 100 });
      const user2 = await testDataFactory.createUser({ balance: 100 });
      
      // Both users add to cart simultaneously
      await checkoutService.addToCart(user1.id, product.id, 1);
      await checkoutService.addToCart(user2.id, product.id, 1);
      
      // Attempt concurrent checkout
      const [result1, result2] = await Promise.allSettled([
        checkoutService.processCheckout({ userId: user1.id, shippingAddress: {} }),
        checkoutService.processCheckout({ userId: user2.id, shippingAddress: {} })
      ]);
      
      // One succeeds, one fails with inventory error
      const outcomes = [result1, result2].map(r => r.status);
      expect(outcomes.filter(s => s === 'fulfilled')).toHaveLength(1);
      expect(outcomes.filter(s => s === 'rejected')).toHaveLength(1);
      
      // Verify inventory consistency
      expect(await db.inventory.getStock(product.id)).toBe(0);
    });
  });

  describe('Failure Recovery', () => {
    it('rolls back transaction when payment fails', async () => {
      const product = await testDataFactory.createProduct({ inventory: 10 });
      const user = await testDataFactory.createUser({ balance: 0 }); // Insufficient funds
      
      await checkoutService.addToCart(user.id, product.id, 5);
      
      await expect(
        checkoutService.processCheckout({ userId: user.id, shippingAddress: {} })
      ).rejects.toThrow('Insufficient funds');
      
      // Verify no side effects
      expect(await db.inventory.getStock(product.id)).toBe(10);
      expect(await db.orders.findByUser(user.id)).toHaveLength(0);
    });

    it('handles partial failure with retry queue', async () => {
      const product = await testDataFactory.createProduct({ inventory: 5 });
      const user = await testDataFactory.createUser({ balance: 500 });
      
      // Mock notification service to fail
      jest.spyOn(notificationService, 'send').mockRejectedValue(new Error('SMTP error'));
      
      const order = await checkoutService.processCheckout({
        userId: user.id,
        shippingAddress: testDataFactory.validAddress()
      });
      
      // Order confirmed despite notification failure
      expect(order.status).toBe('confirmed');
      // Notification queued for retry
      expect(await db.retryQueue.count()).toBe(1);
    });
  });
});
```

```typescript
// tests/e2e/checkout.spec.ts (Playwright)
import { test, expect } from '@playwright/test';
import { CheckoutPage } from './pages/CheckoutPage';
import { testDataFactory } from './factories';

test.describe('Checkout E2E', () => {
  test('completes purchase end-to-end', async ({ page }) => {
    const checkoutPage = new CheckoutPage(page);
    const user = await testDataFactory.createUser({ balance: 200 });
    const product = await testDataFactory.createProduct({ price: 99.99 });
    
    // Login
    await checkoutPage.login(user.email, user.password);
    
    // Add to cart
    await checkoutPage.addToCart(product.id);
    
    // Proceed to checkout
    await checkoutPage.goToCheckout();
    await checkoutPage.fillShippingAddress(testDataFactory.validAddress());
    await checkoutPage.selectPaymentMethod('credit_card');
    
    // Submit order
    await checkoutPage.placeOrder();
    
    // Verify success
    await expect(page).toHaveURL(/\/order\/confirmation/);
    await expect(page.locator('[data-testid="order-success"]')).toBeVisible();
    await expect(page.locator('[data-testid="order-total"]')).toContainText('$99.99');
  });

  test('shows error for insufficient inventory', async ({ page }) => {
    const checkoutPage = new CheckoutPage(page);
    const user = await testDataFactory.createUser();
    const product = await testDataFactory.createProduct({ inventory: 0 });
    
    await checkoutPage.login(user.email, user.password);
    await checkoutPage.addToCart(product.id);
    await checkoutPage.goToCheckout();
    
    const errorMessage = page.locator('[data-testid="inventory-error"]');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('Out of stock');
  });
});
```

**Outcome:**
- Unit test coverage: 87%
- Integration test coverage: 92%
- Zero critical bugs in checkout over 6 releases
- Test execution time: 3.2 minutes for full suite
- Flakiness rate: 0.3%

---

### Scenario 2: API Performance Testing with k6

**Context:** A SaaS platform needs to validate their REST API can handle 2000 concurrent users with p99 latency under 150ms before a major product launch.

**Challenge:** Previous load tests were manual and run too late in the cycle. The team needs automated performance gates and comprehensive load testing patterns.

**k6 Test Implementation:**

```javascript
// tests/performance/api.load.test.js
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const apiLatency = new Trend('api_latency');
const successfulLogins = new Counter('successful_logins');

// Test configuration
export const options = {
  scenarios: {
    // Smoke test: Validate basic functionality
    smoke: {
      executor: 'constant-vus',
      vus: 5,
      duration: '1m',
      tags: { test_type: 'smoke' },
    },
    // Load test: Simulate expected production traffic
    load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 500 },   // Ramp up
        { duration: '5m', target: 500 },   // Steady state
        { duration: '2m', target: 1000 },  // Ramp up
        { duration: '5m', target: 1000 },  // Steady state
        { duration: '2m', target: 2000 },  // Peak load
        { duration: '5m', target: 2000 },  // Sustained peak
        { duration: '2m', target: 0 },     // Ramp down
      ],
      tags: { test_type: 'load' },
    },
    // Stress test: Find breaking point
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 2000 },
        { duration: '2m', target: 4000 },
        { duration: '2m', target: 6000 },
        { duration: '5m', target: 8000 },
        { duration: '2m', target: 0 },
      ],
      tags: { test_type: 'stress' },
    },
  },
  thresholds: {
    http_req_duration: ['p(99)<150'],     // p99 under 150ms
    http_req_failed: ['rate<0.1'],        // Error rate < 0.1%
    errors: ['rate<0.05'],                // Custom error rate < 5%
    api_latency: ['p(95)<100'],           // 95% under 100ms
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.staging.example.com';

// Test data setup
export function setup() {
  const users = JSON.parse(open('./test-data/test-users.json'));
  
  // Authenticate and cache tokens
  const tokens = users.slice(0, 100).map(user => {
    const res = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
      email: user.email,
      password: user.password,
    }), {
      headers: { 'Content-Type': 'application/json' },
    });
    
    if (res.status === 200) {
      successfulLogins.add(1);
      return res.json('token');
    }
    return null;
  }).filter(t => t !== null);
  
  console.log(`Setup complete: ${tokens.length} valid tokens`);
  return { tokens };
}

export default function (data) {
  const userIndex = __VU % data.tokens.length;
  const token = data.tokens[userIndex];
  
  const params = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  };

  group('Core API Flows', () => {
    // GET user profile (lightweight)
    group('Profile', () => {
      const profileRes = http.get(`${BASE_URL}/users/me`, params);
      const profileSuccess = check(profileRes, {
        'profile status is 200': (r) => r.status === 200,
        'profile response time < 50ms': (r) => r.timings.duration < 50,
      });
      errorRate.add(!profileSuccess);
      apiLatency.add(profileRes.timings.duration);
    });

    // GET dashboard data (heavy query with aggregation)
    group('Dashboard', () => {
      const dashboardRes = http.get(`${BASE_URL}/dashboard`, params);
      const dashboardSuccess = check(dashboardRes, {
        'dashboard status is 200': (r) => r.status === 200,
        'dashboard response time < 150ms': (r) => r.timings.duration < 150,
        'dashboard has metrics': (r) => r.json('metrics') !== null,
        'dashboard has recent data': (r) => r.json('lastUpdated') !== null,
      });
      errorRate.add(!dashboardSuccess);
      apiLatency.add(dashboardRes.timings.duration);
    });

    // POST create resource (write operation)
    group('Create Resource', () => {
      const payload = JSON.stringify({
        title: `Performance Test Item ${Date.now()}-${__VU}`,
        description: 'Generated by k6 load test',
        priority: 'medium',
      });
      const createRes = http.post(`${BASE_URL}/items`, payload, params);
      const createSuccess = check(createRes, {
        'create status is 201': (r) => r.status === 201,
        'create response time < 100ms': (r) => r.timings.duration < 100,
        'create returns item id': (r) => r.json('id') !== undefined,
      });
      errorRate.add(!createSuccess);
      apiLatency.add(createRes.timings.duration);
      
      // If creation succeeded, try to fetch the created item
      if (createSuccess) {
        const itemId = createRes.json('id');
        const getRes = http.get(`${BASE_URL}/items/${itemId}`, params);
        check(getRes, {
          'fetch created item status is 200': (r) => r.status === 200,
          'fetch created item response time < 50ms': (r) => r.timings.duration < 50,
        });
      }
    });

    // Search endpoint (complex query)
    group('Search', () => {
      const searchRes = http.get(
        `${BASE_URL}/items/search?q=test&limit=20&sort=created`,
        params
      );
      const searchSuccess = check(searchRes, {
        'search status is 200': (r) => r.status === 200,
        'search response time < 200ms': (r) => r.timings.duration < 200,
        'search returns results array': (r) => Array.isArray(r.json('results')),
      });
      errorRate.add(!searchSuccess);
      apiLatency.add(searchRes.timings.duration);
    });
  });

  // Random sleep to simulate realistic user behavior
  sleep(Math.random() * 2 + 1);
}

export function teardown(data) {
  console.log('Performance test completed');
  console.log(`Tokens used: ${data.tokens.length}`);
  
  // Cleanup test data via API
  http.del(`${BASE_URL}/test/cleanup`, null, {
    headers: { 'X-Test-Key': __ENV.TEST_CLEANUP_KEY },
  });
}
```

**CI Integration (GitHub Actions):**

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    paths:
      - 'src/**'
      - 'tests/performance/**'
  schedule:
    - cron: '0 2 * * *'  # Nightly at 2 AM

jobs:
  performance-smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup k6
        uses: grafana/setup-k6-action@v1
        
      - name: Run Smoke Tests
        run: |
          k6 run \
            --env BASE_URL=${{ secrets.STAGING_URL }} \
            --env TEST_CLEANUP_KEY=${{ secrets.TEST_CLEANUP_KEY }} \
            --tag test_type=smoke \
            tests/performance/api.load.test.js

  performance-load:
    runs-on: ubuntu-latest
    needs: performance-smoke
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup k6
        uses: grafana/setup-k6-action@v1
        
      - name: Run Load Tests
        run: |
          k6 run \
            --env BASE_URL=${{ secrets.STAGING_URL }} \
            --env TEST_CLEANUP_KEY=${{ secrets.TEST_CLEANUP_KEY }} \
            --out influxdb=http://${{ secrets.INFLUXDB_URL }}/k6 \
            --out json=results/load-test.json \
            tests/performance/api.load.test.js
            
      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: k6-load-results
          path: results/
```

**Performance Analysis Report Template:**

```markdown
# Performance Test Report - [Date]

## Executive Summary
- Test Type: Load Test (2000 concurrent users)
- Duration: 21 minutes
- Result: ✅ PASSED / ❌ FAILED

## Key Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p99 Latency | < 150ms | 142ms | ✅ |
| p95 Latency | < 100ms | 89ms | ✅ |
| Error Rate | < 0.1% | 0.03% | ✅ |
| Throughput | > 1000 RPS | 1250 RPS | ✅ |

## Bottleneck Analysis
- Database connection pool: Optimal (no queuing)
- Redis cache hit rate: 94%
- API response time degradation: None detected

## Recommendations
- Monitor database query performance during peak hours
- Consider CDN for static assets
```

**Outcome:**
- Baseline established: p99 = 142ms at 2000 RPS
- Identified and fixed connection pool bottleneck
- Automated performance gates block PRs if p99 > 150ms
- Nightly stress tests detect performance regressions early
- Launch day: 0 performance incidents

---

### Scenario 3: Flaky Test Remediation & Quality Culture

**Context:** A team's E2E test suite has 25% flakiness rate, causing CI failures 3-4 times daily and eroding developer trust. Tests use Cypress with custom commands.

**Challenge:** Flakiness concentrated in authentication flows, form submissions, and data-dependent assertions. Team has started ignoring CI failures.

**Diagnostic Process:**

```typescript
// tests/infrastructure/flaky-test-tracker.ts
interface FlakyTestReport {
  testName: string;
  filePath: string;
  failureCount: number;
  totalRuns: number;
  flakinessRate: number;
  commonErrors: string[];
  lastFailure: Date;
}

export class FlakyTestTracker {
  private reports: Map<string, FlakyTestReport> = new Map();
  
  trackAttempt(testName: string, filePath: string, attempt: number, error?: Error) {
    const key = `${filePath}::${testName}`;
    const existing = this.reports.get(key) || {
      testName,
      filePath,
      failureCount: 0,
      totalRuns: 0,
      flakinessRate: 0,
      commonErrors: [],
      lastFailure: new Date(),
    };
    
    existing.totalRuns++;
    
    if (attempt > 1 || error) {
      existing.failureCount++;
      existing.lastFailure = new Date();
      if (error && !existing.commonErrors.includes(error.message)) {
        existing.commonErrors.push(error.message);
      }
    }
    
    existing.flakinessRate = (existing.failureCount / existing.totalRuns) * 100;
    this.reports.set(key, existing);
    
    // Auto-quarantine if flakiness exceeds threshold
    if (existing.flakinessRate > 10 && existing.totalRuns > 5) {
      this.quarantineTest(key);
    }
  }
  
  generateReport(): FlakyTestReport[] {
    return Array.from(this.reports.values())
      .filter(r => r.flakinessRate > 1)
      .sort((a, b) => b.flakinessRate - a.flakinessRate);
  }
  
  private quarantineTest(testKey: string) {
    console.warn(`arantine: ${testKey} - Flakiness: ${this.reports.get(testKey)?.flakinessRate.toFixed(1)}%`);
    // Write to quarantine file for CI exclusion
  }
}
```

**Remediation Strategy:**

```typescript
// BEFORE: Flaky authentication test
// tests/e2e/auth.spec.ts (flaky version)
describe('Authentication', () => {
  it('should login successfully', () => {
    cy.visit('/login');
    cy.get('[data-testid=email]').type('user@example.com');
    cy.get('[data-testid=password]').type('password123');
    cy.get('[data-testid=submit]').click();
    cy.url().should('include', '/dashboard'); // Flaky: no wait for navigation
  });
});

// AFTER: Stable version with proper waiting patterns
describe('Authentication', () => {
  beforeEach(() => {
    // Clean state before each test
    cy.clearCookies();
    cy.clearLocalStorage();
  });
  
  it('should login successfully', () => {
    // Use Page Object for maintainability
    const loginPage = new LoginPage();
    loginPage.visit();
    loginPage.login('user@example.com', 'password123');
    
    // Multiple assertions for stability
    cy.url({ timeout: 10000 }).should('include', '/dashboard');
    cy.get('[data-testid=dashboard-welcome]', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Welcome');
    cy.get('[data-testid=user-menu]').should('exist');
  });
});

// Page Object implementation
// tests/pages/LoginPage.ts
export class LoginPage {
  private readonly selectors = {
    email: '[data-testid=email]',
    password: '[data-testid=password]',
    submit: '[data-testid=submit]',
    errorMessage: '[data-testid=error-message]',
  };
  
  visit() {
    cy.visit('/login');
    // Wait for page to be fully loaded
    cy.get(this.selectors.email).should('be.visible');
    cy.get(this.selectors.submit).should('not.be.disabled');
  }
  
  login(email: string, password: string) {
    // Type with delay to simulate real user
    cy.get(this.selectors.email).clear().type(email, { delay: 10 });
    cy.get(this.selectors.password).clear().type(password, { delay: 10 });
    
    // Click and wait for navigation
    cy.get(this.selectors.submit).click();
  }
  
  expectError(message: string) {
    cy.get(this.selectors.errorMessage)
      .should('be.visible')
      .and('contain.text', message);
  }
  
  expectFieldError(field: 'email' | 'password', message: string) {
    cy.get(`[data-testid=${field}-error]`)
      .should('be.visible')
      .and('contain.text', message);
  }
}
```

**Root Cause Analysis & Fixes:**

```typescript
// Issue 1: Race condition in form submission
// FIXED: Wait for API response before asserting
Cypress.Commands.add('submitFormAndWait', (selector: string, apiPath: string) => {
  cy.intercept('POST', apiPath).as('formSubmit');
  cy.get(selector).click();
  cy.wait('@formSubmit');
});

// Issue 2: Test data pollution
// FIXED: Factory pattern with unique data
export const userFactory = {
  create: (overrides = {}) => ({
    email: `test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`,
    password: 'SecurePass123!',
    ...overrides,
  }),
};

// Issue 3: Brittle selectors
// FIXED: Enforce data-testid usage
// .eslintrc.js
module.exports = {
  rules: {
    'cypress/require-data-selectors': 'error',
  },
};

// Issue 4: External service dependencies
// FIXED: Stub external APIs
beforeEach(() => {
  cy.intercept('POST', '/api/external/payment', {
    statusCode: 200,
    body: { success: true, transactionId: 'mock-123' },
  }).as('paymentStub');
});
```

**Quality Metrics Dashboard:**

```typescript
// tests/infrastructure/metrics-collector.ts
export class QualityMetricsCollector {
  async collectMetrics(): Promise<QualityMetrics> {
    return {
      // Coverage metrics
      codeCoverage: await this.getCodeCoverage(),
      mutationScore: await this.getMutationScore(),
      
      // Test health
      totalTests: await this.getTotalTestCount(),
      flakyTests: await this.getFlakyTestCount(),
      flakinessRate: await this.getFlakinessRate(),
      averageTestDuration: await this.getAverageTestDuration(),
      
      // Defect metrics
      defectEscapeRate: await this.getDefectEscapeRate(),
      criticalBugsInProd: await this.getCriticalBugsInProd(),
      mttr: await this.getMeanTimeToRecovery(),
      
      // CI health
      ciPassRate: await this.getCIPassRate(),
      ciDuration: await this.getCIDuration(),
    };
  }
  
  generateReport(metrics: QualityMetrics): string {
    return `
# Quality Metrics Report - ${new Date().toISOString()}

## Coverage
- Code Coverage: ${metrics.codeCoverage}%
- Mutation Score: ${metrics.mutationScore}%

## Test Health
- Total Tests: ${metrics.totalTests}
- Flaky Tests: ${metrics.flakyTests} (${metrics.flakinessRate}%)
- Average Duration: ${metrics.averageTestDuration}s

## Defect Metrics
- Defect Escape Rate: ${metrics.defectEscapeRate}%
- Critical Bugs (Prod): ${metrics.criticalBugsInProd}
- MTTR: ${metrics.mttr}h

## CI Health  
- Pass Rate: ${metrics.ciPassRate}%
- Duration: ${metrics.ciDuration}min

## Alerts
${this.generateAlerts(metrics)}
    `;
  }
}
```

**Outcome:**
- Flakiness rate reduced from 25% to 0.5% in 3 weeks
- CI trust restored; merge times reduced by 50%
- 18 tests quarantined and fixed, 5 deleted
- Auto-quarantine system prevents flaky test proliferation
- Quality metrics dashboard drives continuous improvement

---

