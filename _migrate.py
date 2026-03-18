#!/usr/bin/env python3
"""Batch migrate SKILL.md files from old emoji headings to § format."""

import re
import os
from pathlib import Path

HEADING_MAP = {
    r"## 🎯 What This Skill Does": r"## § 2 · What This Skill Does",
    r"## ⚠️ Risk Disclaimer": r"## § 3 · Risk Disclaimer",
    r"## 🤖 Core Philosophy(?: & Decision Framework)?": r"## § 4 · Core Philosophy",
    r"## 🛠️ Professional Toolkit": r"## § 6 · Professional Toolkit",
    r"## 📖 Standards & Reference": r"## § 7 · Standards & Reference",
    r"## 📋 Standard Workflow": r"## § 8 · Standard Workflow",
    r"## 💼 Scenario Examples": r"## § 9 · Scenario Examples",
    r"## ⚡ Common Pitfalls(?: & Anti-Patterns)?": r"## § 10 · Common Pitfalls & Anti-Patterns",
    r"## 🔗 Integration with Other Skills": r"## § 11 · Integration with Other Skills",
    r"## 📌 Scope & Limitations": r"## § 12 · Scope & Limitations",
    r"## 🚀 How to Use This Skill": r"## § 13 · How to Use This Skill",
    r"## ✅ Quality Verification": r"## § 14 · Quality Verification",
    r"## 📝 Version History": r"## § 15 · Version History",
    r"## 📄 License & Author": r"## § 16 · License & Author",
    r"## 🔧 Tools & Equipment": r"## § 6 · Professional Toolkit",
    r"## 🛡️ Security Best Practices": r"## § 10 · Common Pitfalls & Anti-Patterns",
    r"## 📚 References": r"## § 7 · Standards & Reference",
    r"## 💡 Tips & Tricks": r"## § 10 · Common Pitfalls & Anti-Patterns",
    r"## 🎓 Certifications & Training": r"## § 6 · Professional Toolkit",
    r"## 🌟 Best Practices": r"## § 10 · Common Pitfalls & Anti-Patterns",
    r"## 📊 Metrics & KPIs": r"## § 6 · Professional Toolkit",
    r"## 🏆 Case Studies": r"## § 9 · Scenario Examples",
    r"## 🎯 Career Development": r"## § 12 · Scope & Limitations",
    r"## 💼 Real-World Applications": r"## § 9 · Scenario Examples",
    r"## ⚙️ Configuration": r"## § 13 · How to Use This Skill",
    r"## 🧪 Testing": r"## § 14 · Quality Verification",
    r"## 📦 Installation": r"## § 13 · How to Use This Skill",
    r"## 🔄 Updates": r"## § 15 · Version History",
    r"## 🏥 What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 💰 What This Skill Does": r"## § 2 · What This Skill Does",
    r"## ⚖️ What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 📐 What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 🏗️ What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 🎨 What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 🖥️ What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 🔒 What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 📱 What This Skill Does": r"## § 2 · What This Skill Does",
    r"## 🧬 What This Skill Does": r"## § 2 · What This Skill Does",
}

SKILLS_DIR = Path("skills")
TARGETS = [
    "skills/research/research-project-manager/SKILL.md",
    "skills/biotech/biomaterials-engineer/SKILL.md",
    "skills/biotech/cell-therapy-scientist/SKILL.md",
    "skills/tools/database/clickhouse-expert/SKILL.md",
    "skills/tools/database/duckdb-expert/SKILL.md",
    "skills/tools/design/photoshop-expert/SKILL.md",
    "skills/tools/design/canva-expert/SKILL.md",
    "skills/tools/design/illustrator-expert/SKILL.md",
    "skills/tools/design/blender-expert/SKILL.md",
    "skills/tools/enterprise/servicenow-expert/SKILL.md",
    "skills/tools/enterprise/workday-expert/SKILL.md",
    "skills/tools/enterprise/zendesk-expert/SKILL.md",
    "skills/tools/security/burpsuite-expert/SKILL.md",
    "skills/tools/security/metasploit-expert/SKILL.md",
    "skills/tools/security/container-security-expert/SKILL.md",
    "skills/tools/security/nmap-expert/SKILL.md",
    "skills/tools/game-engine/unreal-expert/SKILL.md",
    "skills/tools/game-engine/godot-expert/SKILL.md",
    "skills/tools/game-engine/unity-expert/SKILL.md",
    "skills/tools/observability/pagerduty-expert/SKILL.md",
    "skills/tools/container/istio-servicemesh-expert/SKILL.md",
    "skills/tools/cad/revit-bim-expert/SKILL.md",
    "skills/tools/cad/solidworks-expert/SKILL.md",
    "skills/tools/cad/autocad-expert/SKILL.md",
    "skills/tools/ai-ml/llama-index-expert/SKILL.md",
    "skills/tools/data-platform/lakehouse-expert/SKILL.md",
    "skills/tools/data-platform/flink-expert/SKILL.md",
    "skills/tools/engineering-simulation/labview-expert/SKILL.md",
    "skills/tools/engineering-simulation/abaqus-expert/SKILL.md",
    "skills/tools/engineering-simulation/openfoam-expert/SKILL.md",
    "skills/tools/engineering-simulation/comsol-expert/SKILL.md",
    "skills/materials/superconducting-materials-researcher/SKILL.md",
    "skills/robotics/precision-reducer-engineer/SKILL.md",
    "skills/healthcare/dietitian/SKILL.md",
    "skills/healthcare/epidemiologist/SKILL.md",
    "skills/healthcare/clinical-pharmacist/SKILL.md",
    "skills/healthcare/radiologist/SKILL.md",
    "skills/retail/retail-operations-manager/SKILL.md",
    "skills/retail/ecommerce-product-manager/SKILL.md",
    "skills/special/gerrit-permission-manager/SKILL.md",
    "skills/telecom/ntn-engineer/SKILL.md",
    "skills/hr/recruiter/SKILL.md",
    "skills/marketing/brand-manager/SKILL.md",
    "skills/service-worker/elderly-caregiver/SKILL.md",
    "skills/service-worker/confinement-nanny/SKILL.md",
    "skills/freelancer/ecommerce-seller/SKILL.md",
    "skills/media/news-anchor/SKILL.md",
    "skills/media/podcast-producer/SKILL.md",
]


def migrate_file(filepath):
    """Migrate a single SKILL.md file from old headings to § format."""
    if not os.path.exists(filepath):
        return False, "file not found"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    for old_pattern, new_heading in HEADING_MAP.items():
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_heading, content)
            changes.append(f"  {old_pattern} → {new_heading}")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True, f"Migrated {len(changes)} patterns:\n" + "\n".join(changes)
    return False, "no changes needed"


def main():
    total = 0
    migrated = 0
    for target in TARGETS:
        total += 1
        ok, msg = migrate_file(target)
        if ok:
            migrated += 1
            print(f"✅ {target}")
            for line in msg.split("\n")[1:]:
                print(f"   {line}")
        else:
            print(f"⚠️  {target}: {msg}")

    print(f"\n{total} files processed, {migrated} migrated")


if __name__ == "__main__":
    main()
