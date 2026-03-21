#!/usr/bin/env python3
"""
Continuous Optimization Pipeline

This script implements the continuous optimization workflow for skills:
1. Daily quality scanning
2. Trend analysis
3. Automated optimization suggestions
4. Progress tracking

Usage:
    python scripts/continuous_optimization.py --scan
    python scripts/continuous_optimization.py --trend --days 30
    python scripts/continuous_optimization.py --suggest --priority 5
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))
from skill_analyzer import scorer, structure, antipattern

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
REPORTS_DIR = PROJECT_ROOT / 'reports'
SKILLS_DIR = PROJECT_ROOT / 'skills'


class ContinuousOptimizer:
    """Manages continuous optimization pipeline"""
    
    def __init__(self):
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load historical analysis data"""
        history = []
        for report_file in sorted(REPORTS_DIR.glob('daily_analysis_*.json')):
            try:
                with open(report_file) as f:
                    data = json.load(f)
                    history.append({
                        'date': report_file.stem.replace('daily_analysis_', ''),
                        'data': data
                    })
            except Exception as e:
                print(f"Warning: Could not load {report_file}: {e}")
        return history
    
    def scan_all_skills(self) -> Dict[str, Any]:
        """Perform full quality scan of all skills"""
        print("🔍 Scanning all skills...")
        
        skill_files = list(SKILLS_DIR.rglob('**/SKILL.md'))
        results = []
        
        for i, skill_file in enumerate(skill_files, 1):
            print(f"  [{i}/{len(skill_files)}] {skill_file.parent.name}...", end=' ')
            try:
                result = scorer.score_skill(skill_file)
                results.append(result)
                print(f"{result['weighted_avg']:.2f}")
            except Exception as e:
                print(f"ERROR: {e}")
                results.append({
                    'path': str(skill_file.relative_to(SKILLS_DIR)),
                    'error': str(e)
                })
        
        # Calculate statistics
        valid_results = [r for r in results if 'error' not in r]
        scores = [r['weighted_avg'] for r in valid_results]
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_skills': len(skill_files),
                'successful': len(valid_results),
                'errors': len(results) - len(valid_results),
                'average_score': sum(scores) / len(scores) if scores else 0,
                'min_score': min(scores) if scores else 0,
                'max_score': max(scores) if scores else 0,
            },
            'tier_distribution': self._calculate_tier_distribution(valid_results),
            'skills': results
        }
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d')
        report_path = REPORTS_DIR / f'daily_analysis_{timestamp}.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✅ Scan complete. Report saved: {report_path}")
        return report
    
    def _calculate_tier_distribution(self, results: List[Dict]) -> Dict[str, int]:
        """Calculate tier distribution"""
        tiers = defaultdict(int)
        for r in results:
            tier = r.get('tier', 'unknown')
            tiers[tier] += 1
        return dict(tiers)
    
    def analyze_trends(self, days: int = 30) -> Dict[str, Any]:
        """Analyze quality trends over time"""
        print(f"📈 Analyzing trends over last {days} days...")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_history = [
            h for h in self.history
            if datetime.strptime(h['date'], '%Y%m%d') >= cutoff_date
        ]
        
        if len(recent_history) < 2:
            print("⚠️  Not enough historical data for trend analysis")
            return {'error': 'Insufficient data'}
        
        # Calculate trends
        first_report = recent_history[0]['data']
        last_report = recent_history[-1]['data']
        
        trends = {
            'period_days': days,
            'data_points': len(recent_history),
            'score_trend': {
                'start': first_report['summary']['average_score'],
                'end': last_report['summary']['average_score'],
                'change': last_report['summary']['average_score'] - first_report['summary']['average_score']
            },
            'tier_trends': {},
            'improved_skills': [],
            'degraded_skills': []
        }
        
        # Compare individual skills
        first_skills = {s['skill']: s for s in first_report.get('skills', []) if 'error' not in s}
        last_skills = {s['skill']: s for s in last_report.get('skills', []) if 'error' not in s}
        
        for skill_name in set(first_skills.keys()) & set(last_skills.keys()):
            first_score = first_skills[skill_name]['weighted_avg']
            last_score = last_skills[skill_name]['weighted_avg']
            change = last_score - first_score
            
            if change > 0.5:
                trends['improved_skills'].append({
                    'name': skill_name,
                    'change': round(change, 2),
                    'from': first_score,
                    'to': last_score
                })
            elif change < -0.5:
                trends['degraded_skills'].append({
                    'name': skill_name,
                    'change': round(change, 2),
                    'from': first_score,
                    'to': last_score
                })
        
        # Sort by magnitude
        trends['improved_skills'].sort(key=lambda x: -x['change'])
        trends['degraded_skills'].sort(key=lambda x: x['change'])
        
        # Save trend report
        report_path = REPORTS_DIR / f'trend_analysis_{days}d.json'
        with open(report_path, 'w') as f:
            json.dump(trends, f, indent=2)
        
        print(f"✅ Trend analysis complete. Report saved: {report_path}")
        return trends
    
    def generate_optimization_plan(self, priority_threshold: int = 5) -> Dict[str, Any]:
        """Generate optimization plan for skills needing improvement"""
        print(f"🎯 Generating optimization plan (P{priority_threshold}+)...")
        
        # Load latest scan
        latest_scan = None
        for report_file in sorted(REPORTS_DIR.glob('daily_analysis_*.json'), reverse=True):
            try:
                with open(report_file) as f:
                    latest_scan = json.load(f)
                    break
            except:
                continue
        
        if not latest_scan:
            print("⚠️  No scan data available. Run --scan first.")
            return {'error': 'No scan data'}
        
        # Identify skills needing optimization
        skills_to_optimize = []
        for skill in latest_scan.get('skills', []):
            if 'error' in skill:
                continue
            
            score = skill.get('weighted_avg', 0)
            tier = skill.get('tier', 'community')
            
            # Calculate priority
            priority = 0
            if score < 5.0:
                priority += 5
            elif score < 6.0:
                priority += 4
            elif score < 7.0:
                priority += 3
            elif tier == 'community':
                priority += 2
            
            if priority >= priority_threshold:
                skills_to_optimize.append({
                    'skill': skill['skill'],
                    'category': skill['category'],
                    'priority': priority,
                    'current_score': score,
                    'target_score': min(8.0, score + 2.0),
                    'gaps': skill.get('gaps', []),
                    'suggested_actions': self._generate_actions(skill)
                })
        
        skills_to_optimize.sort(key=lambda x: (-x['priority'], -x['current_score']))
        
        plan = {
            'generated_at': datetime.now().isoformat(),
            'priority_threshold': priority_threshold,
            'total_skills': len(skills_to_optimize),
            'estimated_effort_days': len(skills_to_optimize) * 0.5,  # Rough estimate
            'skills': skills_to_optimize
        }
        
        # Save plan
        report_path = REPORTS_DIR / f'optimization_plan_P{priority_threshold}.json'
        with open(report_path, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"✅ Optimization plan generated: {len(skills_to_optimize)} skills")
        return plan
    
    def _generate_actions(self, skill_data: Dict) -> List[str]:
        """Generate optimization actions based on gaps"""
        actions = []
        gaps = skill_data.get('gaps', [])
        
        for gap in gaps:
            dim = gap.get('dimension', '')
            if dim == 'system_prompt':
                actions.append("Add Decision Framework with 5+ gates")
                actions.append("Add Thinking Patterns section")
            elif dim == 'risk_documentation':
                actions.append("Create Risk Matrix with 8+ risks")
            elif dim == 'workflow':
                actions.append("Define Standard Workflow with 4+ phases")
                actions.append("Add [✓] Done/[✗] FAIL criteria")
            elif dim == 'example_quality':
                actions.append("Add 3+ Scenario Examples with code")
        
        return list(set(actions))  # Remove duplicates
    
    def print_dashboard(self):
        """Print optimization dashboard"""
        print("\n" + "="*70)
        print("CONTINUOUS OPTIMIZATION DASHBOARD")
        print("="*70)
        
        # Latest scan summary
        latest_scan = None
        for report_file in sorted(REPORTS_DIR.glob('daily_analysis_*.json'), reverse=True):
            try:
                with open(report_file) as f:
                    latest_scan = json.load(f)
                    break
            except:
                continue
        
        if latest_scan:
            print(f"\n📊 Latest Scan ({latest_scan['summary']['generated_at'][:10]})")
            print(f"  Total Skills: {latest_scan['summary']['total_skills']}")
            print(f"  Average Score: {latest_scan['summary']['average_score']:.2f}/10")
            print(f"  Tier Distribution:")
            for tier, count in sorted(latest_scan['tier_distribution'].items()):
                print(f"    {tier:12}: {count}")
        
        # Trend summary
        if len(self.history) >= 2:
            trends = self.analyze_trend_summary()
            print(f"\n📈 Trend (Last 30 Days)")
            print(f"  Score Change: {trends.get('score_change', 0):+.2f}")
            print(f"  Skills Improved: {len(trends.get('improved', []))}")
            print(f"  Skills Degraded: {len(trends.get('degraded', []))}")
        
        # Optimization backlog
        plan = self.generate_optimization_plan(priority_threshold=5)
        print(f"\n🎯 Optimization Backlog (P5+)")
        if 'error' not in plan:
            print(f"  Skills Needing Work: {plan['total_skills']}")
            print(f"  Estimated Effort: {plan['estimated_effort_days']:.1f} days")
        
        if plan['skills']:
            print(f"\n  Top 5 Priority:")
            for s in plan['skills'][:5]:
                print(f"    P{s['priority']}: {s['skill']} ({s['current_score']:.2f} → {s['target_score']:.2f})")
        
        print("\n" + "="*70)
    
    def analyze_trend_summary(self) -> Dict:
        """Quick trend summary"""
        if len(self.history) < 2:
            return {}
        
        first = self.history[0]['data']
        last = self.history[-1]['data']
        
        return {
            'score_change': last['summary']['average_score'] - first['summary']['average_score'],
            'improved': [],  # Simplified
            'degraded': []
        }


def main():
    parser = argparse.ArgumentParser(description='Continuous Optimization Pipeline')
    parser.add_argument('--scan', action='store_true', help='Run full quality scan')
    parser.add_argument('--trend', action='store_true', help='Analyze trends')
    parser.add_argument('--days', type=int, default=30, help='Trend analysis period')
    parser.add_argument('--suggest', action='store_true', help='Generate optimization suggestions')
    parser.add_argument('--priority', type=int, default=5, help='Priority threshold')
    parser.add_argument('--dashboard', action='store_true', help='Show optimization dashboard')
    
    args = parser.parse_args()
    
    optimizer = ContinuousOptimizer()
    
    if args.scan:
        optimizer.scan_all_skills()
    
    if args.trend:
        trends = optimizer.analyze_trends(days=args.days)
        if 'error' not in trends:
            print(f"\nScore Trend: {trends['score_trend']['change']:+.2f}")
            print(f"Skills Improved: {len(trends['improved_skills'])}")
            print(f"Skills Degraded: {len(trends['degraded_skills'])}")
    
    if args.suggest:
        plan = optimizer.generate_optimization_plan(priority_threshold=args.priority)
        if 'error' not in plan:
            print(f"\nOptimization Plan (P{args.priority}+):")
            for s in plan['skills'][:10]:
                print(f"  P{s['priority']}: {s['skill']}")
                for action in s['suggested_actions'][:3]:
                    print(f"    - {action}")
    
    if args.dashboard:
        optimizer.print_dashboard()
    
    if not any([args.scan, args.trend, args.suggest, args.dashboard]):
        parser.print_help()


if __name__ == '__main__':
    main()
