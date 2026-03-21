#!/usr/bin/env python3
"""
Skill 文件精简脚本 - 最终版 (修复版)
"""

import os
import re
import glob

BASE_DIR = "/Users/lucas/Documents/Projects/awesome-skills/skills"


def process_skill_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Quality Verification - 精简为索引
        if re.match(r"^## § 14 · Quality Verification", line):
            new_lines.append(line.rstrip())
            new_lines.append("")
            new_lines.append("→ See references/standards.md §7.10 for full checklist")
            new_lines.append("")

            # 跳过旧内容直到 Test Cases
            i += 1
            while i < len(lines):
                if re.match(r"^### Test Cases", lines[i]):
                    break
                if re.match(r"^## ", lines[i]) and "Quality" not in lines[i]:
                    break
                i += 1
            continue

        # Version History - 精简为索引
        if re.match(r"^## § 15 · Version History", line):
            new_lines.append(line.rstrip())
            new_lines.append("")
            new_lines.append("| Version | Date | Changes |")
            new_lines.append("|---------|------|---------|")

            # 保留最多3条版本记录
            version_count = 0
            i += 1
            while i < len(lines):
                current = lines[i]
                if current.strip() == "":
                    i += 1
                    continue
                if "|" in current and re.match(r"^\|", current.strip()):
                    if version_count < 3:
                        new_lines.append(current.rstrip())
                        version_count += 1
                    i += 1
                    continue
                break
            continue

        # License - 精简为索引
        if re.match(r"^## § 16 · License & Author", line):
            new_lines.append(line.rstrip())
            new_lines.append("")
            new_lines.append(
                "MIT with Attribution — Full terms, community links: [COMMON.md](../../../COMMON.md)"
            )
            new_lines.append("")
            new_lines.append("| Field| Details|")
            new_lines.append("|-------------|---------------|")
            new_lines.append("| **Author** | neo.ai <lucas_hsueh@hotmail.com> |")
            new_lines.append("| **Contact** | lucas_hsueh@hotmail.com |")
            new_lines.append(
                "| **GitHub** | https://github.com/theneoai/awesome-skills |"
            )
            new_lines.append("")
            new_lines.append(
                "**Author**: awesome-skills | **License**: MIT with Attribution"
            )

            # 跳过剩余的License内容
            i += 1
            while i < len(lines):
                if re.match(r"^## ", lines[i]):
                    break
                i += 1
            continue

        # 普通行
        new_lines.append(line.rstrip())
        i += 1

    # 写回文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))


def find_all_skill_files():
    pattern = os.path.join(BASE_DIR, "**/SKILL.md")
    return glob.glob(pattern, recursive=True)


def main():
    skill_files = find_all_skill_files()
    print(f"找到 {len(skill_files)} 个 SKILL.md 文件")

    processed = 0
    for filepath in skill_files:
        try:
            process_skill_file(filepath)
            processed += 1
            if processed % 100 == 0:
                print(f"已处理 {processed} 个文件...")
        except Exception as e:
            print(f"处理失败 {filepath}: {e}")

    print(f"完成! 已处理 {processed}/{len(skill_files)} 个文件")


if __name__ == "__main__":
    main()
