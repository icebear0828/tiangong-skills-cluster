---
name: resurrection-evaluator
description: >
  复活评审器 Skill。评估被淘汰方案是否应该复活。当 Round 3 对抗评审发现当前领先方案
  存在 Critical 缺陷时触发。重新评估被淘汰方案的相对优势，决定是否复活。
  作为扩展评审 Skill，具有标准契约。
---

# Resurrection Evaluator — 复活评审器

## 触发条件

- Round 3 发现当前第一名存在 Critical 缺陷
- 由 multi-round-eval-orchestrator 调度
- 需要重新考虑被淘汰方案时

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["eliminated_candidates", "new_critical_defects", "current_survivors"],
  "properties": {
    "eliminated_candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "elimination_round", "elimination_reason"],
        "properties": {
          "name": { "type": "string" },
          "path": { "type": "string" },
          "elimination_round": { "type": "string" },
          "elimination_reason": { "type": "string" },
          "original_defects": {
            "type": "array",
            "items": { "type": "object" }
          },
          "original_score": { "type": "number" }
        }
      },
      "description": "被淘汰方案列表"
    },
    "new_critical_defects": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "affected_candidate": { "type": "string" },
          "defect": { "type": "object" },
          "severity": { "type": "string" }
        }
      },
      "description": "新发现的 Critical 缺陷"
    },
    "current_survivors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "current_rank": { "type": "integer" },
          "current_score": { "type": "number" },
          "known_defects": { "type": "array" }
        }
      },
      "description": "当前存活方案"
    },
    "resurrection_criteria": {
      "type": "object",
      "properties": {
        "require_defect_coverage": {
          "type": "boolean",
          "default": true,
          "description": "是否要求新缺陷覆盖原淘汰原因"
        },
        "min_relative_advantage": {
          "type": "number",
          "default": 0.5,
          "description": "相对优势最低分数"
        }
      },
      "description": "复活标准配置"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["resurrection_decisions", "summary"],
  "properties": {
    "resurrection_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["candidate", "decision", "confidence"],
        "properties": {
          "candidate": { "type": "string" },
          "decision": {
            "type": "string",
            "enum": ["resurrect", "stay_eliminated", "needs_review"]
          },
          "confidence": {
            "type": "string",
            "enum": ["High", "Medium", "Low"]
          },
          "reasoning": { "type": "string" },
          "defect_coverage_analysis": {
            "type": "object",
            "properties": {
              "original_defects_still_valid": { "type": "boolean" },
              "covered_by_new_findings": { "type": "boolean" },
              "relative_severity": { "type": "string" }
            }
          },
          "comparative_analysis": {
            "type": "object",
            "properties": {
              "vs_current_first": {
                "type": "object",
                "properties": {
                  "advantages": { "type": "array", "items": { "type": "string" } },
                  "disadvantages": { "type": "array", "items": { "type": "string" } },
                  "net_score": { "type": "number" }
                }
              }
            }
          }
        }
      },
      "description": "各被淘汰方案的复活决定"
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_evaluated": { "type": "integer" },
        "resurrected_count": { "type": "integer" },
        "resurrected_list": { "type": "array", "items": { "type": "string" } },
        "impact_on_ranking": { "type": "string" }
      },
      "description": "复活评审摘要"
    }
  }
}
```

## 复活条件

方案被复活需满足以下条件之一：

### 条件 A: 缺陷覆盖
- 原淘汰原因已被新发现的 Critical 缺陷覆盖
- 即：当前领先方案有更严重的同类问题

### 条件 B: 相对优势
- 重新评估后，与当前领先方案相比有显著优势
- 优势分数 ≥ 阈值

### 条件 C: 新视角
- 新发现改变了评审维度的权重
- 导致原排名失效

## 执行流程

1. **收集上下文**
   - 获取被淘汰方案原因
   - 获取新发现的 Critical 缺陷
   - 获取当前存活方案状态

2. **缺陷覆盖分析**
   - 比较原淘汰原因与新缺陷
   - 判断是否有覆盖关系
   - 评估相对严重度

3. **相对优势评估**
   - 重新评估被淘汰方案
   - 与当前领先方案对比
   - 计算净优势分数

4. **复活决策**
   - 综合各项分析
   - 做出复活/维持决定
   - 评估决策置信度

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 评估所有被淘汰方案 | 100% |
| 公正性 | 使用相同标准评估 | 100% |
| 透明度 | 理由可追溯 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| devils-advocate | 接收其 Critical 缺陷发现 |
| defect-analyzer | 复用其缺陷分析框架 |
| consensus-builder | 输出参与最终共识 |
| multi-round-eval-orchestrator | 由其调度 |

## 脚本

- `scripts/evaluate_resurrection.py` - 复活评估主脚本
- `scripts/defect_coverage.py` - 缺陷覆盖分析
- `scripts/comparative_analysis.py` - 相对优势评估

## 参考资料

- `references/resurrection-criteria.md` - 复活标准详解
- `references/defect-severity-comparison.md` - 缺陷严重度对比规则
