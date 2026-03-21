#!/usr/bin/env python3
"""Display evaluation summary in GitHub Actions"""

import json
from pathlib import Path

def main():
    report_path = Path('reports/evaluation_report.json')
    if not report_path.exists():
        print("Error: evaluation_report.json not found")
        return 1
    
    with open(report_path) as f:
        data = json.load(f)
    
    summary = data['summary']
    
    print("="*70)
    print("STEP 1 COMPLETE: EVALUATION RESULTS")
    print("="*70)
    print()
    print(f"Total Skills Evaluated: {summary['total_skills']}")
    print()
    print("Quality Scores:")
    print(f"  Text Quality:     {summary['text_quality']['average']:.2f}/10")
    print(f"  Runtime Quality:  {summary['runtime_quality']['average']:.2f}/10")
    print(f"  Dual-Track:       {summary['dual_track']['average']:.2f}/10")
    print()
    print("Certification Status:")
    for status, count in summary['certifications'].items():
        pct = count / summary['total_skills'] * 100
        print(f"  {status}: {count} ({pct:.1f}%)")
    print()
    print("Top 5 Skills:")
    top5 = sorted(data['evaluations'], key=lambda x: -x['dual_track_score'])[:5]
    for i, skill in enumerate(top5, 1):
        print(f"  {i}. {skill['skill_name']}: {skill['dual_track_score']:.2f}")
    print()
    print("="*70)
    return 0

if __name__ == '__main__':
    exit(main())
