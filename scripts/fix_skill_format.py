#!/usr/bin/env python3
"""
修复Skill文件格式，确保符合16-section标准格式

Usage:
    python scripts/fix_skill_format.py --path skills/category/skill-name/SKILL.md
    python scripts/fix_skill_format.py --all  # 修复所有skill
"""

import argparse
import re
from pathlib import Path

# 16-section标准映射
SECTION_MAPPING = {
    r'^#+\s*1\.?\s*System Prompt': '## § 1 · System Prompt',
    r'^#+\s*2\.?\s*What This Skill Does': '## § 2 · What This Skill Does',
    r'^#+\s*3\.?\s*Risk Disclaimer': '## § 3 · Risk Disclaimer',
    r'^#+\s*4\.?\s*Core Philosophy': '## § 4 · Core Philosophy',
    r'^#+\s*5\.?\s*Platform Support': '## § 5 · Platform Support',
    r'^#+\s*6\.?\s*Professional Toolkit': '## § 6 · Professional Toolkit',
    r'^#+\s*7\.?\s*Standards & Reference': '## § 7 · Standards & Reference',
    r'^#+\s*8\.?\s*Standard Workflow': '## § 8 · Standard Workflow',
    r'^#+\s*9\.?\s*Scenario Examples': '## § 9 · Scenario Examples',
    r'^#+\s*10\.?\s*Gotchas & Anti-Patterns': '## § 10 · Gotchas & Anti-Patterns',
    r'^#+\s*11\.?\s*Integration with Other Skills': '## § 11 · Integration with Other Skills',
    r'^#+\s*12\.?\s*Scope & Limitations': '## § 12 · Scope & Limitations',
    r'^#+\s*13\.?\s*How to Use This Skill': '## § 13 · How to Use This Skill',
    r'^#+\s*14\.?\s*Quality Verification': '## § 14 · Quality Verification',
    r'^#+\s*15\.?\s*Version History': '## § 15 · Version History',
    r'^#+\s*16\.?\s*License & Author': '## § 16 · License & Author',
}

# 反向映射 - 将各种变体映射到标准格式
VARIATION_MAPPINGS = {
    # System Prompt variants
    r'^#+\s*System Prompt\s*$': '## § 1 · System Prompt',
    r'^#+\s*1[.\s]+System Prompt': '## § 1 · System Prompt',
    r'^#+\s*Role Definition': '## § 1 · System Prompt',
    
    # What This Skill Does variants  
    r'^#+\s*What (This|the) Skill Does': '## § 2 · What This Skill Does',
    r'^#+\s*2[.\s]+What': '## § 2 · What This Skill Does',
    r'^#+\s*Capabilities': '## § 2 · What This Skill Does',
    
    # Risk Disclaimer variants
    r'^#+\s*Risk Disclaimer': '## § 3 · Risk Disclaimer',
    r'^#+\s*3[.\s]+Risk': '## § 3 · Risk Disclaimer',
    r'^#+\s*Risk Documentation': '## § 3 · Risk Disclaimer',
    
    # Core Philosophy variants
    r'^#+\s*Core Philosophy': '## § 4 · Core Philosophy',
    r'^#+\s*4[.\s]+Core': '## § 4 · Core Philosophy',
    r'^#+\s*Core Mindset': '## § 4 · Core Philosophy',
    
    # Platform Support variants
    r'^#+\s*Platform Support': '## § 5 · Platform Support',
    r'^#+\s*5[.\s]+Platform': '## § 5 · Platform Support',
    r'^#+\s*Install Guide': '## § 5 · Platform Support',
    
    # Professional Toolkit variants
    r'^#+\s*Professional Toolkit': '## § 6 · Professional Toolkit',
    r'^#+\s*6[.\s]+Professional': '## § 6 · Professional Toolkit',
    r'^#+\s*Tools & Frameworks': '## § 6 · Professional Toolkit',
    
    # Standards & Reference variants
    r'^#+\s*Standards? (&|and) Reference': '## § 7 · Standards & Reference',
    r'^#+\s*7[.\s]+Standards': '## § 7 · Standards & Reference',
    
    # Workflow variants
    r'^#+\s*Standard Workflow': '## § 8 · Standard Workflow',
    r'^#+\s*8[.\s]+Workflow': '## § 8 · Standard Workflow',
    r'^#+\s*Workflow': '## § 8 · Standard Workflow',
    
    # Examples variants
    r'^#+\s*Scenario Examples': '## § 9 · Scenario Examples',
    r'^#+\s*9[.\s]+Scenario': '## § 9 · Scenario Examples',
    r'^#+\s*Examples': '## § 9 · Scenario Examples',
    
    # Anti-Patterns variants
    r'^#+\s*Gotchas & Anti-Patterns': '## § 10 · Gotchas & Anti-Patterns',
    r'^#+\s*10[.\s]+Gotchas': '## § 10 · Gotchas & Anti-Patterns',
    r'^#+\s*Anti-Patterns': '## § 10 · Gotchas & Anti-Patterns',
    r'^#+\s*Common Pitfalls': '## § 10 · Gotchas & Anti-Patterns',
    
    # Integration variants
    r'^#+\s*Integration with Other Skills': '## § 11 · Integration with Other Skills',
    r'^#+\s*11[.\s]+Integration': '## § 11 · Integration with Other Skills',
    
    # Scope variants
    r'^#+\s*Scope & Limitations': '## § 12 · Scope & Limitations',
    r'^#+\s*12[.\s]+Scope': '## § 12 · Scope & Limitations',
    
    # Usage variants
    r'^#+\s*How to Use This Skill': '## § 13 · How to Use This Skill',
    r'^#+\s*13[.\s]+How': '## § 13 · How to Use This Skill',
    r'^#+\s*Usage': '## § 13 · How to Use This Skill',
    
    # Quality Verification variants
    r'^#+\s*Quality Verification': '## § 14 · Quality Verification',
    r'^#+\s*14[.\s]+Quality': '## § 14 · Quality Verification',
    
    # Version History variants
    r'^#+\s*Version History': '## § 15 · Version History',
    r'^#+\s*15[.\s]+Version': '## § 15 · Version History',
    r'^#+\s*Changelog': '## § 15 · Version History',
    
    # License variants
    r'^#+\s*License (&|and) Author': '## § 16 · License & Author',
    r'^#+\s*16[.\s]+License': '## § 16 · License & Author',
    r'^#+\s*License': '## § 16 · License & Author',
}


def fix_skill_format(filepath: Path) -> dict:
    """修复skill文件格式"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'error': str(e), 'path': str(filepath)}
    
    original_content = content
    changes = []
    
    # 修复YAML frontmatter格式问题
    # 确保YAML开始标记在第一行
    if not content.startswith('---'):
        # 查找第一个---
        match = re.search(r'\n---\s*\n', content)
        if match:
            # 提取YAML部分
            yaml_end = content.find('---', match.end())
            if yaml_end > 0:
                yaml_content = content[match.start():yaml_end+3]
                rest_content = content[yaml_end+3:]
                content = yaml_content + rest_content
                changes.append("Fixed YAML frontmatter position")
    
    # 修复section标题
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_line = line
        for pattern, replacement in VARIATION_MAPPINGS.items():
            if re.match(pattern, line, re.IGNORECASE):
                new_line = replacement
                changes.append(f"Fixed: '{line.strip()}' -> '{replacement}'")
                break
        new_lines.append(new_line)
    
    content = '\n'.join(new_lines)
    
    # 检查是否有修改
    if content == original_content:
        return {
            'path': str(filepath),
            'fixed': False,
            'message': 'No changes needed'
        }
    
    # 写回文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return {
            'path': str(filepath),
            'fixed': True,
            'changes': changes
        }
    except Exception as e:
        return {
            'path': str(filepath),
            'fixed': False,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Fix skill file format')
    parser.add_argument('--path', type=str, help='Specific skill file to fix')
    parser.add_argument('--all', action='store_true', help='Fix all skill files')
    parser.add_argument('--category', type=str, help='Fix skills in specific category')
    
    args = parser.parse_args()
    
    skills_dir = Path('/Users/lucas/Documents/Projects/awesome-skills/skills')
    
    if args.path:
        files = [Path(args.path)]
    elif args.category:
        files = list((skills_dir / args.category).rglob('SKILL.md'))
    elif args.all:
        files = list(skills_dir.rglob('SKILL.md'))
    else:
        parser.print_help()
        return
    
    print(f"Processing {len(files)} skill files...\n")
    
    fixed_count = 0
    error_count = 0
    
    for i, filepath in enumerate(files, 1):
        try:
            rel_path = filepath.relative_to(skills_dir.parent)
        except ValueError:
            rel_path = filepath
        print(f"[{i}/{len(files)}] {rel_path}...", end=' ')
        result = fix_skill_format(filepath.resolve())
        
        if 'error' in result:
            print(f"ERROR: {result['error']}")
            error_count += 1
        elif result.get('fixed'):
            print(f"FIXED ({len(result.get('changes', []))} changes)")
            fixed_count += 1
        else:
            print("OK")
    
    print(f"\n{'='*60}")
    print(f"Total: {len(files)} | Fixed: {fixed_count} | Errors: {error_count}")


if __name__ == '__main__':
    main()
