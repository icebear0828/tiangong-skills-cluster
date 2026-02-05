---
name: verification-orchestrator
description: >
  内化验证编排器。编排自我解释验证+苏格拉底对话+掌握度评估流程。当需要：
  (1) 验证学习效果，(2) 深化理解，(3) 识别知识盲点时触发。
  支持多种验证方式、自适应对话、掌握度评估。由 learning-commander 调度触发。
---

# Verification Orchestrator — 内化验证编排器

## 触发条件

- 进入 Phase 3 内化阶段
- 由 learning-commander 调度
- 需要验证和深化学习效果

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["knowledge_base", "learner_context"],
  "properties": {
    "knowledge_base": {
      "type": "object",
      "properties": {
        "concepts": { "type": "array" },
        "relationships": { "type": "array" },
        "analogies": { "type": "array" }
      },
      "description": "已学习的知识库"
    },
    "graph": {
      "type": "object",
      "description": "来自 Phase 2 的知识图谱"
    },
    "learner_context": {
      "type": "object",
      "properties": {
        "level": { "type": "string" },
        "prior_responses": { "type": "array" },
        "identified_weaknesses": { "type": "array" }
      },
      "description": "学习者上下文"
    },
    "verification_config": {
      "type": "object",
      "properties": {
        "mode": {
          "type": "string",
          "enum": ["quick_check", "standard", "thorough", "mastery_test"],
          "default": "standard"
        },
        "include_socratic": {
          "type": "boolean",
          "default": true
        },
        "max_rounds": {
          "type": "integer",
          "default": 5
        },
        "target_mastery": {
          "type": "number",
          "default": 0.8
        }
      },
      "description": "验证配置"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["mastery_assessment", "verification_details"],
  "properties": {
    "mastery_assessment": {
      "type": "object",
      "properties": {
        "overall_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "mastery_level": {
          "type": "string",
          "enum": ["mastered", "proficient", "developing", "beginning", "misconceived"]
        },
        "by_concept": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "score": { "type": "number" },
              "status": { "type": "string" }
            }
          }
        },
        "confidence": { "type": "number" }
      },
      "description": "掌握度评估"
    },
    "verification_details": {
      "type": "object",
      "properties": {
        "self_explanation_results": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "concept": { "type": "string" },
              "learner_explanation": { "type": "string" },
              "validation_result": { "type": "object" }
            }
          }
        },
        "socratic_dialogue": {
          "type": "object",
          "properties": {
            "rounds": { "type": "integer" },
            "key_insights": { "type": "array" },
            "progress_trajectory": { "type": "array" }
          }
        },
        "misconceptions_found": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "concept": { "type": "string" },
              "misconception": { "type": "string" },
              "severity": { "type": "string" },
              "corrected": { "type": "boolean" }
            }
          }
        }
      },
      "description": "验证详情"
    },
    "gaps_and_remediation": {
      "type": "object",
      "properties": {
        "knowledge_gaps": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "area": { "type": "string" },
              "severity": { "type": "string" },
              "remediation_suggestion": { "type": "string" }
            }
          }
        },
        "recommended_review": {
          "type": "array",
          "items": { "type": "string" }
        },
        "next_learning_focus": { "type": "string" }
      },
      "description": "差距与补救"
    },
    "certification": {
      "type": "object",
      "properties": {
        "passed": { "type": "boolean" },
        "criteria_met": { "type": "array" },
        "criteria_failed": { "type": "array" }
      },
      "description": "认证结果"
    }
  }
}
```

## 验证模式

| 模式 | 轮次 | 深度 | 适用场景 |
|------|------|------|---------|
| quick_check | 1-2 | 浅 | 快速确认 |
| standard | 3-5 | 中 | 常规验证 |
| thorough | 5-8 | 深 | 重要概念 |
| mastery_test | 8+ | 全面 | 认证级别 |

## 编排流程

```
┌─────────────────────────────────────────────┐
│  Phase 3: 内化 (Internalize)                 │
│                                             │
│  Step 1: 自我解释验证                        │
│  ├─ 要求学习者解释核心概念                   │
│  ├─ 调用 self-explanation-validator         │
│  └─ 识别误解和遗漏                           │
│                                             │
│  Step 2: 苏格拉底对话                        │
│  ├─ 调用 socratic-questioner                │
│  ├─ 通过提问引导深入思考                     │
│  └─ 自适应调整问题难度                       │
│                                             │
│  Step 3: 类比检验                            │
│  ├─ 要求学习者解释类比                       │
│  ├─ 检验类比理解的准确性                     │
│  └─ 使用 analogy-explainer 澄清             │
│                                             │
│  Step 4: 掌握度评估                          │
│  ├─ 综合各项验证结果                         │
│  ├─ 计算掌握度分数                           │
│  └─ 确定掌握等级                             │
│                                             │
│  Step 5: 补救建议                            │
│  ├─ 识别知识差距                             │
│  └─ 生成补救计划                             │
│                                             │
│  输出 → micro-project-orchestrator (Phase 4) │
│  或 → 返回 Phase 1/2 进行补救                │
└─────────────────────────────────────────────┘
```

## 掌握度标准

| 等级 | 分数范围 | 能力描述 |
|------|---------|---------|
| mastered | ≥0.9 | 能教授他人 |
| proficient | 0.75-0.9 | 能独立应用 |
| developing | 0.6-0.75 | 基本理解 |
| beginning | 0.4-0.6 | 初步接触 |
| misconceived | <0.4 | 存在根本误解 |

## 自适应策略

| 学习者表现 | 调整策略 |
|-----------|---------|
| 表现优秀 | 增加难度、减少提示 |
| 表现中等 | 维持当前难度 |
| 表现欠佳 | 降低难度、增加类比 |
| 存在误解 | 暂停、澄清概念 |

## 质量关卡

| 检查点 | 标准 | 未通过处理 |
|--------|------|-----------|
| 自解释覆盖 | ≥80% 核心概念 | 补充概念 |
| 对话有效性 | 有进步迹象 | 调整策略 |
| 误解处理 | 严重误解已纠正 | 返回学习 |
| 最终掌握度 | ≥目标阈值 | 进入补救 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| self-explanation-validator | 调用 | Step 1 |
| socratic-questioner | 调用 | Step 2 |
| analogy-explainer | 调用 | Step 3 澄清 |
| knowledge-graph-orchestrator | 接收输入 | 来自 Phase 2 |
| micro-project-orchestrator | 输出传递 | 到 Phase 4 |
| learning-orchestrator | 可能返回 | 补救循环 |

## 脚本

- `scripts/orchestrate_verification.py` - 验证编排主脚本
- `scripts/mastery_calculator.py` - 掌握度计算器
- `scripts/remediation_planner.py` - 补救计划器

## 参考资料

- `references/verification-rubrics.md` - 验证评分标准
- `references/mastery-criteria.md` - 掌握度标准
- `references/socratic-patterns.md` - 苏格拉底对话模式
