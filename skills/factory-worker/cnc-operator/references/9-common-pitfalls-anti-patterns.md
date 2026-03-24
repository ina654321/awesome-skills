## § 9 · Common Pitfalls & Anti-Patterns

| # | Anti-Pattern | Severity | Consequence | Prevention |
|---|--------------|----------|-------------|------------|
| 1 | Running full program without dry-run | 🔴 Critical | Spindle/tool crash, $10K+ damage | Mandatory dry-run, single-block first part |
| 2 | Wrong tool in spindle | 🔴 Critical | Crash, damaged part, ruined tool | Verify tool number at every change |
| 3 | Ignoring tool length offset | 🔴 Critical | Z-axis crash | Touch off every tool; verify G43 H# |
| 4 | Exceeding spindle RPM limits | 🔴 High | Spindle bearing damage | Check max RPM for tool diameter |
| 5 | Skipping coolant to save time | 🟡 Medium | Tool failure, poor finish | Coolant is cheaper than tools |
| 6 | Using dull tools | 🟡 Medium | Poor finish, dimensional drift | Schedule tool changes, inspect wear |

---
