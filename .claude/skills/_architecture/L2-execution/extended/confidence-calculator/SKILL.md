---
name: confidence-calculator
description: >
  置信度计算器 Skill。根据评审过程数据计算最终推荐的置信度分数，识别不确定性来源。
  当需要：(1) 量化决策置信度，(2) 识别决策弱点，(3) 支持风险评估时触发。
  作为扩展评审 Skill，具有标准契约。
---

# Confidence Calculator — 置信度计算器

## 触发条件

- 评审流程接近尾声
- 由 consensus-builder 或 multi-round-eval-orchestrator 调用
- 需要量化决策置信度时

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["evaluation_process_data"],
  "properties": {
    "evaluation_process_data": {
      "type": "object",
      "required": ["rounds", "final_ranking"],
      "properties": {
        "rounds": {
          "type": "object",
          "properties": {
            "round1": {
              "type": "object",
              "properties": {
                "vote_distribution": { "type": "object" },
                "consensus_level": { "type": "string" },
                "eliminated": { "type": "array" }
              }
            },
            "round2": {
              "type": "object",
              "properties": {
                "ranking_variance": { "type": "number" },
                "conflict_count": { "type": "integer" },
                "score_gaps": { "type": "object" }
              }
            },
            "round3": {
              "type": "object",
              "properties": {
                "critical_found": { "type": "boolean" },
                "attack_severity": { "type": "string" },
                "ranking_changed": { "type": "boolean" }
              }
            },
            "round4": {
              "type": "object",
              "properties": {
                "resurrection_occurred": { "type": "boolean" },
                "final_consensus": { "type": "string" }
              }
            }
          }
        },
        "final_ranking": {
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
        "evaluator_count": { "type": "integer" },
        "total_defects_found": { "type": "integer" }
      }
    },
    "weight_config": {
      "type": "object",
      "properties": {
        "consensus_weight": { "type": "number", "default": 0.25 },
        "stability_weight": { "type": "number", "default": 0.25 },
        "robustness_weight": { "type": "number", "default": 0.25 },
        "margin_weight": { "type": "number", "default": 0.25 }
      },
      "description": "各因素权重配置"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["confidence_score", "confidence_level", "factors", "uncertainty_sources"],
  "properties": {
    "confidence_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "综合置信度分数"
    },
    "confidence_level": {
      "type": "string",
      "enum": ["Very High", "High", "Medium", "Low", "Very Low"],
      "description": "置信度等级"
    },
    "factors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "score", "weight", "impact"],
        "properties": {
          "name": { "type": "string" },
          "score": { "type": "number", "minimum": 0, "maximum": 1 },
          "weight": { "type": "number" },
          "impact": {
            "type": "string",
            "enum": ["positive", "negative", "neutral"]
          },
          "details": { "type": "string" }
        }
      },
      "description": "置信度影响因素"
    },
    "uncertainty_sources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source": { "type": "string" },
          "severity": {
            "type": "string",
            "enum": ["high", "medium", "low"]
          },
          "description": { "type": "string" },
          "mitigation": { "type": "string" }
        }
      },
      "description": "不确定性来源"
    },
    "recommendations": {
      "type": "array",
      "items": { "type": "string" },
      "description": "提升置信度的建议"
    },
    "calculation_details": {
      "type": "object",
      "properties": {
        "formula": { "type": "string" },
        "intermediate_values": { "type": "object" }
      },
      "description": "计算细节"
    }
  }
}
```

## 置信度因素

### 1. 共识度 (Consensus)
| 等级 | 分数 | 条件 |
|------|------|------|
| 全票一致 | 1.0 | 所有评审员结论一致 |
| 强共识 | 0.8 | ≥80% 一致 |
| 中等共识 | 0.6 | ≥60% 一致 |
| 弱共识 | 0.4 | ≥40% 一致 |
| 分裂 | 0.2 | <40% 一致 |

### 2. 稳定性 (Stability)
| 等级 | 分数 | 条件 |
|------|------|------|
| 高稳定 | 1.0 | 排名从未改变 |
| 较稳定 | 0.75 | 仅小幅调整 |
| 中等 | 0.5 | 有明显变化 |
| 低稳定 | 0.25 | 大幅波动 |

### 3. 鲁棒性 (Robustness)
| 等级 | 分数 | 条件 |
|------|------|------|
| 高鲁棒 | 1.0 | 经受住对抗攻击 |
| 较鲁棒 | 0.75 | 发现非 Critical 缺陷 |
| 中等 | 0.5 | 发现 Critical 但可缓解 |
| 低鲁棒 | 0.25 | Critical 缺陷导致排名变化 |

### 4. 领先优势 (Margin)
| 等级 | 分数 | 条件 |
|------|------|------|
| 明显领先 | 1.0 | 领先 ≥2 分 |
| 较大领先 | 0.75 | 领先 1-2 分 |
| 微弱领先 | 0.5 | 领先 0.5-1 分 |
| 接近 | 0.25 | 领先 <0.5 分 |

## 置信度等级映射

| 分数范围 | 等级 | 建议行动 |
|---------|------|---------|
| ≥0.85 | Very High | 可直接采纳 |
| 0.70-0.85 | High | 建议采纳 |
| 0.55-0.70 | Medium | 需额外验证 |
| 0.40-0.55 | Low | 建议人工复核 |
| <0.40 | Very Low | 建议重新评审 |

## 执行流程

1. **数据提取**
   - 从评审过程提取关键指标
   - 计算各因素原始值

2. **因素评分**
   - 根据映射表计算各因素分数
   - 评估影响方向

3. **加权汇总**
   - 应用权重配置
   - 计算综合置信度

4. **不确定性识别**
   - 分析低分因素
   - 识别不确定性来源
   - 生成缓解建议

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 考虑所有因素 | 100% |
| 透明度 | 计算过程可追溯 | 100% |
| 一致性 | 相同输入给出相同输出 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| consensus-builder | 被其调用，结果被使用 |
| vote-aggregator | 提供共识度数据 |
| ranking-synthesizer | 提供稳定性数据 |
| devils-advocate | 提供鲁棒性数据 |

## 脚本

- `scripts/calculate_confidence.py` - 置信度计算主脚本
- `scripts/factor_scorer.py` - 因素评分器
- `scripts/uncertainty_analyzer.py` - 不确定性分析器

## 参考资料

- `references/confidence-factors.md` - 置信度因素详解
- `references/uncertainty-taxonomy.md` - 不确定性分类学
