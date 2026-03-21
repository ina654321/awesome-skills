#!/usr/bin/env python3
"""
Skill 文件精简脚本 - 完整版
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
        lines = f.readlines()

    new_lines = []
    skip_mode = None  # 'quality', 'version', 'license'
    skip_count = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # 检测章节开始
        if re.match(r"^## § 14 · Quality Verification", line):
            # 精简 Quality Verification
            new_lines.append(line.rstrip())
            new_lines.append("")
            new_lines.append("→ See references/standards.md §7.10 for full checklist")
            new_lines.append("")
            skip_mode = "quality"
            i += 1
            continue

        elif re.match(r"^## § 15 · Version History", line):
            # 精简 Version History
            new_lines.append(line.rstrip())
            new_lines.append("")
            new_lines.append("| Version | Date | Changes |")
            new_lines.append("|---------|------|---------|")
            skip_mode = "version"
            version_count = 0
            i += 1
            continue

        elif re.match(r"^## § 16 · License & Author", line):
            # 精简 License
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
            skip_mode = "license"
            i += 1
            continue

        # 处理不同跳过模式
        if skip_mode == "quality":
            # 跳过直到找到 Test Cases 或下一个章节
            if re.match(r"^### Test Cases", line):
                skip_mode = None
            elif re.match(r"^## ", line) and not "Quality" in line:
                skip_mode = None
                new_lines.append(line.rstrip())
                i += 1
                continue

        elif skip_mode == "version":
            # 收集版本行
            if "|" in line and re.match(r"^\|", line.strip()):
                if version_count < 3:
                    new_lines.append(line.rstrip())
                    version_count += 1
                i += 1
                continue
            else:
                # 版本历史结束
                skip_mode = None
                new_lines.append(line.rstrip())
                i += 1
                continue

        elif skip_mode == "license":
            # 跳过直到下一个章节
            if re.match(r"^## ", line):
                skip_mode = None
                new_lines.append(line.rstrip())
                i += 1
                continue
            else:
                i += 1
                continue

        # 移除重复的触发词声明 (在文件开头的)
        if i < 10 and re.match(r"^Triggers:", line):
            # 检查下一行是否重复
            if i + 1 < len(lines) and re.match(r"^Works with:", lines[i]):
                new_lines.append(line.rstrip())
                new_lines.append(lines[i].rstrip())
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
