#!/bin/bash
# Skill scaffolding script for skill-writer-v2
# Usage: ./init-skill.sh --tier={lite|standard|enterprise} --name={skill-name} [--category={category}]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Defaults
TIER=""
NAME=""
CATEGORY="general"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/../assets"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --tier)
      TIER="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --category)
      CATEGORY="$2"
      shift 2
      ;;
    --help)
      echo "Usage: $0 --tier={lite|standard|enterprise} --name={skill-name} [--category={category}]"
      echo ""
      echo "Options:"
      echo "  --tier      Skill complexity tier (lite, standard, enterprise)"
      echo "  --name      Skill name (kebab-case)"
      echo "  --category  Category folder (default: general)"
      echo "  --help      Show this help message"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Validation
if [[ -z "$TIER" ]]; then
  echo -e "${RED}Error: --tier is required${NC}"
  echo "Usage: $0 --tier={lite|standard|enterprise} --name={skill-name}"
  exit 1
fi

if [[ -z "$NAME" ]]; then
  echo -e "${RED}Error: --name is required${NC}"
  echo "Usage: $0 --tier={lite|standard|enterprise} --name={skill-name}"
  exit 1
fi

# Validate tier
if [[ "$TIER" != "lite" && "$TIER" != "standard" && "$TIER" != "enterprise" ]]; then
  echo -e "${RED}Error: tier must be 'lite', 'standard', or 'enterprise'${NC}"
  exit 1
fi

# Convert name to kebab-case if needed
NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Determine skill root directory
if [[ -d "$SCRIPT_DIR/../../../skills" ]]; then
  SKILL_ROOT="$SCRIPT_DIR/../../../skills"
elif [[ -d "$SCRIPT_DIR/../skills" ]]; then
  SKILL_ROOT="$SCRIPT_DIR/../skills"
else
  SKILL_ROOT="./skills"
fi

# Create directory structure
SKILL_DIR="$SKILL_ROOT/$CATEGORY/$NAME"
mkdir -p "$SKILL_DIR"

# Select template
TEMPLATE_FILE="$ASSETS_DIR/TEMPLATE-$TIER.md"
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}Error: Template not found: $TEMPLATE_FILE${NC}"
  exit 1
fi

# Copy and customize template
cp "$TEMPLATE_FILE" "$SKILL_DIR/SKILL.md"

# Replace placeholders
DISPLAY_NAME=$(echo "$NAME" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')
sed -i.bak "s/{skill-name}/$NAME/g" "$SKILL_DIR/SKILL.md"
sed -i.bak "s/{Display Name}/$DISPLAY_NAME/g" "$SKILL_DIR/SKILL.md"
sed -i.bak "s/{category}/$CATEGORY/g" "$SKILL_DIR/SKILL.md"
rm -f "$SKILL_DIR/SKILL.md.bak"

# Create optional directories based on tier
if [[ "$TIER" == "standard" || "$TIER" == "enterprise" ]]; then
  mkdir -p "$SKILL_DIR/references"
  mkdir -p "$SKILL_DIR/assets"
fi

if [[ "$TIER" == "lite" || "$TIER" == "standard" || "$TIER" == "enterprise" ]]; then
  mkdir -p "$SKILL_DIR/scripts"
fi

# Create .gitkeep files
touch "$SKILL_DIR/references/.gitkeep" 2>/dev/null || true
touch "$SKILL_DIR/assets/.gitkeep" 2>/dev/null || true
touch "$SKILL_DIR/scripts/.gitkeep" 2>/dev/null || true

# Output summary
echo -e "${GREEN}✓ Created $TIER skill: $NAME${NC}"
echo ""
echo "Location: $SKILL_DIR"
echo "Template: TEMPLATE-$TIER.md"
echo ""
echo "Directory structure:"
find "$SKILL_DIR" -type f -o -type d | head -20

echo ""
echo -e "${YELLOW}Next steps:${NC}"

case $TIER in
  lite)
    echo "  1. Edit SKILL.md (target: 50-150 lines, 30 min)"
    echo "  2. Add script to scripts/ if needed"
    echo "  3. Test with a real example"
    echo "  4. Ship it!"
    ;;
  standard)
    echo "  1. Edit SKILL.md (target: 150-400 lines, 2 hours)"
    echo "  2. Add detailed content to references/"
    echo "  3. Create 3+ usage scenarios"
    echo "  4. Document anti-patterns"
    ;;
  enterprise)
    echo "  1. Edit SKILL.md (target: 400-800 lines, 1 day)"
    echo "  2. Build three-layer architecture"
    echo "  3. Add case studies to references/"
    echo "  4. Create risk matrix"
    echo "  5. Define learning pathway"
    ;;
esac

echo ""
echo "Quality targets:"
case $TIER in
  lite)
    echo "  - Score: 5.0-6.5 (Community)"
    echo "  - Lines: 50-150"
    echo "  - Time: 30 minutes"
    ;;
  standard)
    echo "  - Score: 6.5-8.0 (Expert)"
    echo "  - Lines: 150-400"
    echo "  - Time: 2 hours"
    ;;
  enterprise)
    echo "  - Score: 8.0-9.5 (Expert/Exemplary)"
    echo "  - Lines: 400-800"
    echo "  - Time: 1 day"
    ;;
esac
