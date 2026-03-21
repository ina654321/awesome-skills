#!/usr/bin/env python3
"""
Dual-Track Skill Evaluator
使用项目自己的双轨评估体系（Text Quality + Runtime Quality）评估skills
并对比refs目录下的社区评估工具skill_evaluator.py
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

@dataclass
class TextQualityScore:
    """文本质量评分（6维度）"""
    system_prompt: float      # 20%
    domain_knowledge: float   # 20%
    workflow: float           # 20%
    error_handling: float     # 15%
    examples: float           # 15%
    metadata: float           # 10%
    
    @property
    def overall(self) -> float:
        return (
            self.system_prompt * 0.20 +
            self.domain_knowledge * 0.20 +
            self.workflow * 0.20 +
            self.error_handling * 0.15 +
            self.examples * 0.15 +
            self.metadata * 0.10
        )

@dataclass
class RuntimeQualityScore:
    """运行时质量评分（6维度）"""
    role_immersion: float           # 20%
    framework_execution: float      # 20%
    output_actionability: float     # 20%
    knowledge_accuracy: float       # 15%
    long_conversation_stability: float  # 15%
    resilience: float               # 10%
    
    @property
    def overall(self) -> float:
        return (
            self.role_immersion * 0.20 +
            self.framework_execution * 0.20 +
            self.output_actionability * 0.20 +
            self.knowledge_accuracy * 0.15 +
            self.long_conversation_stability * 0.15 +
            self.resilience * 0.10
        )

@dataclass
class SkillEvaluation:
    """技能评估结果（双轨）"""
    name: str
    file_path: str
    source: str  # 'project' 或 'refs'
    category: str
    
    # 双轨评分
    text_quality: TextQualityScore
    runtime_quality: RuntimeQualityScore
    
    # 综合评分
    @property
    def overall_score(self) -> float:
        return (self.text_quality.overall + self.runtime_quality.overall) / 2
    
    @property
    def variance(self) -> float:
        return abs(self.text_quality.overall - self.runtime_quality.overall)
    
    # 元数据
    has_references: bool
    has_scripts: bool
    has_assets: bool
    file_size: int
    line_count: int
    
    # 详细发现
    text_findings: List[str]
    runtime_findings: List[str]


class DualTrackEvaluator:
    """双轨评估器"""
    
    def __init__(self, base_dir: str, source: str = "project"):
        self.base_dir = Path(base_dir)
        self.source = source
        self.results: List[SkillEvaluation] = []
    
    def extract_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """提取YAML frontmatter"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    return frontmatter or {}, parts[2]
                except:
                    return {}, content
        return {}, content
    
    def evaluate_text_quality(self, content: str, frontmatter: Dict) -> Tuple[TextQualityScore, List[str]]:
        """
        评估文本质量（6维度）
        基于SKILL.md的内容结构进行评估
        """
        findings = []
        content_lower = content.lower()
        
        # 1. System Prompt (20%)
        # 检查是否有清晰的角色定义、决策框架、思维模式
        system_prompt_score = 7.0  # 基础分
        if re.search(r'system prompt|role definition|identity', content_lower):
            system_prompt_score += 1.5
        if re.search(r'decision framework|first principles', content_lower):
            system_prompt_score += 0.5
        if re.search(r'thinking patterns|analytical approach', content_lower):
            system_prompt_score += 0.5
        if re.search(r'§\s*1|section 1', content_lower):
            system_prompt_score += 0.5
        system_prompt_score = min(10.0, system_prompt_score)
        
        # 2. Domain Knowledge (20%)
        # 检查领域知识深度
        domain_knowledge_score = 7.0
        if len(content) > 3000:
            domain_knowledge_score += 1.0
        if re.search(r'best practice|methodology|framework', content_lower):
            domain_knowledge_score += 1.0
        if re.search(r'§\s*(16|17|18)', content_lower):  # 深度内容
            domain_knowledge_score += 0.5
        if re.search(r'specialized knowledge|expertise', content_lower):
            domain_knowledge_score += 0.5
        domain_knowledge_score = min(10.0, domain_knowledge_score)
        
        # 3. Workflow (20%)
        # 检查工作流程清晰度
        workflow_score = 7.0
        if re.search(r'workflow|process|phase \d', content_lower):
            workflow_score += 1.5
        if re.search(r'step \d+|procedure|protocol', content_lower):
            workflow_score += 0.5
        if re.search(r'done criteria|fail criteria', content_lower):
            workflow_score += 0.5
        if re.search(r'§\s*8|§\s*9', content_lower):
            workflow_score += 0.5
        workflow_score = min(10.0, workflow_score)
        
        # 4. Error Handling (15%)
        # 检查错误处理完整性
        error_handling_score = 6.5
        if re.search(r'error handling|exception|fail', content_lower):
            error_handling_score += 1.5
        if re.search(r'validation|verification|check', content_lower):
            error_handling_score += 1.0
        if re.search(r'§\s*10|troubleshoot', content_lower):
            error_handling_score += 0.5
        if re.search(r'pitfall|anti-pattern', content_lower):
            error_handling_score += 0.5
        error_handling_score = min(10.0, error_handling_score)
        
        # 5. Examples (15%)
        # 检查示例丰富度
        examples_score = 6.5
        example_count = len(re.findall(r'scenario \d|example \d|case study', content_lower))
        if example_count >= 3:
            examples_score += 2.0
        elif example_count >= 1:
            examples_score += 1.0
        if re.search(r'scenario example|usage example', content_lower):
            examples_score += 0.5
        if re.search(r'§\s*9|§\s*20', content_lower):
            examples_score += 0.5
        examples_score = min(10.0, examples_score)
        
        # 6. Metadata (10%)
        # 检查元数据质量
        metadata_score = 7.0
        if frontmatter.get('name'):
            metadata_score += 0.5
        if frontmatter.get('description'):
            metadata_score += 1.0
        if frontmatter.get('metadata', {}).get('author'):
            metadata_score += 0.5
        if frontmatter.get('metadata', {}).get('version'):
            metadata_score += 0.5
        if frontmatter.get('metadata', {}).get('tags'):
            metadata_score += 0.5
        metadata_score = min(10.0, metadata_score)
        
        # 收集发现
        if system_prompt_score < 7:
            findings.append(f"System Prompt得分较低({system_prompt_score:.1f})，建议完善角色定义")
        if domain_knowledge_score < 7:
            findings.append(f"Domain Knowledge得分较低({domain_knowledge_score:.1f})，建议增加领域知识深度")
        if workflow_score < 7:
            findings.append(f"Workflow得分较低({workflow_score:.1f})，建议明确工作流程")
        if error_handling_score < 6:
            findings.append(f"Error Handling得分较低({error_handling_score:.1f})，建议完善错误处理")
        if examples_score < 6:
            findings.append(f"Examples得分较低({examples_score:.1f})，建议增加示例")
        if metadata_score < 7:
            findings.append(f"Metadata得分较低({metadata_score:.1f})，建议完善元数据")
        
        return TextQualityScore(
            system_prompt=system_prompt_score,
            domain_knowledge=domain_knowledge_score,
            workflow=workflow_score,
            error_handling=error_handling_score,
            examples=examples_score,
            metadata=metadata_score
        ), findings
    
    def evaluate_runtime_quality(self, content: str, frontmatter: Dict, 
                                  has_scripts: bool, has_references: bool) -> Tuple[RuntimeQualityScore, List[str]]:
        """
        评估运行时质量（6维度）
        基于实际执行能力的估计
        """
        findings = []
        content_lower = content.lower()
        
        # 1. Role Immersion (20%)
        # 角色沉浸度
        role_immersion_score = 7.0
        if re.search(r'you are|your role|expert in', content_lower):
            role_immersion_score += 1.5
        if re.search(r'professional|specialist|consultant', content_lower):
            role_immersion_score += 0.5
        if re.search(r'personality|approach|style', content_lower):
            role_immersion_score += 0.5
        if re.search(r'§\s*1\.1|1\.1 role', content_lower):
            role_immersion_score += 0.5
        role_immersion_score = min(10.0, role_immersion_score)
        
        # 2. Framework Execution (20%)
        # 框架执行能力
        framework_execution_score = 7.0
        if re.search(r'workflow|framework|methodology', content_lower):
            framework_execution_score += 1.5
        if re.search(r'phase|step|stage', content_lower):
            framework_execution_score += 0.5
        if has_references:
            framework_execution_score += 0.5
        if has_scripts:
            framework_execution_score += 0.5
        framework_execution_score = min(10.0, framework_execution_score)
        
        # 3. Output Actionability (20%)
        # 输出可执行性
        output_actionability_score = 7.0
        if re.search(r'actionable|step.*step|how to', content_lower):
            output_actionability_score += 1.5
        if re.search(r'checklist|deliverable|output', content_lower):
            output_actionability_score += 0.5
        if re.search(r'when to use|capabilities', content_lower):
            output_actionability_score += 0.5
        if re.search(r'tool|command|script', content_lower):
            output_actionability_score += 0.5
        output_actionability_score = min(10.0, output_actionability_score)
        
        # 4. Knowledge Accuracy (15%)
        # 知识准确性
        knowledge_accuracy_score = 7.5
        if re.search(r'standard|best practice|reference', content_lower):
            knowledge_accuracy_score += 1.0
        if has_references:
            knowledge_accuracy_score += 0.5
        if re.search(r'citation|source|authority', content_lower):
            knowledge_accuracy_score += 0.5
        if re.search(r'§\s*(19|20|21)', content_lower):  # 最佳实践和案例
            knowledge_accuracy_score += 0.5
        knowledge_accuracy_score = min(10.0, knowledge_accuracy_score)
        
        # 5. Long-Conversation Stability (15%)
        # 长对话稳定性
        stability_score = 7.0
        if len(content) > 2000:
            stability_score += 1.0
        if re.search(r'context|memory|continuity', content_lower):
            stability_score += 0.5
        if re.search(r'consistency|maintain', content_lower):
            stability_score += 0.5
        score_val = frontmatter.get('metadata', {}).get('score', 0)
        try:
            if isinstance(score_val, str):
                score_val = float(score_val.split('/')[0])
            if score_val >= 8:
                stability_score += 1.0
        except (ValueError, TypeError):
            pass
            stability_score += 1.0
        stability_score = min(10.0, stability_score)
        
        # 6. Resilience & Edge Cases (10%)
        # 弹性和边界情况处理
        resilience_score = 6.5
        if re.search(r'edge case|boundary|limitation', content_lower):
            resilience_score += 1.5
        if re.search(r'error|exception|handle', content_lower):
            resilience_score += 0.5
        if re.search(r'validation|verify|check', content_lower):
            resilience_score += 0.5
        if re.search(r'what if|scenario', content_lower):
            resilience_score += 0.5
        if re.search(r'§\s*10|pitfall', content_lower):
            resilience_score += 0.5
        resilience_score = min(10.0, resilience_score)
        
        # 收集发现
        if role_immersion_score < 7:
            findings.append(f"Role Immersion得分较低({role_immersion_score:.1f})，角色定义可能不够清晰")
        if framework_execution_score < 7:
            findings.append(f"Framework Execution得分较低({framework_execution_score:.1f})，执行框架可能不够完善")
        if output_actionability_score < 7:
            findings.append(f"Output Actionability得分较低({output_actionability_score:.1f})，输出可能不够可执行")
        if knowledge_accuracy_score < 7:
            findings.append(f"Knowledge Accuracy得分较低({knowledge_accuracy_score:.1f})，知识准确性待验证")
        if stability_score < 7:
            findings.append(f"Long-Conversation Stability得分较低({stability_score:.1f})，长对话稳定性可能不足")
        if resilience_score < 6:
            findings.append(f"Resilience得分较低({resilience_score:.1f})，边界情况处理可能不足")
        
        return RuntimeQualityScore(
            role_immersion=role_immersion_score,
            framework_execution=framework_execution_score,
            output_actionability=output_actionability_score,
            knowledge_accuracy=knowledge_accuracy_score,
            long_conversation_stability=stability_score,
            resilience=resilience_score
        ), findings
    
    def infer_category(self, name: str, content: str) -> str:
        """推断skill类别"""
        name_lower = name.lower()
        content_lower = content.lower()
        
        categories = {
            "software": ["code", "dev", "programming", "debug", "refactor", "git", "test", "engineer"],
            "ai-ml": ["ai", "ml", "model", "training", "inference", "llm", "prompt"],
            "data": ["data", "csv", "json", "database", "sql", "analysis", "analyst"],
            "security": ["security", "audit", "vulnerability", "safe", "protect"],
            "creative": ["design", "ui", "ux", "frontend", "css", "html", "art", "write"],
            "business": ["business", "marketing", "seo", "content", "social", "sales"],
            "executive": ["ceo", "cto", "cfo", "executive", "leadership", "strategy"],
            "healthcare": ["medical", "health", "doctor", "nurse", "clinical"],
            "education": ["education", "teacher", "training", "coach", "learn"],
            "legal": ["legal", "law", "compliance", "contract"],
            "finance": ["finance", "accounting", "investment", "bank"],
            "research": ["research", "scientist", "academic", "paper"],
        }
        
        for category, keywords in categories.items():
            for kw in keywords:
                if kw in name_lower or kw in content_lower:
                    return category
        
        return "general"
    
    def evaluate_skill(self, skill_file: Path) -> Optional[SkillEvaluation]:
        """评估单个skill"""
        try:
            content = skill_file.read_text(encoding='utf-8', errors='ignore')
            frontmatter, body = self.extract_frontmatter(content)
            
            skill_name = frontmatter.get('name', skill_file.parent.name)
            skill_dir = skill_file.parent
            
            # 检查目录结构
            has_references = (skill_dir / "references").exists()
            has_scripts = (skill_dir / "scripts").exists()
            has_assets = (skill_dir / "assets").exists()
            
            # 双轨评估
            text_score, text_findings = self.evaluate_text_quality(content, frontmatter)
            runtime_score, runtime_findings = self.evaluate_runtime_quality(
                content, frontmatter, has_scripts, has_references
            )
            
            # 推断类别
            category = self.infer_category(skill_name, content)
            
            return SkillEvaluation(
                name=skill_name,
                file_path=str(skill_file.relative_to(self.base_dir)),
                source=self.source,
                category=category,
                text_quality=text_score,
                runtime_quality=runtime_score,
                has_references=has_references,
                has_scripts=has_scripts,
                has_assets=has_assets,
                file_size=len(content.encode('utf-8')),
                line_count=len(content.splitlines()),
                text_findings=text_findings,
                runtime_findings=runtime_findings
            )
            
        except Exception as e:
            print(f"评估skill失败 {skill_file}: {e}")
            return None
    
    def evaluate_directory(self, pattern: str = "**/SKILL.md", max_skills: Optional[int] = None):
        """评估目录下所有skills"""
        skill_files = list(self.base_dir.rglob(pattern))
        
        if max_skills:
            skill_files = skill_files[:max_skills]
        
        print(f"发现 {len(skill_files)} 个skills，开始评估...")
        
        for i, skill_file in enumerate(skill_files, 1):
            print(f"[{i}/{len(skill_files)}] 评估: {skill_file}")
            result = self.evaluate_skill(skill_file)
            if result:
                self.results.append(result)
        
        return self.results
    
    def generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        lines = []
        
        # 标题
        lines.append(f"# Dual-Track Skill Evaluation Report")
        lines.append(f"")
        lines.append(f"**Source:** {self.source.upper()}")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Total Skills:** {len(self.results)}")
        lines.append(f"")
        
        # 统计摘要
        if self.results:
            avg_text = sum(r.text_quality.overall for r in self.results) / len(self.results)
            avg_runtime = sum(r.runtime_quality.overall for r in self.results) / len(self.results)
            avg_overall = sum(r.overall_score for r in self.results) / len(self.results)
            avg_variance = sum(r.variance for r in self.results) / len(self.results)
            
            lines.append("## 📊 Summary Statistics")
            lines.append("")
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            lines.append(f"| Average Text Quality | {avg_text:.2f}/10 |")
            lines.append(f"| Average Runtime Quality | {avg_runtime:.2f}/10 |")
            lines.append(f"| Average Overall Score | {avg_overall:.2f}/10 |")
            lines.append(f"| Average Variance | {avg_variance:.2f} |")
            lines.append("")
            
            # 质量分布
            lines.append("### Quality Distribution")
            lines.append("")
            
            tiers = {
                "EXEMPLARY (≥9.0)": 0,
                "CERTIFIED (8.0-8.9)": 0,
                "PRODUCTION (7.0-7.9)": 0,
                "DEVELOPMENT (6.0-6.9)": 0,
                "NEEDS_WORK (<6.0)": 0
            }
            
            for r in self.results:
                score = r.overall_score
                if score >= 9.0:
                    tiers["EXEMPLARY (≥9.0)"] += 1
                elif score >= 8.0:
                    tiers["CERTIFIED (8.0-8.9)"] += 1
                elif score >= 7.0:
                    tiers["PRODUCTION (7.0-7.9)"] += 1
                elif score >= 6.0:
                    tiers["DEVELOPMENT (6.0-6.9)"] += 1
                else:
                    tiers["NEEDS_WORK (<6.0)"] += 1
            
            lines.append("| Tier | Count | Percentage |")
            lines.append("|------|-------|------------|")
            for tier, count in tiers.items():
                pct = count / len(self.results) * 100
                lines.append(f"| {tier} | {count} | {pct:.1f}% |")
            lines.append("")
            
            # 类别分布
            lines.append("### Category Distribution")
            lines.append("")
            
            category_counts = defaultdict(int)
            for r in self.results:
                category_counts[r.category] += 1
            
            lines.append("| Category | Count |")
            lines.append("|----------|-------|")
            for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
                lines.append(f"| {cat} | {count} |")
            lines.append("")
            
            # Top Skills
            lines.append("## 🏆 Top 20 Skills")
            lines.append("")
            
            top_skills = sorted(self.results, key=lambda r: -r.overall_score)[:20]
            lines.append("| Rank | Name | Category | Overall | Text | Runtime | Variance |")
            lines.append("|------|------|----------|---------|------|---------|----------|")
            for i, r in enumerate(top_skills, 1):
                var_status = "✅" if r.variance < 1.0 else "⚠️" if r.variance < 2.0 else "❌"
                lines.append(f"| {i} | {r.name} | {r.category} | {r.overall_score:.2f} | {r.text_quality.overall:.2f} | {r.runtime_quality.overall:.2f} | {r.variance:.2f} {var_status} |")
            lines.append("")
            
            # 需要关注的Skills（方差大）
            high_variance = [r for r in self.results if r.variance >= 1.5]
            if high_variance:
                lines.append("## ⚠️ High Variance Skills (Text vs Runtime)")
                lines.append("")
                lines.append("| Name | Text | Runtime | Variance | Issue |")
                lines.append("|------|------|---------|----------|-------|")
                for r in sorted(high_variance, key=lambda x: -x.variance)[:15]:
                    issue = "Text > Runtime" if r.text_quality.overall > r.runtime_quality.overall else "Runtime > Text"
                    lines.append(f"| {r.name} | {r.text_quality.overall:.2f} | {r.runtime_quality.overall:.2f} | {r.variance:.2f} | {issue} |")
                lines.append("")
            
            # 详细评估结果
            lines.append("## 📋 Detailed Evaluation Results")
            lines.append("")
            
            for r in sorted(self.results, key=lambda x: -x.overall_score):
                lines.append(f"### {r.name}")
                lines.append("")
                lines.append(f"- **File:** `{r.file_path}`")
                lines.append(f"- **Category:** {r.category}")
                lines.append(f"- **Overall Score:** {r.overall_score:.2f}/10")
                lines.append(f"- **Text Quality:** {r.text_quality.overall:.2f}/10")
                lines.append(f"- **Runtime Quality:** {r.runtime_quality.overall:.2f}/10")
                lines.append(f"- **Variance:** {r.variance:.2f} {'✅' if r.variance < 1.0 else '⚠️' if r.variance < 2.0 else '❌'}")
                lines.append(f"- **Has References:** {'✅' if r.has_references else '❌'}")
                lines.append(f"- **Has Scripts:** {'✅' if r.has_scripts else '❌'}")
                lines.append("")
                
                # 6维度详细评分
                lines.append("**Text Quality Breakdown:**")
                lines.append("")
                lines.append(f"| Dimension | Score | Weight |")
                lines.append(f"|-----------|-------|--------|")
                lines.append(f"| System Prompt | {r.text_quality.system_prompt:.1f} | 20% |")
                lines.append(f"| Domain Knowledge | {r.text_quality.domain_knowledge:.1f} | 20% |")
                lines.append(f"| Workflow | {r.text_quality.workflow:.1f} | 20% |")
                lines.append(f"| Error Handling | {r.text_quality.error_handling:.1f} | 15% |")
                lines.append(f"| Examples | {r.text_quality.examples:.1f} | 15% |")
                lines.append(f"| Metadata | {r.text_quality.metadata:.1f} | 10% |")
                lines.append("")
                
                lines.append("**Runtime Quality Breakdown:**")
                lines.append("")
                lines.append(f"| Dimension | Score | Weight |")
                lines.append(f"|-----------|-------|--------|")
                lines.append(f"| Role Immersion | {r.runtime_quality.role_immersion:.1f} | 20% |")
                lines.append(f"| Framework Execution | {r.runtime_quality.framework_execution:.1f} | 20% |")
                lines.append(f"| Output Actionability | {r.runtime_quality.output_actionability:.1f} | 20% |")
                lines.append(f"| Knowledge Accuracy | {r.runtime_quality.knowledge_accuracy:.1f} | 15% |")
                lines.append(f"| Long-Conversation Stability | {r.runtime_quality.long_conversation_stability:.1f} | 15% |")
                lines.append(f"| Resilience & Edge Cases | {r.runtime_quality.resilience:.1f} | 10% |")
                lines.append("")
                
                # 发现的问题
                all_findings = r.text_findings + r.runtime_findings
                if all_findings:
                    lines.append("**Findings:**")
                    lines.append("")
                    for f in all_findings[:5]:
                        lines.append(f"- {f}")
                    lines.append("")
                
                lines.append("---")
                lines.append("")
        
        return "\n".join(lines)
    
    def save_json_report(self, output_path: str):
        """保存JSON格式报告"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "source": self.source,
            "total_skills": len(self.results),
            "evaluations": [
                {
                    "name": r.name,
                    "file_path": r.file_path,
                    "category": r.category,
                    "overall_score": r.overall_score,
                    "text_quality": {
                        "system_prompt": r.text_quality.system_prompt,
                        "domain_knowledge": r.text_quality.domain_knowledge,
                        "workflow": r.text_quality.workflow,
                        "error_handling": r.text_quality.error_handling,
                        "examples": r.text_quality.examples,
                        "metadata": r.text_quality.metadata,
                        "overall": r.text_quality.overall
                    },
                    "runtime_quality": {
                        "role_immersion": r.runtime_quality.role_immersion,
                        "framework_execution": r.runtime_quality.framework_execution,
                        "output_actionability": r.runtime_quality.output_actionability,
                        "knowledge_accuracy": r.runtime_quality.knowledge_accuracy,
                        "long_conversation_stability": r.runtime_quality.long_conversation_stability,
                        "resilience": r.runtime_quality.resilience,
                        "overall": r.runtime_quality.overall
                    },
                    "variance": r.variance,
                    "has_references": r.has_references,
                    "has_scripts": r.has_scripts,
                    "has_assets": r.has_assets
                }
                for r in self.results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"JSON报告已保存: {output_path}")


def main():
    """主函数"""
    import sys
    
    # 评估项目自己的skills（采样评估，避免太多）
    print("=" * 60)
    print("评估项目Skills目录 (采样100个)")
    print("=" * 60)
    
    project_evaluator = DualTrackEvaluator(
        base_dir="/Users/lucas/Documents/Projects/awesome-skills/skills",
        source="project"
    )
    project_evaluator.evaluate_directory(max_skills=100)
    
    # 生成项目skills报告
    project_md = project_evaluator.generate_markdown_report()
    project_md_path = "/Users/lucas/Documents/Projects/awesome-skills/reports/project_skills_dual_track_report.md"
    with open(project_md_path, 'w', encoding='utf-8') as f:
        f.write(project_md)
    print(f"项目Skills报告已保存: {project_md_path}")
    
    project_json_path = "/Users/lucas/Documents/Projects/awesome-skills/reports/project_skills_dual_track_data.json"
    project_evaluator.save_json_report(project_json_path)
    
    # 评估refs目录的skills
    print("\n" + "=" * 60)
    print("评估Refs目录Skills")
    print("=" * 60)
    
    refs_evaluator = DualTrackEvaluator(
        base_dir="/Users/lucas/Documents/Projects/awesome-skills/refs",
        source="refs"
    )
    refs_evaluator.evaluate_directory()
    
    # 生成refs报告
    refs_md = refs_evaluator.generate_markdown_report()
    refs_md_path = "/Users/lucas/Documents/Projects/awesome-skills/reports/refs_skills_dual_track_report.md"
    with open(refs_md_path, 'w', encoding='utf-8') as f:
        f.write(refs_md)
    print(f"Refs Skills报告已保存: {refs_md_path}")
    
    refs_json_path = "/Users/lucas/Documents/Projects/awesome-skills/reports/refs_skills_dual_track_data.json"
    refs_evaluator.save_json_report(refs_json_path)
    
    # 输出摘要
    print("\n" + "=" * 60)
    print("评估完成摘要")
    print("=" * 60)
    print(f"项目Skills: {len(project_evaluator.results)} 个已评估")
    if project_evaluator.results:
        avg = sum(r.overall_score for r in project_evaluator.results) / len(project_evaluator.results)
        print(f"  平均分: {avg:.2f}/10")
    print(f"Refs Skills: {len(refs_evaluator.results)} 个已评估")
    if refs_evaluator.results:
        avg = sum(r.overall_score for r in refs_evaluator.results) / len(refs_evaluator.results)
        print(f"  平均分: {avg:.2f}/10")


if __name__ == "__main__":
    main()
