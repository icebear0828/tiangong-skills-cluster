---
name: consensus-builder
description: >
  共识构建器 Skill。综合所有轮次评审结果，构建最终推荐和置信度等级。当需要：
  (1) 最终决策形成，(2) 多轮结果综合，(3) 置信度计算时触发。
  支持冲突解决、路径追溯、置信度分级。作为核心评审 Skill，具有严格契约。
---

# Consensus Builder — 共识构建器

## 触发条件

- 所有评审轮次完成后
- 由 multi-round-eval-orchestrator 调度
- 需要形成最终决策时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["all_rounds_results", "candidates"],
  "properties": {
    "all_rounds_results": {
      "type": "object",
      "required": ["round1", "round2", "round3", "round4"],
      "properties": {
        "round1": {
          "type": "object",
          "properties": {
            "eliminated": { "type": "array", "items": { "type": "string" } },
            "survivors": { "type": "array", "items": { "type": "string" } },
            "vote_distribution": { "type": "object" }
          }
        },
        "round2": {
          "type": "object",
          "properties": {
            "rankings": {
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
            "defect_reports": { "type": "array" },
            "conflicts": { "type": "boolean" }
          }
        },
        "round3": {
          "type": "object",
          "properties": {
            "attacked": { "type": "array", "items": { "type": "string" } },
            "critical_found": { "type": "boolean" },
            "attack_reports": { "type": "array" }
          }
        },
        "round4": {
          "type": "object",
          "properties": {
            "resurrected": { "type": "array", "items": { "type": "string" } },
            "final_eliminated": { "type": "array", "items": { "type": "string" } },
            "final_reviews": { "type": "array" }
          }
        }
      },
      "description": "所有轮次的评审结果"
    },
    "candidates": {
      "type": "array",
      "items": { "type": "string" },
      "description": "初始候选列表"
    },
    "decision_criteria": {
      "type": "object",
      "properties": {
        "primary_weight": { "type": "number", "description": "主要维度权重" },
        "require_no_critical": { "type": "boolean", "default": true },
        "min_confidence": { "type": "number", "default": 0.7 }
      },
      "description": "决策标准配置"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["final_recommendation", "decision_path", "confidence_analysis"],
  "properties": {
    "final_recommendation": {
      "type": "object",
      "required": ["winner", "confidence"],
      "properties": {
        "winner": {
          "type": "string",
          "description": "最终推荐方案"
        },
        "runner_up": {
          "type": "string",
          "description": "次优方案"
        },
        "eliminated": {
          "type": "array",
          "items": { "type": "string" },
          "description": "被淘汰的方案列表"
        },
        "confidence": {
          "type": "string",
          "enum": ["Very High", "High", "Medium", "Low", "Very Low"],
          "description": "推荐置信度"
        },
        "summary": {
          "type": "string",
          "description": "一句话推荐理由"
        }
      }
    },
    "decision_path": {
      "type": "object",
      "properties": {
        "path_type": {
          "type": "string",
          "enum": ["A", "B", "C"],
          "description": "决策路径类型"
        },
        "key_decision_points": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "round": { "type": "string" },
              "decision": { "type": "string" },
              "impact": { "type": "string" }
            }
          },
          "description": "关键决策点列表"
        },
        "turning_points": {
          "type": "array",
          "items": { "type": "string" },
          "description": "关键转折点"
        }
      },
      "description": "决策路径追溯"
    },
    "confidence_analysis": {
      "type": "object",
      "properties": {
        "overall_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "总体置信度分数"
        },
        "factors": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "factor": { "type": "string" },
              "impact": { "type": "string", "enum": ["positive", "negative", "neutral"] },
              "weight": { "type": "number" }
            }
          },
          "description": "置信度影响因素"
        },
        "uncertainty_sources": {
          "type": "array",
          "items": { "type": "string" },
          "description": "不确定性来源"
        }
      }
    },
    "dissent_record": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "evaluator": { "type": "string" },
          "dissenting_opinion": { "type": "string" },
          "alternative_recommendation": { "type": "string" }
        }
      },
      "description": "异议记录（如有）"
    },
    "recommendations": {
      "type": "object",
      "properties": {
        "immediate_actions": {
          "type": "array",
          "items": { "type": "string" }
        },
        "risk_mitigations": {
          "type": "array",
          "items": { "type": "string" }
        },
        "monitoring_points": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "后续建议"
    }
  }
}
```

## 执行流程

1. **结果汇总**
   - 收集所有轮次结果
   - 构建候选状态时间线
   - 识别关键转折点

2. **冲突检测**
   - 检查轮次间的矛盾
   - 识别异议观点
   - 记录分歧

3. **路径分析**
   - 追溯决策路径
   - 标记关键决策点
   - 确定路径类型

4. **置信度计算**
   - 评估各影响因素
   - 计算综合置信度
   - 识别不确定性来源

5. **最终推荐**
   - 确定获胜方案
   - 生成推荐理由
   - 提出后续建议

## 决策路径类型

| 类型 | 描述 | 置信度影响 |
|------|------|-----------|
| A | 早期明确胜出，无翻转 | +0.2 |
| B | 经过对抗后确认 | +0.1 |
| C | 复活后最终胜出 | -0.1 |

## 置信度等级

| 等级 | 分数范围 | 描述 |
|------|---------|------|
| Very High | ≥0.9 | 高度确信 |
| High | 0.8-0.9 | 较有把握 |
| Medium | 0.6-0.8 | 中等确信 |
| Low | 0.4-0.6 | 存在疑虑 |
| Very Low | <0.4 | 高度不确定 |

## 置信度影响因素

| 因素 | 正向影响 | 负向影响 |
|------|---------|---------|
| 一致性 | 评审员高度一致 | 评审员严重分歧 |
| 稳定性 | 排名稳定 | 排名波动大 |
| 对抗结果 | 经受住攻击 | 发现 Critical 缺陷 |
| 复活情况 | 无复活 | 有方案复活 |
| 差距 | 领先明显 | 差距微小 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 考虑所有轮次结果 | 100% |
| 透明性 | 决策路径可追溯 | 100% |
| 公正性 | 记录异议观点 | 必须 |
| 可操作性 | 提供后续建议 | ≥3条 |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| vote-aggregator | 接收其汇总结果 |
| ranking-synthesizer | 接收其排名综合 |
| devils-advocate | 接收其攻击报告 |
| resurrection-evaluator | 接收其复活决定 |
| evaluation-commander | 向其返回最终决策 |

## 脚本

- `scripts/build_consensus.py` - 共识构建主脚本
- `scripts/confidence_calculator.py` - 置信度计算器
- `scripts/path_analyzer.py` - 路径分析器

## 参考资料

- `references/consensus-rules.md` - 共识规则
- `references/confidence-factors.md` - 置信度因素定义
