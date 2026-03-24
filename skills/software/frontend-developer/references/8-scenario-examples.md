## § 8 · Scenario Examples

### Example 1: Dashboard Performance Optimization

**Context**: Dashboard loading in 8 seconds, needs to be < 2s.

**Optimization**:
```
Before:
├── Bundle: 2.5MB
├── 50+ API calls on load
├── No code splitting
├── Unoptimized images

After:
├── Route-based code splitting
├── Lazy load heavy components
├── React Query for caching
├── Optimized images (WebP, lazy)
├── Bundle: 400KB

Results:
├── LCP: 8s → 1.2s
├── Lighthouse: 45 → 95
```

---

### Example 2: Accessible Modal Component

**Context**: Build modal that works for all users.

**Implementation**:
```
Features:
├── Focus trap inside modal
├── Focus returns to trigger on close
├── Escape key closes modal
├── Click outside closes
├── aria-labelledby, aria-describedby
├── role="dialog", aria-modal="true"

Code:
├── useFocusTrap hook
├── useEscapeKey hook
├── useClickOutside hook
├── Portal for rendering
```

---

### Example 3: Complex Form Implementation

**Context**: Multi-step form with validation.

**Architecture**:
```
Libraries:
├── React Hook Form for performance
├── Zod for schema validation
├── React Query for submission

Features:
├── Field-level validation
├── Cross-field validation
├── Auto-save to localStorage
├── Progress indication
├── Error summary on submit
```

---

### Example 4: Real-time Collaboration UI

**Context**: Google Docs-like collaborative editor.

**Implementation**:
```
Tech:
├── React with operational transforms
├── Yjs for CRDT
├── WebSocket for sync
├── Virtual scrolling for large docs

Optimizations:
├── Debounced updates
├── Optimistic UI
├── Offline support
├── Conflict resolution UI
```

---

### Example 5: Design System Creation

**Context**: Build component library for organization.

**Components**:
```
Primitives:
├── Button (variants: primary, secondary, ghost)
├── Input, Select, Checkbox, Radio
├── Modal, Tooltip, Dropdown
├── Card, Layout components

Features:
├── TypeScript types
├── Storybook documentation
├── Visual regression tests
├── Dark mode support
├── Accessibility built-in
```

---
