---

name: {skill-name}
display_name: {Display Name}
author: your-name
version: 1.0.0
quality: community
difficulty: beginner
category: {category}
tags: [tag1, tag2]
platforms: [kimi, claude, cursor]
description: "{One-line description}. Use when {trigger condition}. Triggers: '{keyword1}', '{keyword2}'."

---

# {Skill Display Name}

> Lite Skill | 50-150 lines | Tool/Utility

---

## System Prompt

```
You are a {tool type} that {single purpose}.

Do one thing: {specific task}
Input: {expected input format}
Output: {expected output format}
Never: {scope boundaries}
```

---

## Quick Start

### Installation

```bash
# Kimi Code
mkdir -p .agents/skills/{skill-name}
cp SKILL.md .agents/skills/{skill-name}/

# Claude Code
# Add to .cursorrules or skills directory
```

### Usage

```
"{trigger phrase}"
```

---

## Capabilities

**✓ What This Skill Does:**
- {Capability 1}
- {Capability 2}
- {Capability 3}

**✗ What It Doesn't Do:**
- {Out of scope 1}
- {Out of scope 2}

---

## Usage Examples

### Example 1: {Use case}

**Input:**
```
{User request}
```

**Output:**
```
{Expected output}
```

### Example 2: {Use case}

**Input:**
```
{User request}
```

**Output:**
```
{Expected output}
```

---

## Script (Optional)

If code needed, place in `scripts/{script-name}.py`:

```python
#!/usr/bin/env python3
"""{One-line description}"""

def main():
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

---

**Lines:** ~{X} | **Tier:** Lite | **Time to create:** 30 min
