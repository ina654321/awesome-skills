## § 7 · Standard Workflow

### Phase 1: Component Design (Day 1)

```
├── Design component API (props interface)
├── Consider accessibility requirements
├── Plan for responsive behavior
├── Create Storybook story
└── [✓ Done]: API designed, stories created
    [✗ FAIL]: API unclear → design review
```

### Phase 2: Implementation (Days 2-3)

```
├── Implement component with TypeScript
├── Add styles (Tailwind/CSS-in-JS)
├── Write unit tests
├── Accessibility audit (axe-core)
└── [✓ Done]: Component implemented, tested
    [✗ FAIL]: a11y issues → fix before merge
```

### Phase 3: Integration (Day 4)

```
├── Integrate into feature
├── Test in real application context
├── Performance profiling
├── Responsive testing
└── [✓ Done]: Feature complete, optimized
    [✗ FAIL]: Performance issues → optimize
```

### Phase 4: Documentation (Day 5)

```
├── Document props and usage
├── Add Storybook examples
├── Update changelog
├── Code review
└── [✓ Done]: Documented, reviewed, merged
    [✗ FAIL]: Documentation incomplete → complete
```

---
