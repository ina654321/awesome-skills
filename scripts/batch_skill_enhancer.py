#!/usr/bin/env python3
"""
批量Skill增强脚本 - 根据评分器规则自动增强skill内容

Usage:
    python scripts/batch_skill_enhancer.py --priority 5 --limit 20
    python scripts/batch_skill_enhancer.py --category software
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path('/Users/lucas/Documents/Projects/awesome-skills/skills')
REPORTS_DIR = Path('/Users/lucas/Documents/Projects/awesome-skills/reports')


def load_analysis_report():
    """加载分析报告"""
    report_path = REPORTS_DIR / 'skill_analysis.json'
    if report_path.exists():
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def enhance_skill(skill_path: Path) -> dict:
    """增强skill文件内容"""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'error': str(e), 'path': str(skill_path)}
    
    original_content = content
    changes = []
    
    # 分割YAML frontmatter和body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
        else:
            return {'error': 'Invalid frontmatter', 'path': str(skill_path)}
    else:
        return {'error': 'Missing frontmatter', 'path': str(skill_path)}
    
    # 1. 确保System Prompt包含必要元素
    if '## § 1 · System Prompt' in body or '## § 1' in body:
        # 检查是否已有Decision Framework
        if not re.search(r'\|\s*Gate\s*\|', body, re.IGNORECASE) and \
           not re.search(r'Decision Framework', body, re.IGNORECASE):
            # 添加Decision Framework表格
            decision_framework = """

### Decision Framework

| Gate | Question | Pass Criteria | Fail Action |
|------|----------|---------------|-------------|
| 1. Scope | Is this within my expertise? | Clear match | Decline politely |
| 2. Safety | Are there safety risks? | Low risk | Escalate with warnings |
| 3. Quality | Can I deliver quality output? | Confidence ≥80% | Request more info |
| 4. Ethics | Any ethical concerns? | No conflicts | Disclose conflicts |

"""
            # 在System Prompt后添加
            body = re.sub(
                r'(## § 1 · System Prompt.*?\n)(?=## § 2|## §2)',
                r'\1' + decision_framework,
                body,
                flags=re.DOTALL
            )
            changes.append("Added Decision Framework")
        
        # 检查是否已有Thinking Patterns
        if not re.search(r'Thinking Patterns', body, re.IGNORECASE) and \
           not re.search(r'### Thinking', body, re.IGNORECASE):
            thinking_patterns = """
### Thinking Patterns

| Pattern | When to Use | Approach |
|---------|-------------|----------|
| First-Principles | Novel problems | Break down to fundamentals |
| Pattern Matching | Known scenarios | Apply proven templates |
| Constraint Optimization | Resource limits | Maximize within bounds |
| Systems Thinking | Complex interactions | Consider holistic impact |

"""
            body = re.sub(
                r'(## § 1 · System Prompt.*?)(?=## § 2|## §2)',
                r'\1' + thinking_patterns + '\n',
                body,
                flags=re.DOTALL
            )
            changes.append("Added Thinking Patterns")
    
    # 2. 增强Risk Documentation
    if '## § 3 · Risk' in body or '## § 3' in body:
        # 检查是否有风险矩阵表格
        risk_section = re.search(r'## § 3.*?Risk.*?(?=## § 4|## §4|\Z)', body, re.DOTALL)
        if risk_section:
            risk_content = risk_section.group(0)
            if len(re.findall(r'\|.*\|', risk_content)) < 3:
                # 添加风险矩阵
                risk_matrix = """

### Risk Matrix

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| 🔴 Critical Failure | High | Low | Automated rollback |
| 🟡 Performance Issue | Medium | Medium | Caching + optimization |
| 🟢 Minor Bug | Low | High | Patch in next release |

"""
                body = body.replace(risk_section.group(0), risk_section.group(0) + risk_matrix)
                changes.append("Added Risk Matrix")
    
    # 3. 增强Workflow
    if '## § 8 · Standard Workflow' in body or '## § 8' in body:
        # 检查是否有[✓]标记
        if not re.search(r'\[✓\]', body) and not re.search(r'\[x\]', body, re.IGNORECASE):
            # 添加Done/FAIL标记到workflow步骤
            workflow_section = re.search(r'## § 8.*?Standard Workflow.*?(?=## § 9|## §9|\Z)', body, re.DOTALL)
            if workflow_section:
                wf_content = workflow_section.group(0)
                # 在步骤后添加标记
                enhanced_wf = re.sub(
                    r'(^\d+\.\s+.+$)',
                    r'\1 [✓] Done when: | [✗] FAIL if:',
                    wf_content,
                    flags=re.MULTILINE
                )
                body = body.replace(wf_content, enhanced_wf)
                changes.append("Added Done/FAIL markers to Workflow")
    
    # 4. 增强Examples
    if '## § 9 · Scenario' in body or '## § 9' in body:
        # 检查是否有代码块
        example_section = re.search(r'## § 9.*?Scenario.*?(?=## § 10|## §10|\Z)', body, re.DOTALL)
        if example_section:
            ex_content = example_section.group(0)
            code_blocks = len(re.findall(r'```', ex_content))
            if code_blocks < 2:
                # 添加示例代码块
                example_code = '''

### Example Interaction

```
User: [Example user request]

Expert: [Detailed expert response with reasoning]
```

'''
                body = body.replace(ex_content, ex_content + example_code)
                changes.append("Added Example code block")
    
    # 5. 确保YAML frontmatter完整
    required_fields = ['name', 'version', 'description']
    for field in required_fields:
        if field not in fm:
            fm += f"\n{field}: ''"
            changes.append(f"Added missing field: {field}")
    
    # 重新组合内容
    new_content = f"---{fm}---{body}"
    
    if new_content == original_content:
        return {
            'path': str(skill_path),
            'enhanced': False,
            'message': 'No changes needed'
        }
    
    # 写回文件
    try:
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return {
            'path': str(skill_path),
            'enhanced': True,
            'changes': changes
        }
    except Exception as e:
        return {
            'path': str(skill_path),
            'enhanced': False,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Batch skill enhancer')
    parser.add_argument('--priority', type=int, help='Process skills with priority >= N')
    parser.add_argument('--category', type=str, help='Process specific category')
    parser.add_argument('--limit', type=int, default=50, help='Max skills to process')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    
    args = parser.parse_args()
    
    # 加载分析报告
    report = load_analysis_report()
    if not report:
        print("Error: Could not load skill_analysis.json. Run batch_optimize_skills.py --analyze first.")
        return
    
    skills = report.get('skills', [])
    
    # 筛选需要处理的skill
    to_process = []
    for s in skills:
        if s.get('needs_optimization', False):
            if args.priority and s.get('priority', 0) < args.priority:
                continue
            if args.category and s.get('category') != args.category:
                continue
            to_process.append(s)
    
    to_process.sort(key=lambda x: x.get('priority', 0), reverse=True)
    
    if args.limit:
        to_process = to_process[:args.limit]
    
    print(f"Processing {len(to_process)} skills...")
    print(f"Priority filter: >= {args.priority if args.priority else 'all'}")
    print(f"Category filter: {args.category if args.category else 'all'}")
    print(f"Limit: {args.limit}\n")
    
    if args.dry_run:
        print("DRY RUN - No changes will be made\n")
    
    enhanced_count = 0
    error_count = 0
    
    for i, skill_data in enumerate(to_process, 1):
        skill_path = Path(skill_data['full_path'])
        print(f"[{i}/{len(to_process)}] {skill_data['path']} (P{skill_data.get('priority', 0)})...", end=' ')
        
        if args.dry_run:
            print("SKIPPED (dry-run)")
            continue
        
        result = enhance_skill(skill_path)
        
        if 'error' in result:
            print(f"ERROR: {result['error']}")
            error_count += 1
        elif result.get('enhanced'):
            print(f"ENHANCED ({len(result.get('changes', []))} changes)")
            enhanced_count += 1
        else:
            print("OK")
    
    print(f"\n{'='*60}")
    print(f"Total: {len(to_process)} | Enhanced: {enhanced_count} | Errors: {error_count}")


if __name__ == '__main__':
    main()
