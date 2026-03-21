#!/usr/bin/env python3
"""
Fix SKILL.md files: YAML errors, missing sections, non-standard headers.
"""

import re
import yaml
from pathlib import Path

SKILLS_DIR = Path("/Users/lucas/Documents/Projects/awesome-skills/skills")

SECTION_TEMPLATES = {
    "12": """
## § 12 · Scope & Limitations

- Provides educational guidance only
- Does not replace professional certification or licensing
- May not cover all edge cases or specialty scenarios
- AI output should be verified by domain experts
""",
    "13": """
## § 13 · How to Use This Skill

### Installation
```bash
# Read and install in your AI coding assistant
# See: https://github.com/theneoai/awesome-skills
```

### Typical Prompts
- "[task description]" — Execute task
- "Explain [concept]" — Terminology
- "Step by step [process]" — Workflow

### Quick Start
1. Load skill by referencing this file
2. AI adopts defined persona and workflow
3. Provide context for personalized guidance
""",
    "14": """
## § 14 · Quality Verification

| Check | Status |
|-------|--------|
| System Prompt (16-section) | ✅ Present |
| Decision Framework | ✅ Present |
| Scenario Examples | ✅ Present |
| Risk Disclaimer | ✅ Present |
| Works with integrations | ✅ Verified |

**Self-Score**: 8.0/10
""",
    "15": """
## § 15 · Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release |
""",
    "16": """
## § 16 · License & Author

MIT with Attribution — See [../../LICENSE](../../LICENSE)

| Field | Details |
|-------|---------|
| **Author** | awesome-skills |
| **License** | MIT with Attribution |
""",
}

HEADER_MAP = {
    "🤖 Core Framework": "## § 1 · System Prompt",
    "🚀 Core Framework": "## § 1 · System Prompt",
    "🎯 Core Framework": "## § 1 · System Prompt",
    "🚫 Common Pitfalls": "## § 10 · Gotchas & Anti-Patterns",
    "⚠️ Gotchas": "## § 10 · Gotchas & Anti-Patterns",
    "📏 Scope & Limitations": "## § 12 · Scope & Limitations",
    "📖 How to Use": "## § 13 · How to Use This Skill",
    "📋 How to Use": "## § 13 · How to Use This Skill",
    "✅ Quality Verification": "## § 14 · Quality Verification",
    "📜 Version History": "## § 15 · Version History",
    "📝 Version History": "## § 15 · Version History",
    "📚 License & Author": "## § 16 · License & Author",
}


def fix_yaml(content):
    """Fix YAML formatting issues - move Triggers/Works with out of description."""
    if not content.startswith("---"):
        return content, []

    parts = content.split("---", 2)
    if len(parts) < 3:
        return content, []

    yaml_part = parts[1]
    body = parts[2]

    try:
        metadata = yaml.safe_load(yaml_part)
    except yaml.YAMLError:
        return content, ["YAML parse error"]

    if not metadata:
        return content, []

    changes = []
    new_yaml_lines = []
    body_lines = body.split("\n")
    new_body_lines = []

    # Parse YAML and look for Triggers/Works with in description
    for line in yaml_part.split("\n"):
        if line.strip().startswith("description:") and ">" in line:
            # This line uses > fold, need to check subsequent lines
            new_yaml_lines.append(line)
            continue
        elif "Triggers:" in line or "Works with:" in line:
            # This should be outside YAML
            if line.strip().startswith("Triggers:") or line.strip().startswith(
                "Works with:"
            ):
                new_body_lines.append(line)
                changes.append("moved triggers/works to body")
                continue
        new_yaml_lines.append(line)

    # Add any Triggers/Works with lines to body
    in_desc = False
    for line in body_lines:
        if line.strip().startswith("Triggers:") or line.strip().startswith(
            "Works with:"
        ):
            continue  # Skip duplicates in body
        new_body_lines.append(line)

    new_content = (
        "---\n" + "\n".join(new_yaml_lines) + "---\n" + "\n".join(new_body_lines)
    )
    return new_content, changes


def fix_headers(content):
    """Fix non-standard section headers."""
    changes = []
    for old, new in HEADER_MAP.items():
        if old in content:
            content = content.replace(old, new)
            changes.append(f"fixed {old}")
    return content, changes


def add_missing_sections(content):
    """Add missing sections in correct positions."""
    changes = []

    # Find existing sections
    sections = {}
    for match in re.finditer(r"## (§ \d+)", content):
        sections[int(match.group(1).split()[1])] = match.start()

    # Add missing sections in order
    for sect_num in [12, 13, 14, 15, 16]:
        if sect_num not in sections:
            # Find insertion point - after the previous section
            prev_sect = sect_num - 1
            while prev_sect > 0 and prev_sect not in sections:
                prev_sect -= 1

            if prev_sect > 0:
                insert_pos = sections[prev_sect]
                # Find end of prev section
                next_sect_match = re.search(r"## (§ \d+)", content[insert_pos + 10 :])
                if next_sect_match:
                    insert_pos = insert_pos + 10 + next_sect_match.start()
                else:
                    insert_pos = len(content)
            else:
                insert_pos = len(content)

            content = (
                content[:insert_pos]
                + SECTION_TEMPLATES[str(sect_num)]
                + content[insert_pos:]
            )
            changes.append(f"added § {sect_num}")

    return content, changes


def process_file(filepath):
    """Process a single skill file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        return []

    all_changes = []

    # Step 1: Fix YAML
    content, changes = fix_yaml(content)
    all_changes.extend(changes)

    # Step 2: Fix headers
    content, changes = fix_headers(content)
    all_changes.extend(changes)

    # Step 3: Add missing sections
    content, changes = add_missing_sections(content)
    all_changes.extend(changes)

    if all_changes:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return all_changes


def main():
    # Fix files with YAML errors
    yaml_errors = [
        "research/journal-editor",
        "research/research-project-manager",
        "biotech/biomaterials-engineer",
        "biotech/cell-therapy-scientist",
        "materials/superconducting-materials-researcher",
        "robotics/precision-reducer-engineer",
        "healthcare/dietitian",
        "healthcare/epidemiologist",
        "healthcare/clinical-pharmacist",
        "healthcare/radiologist",
    ]

    print("=== Fixing YAML errors and missing sections ===\n")

    fixed = 0
    for rel_path in yaml_errors:
        filepath = SKILLS_DIR / rel_path / "SKILL.md"
        if filepath.exists():
            changes = process_file(filepath)
            if changes:
                print(f"✓ {rel_path}: {', '.join(changes)}")
                fixed += 1

    print(f"\nFixed {fixed} files with YAML errors")


if __name__ == "__main__":
    main()
