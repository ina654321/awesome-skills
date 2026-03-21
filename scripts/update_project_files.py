#!/usr/bin/env python3
"""Update README.md and index.html with latest statistics"""

import json
import re
from datetime import datetime
from pathlib import Path

def main():
    # Load evaluation data
    with open('reports/evaluation_report.json') as f:
        data = json.load(f)
    
    summary = data['summary']
    
    # Update README.md
    with open('README.md') as f:
        readme = f.read()
    
    stats_section = f"""<!-- STATS_START -->
## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Total Skills** | {summary['total_skills']} |
| **Average Quality** | {summary['dual_track']['average']:.2f}/10 |
| **Text Quality** | {summary['text_quality']['average']:.2f}/10 |
| **Runtime Quality** | {summary['runtime_quality']['average']:.2f}/10 |
| **Last Updated** | {datetime.now().strftime('%Y-%m-%d')} |

### Quality Distribution

| Tier | Count | Percentage |
|------|-------|------------|
| Exemplary (8.0+) | {summary['tiers'].get('exemplary', 0)} | {summary['tiers'].get('exemplary', 0) / summary['total_skills'] * 100:.1f}% |
| Expert (7.0-7.9) | {summary['tiers'].get('expert', 0)} | {summary['tiers'].get('expert', 0) / summary['total_skills'] * 100:.1f}% |
| Community (5.0-6.9) | {summary['tiers'].get('community', 0)} | {summary['tiers'].get('community', 0) / summary['total_skills'] * 100:.1f}% |
| Basic (<5.0) | {summary['tiers'].get('basic', 0)} | {summary['tiers'].get('basic', 0) / summary['total_skills'] * 100:.1f}% |

📈 [View Full Evaluation Report](https://theneoai.github.io/awesome-skills/reports/evaluation_report.html)
<!-- STATS_END -->"""
    
    pattern = r'<!-- STATS_START -->.*?<!-- STATS_END -->'
    if re.search(pattern, readme, re.DOTALL):
        readme = re.sub(pattern, stats_section, readme, flags=re.DOTALL)
    
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print("✅ README.md updated")
    
    # Update index.html
    with open('index.html') as f:
        html = f.read()
    
    # Update stats
    html = re.sub(
        r'<div class="stat-number">\d+</div><div class="stat-label">Skills</div>',
        f'<div class="stat-number">{summary["total_skills"]}</div><div class="stat-label">Skills</div>',
        html
    )
    
    # Update or add quality stat
    if 'Avg Quality' not in html:
        html = re.sub(
            r'(<div class="stat"><div class="stat-number">7</div><div class="stat-label">Platforms</div></div>)',
            r'\1\n            <div class="stat"><div class="stat-number">{:.1f}</div><div class="stat-label">Avg Quality</div></div>'.format(summary['dual_track']['average']),
            html
        )
    else:
        html = re.sub(
            r'<div class="stat-number">[\d.]+</div><div class="stat-label">Avg Quality</div>',
            f'<div class="stat-number">{summary["dual_track"]["average"]:.1f}</div><div class="stat-label">Avg Quality</div>',
            html
        )
    
    with open('index.html', 'w') as f:
        f.write(html)
    
    print("✅ index.html updated")
    
    # Create JavaScript data file
    Path('assets/js').mkdir(parents=True, exist_ok=True)
    
    js_data = f"""// Auto-generated skill statistics
window.SKILL_STATS = {json.dumps(summary, indent=2)};
window.SKILL_EVALUATIONS = {json.dumps(data['evaluations'][:50], indent=2)};
window.EVALUATION_TIMESTAMP = "{datetime.now().isoformat()}";
"""
    
    Path('assets/js/skill-stats.js').write_text(js_data)
    print("✅ assets/js/skill-stats.js created")
    
    return 0

if __name__ == '__main__':
    exit(main())
