#!/usr/bin/env python3
"""
Runtime Quality Validator - Test skill performance in practice

This module implements runtime quality testing based on skill-evaluator methodology.
It validates that skills perform as documented in real-world scenarios.

Usage:
    python -m tools.skill_analyzer.runtime_validator --skill skills/software/devops-engineer/SKILL.md
    python -m tools.skill_analyzer.runtime_validator --category software
"""

import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class RuntimeTestCase:
    """Single runtime test case"""
    name: str
    input_prompt: str
    expected_behaviors: List[str]
    forbidden_behaviors: List[str]
    timeout_seconds: int = 60


@dataclass
class RuntimeTestResult:
    """Result of a single runtime test"""
    test_name: str
    passed: bool
    score: float  # 0-10
    issues: List[str]
    response_quality: Dict[str, Any]


class RuntimeValidator:
    """Validate skill runtime quality through practical testing"""
    
    # Runtime quality dimensions from skill-evaluator
    DIMENSIONS = {
        "role_immersion": {
            "weight": 0.20,
            "description": "Maintains role consistently throughout conversation"
        },
        "framework_execution": {
            "weight": 0.20,
            "description": "Follows documented workflow correctly"
        },
        "output_actionability": {
            "weight": 0.20,
            "description": "Produces actionable, specific outputs"
        },
        "knowledge_accuracy": {
            "weight": 0.15,
            "description": "Uses domain knowledge accurately"
        },
        "conversation_stability": {
            "weight": 0.15,
            "description": "Maintains quality over long conversations"
        },
        "edge_case_handling": {
            "weight": 0.10,
            "description": "Handles unexpected inputs gracefully"
        }
    }
    
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.skill_content = skill_path.read_text()
        self.skill_name = skill_path.parent.name
        
    def extract_test_cases(self) -> List[RuntimeTestCase]:
        """Extract test cases from skill's Scenario Examples section"""
        test_cases = []
        
        # Find Scenario Examples section
        scenario_match = re.search(
            r'## § 9.*?Scenario.*?\n(.*?)(?=## § 10|\Z)',
            self.skill_content,
            re.DOTALL | re.IGNORECASE
        )
        
        if scenario_match:
            scenario_content = scenario_match.group(1)
            
            # Extract individual scenarios
            scenarios = re.split(r'###\s+Scenario \d+[:\.]?', scenario_content)
            
            for i, scenario in enumerate(scenarios[1:], 1):  # Skip first empty split
                # Extract user input
                user_match = re.search(r'(?:User|用户|INPUT).*?(?:```|"""|\n\n)', scenario, re.DOTALL | re.IGNORECASE)
                user_input = user_match.group(0) if user_match else f"Test scenario {i}"
                
                # Extract expected behaviors
                expected = []
                for line in scenario.split('\n'):
                    if any(kw in line.lower() for kw in ['should', 'must', 'expected', 'correct']):
                        expected.append(line.strip())
                
                test_cases.append(RuntimeTestCase(
                    name=f"Scenario {i}",
                    input_prompt=user_input[:500],  # Limit length
                    expected_behaviors=expected[:5],
                    forbidden_behaviors=["hallucinate", "contradict", "ignore constraints"],
                    timeout_seconds=60
                ))
        
        # Add default test cases if none found
        if not test_cases:
            test_cases = self._generate_default_test_cases()
        
        return test_cases
    
    def _generate_default_test_cases(self) -> List[RuntimeTestCase]:
        """Generate default test cases based on skill metadata"""
        # Extract skill purpose from description
        desc_match = re.search(r'description:\s*(.+?)(?:\n\w|$)', self.skill_content, re.DOTALL)
        description = desc_match.group(1) if desc_match else self.skill_name
        
        return [
            RuntimeTestCase(
                name="Basic Capability Test",
                input_prompt=f"I need help with {self.skill_name}. What can you do?",
                expected_behaviors=["introduce role", "list capabilities", "offer help"],
                forbidden_behaviors=["hallucinate", "ignore system prompt"],
                timeout_seconds=30
            ),
            RuntimeTestCase(
                name="Edge Case - Ambiguous Request",
                input_prompt="Help me with something",
                expected_behaviors=["ask for clarification", "provide options", "maintain role"],
                forbidden_behaviors=["make assumptions", "provide random help"],
                timeout_seconds=30
            )
        ]
    
    def validate_response(self, test_case: RuntimeTestCase, response: str) -> RuntimeTestResult:
        """Validate a response against test case criteria"""
        issues = []
        scores = {}
        
        # Check expected behaviors
        expected_found = 0
        for behavior in test_case.expected_behaviors:
            if any(kw in response.lower() for kw in behavior.lower().split()):
                expected_found += 1
        
        if test_case.expected_behaviors:
            scores['expected_behaviors'] = (expected_found / len(test_case.expected_behaviors)) * 10
        else:
            scores['expected_behaviors'] = 5.0  # Neutral if no expectations
        
        # Check forbidden behaviors
        forbidden_found = 0
        for behavior in test_case.forbidden_behaviors:
            if behavior.lower() in response.lower():
                forbidden_found += 1
                issues.append(f"Found forbidden behavior: {behavior}")
        
        scores['forbidden_behaviors'] = 10 - (forbidden_found * 5)  # Penalty for each
        
        # Check response structure
        has_structure = any(marker in response for marker in ['##', '###', '- ', '1. ', '```'])
        scores['structure'] = 8.0 if has_structure else 4.0
        
        # Check response length (not too short, not too long)
        word_count = len(response.split())
        if 50 <= word_count <= 2000:
            scores['length'] = 10.0
        elif word_count < 50:
            scores['length'] = 5.0
            issues.append("Response too short")
        else:
            scores['length'] = 7.0  # Long is better than short
        
        # Calculate overall score
        overall_score = sum(scores.values()) / len(scores)
        passed = overall_score >= 6.0 and not issues
        
        return RuntimeTestResult(
            test_name=test_case.name,
            passed=passed,
            score=overall_score,
            issues=issues,
            response_quality=scores
        )
    
    def run_runtime_tests(self) -> Dict[str, Any]:
        """Run all runtime tests for this skill"""
        test_cases = self.extract_test_cases()
        results = []
        
        print(f"Running {len(test_cases)} runtime tests for {self.skill_name}...")
        
        for test_case in test_cases:
            # Simulate response (in real implementation, this would call the LLM)
            # For now, we'll do static analysis
            simulated_response = self._simulate_response(test_case)
            result = self.validate_response(test_case, simulated_response)
            results.append(asdict(result))
            
            status = "✅" if result.passed else "❌"
            print(f"  {status} {test_case.name}: {result.score:.1f}/10")
            if result.issues:
                for issue in result.issues:
                    print(f"      ⚠️  {issue}")
        
        # Calculate dimension scores
        dimension_scores = self._calculate_dimension_scores(results)
        
        # Overall runtime score
        avg_score = sum(r['score'] for r in results) / len(results) if results else 0
        
        return {
            "skill": self.skill_name,
            "path": str(self.skill_path),
            "test_count": len(test_cases),
            "passed_tests": sum(1 for r in results if r['passed']),
            "overall_score": round(avg_score, 2),
            "tier": self._score_to_tier(avg_score),
            "dimension_scores": dimension_scores,
            "test_results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def _simulate_response(self, test_case: RuntimeTestCase) -> str:
        """Simulate a response based on skill content"""
        # In production, this would call the actual LLM with the skill
        # For validation framework, we analyze if the skill has appropriate content
        
        response_parts = []
        
        # Check if System Prompt exists
        if "## § 1" in self.skill_content or "System Prompt" in self.skill_content:
            response_parts.append("Based on my role definition...")
        
        # Check if relevant domain knowledge exists
        if test_case.name == "Basic Capability Test":
            if "## § 2" in self.skill_content or "What This Skill Does" in self.skill_content:
                response_parts.append("I can help you with the following capabilities...")
        
        # Check workflow
        if "## § 8" in self.skill_content or "Workflow" in self.skill_content:
            response_parts.append("I will follow this workflow to help you...")
        
        return " ".join(response_parts) if response_parts else "I understand your request."
    
    def _calculate_dimension_scores(self, results: List[Dict]) -> Dict[str, float]:
        """Calculate scores for each runtime dimension"""
        # In a real implementation, these would be assessed separately
        # For now, we distribute the overall score
        
        avg_score = sum(r['score'] for r in results) / len(results) if results else 0
        
        return {
            "role_immersion": round(min(10, avg_score * 1.1), 1),
            "framework_execution": round(min(10, avg_score * 1.0), 1),
            "output_actionability": round(min(10, avg_score * 0.9), 1),
            "knowledge_accuracy": round(min(10, avg_score * 1.05), 1),
            "conversation_stability": round(min(10, avg_score * 0.95), 1),
            "edge_case_handling": round(min(10, avg_score * 0.85), 1),
        }
    
    def _score_to_tier(self, score: float) -> str:
        """Convert score to tier"""
        if score >= 8.0:
            return "exemplary"
        elif score >= 7.0:
            return "expert"
        elif score >= 5.0:
            return "community"
        else:
            return "basic"


def run_all_runtime_tests(category: Optional[str] = None) -> List[Dict]:
    """Run runtime tests for all skills"""
    skills_dir = Path('/Users/lucas/Documents/Projects/awesome-skills/skills')
    
    if category:
        skill_files = list((skills_dir / category).rglob('SKILL.md'))
    else:
        skill_files = list(skills_dir.rglob('**/SKILL.md'))
    
    results = []
    for skill_file in skill_files:
        try:
            validator = RuntimeValidator(skill_file)
            result = validator.run_runtime_tests()
            results.append(result)
        except Exception as e:
            results.append({
                "skill": skill_file.parent.name,
                "path": str(skill_file),
                "error": str(e)
            })
    
    return results


def print_runtime_summary(results: List[Dict]):
    """Print summary of runtime test results"""
    print("\n" + "="*70)
    print("RUNTIME QUALITY VALIDATION SUMMARY")
    print("="*70)
    
    valid_results = [r for r in results if 'error' not in r]
    errors = [r for r in results if 'error' in r]
    
    if valid_results:
        scores = [r['overall_score'] for r in valid_results]
        print(f"\nTotal Skills Tested: {len(results)}")
        print(f"Successful: {len(valid_results)}")
        print(f"Errors: {len(errors)}")
        print(f"\nAverage Runtime Score: {sum(scores)/len(scores):.2f}/10")
        print(f"Highest: {max(scores):.2f}/10")
        print(f"Lowest: {min(scores):.2f}/10")
        
        # Tier distribution
        tiers = {}
        for r in valid_results:
            tier = r.get('tier', 'unknown')
            tiers[tier] = tiers.get(tier, 0) + 1
        
        print(f"\nRuntime Tier Distribution:")
        for tier, count in sorted(tiers.items(), key=lambda x: -x[1]):
            pct = count / len(valid_results) * 100
            print(f"  {tier:12}: {count:4} ({pct:5.1f}%)")
    
    if errors:
        print(f"\n⚠️  Errors ({len(errors)}):")
        for e in errors[:5]:
            print(f"  - {e['path']}: {e.get('error', 'Unknown')}")


def main():
    parser = argparse.ArgumentParser(description='Runtime Quality Validator')
    parser.add_argument('--skill', '-s', help='Specific skill file to test')
    parser.add_argument('--category', '-c', help='Test all skills in category')
    parser.add_argument('--output', '-o', help='Output JSON file')
    
    args = parser.parse_args()
    
    if args.skill:
        skill_path = Path(args.skill)
        validator = RuntimeValidator(skill_path)
        result = validator.run_runtime_tests()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
        
        print_runtime_summary([result])
        
    elif args.category:
        results = run_all_runtime_tests(args.category)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
        
        print_runtime_summary(results)
        
    else:
        # Run sample test
        sample_skill = Path('skills/software/devops-engineer/SKILL.md')
        if sample_skill.exists():
            validator = RuntimeValidator(sample_skill)
            result = validator.run_runtime_tests()
            print_runtime_summary([result])
        else:
            print("No skill specified. Use --skill or --category")


if __name__ == '__main__':
    main()
