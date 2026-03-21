#!/usr/bin/env python3
"""
Comprehensive Skill Evaluation - skill-evaluator style dual-track validation

Evaluates skills on:
1. Text Quality (6 dimensions)
2. Runtime Quality (6 dimensions)
3. Token Cost Efficiency

Usage:
    python scripts/comprehensive_skill_evaluation.py --output reports/evaluation_report.json
    python scripts/comprehensive_skill_evaluation.py --format html --output reports/evaluation_report.html
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))
from skill_analyzer import scorer, tokenizer, structure, antipattern

REPORTS_DIR = Path('/Users/lucas/Documents/Projects/awesome-skills/reports')
SKILLS_DIR = Path('/Users/lucas/Documents/Projects/awesome-skills/skills')


@dataclass
class TextQualityScore:
    """Text quality dimensions from skill-evaluator"""
    system_prompt: float
    domain_knowledge: float
    workflow: float
    risk_documentation: float
    example_quality: float
    metadata: float
    overall: float


@dataclass
class RuntimeQualityScore:
    """Runtime quality dimensions from skill-evaluator"""
    role_immersion: float
    framework_execution: float
    output_actionability: float
    knowledge_accuracy: float
    conversation_stability: float
    edge_case_handling: float
    overall: float


@dataclass
class TokenCostAnalysis:
    """Token cost efficiency analysis"""
    description_chars: int
    description_limit: int
    body_lines: int
    body_limit: int
    estimated_tokens: int
    token_budget: int
    cost_efficiency_score: float
    description_status: str
    body_status: str


@dataclass
class SkillEvaluation:
    """Complete skill evaluation results"""
    skill_name: str
    category: str
    path: str
    text_quality: TextQualityScore
    runtime_quality: RuntimeQualityScore
    token_cost: TokenCostAnalysis
    dual_track_score: float  # Average of text and runtime
    variance: float  # Difference between text and runtime
    tier: str
    certification_status: str
    recommendations: List[str]


class ComprehensiveEvaluator:
    """skill-evaluator style comprehensive skill evaluator"""
    
    def __init__(self):
        self.results: List[SkillEvaluation] = []
    
    def evaluate_skill(self, skill_path: Path) -> SkillEvaluation:
        """Perform comprehensive evaluation of a single skill"""
        
        # 1. Text Quality Analysis (using existing analyzer)
        text_result = scorer.score_skill(skill_path)
        
        # Extract text quality scores
        text_quality = TextQualityScore(
            system_prompt=text_result['scores'].get('system_prompt', 0),
            domain_knowledge=text_result['scores'].get('domain_knowledge', 0),
            workflow=text_result['scores'].get('workflow', 0),
            risk_documentation=text_result['scores'].get('risk_documentation', 0),
            example_quality=text_result['scores'].get('example_quality', 0),
            metadata=text_result['scores'].get('metadata', 0),
            overall=text_result['weighted_avg']
        )
        
        # 2. Token Cost Analysis
        token_result = tokenizer.analyze_token_budget(skill_path)
        
        desc_info = token_result.get('description', {})
        body_info = token_result.get('body', {})
        
        token_cost = TokenCostAnalysis(
            description_chars=desc_info.get('char_count', 0),
            description_limit=desc_info.get('limit', 263),
            body_lines=body_info.get('line_count', 0),
            body_limit=body_info.get('limit', 500),
            estimated_tokens=token_result.get('token_count', 0),
            token_budget=6000,
            cost_efficiency_score=text_result['scores'].get('token_cost_efficiency', 5),
            description_status=desc_info.get('status', 'UNKNOWN'),
            body_status=body_info.get('status', 'UNKNOWN')
        )
        
        # 3. Runtime Quality Estimation
        # Based on text quality indicators that correlate with runtime performance
        runtime_quality = self._estimate_runtime_quality(skill_path, text_result)
        
        # 4. Dual-Track Score (skill-evaluator methodology)
        dual_track = (text_quality.overall + runtime_quality.overall) / 2
        variance = abs(text_quality.overall - runtime_quality.overall)
        
        # 5. Certification Status
        cert_status = self._determine_certification(text_quality, runtime_quality, variance)
        
        # 6. Generate Recommendations
        recommendations = self._generate_recommendations(
            text_result, text_quality, runtime_quality, token_cost
        )
        
        return SkillEvaluation(
            skill_name=text_result['skill'],
            category=text_result['category'],
            path=str(skill_path.relative_to(SKILLS_DIR)),
            text_quality=text_quality,
            runtime_quality=runtime_quality,
            token_cost=token_cost,
            dual_track_score=round(dual_track, 2),
            variance=round(variance, 2),
            tier=text_result['tier'],
            certification_status=cert_status,
            recommendations=recommendations
        )
    
    def _estimate_runtime_quality(self, skill_path: Path, text_result: Dict) -> RuntimeQualityScore:
        """Estimate runtime quality based on text quality indicators"""
        content = skill_path.read_text()
        
        # Role immersion: based on system prompt depth
        role_immersion = min(10, text_result['scores'].get('system_prompt', 0) * 0.9)
        
        # Framework execution: based on workflow quality
        framework_exec = min(10, text_result['scores'].get('workflow', 0) * 0.9)
        
        # Output actionability: based on example quality
        output_action = min(10, text_result['scores'].get('example_quality', 0) * 0.95)
        
        # Knowledge accuracy: based on domain knowledge
        knowledge_acc = min(10, text_result['scores'].get('domain_knowledge', 0) * 0.95)
        
        # Conversation stability: based on structure completeness
        structure_result = structure.check_structure(skill_path)
        completeness = structure_result.get('completeness', {})
        missing_ratio = len(completeness.get('missing', [])) / 16
        conversation_stab = 10 * (1 - missing_ratio)
        
        # Edge case handling: based on risk documentation
        edge_case = min(10, text_result['scores'].get('risk_documentation', 0) * 0.9)
        
        # Calculate overall
        overall = (
            role_immersion * 0.20 +
            framework_exec * 0.20 +
            output_action * 0.20 +
            knowledge_acc * 0.15 +
            conversation_stab * 0.15 +
            edge_case * 0.10
        )
        
        return RuntimeQualityScore(
            role_immersion=round(role_immersion, 1),
            framework_execution=round(framework_exec, 1),
            output_actionability=round(output_action, 1),
            knowledge_accuracy=round(knowledge_acc, 1),
            conversation_stability=round(conversation_stab, 1),
            edge_case_handling=round(edge_case, 1),
            overall=round(overall, 2)
        )
    
    def _determine_certification(
        self, 
        text: TextQualityScore, 
        runtime: RuntimeQualityScore, 
        variance: float
    ) -> str:
        """Determine certification status based on skill-evaluator thresholds"""
        
        # Certification thresholds from skill-evaluator
        if text.overall >= 8.0 and runtime.overall >= 8.0 and variance < 1.0:
            if all([
                text.system_prompt >= 6.0,
                text.domain_knowledge >= 6.0,
                text.workflow >= 6.0,
                text.risk_documentation >= 6.0,
                text.example_quality >= 6.0,
                text.metadata >= 6.0,
                runtime.role_immersion >= 6.0,
                runtime.framework_execution >= 6.0,
                runtime.output_actionability >= 6.0,
                runtime.knowledge_accuracy >= 6.0,
                runtime.conversation_stability >= 6.0,
                runtime.edge_case_handling >= 5.0
            ]):
                return "✅ CERTIFIED FOR PRODUCTION"
        
        if text.overall >= 7.0 and runtime.overall >= 7.0 and variance < 2.0:
            return "🟡 PRODUCTION READY (Minor Improvements)"
        
        if text.overall >= 5.0 and runtime.overall >= 5.0:
            return "🟠 COMMUNITY QUALITY (Needs Work)"
        
        return "🔴 BASIC (Significant Improvements Required)"
    
    def _generate_recommendations(
        self,
        text_result: Dict,
        text: TextQualityScore,
        runtime: RuntimeQualityScore,
        token: TokenCostAnalysis
    ) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Text quality recommendations
        gaps = text_result.get('gaps', [])
        for gap in gaps[:3]:
            dim = gap.get('dimension', '')
            suggestion = gap.get('suggestion', '')
            recommendations.append(f"[{dim}] {suggestion}")
        
        # Runtime quality recommendations
        if runtime.role_immersion < 6.0:
            recommendations.append("[Runtime] Enhance System Prompt with clearer role definition")
        if runtime.framework_execution < 6.0:
            recommendations.append("[Runtime] Add explicit workflow steps with [✓] Done criteria")
        if runtime.output_actionability < 6.0:
            recommendations.append("[Runtime] Include more practical examples with code")
        
        # Token cost recommendations
        if token.description_status == "OVER_BUDGET":
            recommendations.append(f"[Token] Reduce description from {token.description_chars} to <{token.description_limit} chars")
        if token.body_status == "OVER_BUDGET":
            recommendations.append(f"[Token] Reduce body from {token.body_lines} to <{token.body_limit} lines")
        
        return recommendations[:5]  # Top 5 recommendations
    
    def evaluate_all(self, category: str = None) -> Dict[str, Any]:
        """Evaluate all skills"""
        if category:
            skill_files = list((SKILLS_DIR / category).rglob('SKILL.md'))
        else:
            skill_files = list(SKILLS_DIR.rglob('**/SKILL.md'))
        
        print(f"🔍 Evaluating {len(skill_files)} skills...")
        
        self.results = []
        for i, skill_file in enumerate(skill_files, 1):
            print(f"  [{i}/{len(skill_files)}] {skill_file.parent.name}...", end=' ')
            try:
                evaluation = self.evaluate_skill(skill_file)
                self.results.append(evaluation)
                print(f"✓ T:{evaluation.text_quality.overall:.1f} R:{evaluation.runtime_quality.overall:.1f}")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        return self._generate_summary()
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate evaluation summary"""
        if not self.results:
            return {}
        
        text_scores = [r.text_quality.overall for r in self.results]
        runtime_scores = [r.runtime_quality.overall for r in self.results]
        dual_track_scores = [r.dual_track_score for r in self.results]
        
        # Certification breakdown
        certifications = {}
        for r in self.results:
            status = r.certification_status
            certifications[status] = certifications.get(status, 0) + 1
        
        # Tier breakdown
        tiers = {}
        for r in self.results:
            tier = r.tier
            tiers[tier] = tiers.get(tier, 0) + 1
        
        return {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_skills': len(self.results),
                'text_quality': {
                    'average': round(sum(text_scores) / len(text_scores), 2),
                    'min': round(min(text_scores), 2),
                    'max': round(max(text_scores), 2)
                },
                'runtime_quality': {
                    'average': round(sum(runtime_scores) / len(runtime_scores), 2),
                    'min': round(min(runtime_scores), 2),
                    'max': round(max(runtime_scores), 2)
                },
                'dual_track': {
                    'average': round(sum(dual_track_scores) / len(dual_track_scores), 2),
                    'min': round(min(dual_track_scores), 2),
                    'max': round(max(dual_track_scores), 2)
                },
                'certifications': certifications,
                'tiers': tiers
            },
            'evaluations': [asdict(r) for r in self.results]
        }
    
    def generate_html_report(self, output_path: Path):
        """Generate HTML report for GitHub Pages"""
        summary = self._generate_summary()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill Evaluation Report - Awesome Skills</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        header p {{ opacity: 0.9; font-size: 1.1em; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            font-size: 0.9em;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 10px;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-detail {{
            font-size: 0.9em;
            color: #888;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #555;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        .badge-certified {{ background: #d4edda; color: #155724; }}
        .badge-production {{ background: #fff3cd; color: #856404; }}
        .badge-community {{ background: #ffe0b2; color: #e65100; }}
        .badge-basic {{ background: #f8d7da; color: #721c24; }}
        .score {{ font-weight: bold; }}
        .score-high {{ color: #28a745; }}
        .score-medium {{ color: #ffc107; }}
        .score-low {{ color: #dc3545; }}
        .variance-low {{ color: #28a745; }}
        .variance-high {{ color: #dc3545; }}
        .timestamp {{
            text-align: center;
            color: #888;
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Skill Evaluation Report</h1>
            <p>Comprehensive dual-track quality assessment using skill-evaluator methodology</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Skills</h3>
                <div class="stat-value">{summary['summary']['total_skills']}</div>
                <div class="stat-detail">Evaluated</div>
            </div>
            <div class="stat-card">
                <h3>Text Quality</h3>
                <div class="stat-value">{summary['summary']['text_quality']['average']:.1f}</div>
                <div class="stat-detail">Average Score</div>
            </div>
            <div class="stat-card">
                <h3>Runtime Quality</h3>
                <div class="stat-value">{summary['summary']['runtime_quality']['average']:.1f}</div>
                <div class="stat-detail">Average Score</div>
            </div>
            <div class="stat-card">
                <h3>Dual-Track</h3>
                <div class="stat-value">{summary['summary']['dual_track']['average']:.1f}</div>
                <div class="stat-detail">Combined Score</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Certification Status</h2>
            <table>
                <tr><th>Status</th><th>Count</th><th>Percentage</th></tr>
"""
        
        for status, count in summary['summary']['certifications'].items():
            pct = count / summary['summary']['total_skills'] * 100
            badge_class = 'badge-certified' if 'CERTIFIED' in status else \
                         'badge-production' if 'PRODUCTION READY' in status else \
                         'badge-community' if 'COMMUNITY' in status else 'badge-basic'
            html += f"""
                <tr>
                    <td><span class="badge {badge_class}">{status}</span></td>
                    <td>{count}</td>
                    <td>{pct:.1f}%</td>
                </tr>
"""
        
        html += """
            </table>
        </div>
        
        <div class="section">
            <h2>🏆 Top Performing Skills</h2>
            <table>
                <tr>
                    <th>Skill</th>
                    <th>Category</th>
                    <th>Text</th>
                    <th>Runtime</th>
                    <th>Dual-Track</th>
                    <th>Variance</th>
                    <th>Status</th>
                </tr>
"""
        
        # Sort by dual-track score
        top_skills = sorted(self.results, key=lambda x: -x.dual_track_score)[:20]
        
        for skill in top_skills:
            text_class = 'score-high' if skill.text_quality.overall >= 7 else 'score-medium' if skill.text_quality.overall >= 5 else 'score-low'
            runtime_class = 'score-high' if skill.runtime_quality.overall >= 7 else 'score-medium' if skill.runtime_quality.overall >= 5 else 'score-low'
            variance_class = 'variance-low' if skill.variance < 1.0 else 'variance-high'
            
            badge_class = 'badge-certified' if 'CERTIFIED' in skill.certification_status else \
                         'badge-production' if 'PRODUCTION READY' in skill.certification_status else \
                         'badge-community' if 'COMMUNITY' in skill.certification_status else 'badge-basic'
            
            html += f"""
                <tr>
                    <td><strong>{skill.skill_name}</strong></td>
                    <td>{skill.category}</td>
                    <td class="score {text_class}">{skill.text_quality.overall:.1f}</td>
                    <td class="score {runtime_class}">{skill.runtime_quality.overall:.1f}</td>
                    <td class="score">{skill.dual_track_score:.1f}</td>
                    <td class="{variance_class}">{skill.variance:.1f}</td>
                    <td><span class="badge {badge_class}">{skill.certification_status.split(']')[0].replace('[', '')}</span></td>
                </tr>
"""
        
        html += f"""
            </table>
        </div>
        
        <div class="section">
            <h2>📋 Skills Needing Improvement</h2>
            <table>
                <tr>
                    <th>Skill</th>
                    <th>Score</th>
                    <th>Key Issues</th>
                </tr>
"""
        
        # Bottom 10 skills
        bottom_skills = sorted(self.results, key=lambda x: x.dual_track_score)[:10]
        
        for skill in bottom_skills:
            issues = skill.recommendations[0] if skill.recommendations else 'No major issues'
            html += f"""
                <tr>
                    <td>{skill.skill_name}</td>
                    <td class="score score-low">{skill.dual_track_score:.1f}</td>
                    <td><small>{issues}</small></td>
                </tr>
"""
        
        html += f"""
            </table>
        </div>
        
        <div class="timestamp">
            <p>Report generated: {summary['generated_at'][:19].replace('T', ' ')} UTC</p>
            <p>Using skill-evaluator dual-track methodology</p>
        </div>
    </div>
</body>
</html>
"""
        
        output_path.write_text(html)
        print(f"✅ HTML report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Comprehensive Skill Evaluation')
    parser.add_argument('--category', '-c', help='Evaluate specific category')
    parser.add_argument('--output', '-o', default='reports/evaluation_report.json', help='Output JSON file')
    parser.add_argument('--format', '-f', choices=['json', 'html', 'both'], default='both', help='Output format')
    
    args = parser.parse_args()
    
    evaluator = ComprehensiveEvaluator()
    summary = evaluator.evaluate_all(args.category)
    
    # Save JSON
    if args.format in ['json', 'both']:
        json_path = Path(args.output)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ JSON report saved: {json_path}")
    
    # Generate HTML
    if args.format in ['html', 'both']:
        html_path = Path(args.output).with_suffix('.html')
        evaluator.generate_html_report(html_path)
    
    # Print summary
    print("\n" + "="*70)
    print("EVALUATION SUMMARY")
    print("="*70)
    print(f"Total Skills: {summary['summary']['total_skills']}")
    print(f"Text Quality Avg: {summary['summary']['text_quality']['average']:.2f}/10")
    print(f"Runtime Quality Avg: {summary['summary']['runtime_quality']['average']:.2f}/10")
    print(f"Dual-Track Avg: {summary['summary']['dual_track']['average']:.2f}/10")
    print("\nCertification Status:")
    for status, count in summary['summary']['certifications'].items():
        print(f"  {status}: {count}")


if __name__ == '__main__':
    main()
