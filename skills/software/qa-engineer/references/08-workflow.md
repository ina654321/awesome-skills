# Standard Workflow

## 8.1 Test-Driven Development (TDD) Workflow

### Red Phase
1. Write a failing test that describes the desired behavior
2. Test should fail for the right reason (behavior not implemented)
3. Keep test small and focused

### Green Phase
1. Write minimum code to make test pass
2. No refactoring yet — just make it work
3. Tests guide the implementation

### Refactor Phase
1. Improve code structure while keeping tests green
2. Remove duplication
3. Improve naming
4. Re-run all tests

## 8.2 Test Automation Development

### Phase 1: Identify Test Cases
1. Review requirements and user stories
2. Identify positive and negative test cases
3. Map to test pyramid level
4. Prioritize by risk and frequency

### Phase 2: Select Appropriate Tools
- Unit tests: Jest, pytest, JUnit
- API tests: Postman, Rest Assured, Supertest
- E2E tests: Playwright, Cypress, Selenium
- Performance: k6, Locust, JMeter

### Phase 3: Write Tests
1. Create test data/fixtures
2. Write test in Given-When-Then format
3. Follow naming conventions: `describe` for suite, `it` for cases
4. Include assertions for expected behavior

### Phase 4: Integrate with CI/CD
1. Add test stage to pipeline
2. Set failure conditions
3. Configure parallel execution for speed
4. Set up test reporting

## 8.3 Bug Investigation Workflow

### Step 1: Reproduce
- Gather environment details (version, OS, browser)
- Document exact steps to reproduce
- Create minimal reproduction case
- Verify bug exists in current version

### Step 2: Isolate
- Identify which component/service fails
- Check recent changes to that area
- Test in isolation if possible
- Determine root cause, not just symptoms

### Step 3: Report
- Write clear bug report with:
  - Summary
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details
  - Screenshots/logs if applicable

### Step 4: Verify Fix
- Confirm fix in staging
- Run regression tests
- Verify fix doesn't break other areas
- Update test suite if needed

## 8.4 Test Strategy Development

### Step 1: Understand Product
- Review product requirements and roadmap
- Identify critical user journeys
- Map system architecture
- Understand team capabilities and constraints

### Step 2: Risk Assessment
- Identify high-risk areas (payments, auth, data)
- Assess technical complexity
- Evaluate change frequency
- Consider customer impact

### Step 3: Define Test Approach
- Unit testing strategy (coverage targets, mocking)
- Integration testing scope
- E2E test selection
- Manual/exploratory testing areas
- Performance testing triggers

### Step 4: Implement and Iterate
- Start with highest ROI tests
- Automate repetitive manual testing
- Measure and adjust
- Continuously refine based on defect data