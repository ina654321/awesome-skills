#!/usr/bin/env python3
"""
Skill 文件精简脚本 - 修复版本
- 精简 §14 Quality Verification
- 精简 §15 Version History (保留最近3条)
- 精简 §16 License & Author
- 移除重复的触发词声明
- 移除重复的 "Works with" 声明
"""

import os
import re
import glob

BASE_DIR = "/Users/lucas/Documents/Projects/awesome-skills/skills"


def process_skill_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    new_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # 标记各个章节的起始
        if re.match(r"^## § 14 · Quality Verification", line):
            # 简化版本
            new_lines.append(line)
            new_lines.append("")
            new_lines.append("→ See references/standards.md §7.10 for full checklist")
            new_lines.append("")
            # 跳过原来的内容，寻找 Test Cases
            i += 1
            # 找到 Test Cases 部分
            found_test_cases = False
            while i < len(lines):
                if re.match(r"^### Test Cases", lines[i]) or re.match(
                    r"^## § 15", lines[i]
                ):
                    found_test_cases = True
                    break
                i += 1

            if found_test_cases:
                # 复制 Test Cases 部分及其后的内容
                while i < len(lines):
                    if re.match(r"^## § 15", lines[i]):
                        break
                    new_lines.append(lines[i])
                    i += 1
            continue

        elif re.match(r"^## § 15 · Version History", line):
            new_lines.append(line)
            new_lines.append("")
            new_lines.append("| Version | Date | Changes |")
            new_lines.append("|---------|------|---------|")
            # 只保留最近3条
            version_count = 0
            i += 1
            while i < len(lines):
                # 检查是否是空行或分隔线
                if lines[i].strip() == "" or lines[i].strip() == "---":
                    i += 1
                    continue
                # 检查是否是版本行 (以 | 开头)
                if "|" in lines[i] and re.match(r"^\|", lines[i]):
                    if version_count < 3:
                        new_lines.append(lines[i])
                        version_count += 1
                    i += 1
                else:
                    break
            continue

        elif re.match(r"^## § 16 · License & Author", line):
            new_lines.append(line)
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
            # 跳过后面的内容 - 跳过直到下一个 ## 或文件结束
            i += 1
            while i < len(lines):
                if re.match(r"^## ", lines[i]):
                    break
                i += 1
            continue

        # 移除重复的触发词声明 (在文件开头的)
        if i < 10 and re.match(r"^Triggers:", line):
            # 检查下一行是否重复
            if i + 1 < len(lines) and re.match(r"^Works with:", lines[i + 1]):
                new_lines.append(line)
                new_lines.append(lines[i + 1])
                new_lines.append("")  # 空行
                i += 2
                # 跳过后续的重复声明
                while i < len(lines) and not re.match(r"^## ", lines[i]):
                    if re.match(r"^Triggers:|^Works with:", lines[i]):
                        i += 1
                        continue
                    break
                continue

        # 普通行
        new_lines.append(line)
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
            print(f"已处理: {filepath}")
        except Exception as e:
            print(f"处理失败 {filepath}: {e}")

    print(f"完成! 已处理 {processed}/{len(skill_files)} 个文件")


if __name__ == "__main__":
    main()
