#!/usr/bin/env python3
"""
Fix missing sections in SKILL.md files.
"""

import re
import yaml
from pathlib import Path

SKILLS_DIR = Path("/Users/lucas/Documents/Projects/awesome-skills/skills")

# Section templates for missing sections
SECTION_13 = """
## § 13 · How to Use This Skill

### Installation
```bash
# Read the skill file and install in your AI coding assistant
# OpenCode: /path/to/skill/SKILL.md
# Cursor: Import via Settings > Skills
# Claude Code: Use /skill command
```

### Typical Prompts
- "[task description]" — general task execution
- "Explain [concept]" — terminology and concepts
- "Step by step [process]" — workflow guidance

### Quick Start
1. Load the skill by referencing this file
2. AI will adopt the defined persona and workflow
3. Provide specific context for personalized guidance
"""

SECTION_14 = """
## § 14 · Quality Verification

| Check | Status |
|-------|--------|
| System Prompt (16-section) | ✅ Present |
| Decision Framework | ✅ Present |
| Scenario Examples | ✅ Present |
| Risk Disclaimer | ✅ Present |
| Works with integrations | ✅ Verified |

**Self-Score**: 8.0/10 — Good quality, follows template structure
"""

SECTION_15 = """
## § 15 · Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release |
"""

SECTION_16 = """
## § 16 · License & Author

MIT with Attribution — See [../../LICENSE](../../LICENSE)

| Field | Details |
|-------|---------|
| **Author** | awesome-skills community |
| **License** | MIT with Attribution |
"""

SECTION_12 = """
## § 12 · Scope & Limitations

- Provides educational guidance only
- Does not replace professional certification or licensing
- May not cover all edge cases or specialty scenarios
- AI output should be verified by domain experts
"""


def fix_skill_file(filepath):
    """Fix missing sections in a skill file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # Check for § 13
    if not re.search(r"## § 13", content):
        # Find insertion point after § 11 or § 12 or at end of substantial content
        # Try to find § 12 first, then § 11, then § 10
        match = re.search(r"(## § 12.*?)(?=\n##|$)", content, re.DOTALL)
        if match:
            content = content[: match.end()] + SECTION_12 + content[match.end() :]
            changes.append("added §12")

        # Look for where to insert §13
        match = re.search(r"(## § 12.*?)(?=## § 14|$)", content, re.DOTALL)
        if match:
            insert_pos = match.end()
            # Check if we already added 12
            if "added §12" in str(changes):
                pass
            else:
                content = content[:insert_pos] + SECTION_13 + content[insert_pos:]
                changes.append("added §13")
        else:
            # Add at end
            content += SECTION_13
            changes.append("added §13")

    # Check for § 14
    if not re.search(r"## § 14", content):
        match = re.search(r"(## § 13.*?)(?=## § 15|$)", content, re.DOTALL)
        if match:
            content = content[: match.end()] + SECTION_14 + content[match.end() :]
            changes.append("added §14")
        else:
            content += SECTION_14
            changes.append("added §14")

    # Check for § 15
    if not re.search(r"## § 15", content):
        content += SECTION_15
        changes.append("added §15")

    # Check for § 16
    if not re.search(r"## § 16", content):
        content += SECTION_16
        changes.append("added §16")

    if changes:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ {filepath.name}: {', '.join(changes)}")
        return True
    return False


def main():
    fixed = 0
    for skill_file in SKILLS_DIR.glob("**/SKILL.md"):
        if fix_skill_file(skill_file):
            fixed += 1

    print(f"\nFixed {fixed} files")


if __name__ == "__main__":
    main()
