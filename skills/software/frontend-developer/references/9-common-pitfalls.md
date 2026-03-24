## § 9 · Common Pitfalls

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Prop Drilling** | Props passed through many layers | Context, composition |
| **Large Bundle** | Slow initial load | Code splitting, tree shaking |
| **No Error Boundaries** | One error crashes app | React Error Boundaries |
| **Over-rendering** | Unnecessary re-renders | React.memo, useMemo |
| **Inline Functions** | New function on every render | useCallback |
| **Missing Cleanup** | Memory leaks | useEffect cleanup |

---
