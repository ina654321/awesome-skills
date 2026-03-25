#!/usr/bin/env bash
# optimize.sh — Description trigger rate optimization
# Usage: ./optimize.sh path/to/SKILL.md
# Iteratively improves description trigger rate using evals-driven methodology.

set -euo pipefail

SKILL_FILE="${1:-}"

if [[ -z "$SKILL_FILE" || ! -f "$SKILL_FILE" ]]; then
  echo "Usage: $0 path/to/SKILL.md"
  echo ""
  echo "Description trigger rate optimization using evals-driven methodology."
  exit 1
fi

SKILL_DIR=$(dirname "$SKILL_FILE")
SKILL_NAME=$(basename "$SKILL_DIR")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DESCRIPTION OPTIMIZATION"
echo "  Skill: $SKILL_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo "This tool uses the 'pushy description' pattern from skill-creator:"
echo "  'Make descriptions a little bit pushy'"
echo ""

CURRENT_DESC=$(grep -A5 "^description:" "$SKILL_FILE" | head -6)
echo "Current description:"
echo "$CURRENT_DESC"
echo ""

read -rp "Continue with trigger rate testing? [y/n] " CONT
[[ "${CONT:-y}" =~ ^[Nn] ]] && exit 0

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  TRIGGER RATE TESTING"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Generate 20 eval queries (10 should trigger, 10 shouldn't)"
echo "Then test your description against each query."
echo ""

TOTAL=0
CORRECT=0
TRIGGERED=0

for i in {1..10}; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  read -rp "Positive $i - Query that SHOULD trigger: " QUERY
  read -rp "  Did it trigger? [y/n] " RESP
  
  TOTAL=$((TOTAL + 1))
  if [[ "$RESP" =~ ^[Yy] ]]; then
    TRIGGERED=$((TRIGGERED + 1))
    CORRECT=$((CORRECT + 1))
    echo -e "  ${GREEN}✓${NC}"
  else
    echo -e "  ${RED}✗${NC}"
  fi
done

for i in {1..10}; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  read -rp "Negative $i - Query that should NOT trigger: " QUERY
  read -rp "  Did it trigger? [y/n] " RESP
  
  TOTAL=$((TOTAL + 1))
  if [[ "$RESP" =~ ^[Nn] ]]; then
    CORRECT=$((CORRECT + 1))
    echo -e "  ${GREEN}✓${NC}"
  else
    TRIGGERED=$((TRIGGERED + 1))
    echo -e "  ${RED}✗ Triggered (false positive)${NC}"
  fi
done

TRIGGER_RATE=$(echo "scale=2; $CORRECT / $TOTAL * 100" | bc)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Trigger Rate: ${TRIGGER_RATE}%"
echo ""

if (( $(echo "$TRIGGER_RATE >= 90" | bc -l) )); then
  echo -e "  ${GREEN}EXCELLENT — ≥90% trigger rate${NC}"
elif (( $(echo "$TRIGGER_RATE >= 70" | bc -l) ]]; then
  echo -e "  ${YELLOW}GOOD — 70-89% trigger rate${NC}"
  echo ""
  echo "  Tips to improve:"
  echo "  - Make description more 'pushy'"
  echo "  - Add more explicit trigger phrases"
  echo "  - Use 'Use when:' pattern"
else
  echo -e "  ${RED}NEEDS WORK — <70% trigger rate${NC}"
  echo ""
  echo "  Recommendations:"
  echo "  1. Start with verb: 'Create', 'Evaluate', 'Restore'"
  echo "  2. Add 'Use when:' section with trigger phrases"
  echo "  3. Be specific: 'create skill' not just 'create'"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
