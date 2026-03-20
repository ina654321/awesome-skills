# UX Designer — Troubleshooting Guide

## Usability Testing Problems

**Problem: Test participants not matching target user**
- Diagnosis: Recruiting screeners not specific enough
- Fix: Revise screener questions to verify specific experience
- Re-test: Run additional sessions with corrected recruiting
- Prevention: Validate screener with pilot participant

**Problem: Usability issues found late in design process**
- Diagnosis: Testing happened after visual design, not during
- Fix: Test at lo-fi prototype stage (paper or wireframe)
- Prevention: Test early, test often, test cheap
- Cost: Fixing at wireframe costs 1/10th of fixing at production

**Problem: Stakeholders dismissing usability findings**
- Approach: Connect findings to business metrics
- Frame: "If 60% of users fail this task, X% will not complete purchase"
- Show: Video clips are powerful evidence
- Reference: Nielsen Norman research on ROI of UX

## Design Consistency Problems

**Problem: Different patterns across the product**
- Diagnosis: No component library, or not being used
- Fix: Audit all existing patterns
- Consolidate: Choose canonical version
- Document: In design system with clear usage rules
- Enforce: Design review gate for new components

**Problem: Design system not adopted by team**
- Diagnosis: Too complex, not integrated, or not maintained
- Assessment: What are the barriers to adoption?
- Fix: Simplify, integrate into workflow, show value
- Governance: Assign design system owner
- Training: Team workshops on using system

**Problem: Inconsistent error handling across forms**
- Fix: Audit all forms
- Create: Standard error message pattern
- Include: Error positioning, language, and recovery guidance
- Document: In design system

## Accessibility Problems

**Problem: Low contrast text throughout product**
- Diagnosis: Designers choosing aesthetically pleasing over readable
- Fix: Run accessibility audit (axe DevTools)
- Review: All text combinations against 4.5:1 ratio
- Fix: Update to compliant colors
- Prevention: Add contrast checking to design review checklist

**Problem: Keyboard navigation doesn't follow logical order**
- Diagnosis: Focus order not considered in design
- Fix: Review focus order with developer
- Test: Tab through every flow
- Fix: Reorder components or use tabindex carefully

**Problem: Screen reader can't access important content**
- Diagnosis: Missing ARIA labels, semantic HTML issues
- Fix: Use semantic HTML first (button vs div, label vs div)
- Add: ARIA labels for dynamic content
- Test: With NVDA (Windows) or VoiceOver (Mac)
- Reference: ARIA Authoring Practices Guide

## Research Problems

**Problem: Research findings contradict each other**
- Diagnosis: Different methods, different user segments, or noise
- Approach: Synthesize findings holistically
- Look for: Patterns across methods
- Document: Conflicting findings and context
- Decide: Based on what's most representative

**Problem: Stakeholders want to skip user research**
- Approach: Show value with quick research
- Compromise: 5 quick interviews beats 0 interviews
- Evidence: Share videos, quotes, findings
- Frame: "This takes 1 week and prevents a $X mistake"

**Problem: Research insights don't translate to design**
- Diagnosis: Insights too high-level or too specific
- Fix: Create "How Might We" statements from insights
- Translate: Insights → Design principles → Specific solutions
- Include: Engineering in research synthesis

## Visual Design Problems

**Problem: Too many typefaces in the product**
- Diagnosis: No typography system established
- Fix: Audit all typefaces used
- Decision: Choose 1-2 typefaces maximum
- Document: Type scale with specific styles
- Enforcement: Design review gate

**Problem: Layout breaks on different screen sizes**
- Diagnosis: Designing for one breakpoint only
- Fix: Design responsive at multiple breakpoints
- Minimum: Mobile (375px), Tablet (768px), Desktop (1280px)
- Prevention: Check design at all breakpoints before handoff

**Problem: Empty states are confusing**
- Fix: Design empty states for every possible empty scenario
- Include: Illustration + message + action
- Example: "No results yet. Try adjusting your filters →"
- Prevention: Design empty states in component system
