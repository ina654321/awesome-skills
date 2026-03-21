#!/usr/bin/env python3
"""
修复 Version History 表格重复表头的问题 - 第二版
"""

import os
import re
import glob

BASE_DIR = "/Users/lucas/Documents/Projects/awesome-skills/skills"


def fix_duplicate_headers(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue

        # 检查是否是第二个重复的表头（在分隔线之后）
        if (
            i > 0
            and line.strip() == "| Version | Date | Changes |"
            and lines[i - 1].strip() == "|---------|------|---------|"
        ):
            # 跳过这一行
            skip_next = True
            continue

        new_lines.append(line)

    # 写回文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


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
