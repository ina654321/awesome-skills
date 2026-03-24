#!/usr/bin/env python3
"""
Progressive Disclosure Refactoring Tool

Splits a large SKILL.md into:
1. SKILL.md (< 300 lines) - Navigation + overview
2. references/ - Detailed content

Based on skill-writer v5 methodology.
"""

import re
import os
from pathlib import Path

SECTION_PATTERNS = [
    r"^##?\s*§\s*(\d+)",  # §1, § 1
    r"^##?\s*(\d+)\s*[·.]\s*",  # 1. or 1.
    r"^##?\s*([A-Z])\s*[·.]\s*",  # A. or A
]


def extract_section_number(line):
    for pattern in SECTION_PATTERNS:
        match = re.match(pattern, line.strip())
        if match:
            return match.group(1)
    return None


def is_section_header(line):
    return extract_section_number(line) is not None


def split_into_sections(content):
    lines = content.split("\n")
    sections = {}
    current_section = "header"
    current_lines = []

    for line in lines:
        if is_section_header(line):
            if current_lines:
                sections[current_section] = "\n".join(current_lines)
            current_section = line.strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_section] = "\n".join(current_lines)

    return sections


def refactor_skill(skill_path, target_lines=280):
    """Refactor a skill to use progressive disclosure."""
    skill_path = Path(skill_path)
    if not skill_path.exists():
        print(f"Error: {skill_path} not found")
        return False

    content = skill_path.read_text()
    original_lines = len(content.split("\n"))

    if original_lines <= target_lines:
        print(f"  {skill_path.name}: Already under {target_lines} lines ({original_lines})")
        return True

    # Split into sections
    sections = split_into_sections(content)

    # Create references directory
    refs_dir = skill_path.parent / "references"
    refs_dir.mkdir(exist_ok=True)

    # Keep header + §1 in main file, move rest to references
    header_and_section1 = []
    remaining_sections = {}

    for section_name, section_content in sections.items():
        if (
            section_name == "header"
            or "§1" in section_name
            or section_name.startswith("##")
            and "1" in section_name[:10]
        ):
            header_and_section1.append(section_content)
        else:
            remaining_sections[section_name] = section_content

    # Write remaining sections to references/
    for section_name, section_content in remaining_sections.items():
        # Clean section name for filename
        filename = re.sub(r"[^a-zA-Z0-9]", "-", section_name.lower())
        filename = re.sub(r"-+", "-", filename).strip("-")
        if len(filename) > 50:
            filename = filename[:50]

        ref_file = refs_dir / f"{filename}.md"
        ref_file.write_text(section_content)

    # Rebuild SKILL.md
    new_content = "\n\n".join(header_and_section1)

    # Add references section
    if remaining_sections:
        refs_list = "\n\n## References\n\nDetailed content:\n\n"
        for section_name in remaining_sections.keys():
            filename = re.sub(r"[^a-zA-Z0-9]", "-", section_name.lower())
            filename = re.sub(r"-+", "-", filename).strip("-")[:50]
            refs_list += f"- [{section_name}](./references/{filename}.md)\n"

        new_content += refs_list

    new_lines = len(new_content.split("\n"))
    skill_path.write_text(new_content)

    print(
        f"  {skill_path.name}: {original_lines} → {new_lines} lines ({len(remaining_sections)} sections moved)"
    )
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Process specific skill
        refactor_skill(sys.argv[1])
    else:
        print("Usage: python progressive_disclosure.py <skill-path>")
        print("   or: python progressive_disclosure.py --all")

        if len(sys.argv) > 1 and sys.argv[1] == "--all":
            # Process all skills
            skills_dir = Path("skills")
            count = 0
            for skill_file in skills_dir.glob("*/*/SKILL.md"):
                if refactor_skill(skill_file):
                    count += 1
            print(f"\nProcessed {count} skills")
