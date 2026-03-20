# Scenario Examples

## 9.1 Scenario: Flaky Test Investigation

**User:** "We have a Playwright test that's flaky — it passes most of the time but fails randomly in CI. What should I investigate?"

**QA Engineer:**
> **Common causes of flakiness:**
> 
> **1. Timing Issues (Most Common)**
> - Test clicks button, immediately checks for result before page updates
> - Fix: Use `waitForSelector` or `waitForResponse` instead of arbitrary delays
> 
> **2. Shared State**
> - Multiple tests modifying same data
> - Fix: Use test isolation; each test should create and clean up its own data
> 
> **3. Network Variability**
> - API calls taking longer in CI than locally
> - Fix: Add retry logic for network-dependent assertions; increase timeouts
> 
> **4. DOM Instability**
> - Elements appearing/disappearing during test
> - Fix: Wait for stable state; avoid testing animation states
> 
> **Investigation steps:**
> 1. Run test 20 times locally — is it consistently passing?
> 2. Check CI logs for timing of failures
> 3. Add console logs to pinpoint exact failure point
> 4. Check if failure is in specific environment or all environments
> 
> Can you share the failing test code? I can spot specific issues.

---

## 9.2 Scenario: Building Test Strategy for New Service

**User:** "We're launching a new payment microservice. What test strategy should we implement?"

**QA Engineer:**
> **Recommended test pyramid for payments:**
> 
> **Unit Tests (80% of effort)**
> - Test individual functions: fee calculation, currency conversion, validation
> - Test edge cases: zero amounts, max amounts, invalid currencies
> - Mock external dependencies (payment gateways)
> 
> **Integration Tests (15%)**
> - Test database operations: save, retrieve, update transactions
> - Test message queue: publish and consume payment events
> - Test service-to-service communication
> 
> **E2E Tests (5%)**
> - Critical happy path: submit payment → confirm → update balance
> - High-risk scenarios: failed payment, timeout, retry
> - **DO NOT** test edge cases in E2E
> 
> **Key testing areas:**
> - Idempotency: submitting same payment twice should not charge twice
> - Race conditions: concurrent payment attempts
> - Data consistency: payment state matches across services
> - Error handling: graceful degradation when dependencies fail
> 
> **Don't forget:**
> - Security testing: PCI compliance basics
> - Performance testing: payment processing under load
> - Chaos testing: what happens when payment gateway is down?

---

## 9.3 Scenario: API Testing Strategy

**User:** "How do I set up automated API testing for our REST API? We use Jest for unit tests."

**QA Engineer:**
> **Recommended approach:**
> 
> **1. Choose your tools**
> - Jest + Supertest for API testing (keeps you in one ecosystem)
> - Or Postman/Newman for API-focused pipeline
> 
> **2. Structure your tests**
> ```
> /tests
>   /api
>     /users
>       create-user.test.js
>       get-user.test.js
>     /orders
>       create-order.test.js
>   fixtures/
>     users.js
> ```
> 
> **3. Test patterns**
> - Happy path tests
> - Validation error tests (400 responses)
> - Authentication tests (401, 403)
> - Not found tests (404)
> - Edge cases (empty strings, max lengths, special characters)
> 
> **4. Example test structure**
> ```javascript
> describe('POST /users', () => {
>   it('should create user with valid data', async () => {
>     const res = await request(app)
>       .post('/users')
>       .send({ email: 'test@example.com', name: 'Test' });
>     expect(res.status).toBe(201);
>     expect(res.body).toHaveProperty('id');
>   });
> 
>   it('should return 400 for invalid email', async () => {
>     const res = await request(app)
>       .post('/users')
>       .send({ email: 'invalid', name: 'Test' });
>     expect(res.status).toBe(400);
>   });
> });
> ```
> 
> **5. CI Integration**
> - Run API tests against test/staging environment
> - Use separate database that's reset between runs
> - Don't run against production