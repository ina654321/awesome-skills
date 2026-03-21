#!/usr/bin/env python3
"""
Analyze skill structure completeness against 16-section standard.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

# 16 required sections (with § format variants: · and —)
REQUIRED_SECTIONS = [
    ("## § 1", "System Prompt"),
    ("## § 2", "What This Skill Does"),
    ("## § 3", "Risk Disclaimer"),
    ("## § 4", "Core Philosophy"),
    ("## § 5", "Platform Support"),
    ("## § 6", "Professional Toolkit"),
    ("## § 7", "Standards & Reference"),
    ("## § 8", "Standard Workflow"),
    ("## § 9", "Scenario Examples"),
    ("## § 10", "Gotchas & Anti-Patterns"),
    ("## § 11", "Integration with Other Skills"),
    ("## § 12", "Scope & Limitations"),
    ("## § 13", "How to Use This Skill"),
    ("## § 14", "Quality Verification"),
    ("## § 15", "Version History"),
    ("## § 16", "License & Author"),
]

# 9 required metadata fields
REQUIRED_METADATA = [
    "name",
    "display_name",
    "author",
    "version",
    "difficulty",
    "category",
    "tags",
    "platforms",
    "description",
]


def parse_skill_file(filepath):
    """Parse a skill file and return analysis results."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e), "filepath": str(filepath)}

    result = {
        "filepath": str(filepath),
        "skill_name": filepath.parent.name,
        "category": filepath.parent.parent.name,
        "missing_sections": [],
        "present_sections": [],
        "metadata_missing": [],
        "metadata_present": [],
        "metadata_issues": [],
        "has_system_prompt_framework": False,
        "example_count": 0,
        "has_risk_disclaimer": False,
        "section_order_issues": [],
        "line_count": len(content.split("\n")),
        "total_chars": len(content),
    }

    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1])
                if metadata:
                    for field in REQUIRED_METADATA:
                        if field in metadata and metadata[field]:
                            result["metadata_present"].append(field)
                        else:
                            result["metadata_missing"].append(field)

                    # Check metadata quality issues
                    if "description" in metadata:
                        desc = str(metadata["description"])
                        if len(desc) > 263:
                            result["metadata_issues"].append(
                                f"description > 263 chars ({len(desc)})"
                            )
                        if "<" in desc or ">" in desc:
                            result["metadata_issues"].append(
                                "description contains HTML"
                            )

                    if "platforms" in metadata:
                        platforms = metadata["platforms"]
                        if isinstance(platforms, list) and len(platforms) < 7:
                            result["metadata_issues"].append(
                                f"only {len(platforms)} platforms (expected 7)"
                            )

                    if "tags" in metadata:
                        tags = metadata["tags"]
                        if isinstance(tags, list) and len(tags) < 3:
                            result["metadata_issues"].append(
                                f"only {len(tags)} tags (expected 3-5)"
                            )

                    # Check for quality/score fields
                    if "quality" not in metadata:
                        result["metadata_issues"].append("missing 'quality' field")
                    if "score" not in metadata:
                        result["metadata_issues"].append("missing 'score' field")
            except yaml.YAMLError:
                result["metadata_issues"].append("YAML parse error")

    # Find all § sections with flexible matching (both · and — separators)
    # Pattern matches: ## § 1 · Title, ## § 1 — Title, ## § 1. Title, ## § 1 Title
    section_pattern = re.compile(r"^## § (\d+)[\s·—-]+(.+)$", re.MULTILINE)
    found_sections = {}

    for match in section_pattern.finditer(content):
        num = match.group(1)
        title = match.group(2).strip()
        found_sections[num] = title

    # Check for each required section
    for section_key, section_name in REQUIRED_SECTIONS:
        match = re.search(r"\d+", section_key)
        section_num = match.group() if match else None
        if section_num and section_num in found_sections:
            result["present_sections"].append(section_key)
        else:
            result["missing_sections"].append(section_key)

    # Check for system prompt decision framework
    if "## § 1" in str(result["present_sections"]) or any(
        "§ 1" in s for s in found_sections.values()
    ):
        # Look for Decision Framework in content
        if re.search(r"Decision Framework", content, re.IGNORECASE):
            result["has_system_prompt_framework"] = True
        # Or look for Gate table
        if re.search(r"\|.*Gate.*\|.*Question.*\|", content, re.IGNORECASE):
            result["has_system_prompt_framework"] = True

    # Check for Risk Disclaimer content
    if any("§ 3" in s or "Risk Disclaimer" in s for s in found_sections.values()):
        risk_pattern = r"## § 3[\s·—-]+Risk Disclaimer.*?(?=## §|\Z)"
        risk_match = re.search(risk_pattern, content, re.DOTALL)
        if risk_match:
            risk_content = risk_match.group(0)
            if len(risk_content.split("\n")) > 5:  # Has some content
                result["has_risk_disclaimer"] = True

    # Count scenario examples (### 9.X patterns)
    example_pattern = re.compile(r"^### 9\.\d+\s+", re.MULTILINE)
    result["example_count"] = len(example_pattern.findall(content))

    # Check section order - verify § sections are in sequence
    section_nums = sorted([int(n) for n in found_sections.keys()])
    expected_nums = list(range(1, 17))
    if section_nums != expected_nums:
        missing_in_seq = set(expected_nums) - set(section_nums)
        result["section_order_issues"].append(
            f"Missing sections in sequence: {sorted(missing_in_seq)}"
        )

    return result


def main():
    skills_dir = Path("/Users/lucas/Documents/Projects/awesome-skills/skills")
    results = []

    # Find all SKILL.md files
    skill_files = list(skills_dir.glob("**/SKILL.md"))
    print(f"Found {len(skill_files)} skill files\n")

    for skill_file in skill_files:
        result = parse_skill_file(skill_file)
        results.append(result)

    # Sort by missing sections count (descending)
    results.sort(key=lambda x: len(x.get("missing_sections", [])), reverse=True)

    # Statistics
    total_skills = len(results)
    section_missing_count = defaultdict(int)
    metadata_missing_count = defaultdict(int)
    metadata_issue_count = defaultdict(int)
    issues_by_skill = []

    for result in results:
        if "error" in result:
            continue

        for section in result.get("missing_sections", []):
            section_missing_count[section] += 1

        for field in result.get("metadata_missing", []):
            metadata_missing_count[field] += 1

        for issue in result.get("metadata_issues", []):
            metadata_issue_count[issue] += 1

        issues_by_skill.append(
            {
                "skill": f"{result['category']}/{result['skill_name']}",
                "missing_count": len(result.get("missing_sections", [])),
                "missing": result.get("missing_sections", []),
                "metadata_missing": result.get("metadata_missing", []),
                "metadata_issues": result.get("metadata_issues", []),
                "has_framework": result.get("has_system_prompt_framework", False),
                "example_count": result.get("example_count", 0),
                "has_risk": result.get("has_risk_disclaimer", False),
                "line_count": result.get("line_count", 0),
                "total_chars": result.get("total_chars", 0),
                "order_issues": result.get("section_order_issues", []),
                "category": result.get("category", ""),
            }
        )

    # Generate report
    print("=" * 80)
    print("SKILL CONTENT COMPLETENESS ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nTotal Skills Analyzed: {total_skills}\n")

    # 1. Skills needing most improvement (by missing sections)
    print("-" * 80)
    print("1. TOP 20 SKILLS NEEDING MOST IMPROVEMENT (by missing sections)")
    print("-" * 80)
    skills_with_issues = [i for i in issues_by_skill if i["missing_count"] > 0]
    for i, issue in enumerate(skills_with_issues[:20]):
        print(f"\n{i + 1}. {issue['skill']}")
        print(
            f"   Missing: {len(issue['missing'])} sections | Metadata issues: {len(issue['metadata_missing'])} missing + {len(issue['metadata_issues'])} quality"
        )
        if issue["missing"]:
            print(
                f"   Sections missing: {[s.split(' ')[-1] for s in issue['missing']]}"
            )
        if issue["metadata_missing"]:
            print(f"   Metadata missing: {issue['metadata_missing']}")
        if issue["metadata_issues"]:
            print(f"   Metadata issues: {issue['metadata_issues']}")

    # 2. Most common missing sections
    print("\n" + "=" * 80)
    print("2. MOST COMMON MISSING SECTIONS (frequency across all skills)")
    print("-" * 80)
    sorted_sections = sorted(
        section_missing_count.items(), key=lambda x: x[1], reverse=True
    )
    for section, count in sorted_sections:
        percentage = (count / total_skills) * 100
        bar = "█" * int(percentage / 5)
        section_name = section.split(" ", 1)[-1]
        print(f"{section_name:40} {count:4} ({percentage:5.1f}%) {bar}")

    # 3. Most common missing metadata
    print("\n" + "=" * 80)
    print("3. MOST COMMON MISSING METADATA FIELDS")
    print("-" * 80)
    if metadata_missing_count:
        sorted_metadata = sorted(
            metadata_missing_count.items(), key=lambda x: x[1], reverse=True
        )
        for field, count in sorted_metadata:
            percentage = (count / total_skills) * 100
            bar = "█" * int(percentage / 5)
            print(f"{field:20} {count:4} ({percentage:5.1f}%) {bar}")
    else:
        print("All skills have required metadata fields!")

    # 4. Metadata quality issues summary
    print("\n" + "=" * 80)
    print("4. METADATA QUALITY ISSUES SUMMARY")
    print("-" * 80)

    # Aggregate by issue type
    issue_types = defaultdict(int)
    for issue, count in metadata_issue_count.items():
        if "description >" in issue:
            issue_types["description > 263 chars"] += count
        elif "platforms" in issue:
            issue_types["incomplete platforms list"] += count
        elif "YAML" in issue:
            issue_types["YAML parse error"] += count
        elif "tags" in issue:
            issue_types["insufficient tags"] += count
        elif "quality" in issue or "score" in issue:
            issue_types["missing quality/score"] += count
        else:
            issue_types[issue] = count

    for issue_type, count in sorted(
        issue_types.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = (count / total_skills) * 100
        bar = "█" * int(percentage / 5)
        print(f"{issue_type:30} {count:4} ({percentage:5.1f}%) {bar}")

    # 5. Structural issues
    print("\n" + "=" * 80)
    print("5. STRUCTURAL ISSUES")
    print("-" * 80)

    no_framework = [i for i in issues_by_skill if not i["has_framework"]]
    no_examples = [i for i in issues_by_skill if i["example_count"] == 0]
    no_risk = [i for i in issues_by_skill if not i["has_risk"]]
    order_issues = [i for i in issues_by_skill if i["order_issues"]]

    print(
        f"\nSkills WITHOUT System Prompt Decision Framework: {len(no_framework)} ({len(no_framework) / total_skills * 100:.1f}%)"
    )
    if no_framework:
        print(f"   Examples: {', '.join([i['skill'] for i in no_framework[:5]])}...")

    print(
        f"\nSkills WITHOUT Scenario Examples (§9): {len(no_examples)} ({len(no_examples) / total_skills * 100:.1f}%)"
    )
    if no_examples:
        print(f"   Examples: {', '.join([i['skill'] for i in no_examples[:5]])}...")

    print(
        f"\nSkills WITHOUT Risk Disclaimer content: {len(no_risk)} ({len(no_risk) / total_skills * 100:.1f}%)"
    )
    if no_risk:
        print(f"   Examples: {', '.join([i['skill'] for i in no_risk[:5]])}...")

    print(f"\nSkills with Section Sequence Issues: {len(order_issues)}")
    if order_issues:
        for oi in order_issues[:5]:
            print(f"   - {oi['skill']}: {oi['order_issues']}")

    # 6. Priority improvement suggestions
    print("\n" + "=" * 80)
    print("6. IMPROVEMENT PRIORITY RECOMMENDATIONS")
    print("-" * 80)

    # Critical: Missing sections in >50% of skills
    critical_sections = [(s, c) for s, c in sorted_sections if c > total_skills * 0.5]
    print("\n🔴 CRITICAL (>50% missing - immediate attention):")
    for section, count in critical_sections:
        section_name = section.split(" ", 1)[-1]
        print(f"   - {section_name}: {count} skills missing")

    # High: Missing in 20-50%
    high_sections = [
        (s, c)
        for s, c in sorted_sections
        if total_skills * 0.2 < c <= total_skills * 0.5
    ]
    print("\n🟠 HIGH PRIORITY (20-50% missing):")
    for section, count in high_sections:
        section_name = section.split(" ", 1)[-1]
        print(f"   - {section_name}: {count} skills missing")

    # Medium: Missing in 10-20%
    medium_sections = [
        (s, c)
        for s, c in sorted_sections
        if total_skills * 0.1 < c <= total_skills * 0.2
    ]
    print("\n🟡 MEDIUM PRIORITY (10-20% missing):")
    for section, count in medium_sections:
        section_name = section.split(" ", 1)[-1]
        print(f"   - {section_name}: {count} skills missing")

    # Low: Missing < 10%
    low_sections = [
        (s, c) for s, c in sorted_sections if c <= total_skills * 0.1 and c > 0
    ]
    print("\n🟢 LOW PRIORITY (<10% missing):")
    for section, count in low_sections:
        section_name = section.split(" ", 1)[-1]
        print(f"   - {section_name}: {count} skills missing")

    # Summary stats
    print("\n" + "=" * 80)
    print("7. SUMMARY STATISTICS")
    print("-" * 80)
    perfect_skills = len(
        [
            i
            for i in issues_by_skill
            if len(i["missing"]) == 0 and len(i["metadata_missing"]) == 0
        ]
    )
    good_skills = len(
        [
            i
            for i in issues_by_skill
            if len(i["missing"]) <= 2 and len(i["metadata_missing"]) <= 1
        ]
    )
    needs_work = len([i for i in issues_by_skill if len(i["missing"]) > 4])

    print(
        f"\nPerfect skills (0 missing sections, 0 missing metadata): {perfect_skills} ({perfect_skills / total_skills * 100:.1f}%)"
    )
    print(
        f"Good skills (≤2 missing sections, ≤1 missing metadata): {good_skills} ({good_skills / total_skills * 100:.1f}%)"
    )
    print(
        f"Needs significant work (>4 missing sections): {needs_work} ({needs_work / total_skills * 100:.1f}%)"
    )

    avg_missing = sum(len(i["missing"]) for i in issues_by_skill) / total_skills
    avg_examples = sum(i["example_count"] for i in issues_by_skill) / total_skills
    avg_chars = sum(i["total_chars"] for i in issues_by_skill) / total_skills
    print(f"\nAverage missing sections per skill: {avg_missing:.1f}")
    print(f"Average scenario examples per skill: {avg_examples:.1f}")
    print(f"Average content size per skill: {avg_chars:.0f} chars")

    # Category breakdown
    print("\n" + "=" * 80)
    print("8. CATEGORY BREAKDOWN")
    print("-" * 80)
    categories = defaultdict(list)
    for issue in issues_by_skill:
        if issue.get("category"):
            categories[issue["category"]].append(issue)

    category_stats = []
    for cat, skills in sorted(categories.items()):
        avg_missing = sum(len(s["missing"]) for s in skills) / len(skills)
        perfect = len([s for s in skills if len(s["missing"]) == 0])
        category_stats.append((cat, len(skills), avg_missing, perfect))

    category_stats.sort(key=lambda x: x[2], reverse=True)
    for cat, count, avg_missing, perfect in category_stats:
        bar = "█" * int((16 - avg_missing) / 2)
        completeness = f"{perfect}/{count} perfect"
        print(
            f"{cat:30} {count:3} skills  avg missing: {avg_missing:4.1f} {completeness:>20} {bar}"
        )


if __name__ == "__main__":
    main()
