#!/usr/bin/env python3
"""
修复所有 SKILL.md 文件中的问题
- 移除重复的 Quality Verification 行
- 移除重复的 Version History 表头
- 确保所有内容格式正确
"""

import os
import re
import glob

BASE_DIR = "/Users/lucas/Documents/Projects/awesome-skills/skills"


def fix_skill_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    new_lines = []
    prev_line = ""

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 跳过重复的空行
        if stripped == "" and prev_line.strip() == "":
            i += 1
            continue

        # 跳过重复的 Quality Verification 索引行
        if "→ See references/standards.md §7.10 for full checklist" in stripped:
            # 检查上一行是否相同
            if len(new_lines) > 0 and new_lines[-1] == stripped:
                i += 1
                continue

        # 跳过重复的 Version History 表头
        if stripped == "| Version | Date | Changes |":
            if len(new_lines) > 0 and new_lines[-1] == stripped:
                i += 1
                continue
            # 也检查前一行是否是分隔符
            if (
                len(new_lines) > 1
                and new_lines[-1] == "|---------|------|---------|"
                and new_lines[-2] == stripped
            ):
                i += 1
                continue

        new_lines.append(line)
        prev_line = line
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
            fix_skill_file(filepath)
            processed += 1
        except Exception as e:
            print(f"处理失败 {filepath}: {e}")

    print(f"完成! 已处理 {processed}/{len(skill_files)} 个文件")


if __name__ == "__main__":
    main()
