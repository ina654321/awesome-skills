#!/usr/bin/env python3
"""
Update category filters in index.html based on skills directory structure

Usage:
    python scripts/update_category_filters.py
"""

import re
from pathlib import Path
from collections import Counter

SKILLS_DIR = Path(__file__).parent.parent / "skills"
INDEX_FILE = Path(__file__).parent.parent / "index.html"

# Category display names mapping
CATEGORY_NAMES = {
    'admin': 'Admin',
    'aerospace': 'Aerospace',
    'agriculture': 'Agriculture',
    'ai-ml': 'AI/ML',
    'automotive': 'Automotive',
    'biotech': 'Biotech',
    'blockchain': 'Blockchain',
    'business': 'Business',
    'construction': 'Construction',
    'construction-worker': 'Construction Worker',
    'content': 'Content',
    'crafts': 'Crafts',
    'creative': 'Creative',
    'cybersecurity': 'Security',
    'data': 'Data',
    'education': 'Education',
    'energy': 'Energy',
    'enterprise': 'Enterprise',
    'entertainment': 'Entertainment',
    'environmental': 'Environmental',
    'executive': 'Executive',
    'factory-worker': 'Factory',
    'farmer': 'Farmer',
    'finance': 'Finance',
    'freelancer': 'Freelancer',
    'government': 'Government',
    'healthcare': 'Healthcare',
    'hospitality': 'Hospitality',
    'hr': 'HR',
    'international': 'International',
    'it-support': 'IT Support',
    'legal': 'Legal',
    'logistics': 'Logistics',
    'manufacturing': 'Manufacturing',
    'marketing': 'Marketing',
    'materials': 'Materials',
    'media': 'Media',
    'medical': 'Medical',
    'mining': 'Mining',
    'product': 'Product',
    'public-service': 'Public Service',
    'quantum': 'Quantum',
    'realestate': 'Real Estate',
    'repair-worker': 'Repair Worker',
    'research': 'Research',
    'retail': 'Retail',
    'robotics': 'Robotics',
    'sales': 'Sales',
    'science': 'Science',
    'semiconductor': 'Semiconductor',
    'service-worker': 'Service Worker',
    'social': 'Social',
    'sports': 'Sports',
    'technology': 'Technology',
    'telecom': 'Telecom',
    'tools': 'Tools',
    'transport-worker': 'Transport Worker',
    'transportation': 'Transportation',
}


def extract_categories_from_directories():
    """Extract categories from skills directory structure"""
    if not SKILLS_DIR.exists():
        print(f"Error: {SKILLS_DIR} not found")
        return []
    
    # Get all subdirectories (categories)
    categories = []
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('_') and not item.name.startswith('.'):
            # Count skills in this directory
            skill_count = len(list(item.glob('*/SKILL.md')))
            categories.append((item.name, skill_count))
    
    # Sort by skill count (descending)
    categories.sort(key=lambda x: x[1], reverse=True)
    
    return categories


def generate_filter_buttons(categories):
    """Generate HTML for filter buttons"""
    buttons = ['<button class="filter-btn active" data-category="all" onclick="filterByCategory(\'all\')">All</button>']
    
    for category, count in categories:
        display_name = CATEGORY_NAMES.get(category, category.replace('-', ' ').title())
        buttons.append(
            f'<button class="filter-btn" data-category="{category}" onclick="filterByCategory(\'{category}\')">{display_name}</button>'
        )
    
    return '\n            '.join(buttons)


def update_index_html():
    """Update category filters in index.html"""
    print("🔍 Extracting categories from directory structure...")
    categories = extract_categories_from_directories()
    
    if not categories:
        print("❌ No categories found")
        return False
    
    print(f"✅ Found {len(categories)} categories from directory structure")
    print(f"\nTop 10 categories:")
    for cat, count in categories[:10]:
        print(f"  - {cat}: {count} skills")
    
    # Generate new filter buttons HTML
    new_filters = generate_filter_buttons(categories)
    
    # Read index.html
    with open(INDEX_FILE) as f:
        content = f.read()
    
    # Find and replace category filters section
    pattern = r'(<div class="category-filters" id="categoryFilters">)[\s\S]*?(</div>)'
    
    replacement = f'''<div class="category-filters" id="categoryFilters">
            {new_filters}
        </div>'''
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print("\n⚠️  No changes made (pattern not found)")
        return False
    
    # Write back
    with open(INDEX_FILE, 'w') as f:
        f.write(new_content)
    
    print(f"\n✅ Updated {INDEX_FILE} with {len(categories)} category filters")
    return True


def main():
    if update_index_html():
        print("\n🎉 Category filters updated successfully!")
        return 0
    else:
        print("\n❌ Failed to update category filters")
        return 1


if __name__ == '__main__':
    exit(main())
