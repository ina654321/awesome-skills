# Common Pitfalls & Anti-Patterns

## 10.1 High-Severity Anti-Patterns

### 🔴 Anti-Pattern 1: Test Implementation Details
```
❌ BAD: expect(component.state.activeTab).toBe('details')
✅ GOOD: expect(getByText('Details Tab')).toBeVisible()
```
**Why it matters**: Tests that check implementation details break with refactoring; test behavior users see.

### 🔴 Anti-Pattern 2: No Test Isolation
```
❌ BAD: Tests share database; Test A's data affects Test B
✅ GOOD: Each test creates and tears down its own data
```
**Why it matters**: Shared state causes flaky tests and makes debugging impossible.

### 🔴 Anti-Pattern 3: Slow E2E Tests for Everything
```
❌ BAD: Testing login form validation with full E2E test
✅ GOOD: Unit test for validation logic; E2E for complete user flows only
```
**Why it matters**: E2E tests are slow and expensive; reserve for high-value scenarios.

### 🔴 Anti-Pattern 4: Ignoring Flaky Tests
```
❌ BAD: "It's only failing 10% of the time, we'll fix it later"
✅ GOOD: Flaky tests are worse than no tests — fix immediately or delete
```
**Why it matters**: Team learns to ignore test failures; real failures get dismissed.

## 10.2 Medium-Severity Anti-Patterns

### 🟡 Anti-Pattern 5: Test Data Magic Numbers
```
❌ BAD: userId: 12345 appearing everywhere with no context
✅ GOOD: createTestUser({ id: 'user_001', role: 'admin' })
```

### 🟡 Anti-Pattern 6: No Retry Strategy
```
❌ BAD: Tests fail immediately on network flakiness
✅ GOOD: Configure retry for transient failures (not for logic errors)
```

### 🟡 Anti-Pattern 7: Hardcoded Timestamps
```
❌ BAD: expect(user.createdAt).toBe('2024-01-01')
✅ GOOD: expect user.createdAt to be within last second
```

### 🟡 Anti-Pattern 8: Testing Only Happy Paths
```
❌ BAD: Only testing successful scenarios
✅ GOOD: Test error cases, edge cases, boundary conditions
```

## 10.3 Best Practices Checklist

### Before Writing Tests
- [ ] Identify what behavior you're testing
- [ ] Decide which test type (unit, integration, E2E)
- [ ] Understand test data requirements

### Writing Tests
- [ ] Follow AAA pattern (Arrange, Act, Assert)
- [ ] One assertion concept per test (or closely related)
- [ ] Descriptive test names: "should return 404 when user not found"
- [ ] No logic in tests (no loops, if statements)

### Maintaining Tests
- [ ] Review test failures immediately
- [ ] Fix or delete flaky tests
- [ ] Refactor tests when refactoring code
- [ ] Monitor test execution time

## 10.4 Red Flags to Watch For

| Red Flag | Risk Level | Action |
|----------|------------|--------|
| >5% flaky test rate | High | Dedicate sprint to fixing flakiness |
| Tests taking >10 minutes | Medium | Parallelize, reduce E2E coverage |
| Coverage <70% on critical paths | High | Add targeted tests for gaps |
| No performance tests | Medium | Add load tests for critical paths |
| Manual testing for automatable scenarios | Medium | Prioritize automation |