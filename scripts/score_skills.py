#!/usr/bin/env python3
import os
import re
import yaml
from pathlib import Path


def analyze_skill(file_path):
    """Analyze a SKILL.md file and return scores for each dimension."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Extract frontmatter
    frontmatter_end = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if frontmatter_end == 0:
                frontmatter_end = i
            else:
                frontmatter_end = i
                break

    if frontmatter_end > 0:
        frontmatter = "\n".join(lines[1:frontmatter_end])
        body = "\n".join(lines[frontmatter_end + 1 :])
    else:
        frontmatter = ""
        body = content

    # Count dimensions
    lines_count = len(body)

    # 1. System Prompt Depth (20%) - Check for role definition, decision framework, thinking patterns
    system_prompt_score = 0
    if "## § 1 · System Prompt" in body or "# System Prompt" in body:
        system_prompt_score += 2
    if "Role Definition" in body or "Role" in body:
        system_prompt_score += 2
    if "Decision Framework" in body or "Gate" in body:
        system_prompt_score += 2
    if "Thinking Patterns" in body or "Thinking" in body:
        system_prompt_score += 2
    if "Communication Style" in body:
        system_prompt_score += 2

    # 2. Domain Knowledge Density (25%) - Check for core expertise, specific details
    domain_score = 0
    if "Core Expertise" in body or "Expertise" in body:
        domain_score += 3
    if re.search(r"\d+\+ years", body):  # Years of experience
        domain_score += 2
    if re.search(r"(framework|model|methodology)", body, re.IGNORECASE):
        domain_score += 2
    if re.search(r"\*\*[A-Z][a-z]+:", body):  # Bold labeled sections
        domain_score += 3
    if "Identity" in body:
        domain_score += 3
    if re.search(r"\*\*Writing Style\*\*:", body):
        domain_score += 2

    # 3. Workflow Actionability (15%) - Check for actionable steps, procedures
    workflow_score = 0
    if "## § 2" in body or "## What This Skill Does" in body:
        workflow_score += 3
    if re.search(r"^\d+\.", body, re.MULTILINE):  # Numbered lists
        workflow_score += 3
    if re.search(r"(step|procedure|process|protocol)", body, re.IGNORECASE):
        workflow_score += 3
    if "Examples" in body or "## § 3" in body:
        workflow_score += 3
    if re.search(r"\*\*[A-Z][a-z]+\*\*:.*→", body):  # Structured formats
        workflow_score += 3

    # 4. Risk Documentation (10%) - Check for risks, warnings, considerations
    risk_score = 0
    if re.search(r"(risk|warning|caution|danger)", body, re.IGNORECASE):
        risk_score += 4
    if re.search(r"(limitation|caveat|consider)", body, re.IGNORECASE):
        risk_score += 3
    if re.search(r"(fail action|error|failure)", body, re.IGNORECASE):
        risk_score += 3

    # 5. Example Quality (20%) - Check for examples, prompts
    example_score = 0
    if "Example" in body or "Prompt" in body:
        example_score += 4
    if re.search(r"```\w*", body):  # Code blocks
        example_score += 3
    if "## § 3" in body or "## § 4" in body:
        example_score += 4
    if re.search(r"\|.*\|.*\|", body):  # Tables
        example_score += 3
    if re.search(r"user:|assistant:|human:|ai:", body, re.IGNORECASE):
        example_score += 6

    # 6. Metadata Completeness (10%) - Check frontmatter completeness
    metadata_score = 0
    required_fields = [
        "name",
        "display_name",
        "author",
        "version",
        "quality",
        "score",
        "category",
    ]
    for field in required_fields:
        if field in frontmatter:
            metadata_score += 1
    if "tags:" in frontmatter:
        metadata_score += 1
    if "platforms:" in frontmatter:
        metadata_score += 1
    if "description:" in frontmatter:
        metadata_score += 1

    # Normalize scores to 1-10
    system_prompt_score = min(10, max(1, system_prompt_score))
    domain_score = min(10, max(1, domain_score))
    workflow_score = min(10, max(1, workflow_score))
    risk_score = min(10, max(1, risk_score))
    example_score = min(10, max(1, example_score))
    metadata_score = min(10, max(1, metadata_score))

    # Calculate weighted total
    total = (
        system_prompt_score * 0.20
        + domain_score * 0.25
        + workflow_score * 0.15
        + risk_score * 0.10
        + example_score * 0.20
        + metadata_score * 0.10
    )

    # Determine quality level
    if total < 4:
        quality = "basic"
    elif total < 7:
        quality = "community"
    elif total < 9:
        quality = "expert"
    else:
        quality = "exemplary"

    return {
        "file": file_path,
        "system_prompt": system_prompt_score,
        "domain": domain_score,
        "workflow": workflow_score,
        "risk": risk_score,
        "example": example_score,
        "metadata": metadata_score,
        "total": round(total, 1),
        "quality": quality,
    }


def update_skill_file(file_path, new_quality, new_score):
    """Update the quality and score fields in the SKILL.md file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Find and update quality line
    new_lines = []
    for line in lines:
        if line.startswith("quality:"):
            new_lines.append(f"quality: {new_quality}")
        elif line.startswith("score:"):
            new_lines.append(f"score: {new_score}/10")
        else:
            new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))


def main():
    skills_dir = Path("/Users/lucas/Documents/Projects/awesome-skills/skills")
    results = []

    # Process all SKILL.md files
    for skill_dir in skills_dir.rglob("SKILL.md"):
        result = analyze_skill(skill_dir)
        results.append(result)

        # Update the file
        update_skill_file(skill_dir, result["quality"], result["total"])

    # Print summary
    print(
        f"{'Skill':<50} {'SP':>4} {'Dom':>4} {'WF':>4} {'Risk':>4} {'Ex':>4} {'Meta':>4} {'Total':>6} {'Quality':<10}"
    )
    print("-" * 100)

    for r in sorted(results, key=lambda x: x["total"], reverse=True):
        print(
            f"{Path(r['file']).parent.name:<50} {r['system_prompt']:>4} {r['domain']:>4} {r['workflow']:>4} {r['risk']:>4} {r['example']:>4} {r['metadata']:>4} {r['total']:>6.1f} {r['quality']:<10}"
        )

    # Summary statistics
    quality_counts = {}
    for r in results:
        q = r["quality"]
        quality_counts[q] = quality_counts.get(q, 0) + 1

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total Skills: {len(results)}")
    print(f"Average Score: {sum(r['total'] for r in results) / len(results):.2f}")
    print("\nQuality Distribution:")
    for q, count in sorted(quality_counts.items()):
        print(f"  {q}: {count} ({count * 100 / len(results):.1f}%)")


if __name__ == "__main__":
    main()
