# UX Designer — Standards & Reference

## Design Frameworks

### Nielsen's 10 Usability Heuristics

| # | Heuristic | Key Question |
|---|-----------|-------------|
| 1 | Visibility of system status | Does the user always know what's happening? |
| 2 | Match between system and real world | Does it use language/concepts users know? |
| 3 | User control and freedom | Can users undo actions and exit unwanted states? |
| 4 | Consistency and standards | Are conventions followed across the product? |
| 5 | Error prevention | Are errors prevented before they happen? |
| 6 | Recognition rather than recall | Is information visible rather than requiring memory? |
| 7 | Flexibility and efficiency | Can expert users shortcut? |
| 8 | Aesthetic and minimalist design | Is only relevant information shown? |
| 9 | Help users recognize, diagnose, recover from errors | Are error messages specific and constructive? |
| 10 | Help and documentation | Is assistance findable and task-focused? |

### Atomic Design (Brad Frost)

| Level | Description | Examples |
|--------|-------------|----------|
| **Atoms** | Smallest UI elements | Button, input, label, icon |
| **Molecules** | Groups of atoms | Search form, card, navigation item |
| **Organisms** | Distinct UI components | Header, footer, product card grid |
| **Templates** | Page-level layout structure | Article template, dashboard layout |
| **Pages** | Specific instances of templates | Homepage, profile page, settings page |

### User Research Standards

**Sample sizes:**
- Qualitative interviews: 5-8 users per user segment (patterns emerge)
- Quantitative surveys: n ≥ 100 for 95% confidence ±10%
- Usability testing: 5 users to find 85% of usability problems (Nielsen's law)
- A/B testing: Calculate sample size before running (typically 1,000-10,000+ per variant)

### Information Architecture

**Card Sorting:**
- Open card sort: Users categorize topics → inform navigation structure
- Closed card sort: Users categorize into pre-defined categories → validate navigation

**Tree Testing:**
- Task success rate >70% is good
- Directness (distance from optimal path): Lower is better

## Accessibility Standards (WCAG 2.1 AA)

### Critical Criteria

| Criterion | Level | Description |
|-----------|-------|-------------|
| 1.1.1 Non-text Content | A | All images have alt text |
| 1.3.1 Info and Relationships | A | Structure conveyed programmatically |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 normal text, 3:1 large text |
| 1.4.4 Resize Text | AA | Text can resize to 200% without loss |
| 2.1.1 Keyboard | A | All functions via keyboard |
| 2.4.3 Focus Order | A | Logical focus sequence |
| 2.4.4 Link Purpose | A | Link purpose is clear from context |
| 2.4.6 Headings and Labels | AA | Headings and labels describe topic/purpose |
| 2.4.7 Focus Visible | AA | Keyboard focus indicator visible |
| 3.1.1 Language of Page | A | Page language declared |
| 3.3.1 Error Identification | A | Errors identified and described |
| 3.3.2 Labels or Instructions | A | Labels provided for input |
| 4.1.2 Name, Role, Value | A | UI components have accessible name, role, state |
| 4.1.3 Status Messages | AA | Status messages conveyed without focus |

### Color Contrast Tools

- **WebAIM Contrast Checker**: webaim.org/resources/contrastchecker
- **Colour Contrast Analyser**: pearson.com
- **axe DevTools**: Accessibility testing in browser

## UX Metrics Reference

### Task Success Metrics

| Metric | Formula | Good Score |
|--------|---------|------------|
| **Task Success Rate** | (Completed tasks / Total tasks) × 100 | >85% |
| **Time on Task** | Median time to complete | Comparable to benchmarks |
| **Error Rate** | Errors per task | <15% |
| **Efficiency** | Tasks completed / attempts | >90% |

### SUS Score (System Usability Scale)

**10 questions, scored 1-5:**
- SUS Score = (sum of odd responses - 5) + (25 - sum of even responses) × 2.5
- Score range: 0-100
- >68 = above average
- >80 = excellent
- >90 = best possible

### Heuristic Evaluation Severity Rating

| Rating | Description |
|--------|-------------|
| 4 | Catastrophic — must fix before release |
| 3 | Major — should fix before release |
| 2 | Minor — should fix eventually |
| 1 | Cosmetic — fix if time permits |

## Design System Reference

### Typography Scale

| Name | Size | Use |
|------|------|-----|
| H1 | 32-48px | Page titles |
| H2 | 24-32px | Section headers |
| H3 | 20-24px | Subsection headers |
| H4 | 16-20px | Component titles |
| Body | 14-16px | Primary text |
| Caption | 12-14px | Secondary text, labels |
| Overline | 10-12px | Category labels |

### Spacing System

**8px Grid:**
- 4px: Minimal spacing
- 8px: Tight spacing
- 16px: Default spacing
- 24px: Section spacing
- 32px: Large section gaps
- 48px: Major section breaks
- 64px: Page-level spacing

### Touch Target Sizes

- Minimum: 44×44px (iOS HIG)
- Recommended: 48×48px
- Apple HIG: 44×44pt minimum
- Material Design: 48×48dp minimum

### Border Radius

| Use | Radius |
|-----|--------|
| Buttons, inputs | 4-8px |
| Cards | 8-12px |
| Modals | 12-16px |
| Full-round | 50% |

## Professional Resources

**Nielsen Norman Group** — UX research and consulting. Website: nngroup.com

**UX Collective (Medium)** — Industry articles and case studies. Website: uxdesign.cc

**A List Apart** — Web standards and best practices. Website: alistapart.com

**UX London** — Annual UX conference and community.

**Interaction Design Foundation** — Online UX courses. Website: interaction-design.org

**Accessible Components:**
- **ARIA Authoring Practices Guide**: w3.org/WAI/ARIA/apg
- **Inclusive Components**: inclusive-components.design
