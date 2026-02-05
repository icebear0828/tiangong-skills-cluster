---
name: vote-aggregator
description: >
  投票汇总器 Skill。汇总多个评审员的投票结果，判断是否达到淘汰阈值。当需要：
  (1) 汇总多方投票，(2) 计算共识程度，(3) 判定淘汰阈值时触发。
  支持加权投票、置信度加权、冲突检测。作为核心评审 Skill，具有严格契约。
---

# Vote Aggregator — 投票汇总器

## 触发条件

- 多个评审员完成投票后
- 由 multi-round-eval-orchestrator 调度
- 需要汇总评审结果时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["votes", "elimination_threshold"],
  "properties": {
    "votes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["evaluator_id", "elimination_decision"],
        "properties": {
          "evaluator_id": { "type": "string" },
          "elimination_decision": {
            "type": "object",
            "properties": {
              "eliminated": { "type": "string" },
              "reason": { "type": "string" },
              "confidence": { "type": "string", "enum": ["High", "Medium", "Low"] }
            }
          },
          "quick_assessments": { "type": "object" }
        }
      },
      "description": "各评审员的投票结果"
    },
    "elimination_threshold": {
      "type": "integer",
      "description": "淘汰所需的最低票数",
      "minimum": 1
    },
    "confidence_weights": {
      "type": "object",
      "properties": {
        "High": { "type": "number", "default": 1.5 },
        "Medium": { "type": "number", "default": 1.0 },
        "Low": { "type": "number", "default": 0.5 }
      },
      "description": "置信度权重配置"
    },
    "require_unanimous": {
      "type": "boolean",
      "default": false,
      "description": "是否要求全票通过"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["aggregated_result", "threshold_reached", "vote_distribution"],
  "properties": {
    "aggregated_result": {
      "type": "object",
      "properties": {
        "eliminated_candidates": {
          "type": "array",
          "items": { "type": "string" },
          "description": "被淘汰的候选列表"
        },
        "survivors": {
          "type": "array",
          "items": { "type": "string" },
          "description": "存活的候选列表"
        }
      }
    },
    "threshold_reached": {
      "type": "boolean",
      "description": "是否达到淘汰阈值"
    },
    "vote_distribution": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "raw_votes": { "type": "integer" },
          "weighted_votes": { "type": "number" },
          "voters": { "type": "array", "items": { "type": "string" } }
        }
      },
      "description": "每个候选的票数分布"
    },
    "consensus_analysis": {
      "type": "object",
      "properties": {
        "consensus_level": {
          "type": "string",
          "enum": ["unanimous", "strong", "moderate", "weak", "split"],
          "description": "共识程度"
        },
        "agreement_ratio": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "一致性比例"
        },
        "conflicts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "candidate": { "type": "string" },
              "conflicting_evaluators": { "type": "array" },
              "description": { "type": "string" }
            }
          },
          "description": "投票冲突详情"
        }
      }
    },
    "reasoning_summary": {
      "type": "object",
      "additionalProperties": {
        "type": "array",
        "items": { "type": "string" }
      },
      "description": "各候选被淘汰的理由汇总"
    }
  }
}
```

## 执行流程

1. **收集投票**
   - 验证所有评审员已提交
   - 检查投票格式完整性

2. **票数统计**
   - 统计原始票数
   - 应用置信度权重
   - 计算加权票数

3. **阈值判定**
   - 比较加权票数与阈值
   - 判定是否淘汰

4. **共识分析**
   - 计算一致性比例
   - 识别投票冲突
   - 汇总淘汰理由

## 共识等级定义

| 等级 | 一致性比例 | 描述 |
|------|-----------|------|
| unanimous | 100% | 全票一致 |
| strong | ≥80% | 强共识 |
| moderate | ≥60% | 中等共识 |
| weak | ≥40% | 弱共识 |
| split | <40% | 分裂 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 处理所有投票 | 100% |
| 准确性 | 票数统计正确 | 100% |
| 透明度 | 理由可追溯 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| initial-screener | 接收其投票输出 |
| defect-analyzer | 接收其评分结果 |
| multi-round-eval-orchestrator | 向其返回汇总结果 |
| consensus-builder | 共享共识计算逻辑 |

## 脚本

- `scripts/aggregate.py` - 投票汇总主脚本
- `scripts/consensus.py` - 共识分析脚本

## 参考资料

- `references/voting-rules.md` - 投票规则说明
