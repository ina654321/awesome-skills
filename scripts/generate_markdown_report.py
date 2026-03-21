#!/usr/bin/env python3
"""Generate Markdown report from optimization recommendations"""

import json
from datetime import datetime
from pathlib import Path

def main():
    # Load recommendations
    report_path = Path('reports/optimization_recommendations.json')
    if not report_path.exists():
        print("Error: optimization_recommendations.json not found")
        return 1
    
    with open(report_path) as f:
        report = json.load(f)
    
    # Generate Markdown
    lines = []
    lines.append('# Daily Optimization Report')
    lines.append('')
    lines.append(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}')
    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append('| Metric | Count |')
    lines.append('|--------|-------|')
    lines.append(f"| Total Skills | {report['total_skills']} |")
    lines.append(f"| Need Optimization | {report['total_skills']} |")
    
    high_priority = len([s for s in report['skills'] if s['priority'] >= 5])
    lines.append(f"| High Priority (P5+) | {high_priority} |")
    lines.append('')
    lines.append('## Priority Breakdown')
    lines.append('')
    lines.append('| Priority | Count |')
    lines.append('|----------|-------|')
    
    # Count by priority
    priority_counts = {}
    for s in report['skills']:
        p = s['priority']
        priority_counts[p] = priority_counts.get(p, 0) + 1
    
    for p in sorted(priority_counts.keys(), reverse=True):
        lines.append(f"| P{p} | {priority_counts[p]} |")
    
    lines.append('')
    lines.append('## Top 20 Recommendations')
    lines.append('')
    lines.append('| Priority | Skill | Score | Tier | Gaps |')
    lines.append('|----------|-------|-------|------|------|')
    
    for rec in report['skills'][:20]:
        gaps_str = ', '.join(rec['gaps'][:3]) if rec['gaps'] else 'None'
        lines.append(f"| P{rec['priority']} | {rec['skill']} | {rec['current_score']:.2f} | {rec['tier']} | {gaps_str} |")
    
    lines.append('')
    lines.append('## Action Items')
    lines.append('')
    lines.append('1. **P7 Skills**: Immediate attention required')
    lines.append('2. **P6 Skills**: Schedule for this week')
    lines.append('3. **P5 Skills**: Schedule for this sprint')
    lines.append('4. **P3-P4 Skills**: Backlog for next month')
    lines.append('')
    lines.append('---')
    lines.append('*This report is auto-generated daily.*')
    
    # Write report
    output_path = Path('reports/OPTIMIZATION_REPORT.md')
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"Report generated: {len(report['skills'])} skills need optimization")
    return 0

if __name__ == '__main__':
    exit(main())
