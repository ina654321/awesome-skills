# Skill-Manager 稳定性改进方案

**生成时间**: 2026-03-26  
**分析模型**: minimax-cn-coding-plan/MiniMax-M2.7-highspeed  
**版本**: v1.0

---

## 1. 不稳定性根因分析

### 1.1 触发词匹配不一致

| 脚本 | 正则模式 | 问题 |
|------|----------|------|
| `score.sh` (L38-48) | `§1\.1\|1\.1 Identity\|## 1\.1\|### Identity` | 多重模式，部分重叠 |
| `score-v2.sh` (L41-43) | `§1\.1\|Identity` | 过于宽泛，可能误匹配 |
| `score-llm.sh` (L49-52) | `§ 1\b\|## §` | 空格敏感，匹配不稳定 |

**根因**: 同一文件使用不同正则模式导致评分差异

### 1.2 多轮对话上下文不稳定

`tune.sh` (L42-48):
```bash
IMP_TYPES=("add §1.1" "add §1.2" "add §1.3" "add benchmark" ...)
IMP_TYPE="${IMP_TYPES[$((RANDOM % ${#IMP_TYPES[@]}))]}"
```

**根因**: 使用 `RANDOM` 随机选择改进方向，同一起点产生不同路径

### 1.3 权重体系不一致

| 维度 | score.sh | score-v2.sh |
|------|----------|-------------|
| System Prompt | 20% | 15% |
| Domain Knowledge | 20% | 20% |
| Workflow | 20% | 20% |
| Error Handling | 15% | - (替换为 Consistency 15%) |
| Consistency | - | 15% |
| Executability | - | 15% |
| Recency | - | 10% |
| Examples | 15% | - (与 Executability 合并) |
| Metadata | 10% | 15% |

**根因**: 不同评分脚本对同一文件给出不同总分

### 1.4 辅助脚本依赖缺失

- `tune.sh` 调用 `score.sh` 但未校验 `SCORE_SCRIPT` 路径
- 所有脚本假设 `bc` 命令可用，但未检查
- LLM 相关脚本依赖 API key 但错误处理不一致

---

## 2. 确定性改进方案

### 2.1 统一触发词正则引擎

创建 `/Users/lucas/.agents/skills/skill-manager/scripts/lib/trigger_patterns.sh`:

```bash
#!/usr/bin/env bash
# trigger_patterns.sh — 统一触发词匹配引擎
# 解决不同脚本正则不一致问题

set -euo pipefail

# 标准化模式库
declare -A PATTERNS=(
    ["IDENTITY_SECTIONS"]='§1\.1|1\.1 Identity|## 1\.1|### Identity|## § 1 · Identity'
    ["FRAMEWORK_SECTIONS"]='§1\.2|1\.2 Framework|## 1\.2|### Framework|## § 2 ·'
    ["THINKING_SECTIONS"]='§1\.3|1\.3 Thinking|## 1\.3|### Thinking|## § 3 ·'
    ["SYSTEM_PROMPT"]='system prompt|§ 1\b|## §'
    ["WORKFLOW"]='workflow|## Workflow|## Phase|Step [0-9]'
    ["DONE_CRITERIA"]='done\.criteria|done:|✅'
    ["FAIL_CRITERIA"]='fail\.criteria|fail:|❌'
    ["ERROR_HANDLING"]='error\.handling|edge case|anti\.pattern|risk|failure|recovery'
    ["EXAMPLES"]='^## .*[Ee]xample|^### .*[Ee]xample'
    ["METADATA"]='^name:|^description:|^license:|^version:|^metadata:'
)

# 统一计数函数
count_matches() {
    local pattern="$1"
    local file="$2"
    grep -cE "$pattern" "$file" 2>/dev/null || echo "0"
}

# 布尔检查函数
has_pattern() {
    local pattern="$1"
    local file="$2"
    local threshold="${3:-1}"
    local count
    count=$(count_matches "$pattern" "$file")
    [[ $count -ge $threshold ]]
}

# 稳定性验证
validate_trigger_consistency() {
    local file="$1"
    local results=()
    
    for script in score.sh score-v2.sh score-llm.sh; do
        script_path="$(dirname "$0")/../scripts/$script"
        if [[ -f "$script_path" ]]; then
            local sp_count
            sp_count=$(grep -ciE "${PATTERNS[SYSTEM_PROMPT]}" "$file" || true)
            results+=("$script:SP=$sp_count")
        fi
    done
    
    printf '%s\n' "${results[@]}"
}
```

### 2.2 确定性改进选择器

替换 `tune.sh` 中的随机选择逻辑:

```bash
# 改进选择器 - 确定性版本
SELECTION_STRATEGY="${SELECTION_STRATEGY:-priority_based}"

get_next_improvement() {
    local skill_file="$1"
    local round="$2"
    local last_imp="${3:-}"
    
    # 分析当前薄弱维度
    local current_score output
    current_score=$(bash "$(dirname "$0")/score.sh" "$skill_file" 2>/dev/null | grep "Text Score" | awk '{print $4}')
    output=$(bash "$(dirname "$0")/score.sh" "$skill_file")
    
    # 检测最低分维度
    local lowest_dim
    lowest_dim=$(echo "$output" | grep -E "^[A-Za-z]" | sort -t'/' -k1 -n | head -1 | awk '{print $1}')
    
    # 确定性选择: 总是选择影响最低维度的改进
    case "$lowest_dim" in
        "System Prompt")
            if ! grep -qE "${PATTERNS[IDENTITY_SECTIONS]}" "$skill_file"; then
                echo "add §1.1 Identity section"
            elif ! grep -qE "${PATTERNS[FRAMEWORK_SECTIONS]}" "$skill_file"; then
                echo "add §1.2 Framework section"
            elif ! grep -qE "${PATTERNS[THINKING_SECTIONS]}" "$skill_file"; then
                echo "add §1.3 Thinking section"
            else
                echo "add constraints to System Prompt"
            fi
            ;;
        "Domain Knowledge")
            if ! grep -qE "[0-9]+%|[0-9]+\.[0-9]+" "$skill_file"; then
                echo "add specific quantitative data"
            elif ! grep -qE "McKinsey|TOGAF|ISO |NIST|OWASP" "$skill_file"; then
                echo "add framework references"
            else
                echo "add case studies or benchmarks"
            fi
            ;;
        "Workflow")
            if ! grep -qE "Phase [1-9]|Step [1-9]" "$skill_file"; then
                echo "add workflow phases"
            elif ! grep -qE "${PATTERNS[DONE_CRITERIA]}" "$skill_file"; then
                echo "add Done criteria"
            elif ! grep -qE "${PATTERNS[FAIL_CRITERIA]}" "$skill_file"; then
                echo "add Fail criteria"
            else
                echo "add decision tree to workflow"
            fi
            ;;
        "Error Handling")
            if ! grep -qE "anti.pattern|anti-pattern" "$skill_file"; then
                echo "add anti-patterns section"
            elif ! grep -qE "retry|fallback|circuit.breaker" "$skill_file"; then
                echo "add recovery strategies"
            else
                echo "add edge case scenarios"
            fi
            ;;
        "Examples")
            local ex_count
            ex_count=$(grep -cE "^## .*[Ee]xample|^### .*[Ee]xample" "$skill_file" || true)
            if [[ $ex_count -lt 3 ]]; then
                echo "expand examples to 3+ detailed scenarios"
            elif [[ $ex_count -lt 5 ]]; then
                echo "expand examples to 5+ scenarios with input/output"
            else
                echo "add edge case examples"
            fi
            ;;
        "Metadata")
            echo "add missing metadata fields"
            ;;
        *)
            echo "add §1.1 Identity section"
            ;;
    esac
}
```

### 2.3 统一权重体系

创建 `/Users/lucas/.agents/skills/skill-manager/scripts/lib/weights.sh`:

```bash
#!/usr/bin/env bash
# weights.sh — 统一权重体系

set -euo pipefail

# 标准化权重定义
declare -A DIMENSION_WEIGHTS=(
    ["System Prompt"]=20
    ["Domain Knowledge"]=20
    ["Workflow"]=20
    ["Error Handling"]=15
    ["Examples"]=15
    ["Metadata"]=10
)

# V2 权重
declare -A DIMENSION_WEIGHTS_V2=(
    ["System Prompt"]=15
    ["Domain Knowledge"]=20
    ["Workflow"]=20
    ["Consistency"]=15
    ["Executability"]=15
    ["Metadata"]=15
)

# 验证权重总和
validate_weights() {
    local total=0
    for weight in "${DIMENSION_WEIGHTS[@]}"; do
        total=$((total + weight))
    done
    [[ $total -eq 100 ]]
}

# 验证分数一致性
validate_score_consistency() {
    local skill_file="$1"
    
    local score_v1 score_v2
    score_v1=$(bash "$(dirname "$0")/score.sh" "$skill_file" 2>/dev/null | grep "Text Score" | awk '{print $4}')
    score_v2=$(bash "$(dirname "$0")/score-v2.sh" "$skill_file" 2>/dev/null | grep "TOTAL SCORE" | awk '{print $3}')
    
    local diff
    diff=$(python3 -c "print(abs(float('$score_v1') - float('$score_v2')))")
    
    if (( $(echo "$diff > 1.5" | bc -l) )); then
        echo "INSTABILITY_DETECTED: v1=$score_v1 v2=$score_v2 diff=$diff"
        return 1
    else
        echo "STABLE: v1=$score_v1 v2=$score_v2 diff=$diff"
        return 0
    fi
}
```

### 2.4 稳定性检测机制

创建 `/Users/lucas/.agents/skills/skill-manager/scripts/stability-check.sh`:

```bash
#!/usr/bin/env bash
# stability-check.sh — 稳定性检测机制

set -euo pipefail

SKILL_FILE="${1:-}"

if [[ -z "$SKILL_FILE" || ! -f "$SKILL_FILE" ]]; then
    echo "Usage: $0 path/to/SKILL.md"
    exit 1
fi

SCRIPT_DIR="$(dirname "$0")"
LIB_DIR="$SCRIPT_DIR/lib"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STABILITY CHECK"
echo "  $(basename "$SKILL_FILE")"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

STABILITY_ISSUES=()
STABILITY_SCORE=10

# CHECK 1: 触发词匹配一致性
echo "【Check 1/4】 Trigger Word Consistency"
declare -A sp_counts
for script in "score.sh" "score-v2.sh" "score-llm.sh"; do
    case "$script" in
        "score.sh")
            sp_counts[$script]=$(grep -ciE 'system prompt|§ 1\b|## §' "$SKILL_FILE" || true)
            ;;
        "score-v2.sh")
            sp_counts[$script]=$(grep -ciE 'system prompt|## §|§ [0-9]' "$SKILL_FILE" || true)
            ;;
        "score-llm.sh")
            sp_counts[$script]=$(grep -ciE 'system prompt|§ 1\b|## §' "$SKILL_FILE" || true)
            ;;
    esac
done

max_count=0
min_count=999
for count in "${sp_counts[@]}"; do
    [[ $count -gt $max_count ]] && max_count=$count
    [[ $count -lt $min_count ]] && min_count=$count
done

count_diff=$((max_count - min_count))
if [[ $count_diff -gt 2 ]]; then
    STABILITY_ISSUES+=("TRIGGER_INCONSISTENCY: max=$max_count min=$min_count diff=$count_diff")
    STABILITY_SCORE=$((STABILITY_SCORE - 2))
    echo "  ❌ Inconsistent trigger matches (diff=$count_diff)"
else
    echo "  ✅ Consistent trigger matches (diff=$count_diff)"
fi

# CHECK 2: 评分一致性
echo ""
echo "【Check 2/4】 Scoring Consistency"
score_sh=$(bash "$SCRIPT_DIR/score.sh" "$SKILL_FILE" 2>/dev/null | grep "Text Score" | awk '{print $4}' || echo "N/A")
score_v2=$(bash "$SCRIPT_DIR/score-v2.sh" "$SKILL_FILE" 2>/dev/null | grep "TOTAL SCORE" | awk '{print $3}' || echo "N/A")

if [[ "$score_sh" != "N/A" && "$score_v2" != "N/A" ]]; then
    diff=$(python3 -c "print(abs(float('$score_sh') - float('$score_v2')))")
    
    if (( $(echo "$diff > 1.5" | bc -l) )); then
        STABILITY_ISSUES+=("SCORING_INCONSISTENCY: score.sh=$score_sh score-v2.sh=$score_v2 diff=$diff")
        STABILITY_SCORE=$((STABILITY_SCORE - 3))
        echo "  ❌ Score divergence detected (diff=$diff)"
    else
        echo "  ✅ Score consistent (diff=$diff)"
    fi
fi

# CHECK 3: 权重完整性
echo ""
echo "【Check 3/4】 Weight Integrity"
weights_v1_sum=$(python3 -c "print(sum([20, 20, 20, 15, 15, 10]))")
weights_v2_sum=$(python3 -c "print(sum([15, 20, 20, 15, 15, 15]))")
echo "  v1 weights sum: $weights_v1_sum"
echo "  v2 weights sum: $weights_v2_sum"

# CHECK 4: 幂等性测试
echo ""
echo "【Check 4/4】 Idempotency Test"
run1=$(bash "$SCRIPT_DIR/score.sh" "$SKILL_FILE" 2>/dev/null | grep "Text Score" | awk '{print $4}')
run2=$(bash "$SCRIPT_DIR/score.sh" "$SKILL_FILE" 2>/dev/null | grep "Text Score" | awk '{print $4}')
run3=$(bash "$SCRIPT_DIR/score.sh" "$SKILL_FILE" 2>/dev/null | grep "Text Score" | awk '{print $4}')

if [[ "$run1" == "$run2" && "$run2" == "$run3" ]]; then
    echo "  ✅ Idempotent (3 runs: $run1, $run2, $run3)"
else
    STABILITY_ISSUES+=("NON_IDEMPOTENT: run1=$run1 run2=$run2 run3=$run3")
    STABILITY_SCORE=$((STABILITY_SCORE - 2))
    echo "  ❌ Non-idempotent scoring detected"
fi

# 汇总
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STABILITY REPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Stability Score: ${STABILITY_SCORE}/10"

if [[ $STABILITY_SCORE -ge 9 ]]; then
    echo "  Status: ✅ STABLE"
elif [[ $STABILITY_SCORE -ge 7 ]]; then
    echo "  Status: ⚠️  MARGINALLY STABLE"
else
    echo "  Status: ❌ UNSTABLE"
fi

[[ ${#STABILITY_ISSUES[@]} -gt 0 ]] && echo "  Issues: ${STABILITY_ISSUES[*]}"

[[ $STABILITY_SCORE -ge 8 ]]
```

---

## 3. 改进后的代码片段

### 3.1 统一触发词匹配 (trigger_patterns.sh)

```bash
#!/usr/bin/env bash
# trigger_patterns.sh — 统一触发词匹配引擎
# 版本: 1.0.0

set -euo pipefail

declare -A PATTERNS=(
    ["IDENTITY"]='§1\.1|1\.1 Identity|## 1\.1|### Identity|## § 1 · Identity'
    ["FRAMEWORK"]='§1\.2|1\.2 Framework|## 1\.2|### Framework|## § 2 ·'
    ["THINKING"]='§1\.3|1\.3 Thinking|## 1\.3|### Thinking|## § 3 ·'
    ["SYSTEM_PROMPT"]='system prompt|§ 1\b|## §'
    ["WORKFLOW"]='workflow|## Workflow|## Phase|Step [0-9]'
    ["DONE"]='done\.criteria|done:|✅'
    ["FAIL"]='fail\.criteria|fail:|❌'
    ["ERROR"]='error\.handling|edge case|anti\.pattern|risk|failure|recovery'
    ["EXAMPLES"]='^## .*[Ee]xample|^### .*[Ee]xample'
    ["METADATA"]='^name:|^description:|^license:|^version:|^metadata:'
)

get_match_count() {
    local pattern="$1"
    local file="$2"
    grep -cE "$pattern" "$file" 2>/dev/null || echo "0"
}

has_pattern() {
    local pattern="$1"
    local file="$2"
    local threshold="${3:-1}"
    local count
    count=$(get_match_count "$pattern" "$file")
    [[ $count -ge $threshold ]]
}

diagnose_triggers() {
    local file="$1"
    echo "=== Trigger Diagnosis for: $file ==="
    for key in "${!PATTERNS[@]}"; do
        local count
        count=$(get_match_count "${PATTERNS[$key]}" "$file")
        printf "  %-20s: %s matches\n" "$key" "$count"
    done
}
```

### 3.2 确定性改进选择 (tune.sh 改进版)

```bash
#!/usr/bin/env bash
# tune.sh — 确定性版本

set -euo pipefail

SKILL_FILE="${1:-}"
ROUNDS="${2:-100}"
SELECTION_MODE="${SELECTION_MODE:-priority}"

select_improvement() {
    local skill_file="$1"
    local current_round="$2"
    local previous_imp="${3:-}"
    
    local score_output
    score_output=$(bash "$SCORE_SCRIPT" "$skill_file" 2>/dev/null)
    local current_score
    current_score=$(echo "$score_output" | grep "Text Score" | awk '{print $4}')
    
    local weakest_dim
    weakest_dim=$(echo "$score_output" | grep -E "^  [A-Za-z]" | \
        while read line; do
            echo "$line" | awk '{print $1}'
        done | \
        sort -t'/' -k1 -n | head -1)
    
    case "$weakest_dim" in
        "System")
            if ! has_pattern "${PATTERNS[IDENTITY]}" "$skill_file"; then
                echo "add §1.1 Identity section"
            elif ! has_pattern "${PATTERNS[FRAMEWORK]}" "$skill_file"; then
                echo "add §1.2 Framework section"
            elif ! has_pattern "${PATTERNS[THINKING]}" "$skill_file"; then
                echo "add §1.3 Thinking section"
            else
                echo "enhance System Prompt constraints"
            fi
            ;;
        "Domain")
            if ! has_pattern "[0-9]+%|F1|MRR|Accuracy" "$skill_file"; then
                echo "add quantitative benchmarks"
            elif ! has_pattern "McKinsey|TOGAF|ISO |NIST|OWASP" "$skill_file"; then
                echo "add framework references"
            else
                echo "add case studies"
            fi
            ;;
        "Workflow")
            if ! has_pattern "Phase [1-9]|Step [1-9]" "$skill_file"; then
                echo "add workflow phases"
            elif ! has_pattern "${PATTERNS[DONE]}" "$skill_file"; then
                echo "add Done criteria"
            elif ! has_pattern "${PATTERNS[FAIL]}" "$skill_file"; then
                echo "add Fail criteria"
            else
                echo "add decision tree"
            fi
            ;;
        "Error")
            if ! has_pattern "anti.pattern" "$skill_file"; then
                echo "add anti-patterns"
            elif ! has_pattern "retry|fallback|circuit.breaker" "$skill_file"; then
                echo "add recovery strategies"
            else
                echo "add edge cases"
            fi
            ;;
        "Examples")
            local ex_count
            ex_count=$(get_match_count "${PATTERNS[EXAMPLES]}" "$skill_file")
            if [[ $ex_count -lt 3 ]]; then
                echo "add examples (target: 3+)"
            elif [[ $ex_count -lt 5 ]]; then
                echo "expand to 5+ examples with I/O"
            else
                echo "add edge case examples"
            fi
            ;;
        "Metadata")
            echo "complete metadata fields"
            ;;
        *)
            echo "fix lowest scoring dimension"
            ;;
    esac
}
```

---

## 4. 实施建议

### 4.1 短期 (立即实施)

1. 创建 `lib` 目录: `/Users/lucas/.agents/skills/skill-manager/scripts/lib/`
2. 部署 `trigger_patterns.sh`: 统一所有脚本的模式引用
3. 创建 `stability-check.sh`: 添加稳定性检测

### 4.2 中期 (1 周内)

1. 重写 `tune.sh`: 使用确定性选择器替代随机
2. 统一权重: 确保 score.sh 和 score-v2.sh 权重总和都是 100%
3. 添加幂等性测试: 确保多次评分结果一致

### 4.3 长期 (持续改进)

1. 添加回归测试: 每次修改后运行稳定性检测
2. 版本锁定: score.sh 和 score-v2.sh 的维度权重应该版本锁定
3. 日志审计: 记录每次评分的所有中间值用于调试

---

## 5. 验证检查清单

- [ ] `trigger_patterns.sh` 已创建并被所有脚本引用
- [ ] `tune.sh` 使用确定性选择 (无 RANDOM)
- [ ] 权重总和 = 100% (v1 和 v2)
- [ ] 幂等性测试通过 (3 次连续运行结果一致)
- [ ] 稳定性得分 >= 8/10
- [ ] score.sh 和 score-v2.sh 对同一文件评分差异 < 1.5

---

**改进文件位置**: `/Users/lucas/.agents/skills/skill-manager/improvements/stability_fix.md`

**下一步**: 
1. 创建 `/Users/lucas/.agents/skills/skill-manager/scripts/lib/` 目录
2. 部署 `trigger_patterns.sh` 和 `weights.sh`
3. 更新 `tune.sh` 使用确定性选择器
4. 运行 `stability-check.sh` 验证改进效果
