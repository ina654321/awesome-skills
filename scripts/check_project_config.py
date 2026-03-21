#!/usr/bin/env python3
"""
Project Configuration Checker

Verifies that all required files and configurations are in place.

Usage:
    python scripts/check_project_config.py
"""

import sys
from pathlib import Path
from typing import List, Tuple

REQUIRED_FILES = [
    # Workflows
    '.github/workflows/comprehensive-evaluation.yml',
    '.github/workflows/pages-deploy.yml',
    '.github/workflows/skill-quality-gate.yml',
    '.github/workflows/daily-optimization-scan.yml',
    '.github/workflows/pr-skill-check.yml',
    
    # Scripts
    'scripts/comprehensive_skill_evaluation.py',
    'scripts/continuous_optimization.py',
    'scripts/batch_optimize_skills.py',
    'scripts/batch_skill_enhancer.py',
    'scripts/fix_skill_format.py',
    'scripts/generate_markdown_report.py',
    
    # Analysis tools
    'tools/skill_analyzer/scorer.py',
    'tools/skill_analyzer/runtime_validator.py',
    'tools/skill_analyzer/structure.py',
    'tools/skill_analyzer/antipattern.py',
    'tools/skill_analyzer/tokenizer.py',
    
    # Documentation
    'README.md',
    'index.html',
    'CI_CD_GUIDE.md',
    'PROJECT_CONFIG.md',
]

REQUIRED_DIRS = [
    'skills',
    'reports',
    'assets/js',
    '.github/workflows',
]


def check_files() -> Tuple[List[str], List[str]]:
    """Check if required files exist"""
    missing = []
    found = []
    
    for file_path in REQUIRED_FILES:
        path = Path(file_path)
        if path.exists():
            found.append(file_path)
        else:
            missing.append(file_path)
    
    return found, missing


def check_directories() -> Tuple[List[str], List[str]]:
    """Check if required directories exist"""
    missing = []
    found = []
    
    for dir_path in REQUIRED_DIRS:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            found.append(dir_path)
        else:
            missing.append(dir_path)
    
    return found, missing


def check_readme_stats_section() -> bool:
    """Check if README has stats section"""
    readme = Path('README.md')
    if not readme.exists():
        return False
    
    content = readme.read_text()
    return '<!-- STATS_START -->' in content and '<!-- STATS_END -->' in content


def check_index_quality_link() -> bool:
    """Check if index.html has quality report link"""
    index = Path('index.html')
    if not index.exists():
        return False
    
    content = index.read_text()
    return 'evaluation_report.html' in content


def main():
    print("="*70)
    print("PROJECT CONFIGURATION CHECK")
    print("="*70)
    print()
    
    # Check files
    found_files, missing_files = check_files()
    print(f"📁 Files: {len(found_files)}/{len(REQUIRED_FILES)} found")
    if missing_files:
        print("   ❌ Missing:")
        for f in missing_files:
            print(f"      - {f}")
    else:
        print("   ✅ All required files present")
    print()
    
    # Check directories
    found_dirs, missing_dirs = check_directories()
    print(f"📂 Directories: {len(found_dirs)}/{len(REQUIRED_DIRS)} found")
    if missing_dirs:
        print("   ❌ Missing:")
        for d in missing_dirs:
            print(f"      - {d}")
    else:
        print("   ✅ All required directories present")
    print()
    
    # Check README stats section
    print("📝 README.md:")
    if check_readme_stats_section():
        print("   ✅ Stats section found (<!-- STATS_START -->...<!-- STATS_END -->)")
    else:
        print("   ❌ Stats section not found")
    print()
    
    # Check index.html quality link
    print("🌐 index.html:")
    if check_index_quality_link():
        print("   ✅ Quality report link found")
    else:
        print("   ❌ Quality report link not found")
    print()
    
    # Summary
    print("="*70)
    total_checks = len(REQUIRED_FILES) + len(REQUIRED_DIRS) + 2
    passed_checks = len(found_files) + len(found_dirs)
    if check_readme_stats_section():
        passed_checks += 1
    if check_index_quality_link():
        passed_checks += 1
    
    percentage = (passed_checks / total_checks) * 100
    
    if missing_files or missing_dirs:
        print(f"⚠️  Status: {passed_checks}/{total_checks} checks passed ({percentage:.0f}%)")
        print("   Some required files are missing.")
        return 1
    else:
        print(f"✅ Status: {passed_checks}/{total_checks} checks passed ({percentage:.0f}%)")
        print("   Project configuration is complete!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
