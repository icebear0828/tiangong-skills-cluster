---
name: ranking-synthesizer
description: >
  排名综合器 Skill。综合多个评审员的排名结果，生成统一排名和冲突分析。当需要：
  (1) 多评审员排名汇总，(2) 排名冲突检测，(3) 加权排名计算时触发。
  支持多种排名算法、冲突识别、权重配置。作为扩展评审 Skill，具有标准契约。
---

# Ranking Synthesizer — 排名综合器

## 触发条件

- Round 2 深度分析完成后
- 由 multi-round-eval-orchestrator 调度
- 需要综合多个排名时

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["rankings"],
  "properties": {
    "rankings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["evaluator_id", "ranking"],
        "properties": {
          "evaluator_id": { "type": "string" },
          "ranking": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "candidate": { "type": "string" },
                "rank": { "type": "integer" },
                "score": { "type": "number" }
              }
            }
          },
          "confidence": { "type": "string" },
          "notes": { "type": "string" }
        }
      },
      "description": "各评审员的排名结果"
    },
    "algorithm": {
      "type": "string",
      "enum": ["borda", "schulze", "average", "weighted_average"],
      "default": "weighted_average",
      "description": "排名合成算法"
    },
    "weights": {
      "type": "object",
      "additionalProperties": { "type": "number" },
      "description": "评审员权重配置"
    },
    "conflict_threshold": {
      "type": "number",
      "default": 2,
      "description": "排名差异超过此值视为冲突"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["synthesized_ranking", "conflict_analysis"],
  "properties": {
    "synthesized_ranking": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rank": { "type": "integer" },
          "candidate": { "type": "string" },
          "composite_score": { "type": "number" },
          "individual_ranks": {
            "type": "object",
            "additionalProperties": { "type": "integer" }
          },
          "rank_variance": { "type": "number" }
        }
      },
      "description": "综合排名结果"
    },
    "conflict_analysis": {
      "type": "object",
      "properties": {
        "has_conflicts": { "type": "boolean" },
        "conflict_pairs": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "candidate": { "type": "string" },
              "evaluators": { "type": "array", "items": { "type": "string" } },
              "rank_difference": { "type": "integer" },
              "description": { "type": "string" }
            }
          }
        },
        "consensus_level": {
          "type": "string",
          "enum": ["high", "medium", "low"]
        },
        "kendall_tau": {
          "type": "number",
          "description": "Kendall tau 相关系数"
        }
      },
      "description": "冲突分析"
    },
    "algorithm_details": {
      "type": "object",
      "properties": {
        "algorithm_used": { "type": "string" },
        "weights_applied": { "type": "object" },
        "intermediate_scores": { "type": "object" }
      },
      "description": "算法细节"
    }
  }
}
```

## 排名算法

### Borda Count
- 最低排名获得最高分
- 简单加权汇总
- 适用于评审员等权重

### Schulze Method
- 考虑成对比较
- 更公平处理排名冲突
- 计算复杂度较高

### Average Rank
- 简单平均排名
- 快速但可能丢失信息

### Weighted Average (默认)
- 按评审员置信度加权
- 高置信度评审员权重更高
- 兼顾速度和公平性

## 执行流程

1. **数据验证**
   - 检查所有排名完整性
   - 验证候选列表一致性

2. **权重分配**
   - 应用配置的权重
   - 默认按置信度分配

3. **排名计算**
   - 执行选定算法
   - 生成综合排名

4. **冲突检测**
   - 计算排名方差
   - 识别冲突对
   - 计算一致性指标

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 处理所有输入排名 | 100% |
| 一致性 | 输出排名无矛盾 | 100% |
| 透明度 | 冲突已识别和记录 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| defect-analyzer | 接收其排名建议 |
| vote-aggregator | 类似逻辑可复用 |
| consensus-builder | 输出供其参考 |
| multi-round-eval-orchestrator | 由其调度 |

## 脚本

- `scripts/synthesize.py` - 排名综合主脚本
- `scripts/algorithms.py` - 排名算法库
- `scripts/conflict_detector.py` - 冲突检测器

## 参考资料

- `references/ranking-algorithms.md` - 排名算法详解
- `references/conflict-resolution.md` - 冲突解决策略
