## § 9 · Common Pitfalls & Anti-Patterns

| # | Anti-Pattern| Severity| Quick Fix|
|---|----------------------|-----------------|---------------------|
| 1 | **Putting money in drawer before verifying** | 🔴 High | Count the cash first; if wrong, customer is still there |
| 2 | **Not checking card signature** | 🔴 High | Verify signature against card; request ID if needed |
| 3 | **Leaving drawer open/unattended** | 🔴 High | Lock it; get manager to cover if leaving |
| 4 | **Rushing through greeting** | 🟡 Medium | "Hi, welcome in!" — takes 2 seconds, sets tone |
| 5 | **Forgetting to offer receipt** | 🟡 Medium | Always offer; especially for large purchases |

```
❌ *Slaps items on counter* "That'll be $47.23." *Grabs money, hands change*
✅ "Hi! Finding everything okay today? ... Your total is $47.23. How would you like to pay?" *Processes payment* "Out of $50... that's $2.77. Here's your receipt. Have a great day!"
```

---
