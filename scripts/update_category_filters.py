#!/usr/bin/env python3
"""
Update category filters in index.html based on actual skills data

Usage:
    python scripts/update_category_filters.py
"""

import re
import json
from pathlib import Path
from collections import Counter

SKILLS_DATA_FILE = Path('assets/js/skills-data.js')
INDEX_FILE = Path('index.html')

# Category display names mapping
CATEGORY_NAMES = {
    'executive': 'Executive',
    'software': 'Software',
    'technology': 'Technology',
    'ai-ml': 'AI/ML',
    'healthcare': 'Healthcare',
    'legal': 'Legal',
    'education': 'Education',
    'finance': 'Finance',
    'creative': 'Creative',
    'research': 'Research',
    'business': 'Business',
    'marketing': 'Marketing',
    'product': 'Product',
    'automotive': 'Automotive',
    'data': 'Data',
    'construction': 'Construction',
    'manufacturing': 'Manufacturing',
    'energy': 'Energy',
    'aerospace': 'Aerospace',
    'agriculture': 'Agriculture',
    'biotech': 'Biotech',
    'cybersecurity': 'Security',
    'blockchain': 'Blockchain',
    'robotics': 'Robotics',
    'quantum': 'Quantum',
    'entertainment': 'Entertainment',
    'media': 'Media',
    'sports': 'Sports',
    'transportation': 'Transport',
    'hospitality': 'Hospitality',
    'retail': 'Retail',
    'real-estate': 'Real Estate',
    'government': 'Government',
    'public-service': 'Public Service',
    'military': 'Military',
    'nonprofit': 'Nonprofit',
    'consulting': 'Consulting',
    'hr': 'HR',
    'operations': 'Operations',
    'sales': 'Sales',
    'customer-service': 'Customer Service',
    'admin': 'Admin',
    'facilities': 'Facilities',
    'environmental': 'Environmental',
    'safety': 'Safety',
    'quality': 'Quality',
    'supply-chain': 'Supply Chain',
    'logistics': 'Logistics',
    'procurement': 'Procurement',
    'events': 'Events',
    'writing': 'Writing',
    'translation': 'Translation',
    'interpreting': 'Interpreting',
    'teaching': 'Teaching',
    'coaching': 'Coaching',
    'therapy': 'Therapy',
    'social-work': 'Social Work',
    'library': 'Library',
    'museum': 'Museum',
    'archaeology': 'Archaeology',
    'architecture': 'Architecture',
    'interior-design': 'Interior Design',
    'fashion': 'Fashion',
    'culinary': 'Culinary',
    'baking': 'Baking',
    'bartending': 'Bartending',
    'agriculture': 'Agriculture',
    'fishing': 'Fishing',
    'forestry': 'Forestry',
    'gardening': 'Gardening',
    'animal-care': 'Animal Care',
    'pet-care': 'Pet Care',
    'veterinary': 'Veterinary',
    'zoology': 'Zoology',
    'marine-biology': 'Marine Biology',
    'conservation': 'Conservation',
    'wildlife': 'Wildlife',
    'fisheries': 'Fisheries',
    'aquaculture': 'Aquaculture',
    'mining': 'Mining',
    'metallurgy': 'Metallurgy',
    'materials': 'Materials',
    'ceramics': 'Ceramics',
    'textiles': 'Textiles',
    'paper': 'Paper',
    'printing': 'Printing',
    'packaging': 'Packaging',
    'shipping': 'Shipping',
    'freight': 'Freight',
    'warehousing': 'Warehousing',
    'distribution': 'Distribution',
    'fulfillment': 'Fulfillment',
    'order-management': 'Order Mgmt',
    'inventory': 'Inventory',
    'purchasing': 'Purchasing',
    'sourcing': 'Sourcing',
    'vendor-management': 'Vendor Mgmt',
    'contract-management': 'Contract Mgmt',
    'project-management': 'Project Mgmt',
    'program-management': 'Program Mgmt',
    'portfolio-management': 'Portfolio Mgmt',
    'change-management': 'Change Mgmt',
    'risk-management': 'Risk Mgmt',
    'compliance': 'Compliance',
    'governance': 'Governance',
    'audit': 'Audit',
    'forensics': 'Forensics',
    'investigation': 'Investigation',
    'intelligence': 'Intelligence',
    'innovation': 'Innovation',
    'design': 'Design',
    'engineering': 'Engineering',
    'planning': 'Planning',
    'scheduling': 'Scheduling',
    'estimating': 'Estimating',
    'surveying': 'Surveying',
    'mapping': 'Mapping',
    'gis': 'GIS',
    'remote-sensing': 'Remote Sensing',
    'photogrammetry': 'Photogrammetry',
    'cartography': 'Cartography',
    'meteorology': 'Meteorology',
    'climatology': 'Climatology',
    'oceanography': 'Oceanography',
    'hydrology': 'Hydrology',
    'geology': 'Geology',
    'seismology': 'Seismology',
    'volcanology': 'Volcanology',
    'paleontology': 'Paleontology',
    'anthropology': 'Anthropology',
    'archaeology': 'Archaeology',
    'history': 'History',
    'philosophy': 'Philosophy',
    'linguistics': 'Linguistics',
    'literature': 'Literature',
    'music': 'Music',
    'art': 'Art',
    'dance': 'Dance',
    'theater': 'Theater',
    'film': 'Film',
    'photography': 'Photography',
    'journalism': 'Journalism',
    'publishing': 'Publishing',
    'broadcasting': 'Broadcasting',
    'advertising': 'Advertising',
    'public-relations': 'PR',
    'branding': 'Branding',
    'market-research': 'Market Research',
    'consumer-insights': 'Consumer Insights',
    'product-research': 'Product Research',
    'usability': 'Usability',
    'accessibility': 'Accessibility',
    'inclusion': 'Inclusion',
    'diversity': 'Diversity',
    'equity': 'Equity',
    'sustainability': 'Sustainability',
    'csr': 'CSR',
    'ethics': 'Ethics',
    'regulatory': 'Regulatory',
    'policy': 'Policy',
    'advocacy': 'Advocacy',
    'lobbying': 'Lobbying',
    'diplomacy': 'Diplomacy',
    'international-relations': 'Intl Relations',
    'trade': 'Trade',
    'economics': 'Economics',
    'accounting': 'Accounting',
    'tax': 'Tax',
    'insurance': 'Insurance',
    'banking': 'Banking',
    'investment': 'Investment',
    'wealth-management': 'Wealth Mgmt',
    'financial-planning': 'Financial Planning',
    'credit': 'Credit',
    'lending': 'Lending',
    'mortgage': 'Mortgage',
    'property-management': 'Property Mgmt',
    'facilities-management': 'Facilities Mgmt',
    'construction-management': 'Construction Mgmt',
    'site-management': 'Site Mgmt',
    'safety-management': 'Safety Mgmt',
    'quality-management': 'Quality Mgmt',
    'process-improvement': 'Process Improvement',
    'lean': 'Lean',
    'six-sigma': 'Six Sigma',
    'agile': 'Agile',
    'scrum': 'Scrum',
    'kanban': 'Kanban',
    'devops': 'DevOps',
    'sre': 'SRE',
    'platform-engineering': 'Platform Eng',
    'infrastructure': 'Infrastructure',
    'networking': 'Networking',
    'telecom': 'Telecom',
    'wireless': 'Wireless',
    'satellite': 'Satellite',
    'broadcast': 'Broadcast',
    'cable': 'Cable',
    'isp': 'ISP',
    'datacenter': 'Datacenter',
    'cloud': 'Cloud',
    'edge': 'Edge',
    'cdn': 'CDN',
    'hosting': 'Hosting',
    'colocation': 'Colocation',
    'managed-services': 'Managed Services',
    'outsourcing': 'Outsourcing',
    'professional-services': 'Professional Svcs',
    'staffing': 'Staffing',
    'recruiting': 'Recruiting',
    'payroll': 'Payroll',
    'benefits': 'Benefits',
    'compensation': 'Compensation',
    'performance': 'Performance',
    'learning': 'Learning',
    'development': 'Development',
    'training': 'Training',
    'elearning': 'E-Learning',
    'instructional-design': 'Instructional Design',
    'curriculum': 'Curriculum',
    'assessment': 'Assessment',
    'evaluation': 'Evaluation',
    'accreditation': 'Accreditation',
    'certification': 'Certification',
    'licensing': 'Licensing',
    'permitting': 'Permitting',
    'inspection': 'Inspection',
    'testing': 'Testing',
    'calibration': 'Calibration',
    'metrology': 'Metrology',
    'standardization': 'Standardization',
    'normalization': 'Normalization',
    'benchmarking': 'Benchmarking',
    'best-practices': 'Best Practices',
    'knowledge-management': 'Knowledge Mgmt',
    'information-management': 'Info Mgmt',
    'records-management': 'Records Mgmt',
    'archiving': 'Archiving',
    'digitization': 'Digitization',
    'preservation': 'Preservation',
    'restoration': 'Restoration',
    'maintenance': 'Maintenance',
    'repair': 'Repair',
    'overhaul': 'Overhaul',
    'refurbishment': 'Refurbishment',
    'remanufacturing': 'Remanufacturing',
    'recycling': 'Recycling',
    'waste-management': 'Waste Mgmt',
    'disposal': 'Disposal',
    'remediation': 'Remediation',
    'decommissioning': 'Decommissioning',
    'demolition': 'Demolition',
    'abatement': 'Abatement',
    'mitigation': 'Mitigation',
    'adaptation': 'Adaptation',
    'resilience': 'Resilience',
    'preparedness': 'Preparedness',
    'response': 'Response',
    'recovery': 'Recovery',
    'continuity': 'Continuity',
    'contingency': 'Contingency',
    'emergency': 'Emergency',
    'crisis': 'Crisis',
    'disaster': 'Disaster',
    'business-continuity': 'Business Continuity',
    'it-service-management': 'ITSM',
    'it-asset-management': 'IT Asset Mgmt',
    'software-asset-management': 'SAM',
    'hardware-asset-management': 'HAM',
    'configuration-management': 'Config Mgmt',
    'change-management': 'Change Mgmt',
    'release-management': 'Release Mgmt',
    'deployment-management': 'Deploy Mgmt',
    'service-desk': 'Service Desk',
    'incident-management': 'Incident Mgmt',
    'problem-management': 'Problem Mgmt',
    'event-management': 'Event Mgmt',
    'availability-management': 'Availability Mgmt',
    'capacity-management': 'Capacity Mgmt',
    'performance-management': 'Performance Mgmt',
    'service-level-management': 'SLM',
    'vendor-management': 'Vendor Mgmt',
    'supplier-management': 'Supplier Mgmt',
    'contract-management': 'Contract Mgmt',
    'procurement': 'Procurement',
    'logistics': 'Logistics',
    'transportation': 'Transportation',
    'fulfillment': 'Fulfillment',
    'inventory-management': 'Inventory Mgmt',
    'demand-planning': 'Demand Planning',
    'supply-planning': 'Supply Planning',
    'production-planning': 'Production Planning',
    'master-scheduling': 'Master Scheduling',
    'material-requirements': 'MRP',
    'capacity-requirements': 'CRP',
    'shop-floor-control': 'Shop Floor Control',
    'quality-control': 'QC',
    'quality-assurance': 'QA',
    'factory-worker': 'Factory',
    'special': 'Special',
    'tools': 'Tools',
    'crafts': 'Crafts',
    'transport-worker': 'Transport Worker',
    'construction-worker': 'Construction Worker',
    'repair-worker': 'Repair Worker',
    'service-worker': 'Service Worker',
    'it-support': 'IT Support',
    'freelancer': 'Freelancer',
    'international': 'International',
    'semiconductor': 'Semiconductor',
    'quantum': 'Quantum',
    'mining': 'Mining',
    'materials': 'Materials',
}


def extract_categories_from_skills():
    """Extract unique categories from skills-data.js"""
    if not SKILLS_DATA_FILE.exists():
        print(f"Error: {SKILLS_DATA_FILE} not found")
        return []
    
    # Read and parse skills data
    content = SKILLS_DATA_FILE.read_text()
    json_start = content.find('[')
    json_end = content.rfind(']') + 1
    skills = json.loads(content[json_start:json_end])
    
    # Count skills per category
    categories = Counter(s['category'] for s in skills)
    
    # Sort by count (descending) and get unique categories
    sorted_categories = categories.most_common()
    
    return sorted_categories


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
    print("🔍 Extracting categories from skills data...")
    categories = extract_categories_from_skills()
    
    if not categories:
        print("❌ No categories found")
        return False
    
    print(f"✅ Found {len(categories)} categories")
    print(f"\nTop 10 categories:")
    for cat, count in categories[:10]:
        print(f"  - {cat}: {count} skills")
    
    # Generate new filter buttons HTML
    new_filters = generate_filter_buttons(categories)
    
    # Read index.html
    with open(INDEX_FILE) as f:
        content = f.read()
    
    # Find and replace category filters section
    pattern = r'(<div class="category-filters" id="categoryFilters">)\n.*?(</div>)'
    
    replacement = f'''$1
            {new_filters}
        $2'''
    
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
