#!/usr/bin/env python3
"""
批量Skill优化脚本 - 使用skill-writer和skill-evaluator优化所有skill

Usage:
    python scripts/batch_optimize_skills.py --analyze              # 分析所有skill质量
    python scripts/batch_optimize_skills.py --optimize --limit 10  # 优化前10个skill
    python scripts/batch_optimize_skills.py --category software    # 只处理software分类
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add tools to path
TOOLS_DIR = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from skill_analyzer import scorer, tokenizer, structure, antipattern

SKILLS_DIR = Path(__file__).parent.parent / "skills"
REPORTS_DIR = Path(__file__).parent.parent / "reports"


def get_all_skills(category: str = None) -> List[Path]:
    """获取所有skill文件路径"""
    if category:
        pattern = f"{category}/**/SKILL.md"
        return list((SKILLS_DIR / category).rglob("SKILL.md"))
    else:
        return list(SKILLS_DIR.rglob("**/SKILL.md"))


def analyze_skill(skill_path: Path) -> Dict[str, Any]:
    """分析单个skill的质量"""
    try:
        # 运行所有分析器
        score_result = scorer.score_skill(skill_path)
        token_result = tokenizer.analyze_token_budget(skill_path)
        struct_result = structure.check_structure(skill_path)
        anti_result = antipattern.scan_antipatterns(skill_path)
        
        return {
            "path": str(skill_path.relative_to(SKILLS_DIR)),
            "full_path": str(skill_path),
            "category": skill_path.parent.parent.name,
            "skill_name": skill_path.parent.name,
            "score": score_result,
            "tokens": token_result,
            "structure": struct_result,
            "antipatterns": anti_result,
            "needs_optimization": _needs_optimization(score_result, anti_result),
            "priority": _calculate_priority(score_result, anti_result),
        }
    except Exception as e:
        return {
            "path": str(skill_path.relative_to(SKILLS_DIR)),
            "full_path": str(skill_path),
            "error": str(e),
        }


def _needs_optimization(score_result: Dict, anti_result: Dict) -> bool:
    """判断是否需要优化"""
    if "error" in score_result:
        return True
    
    weighted_avg = score_result.get("weighted_avg", 0)
    tier = score_result.get("tier", "community")
    
    # 低分或community级别需要优化
    if weighted_avg < 7.0 or tier == "community":
        return True
    
    # 有高危反模式需要优化
    high_issues = anti_result.get("severity_counts", {}).get("high", 0)
    if high_issues > 0:
        return True
    
    return False


def _calculate_priority(score_result: Dict, anti_result: Dict) -> int:
    """计算优化优先级 (1-10, 10最高)"""
    priority = 0
    
    if "error" in score_result:
        return 10
    
    weighted_avg = score_result.get("weighted_avg", 0)
    tier = score_result.get("tier", "community")
    
    # 分数越低优先级越高
    if weighted_avg < 5.0:
        priority += 5
    elif weighted_avg < 6.0:
        priority += 4
    elif weighted_avg < 7.0:
        priority += 3
    elif tier == "community":
        priority += 2
    
    # 反模式问题
    high_issues = anti_result.get("severity_counts", {}).get("high", 0)
    medium_issues = anti_result.get("severity_counts", {}).get("medium", 0)
    priority += high_issues * 2 + medium_issues // 2
    
    return min(priority, 10)


def generate_analysis_report(skills_data: List[Dict], output_file: Path):
    """生成分析报告"""
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # 统计信息
    total = len(skills_data)
    errors = len([s for s in skills_data if "error" in s])
    needs_opt = len([s for s in skills_data if s.get("needs_optimization", False)])
    
    tier_counts = {}
    priority_dist = {i: 0 for i in range(1, 11)}
    
    for s in skills_data:
        if "error" not in s and "score" in s:
            tier = s["score"].get("tier", "unknown")
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        priority = s.get("priority", 1)
        priority_dist[priority] = priority_dist.get(priority, 0) + 1
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_skills": total,
            "errors": errors,
            "needs_optimization": needs_opt,
            "tier_distribution": tier_counts,
            "priority_distribution": priority_dist,
        },
        "skills": skills_data,
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report


def print_summary(report: Dict):
    """打印摘要"""
    summary = report["summary"]
    print("\n" + "=" * 80)
    print("SKILL质量分析报告")
    print("=" * 80)
    print(f"\n总Skill数: {summary['total_skills']}")
    print(f"分析错误: {summary['errors']}")
    print(f"需要优化: {summary['needs_optimization']}")
    
    print("\n质量分布:")
    for tier, count in sorted(summary["tier_distribution"].items()):
        pct = count / summary["total_skills"] * 100
        bar = "█" * int(pct / 5)
        print(f"  {tier:12}: {count:4} ({pct:5.1f}%) {bar}")
    
    print("\n优先级分布 (1-10):")
    for p in range(10, 0, -1):
        count = summary["priority_distribution"].get(p, 0)
        if count > 0:
            bar = "█" * count
            print(f"  P{p:2}: {count:4} {bar}")
    
    # 打印Top 10需要优化的skill
    skills = report["skills"]
    needs_opt_skills = [s for s in skills if s.get("needs_optimization", False)]
    needs_opt_skills.sort(key=lambda x: x.get("priority", 0), reverse=True)
    
    print("\n" + "-" * 80)
    print("Top 10 需要优化的Skill:")
    print("-" * 80)
    for i, s in enumerate(needs_opt_skills[:10], 1):
        score = s.get("score", {})
        print(f"\n{i}. {s['path']}")
        print(f"   优先级: P{s.get('priority', 0)} | 当前分数: {score.get('weighted_avg', 0):.2f}")
        if score.get("gaps"):
            print(f"   改进点: {len(score['gaps'])}个维度需要改进")


def main():
    parser = argparse.ArgumentParser(description="批量Skill优化工具")
    parser.add_argument("--analyze", action="store_true", help="分析所有skill质量")
    parser.add_argument("--optimize", action="store_true", help="执行优化")
    parser.add_argument("--category", type=str, help="只处理指定分类")
    parser.add_argument("--limit", type=int, default=None, help="限制处理数量")
    parser.add_argument("--priority-threshold", type=int, default=5, 
                        help="优先级阈值，只处理优先级>=该值的skill")
    parser.add_argument("--output", type=str, default="reports/skill_analysis.json",
                        help="分析报告输出路径")
    
    args = parser.parse_args()
    
    # 获取skill列表
    print("正在获取skill列表...")
    skills = get_all_skills(args.category)
    print(f"找到 {len(skills)} 个skill")
    
    if args.limit:
        skills = skills[:args.limit]
        print(f"限制处理前 {args.limit} 个")
    
    # 分析所有skill
    if args.analyze or args.optimize:
        print("\n正在分析skill质量...")
        skills_data = []
        
        for i, skill_path in enumerate(skills, 1):
            print(f"  [{i}/{len(skills)}] 分析 {skill_path.relative_to(SKILLS_DIR)}...", end=" ")
            data = analyze_skill(skill_path)
            skills_data.append(data)
            
            if "error" in data:
                print(f"错误: {data['error']}")
            else:
                score = data.get("score", {})
                print(f"分数: {score.get('weighted_avg', 0):.2f}, 优先级: P{data.get('priority', 0)}")
        
        # 生成报告
        report = generate_analysis_report(skills_data, Path(args.output))
        print(f"\n报告已保存到: {args.output}")
        
        # 打印摘要
        print_summary(report)
        
        # 如果需要优化，输出优化列表
        if args.optimize:
            needs_opt = [s for s in skills_data 
                        if s.get("needs_optimization", False) 
                        and s.get("priority", 0) >= args.priority_threshold]
            needs_opt.sort(key=lambda x: x.get("priority", 0), reverse=True)
            
            print(f"\n需要优化的Skill ({len(needs_opt)}个, 优先级>={args.priority_threshold}):")
            for s in needs_opt:
                print(f"  - {s['path']} (P{s.get('priority', 0)})")
            
            # 保存优化任务列表
            tasks_file = REPORTS_DIR / "optimization_tasks.json"
            with open(tasks_file, "w", encoding="utf-8") as f:
                json.dump(needs_opt, f, indent=2, ensure_ascii=False)
            print(f"\n优化任务列表已保存到: {tasks_file}")
            
            return needs_opt
    
    else:
        parser.print_help()
    
    return None


if __name__ == "__main__":
    main()
