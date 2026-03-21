#!/usr/bin/env python3
"""
修复 Version History 表格重复表头的问题
"""

import os
import re
import glob

BASE_DIR = "/Users/lucas/Documents/Projects/awesome-skills/skills"


def fix_duplicate_headers(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    new_lines = []

    i = 0
    while i < len(lines):
        # 检测重复的表头模式
        if i > 0 and i < len(lines) - 3:
            # 检查是否有连续的重复表头
            if (
                lines[i].strip() == "| Version | Date | Changes |"
                and lines[i + 1].strip() == "|---------|------|---------|"
                and lines[i + 2].strip() == "| Version | Date | Changes |"
            ):
                # 跳过第一个重复的表头，保留第二个
                new_lines.append(lines[i])  # First header
                new_lines.append(lines[i + 1])  # Separator
                i += 2  # Skip second header, will add in next iteration

        new_lines.append(lines[i])
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
            fix_duplicate_headers(filepath)
            processed += 1
        except Exception as e:
            print(f"处理失败 {filepath}: {e}")

    print(f"完成! 已处理 {processed}/{len(skill_files)} 个文件")


if __name__ == "__main__":
    main()
