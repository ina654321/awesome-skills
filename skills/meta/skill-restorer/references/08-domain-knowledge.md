# § 4 · Domain Knowledge - Full Details

## skill-writer v5 Specification

### 6-Dimension Quality Rubric

| Dimension | Weight | Requirements |
|-----------|--------|--------------|
| System Prompt | 20% | §1.1, §1.2, §1.3 |
| Domain Knowledge | 20% | Specific data, methodologies |
| Workflow | 20% | 4-5 phases, Done/Fail |
| Error Handling | 15% | Anti-patterns, risk matrix |
| Examples | 15% | 5+ detailed scenarios |
| Metadata | 10% | Complete YAML |

### Quality Thresholds

- Production: ≥ 7.0
- Certified: ≥ 8.5
- Exemplary: ≥ 9.5

## skill-evaluator v2.1

### Dual-Track Assessment

**Text Quality (50%)**:
- System Prompt
- Domain Knowledge
- Workflow
- Error Handling
- Examples
- Metadata

**Runtime Quality (50%)**:
- Role Immersion
- Framework Execution
- Output Actionability
- Knowledge Accuracy
- Long-Conversation Stability
- Resilience

### Certification Requirements

- Text Score ≥ 8.0
- Runtime Score ≥ 8.0
- Variance < 1.0
- All dimensions ≥ 6.0

## Progressive Disclosure Standard

**Token Efficiency**:
- SKILL.md: < 350 lines
- references/: 3000+ lines
- Ratio: 1:10

**Benefits**:
- 10x faster initial load
- Details on demand
- Better user experience
- Lower token costs
