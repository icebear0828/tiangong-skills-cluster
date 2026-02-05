---
name: socratic-questioner
description: >
  苏格拉底提问器 Skill。通过提问引导学习者深入思考。当需要：(1) 深化理解，
  (2) 检验思维过程，(3) 引导自我发现时触发。支持自适应问题、进度评估、
  多级提示。作为扩展学习 Skill，具有标准契约。
---

# Socratic Questioner — 苏格拉底提问器

## 触发条件

- 验证阶段需要深化理解
- 由 verification-orchestrator 调度
- 需要通过对话引导学习

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["topic", "current_understanding"],
  "properties": {
    "topic": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string" },
        "definition": { "type": "string" },
        "key_concepts": {
          "type": "array",
          "items": { "type": "string" }
        },
        "common_misconceptions": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "学习主题"
    },
    "current_understanding": {
      "type": "object",
      "properties": {
        "level": {
          "type": "string",
          "enum": ["none", "basic", "developing", "solid", "advanced"]
        },
        "known_concepts": {
          "type": "array",
          "items": { "type": "string" }
        },
        "gaps": {
          "type": "array",
          "items": { "type": "string" }
        },
        "misconceptions": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "当前理解状态"
    },
    "dialogue_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "role": { "type": "string", "enum": ["questioner", "learner"] },
          "content": { "type": "string" }
        }
      },
      "description": "对话历史"
    },
    "config": {
      "type": "object",
      "properties": {
        "questioning_style": {
          "type": "string",
          "enum": ["gentle", "moderate", "challenging"],
          "default": "moderate"
        },
        "max_questions": {
          "type": "integer",
          "default": 5
        },
        "provide_hints": {
          "type": "boolean",
          "default": true
        },
        "target_depth": {
          "type": "string",
          "enum": ["surface", "conceptual", "deep", "synthesis"],
          "default": "conceptual"
        }
      },
      "description": "提问配置"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["questions", "progress_assessment"],
  "properties": {
    "questions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "question", "type", "purpose"],
        "properties": {
          "id": { "type": "string" },
          "question": { "type": "string" },
          "type": {
            "type": "string",
            "enum": [
              "clarifying",
              "probing",
              "reason_evidence",
              "viewpoint",
              "implication",
              "about_question"
            ]
          },
          "purpose": { "type": "string" },
          "target_concept": { "type": "string" },
          "expected_depth": { "type": "string" },
          "hints": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "level": { "type": "integer" },
                "hint": { "type": "string" }
              }
            }
          },
          "follow_up_if_stuck": { "type": "string" },
          "ideal_response_elements": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "description": "生成的问题序列"
    },
    "progress_assessment": {
      "type": "object",
      "properties": {
        "current_level": {
          "type": "string",
          "enum": ["none", "basic", "developing", "solid", "advanced"]
        },
        "progress_since_start": {
          "type": "number",
          "minimum": -1,
          "maximum": 1
        },
        "concepts_solidified": {
          "type": "array",
          "items": { "type": "string" }
        },
        "concepts_still_weak": {
          "type": "array",
          "items": { "type": "string" }
        },
        "misconceptions_addressed": {
          "type": "array",
          "items": { "type": "string" }
        },
        "new_insights_demonstrated": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "进度评估"
    },
    "adaptation_suggestions": {
      "type": "object",
      "properties": {
        "recommended_style_change": { "type": "string" },
        "topics_to_revisit": { "type": "array" },
        "ready_for_next_level": { "type": "boolean" },
        "scaffolding_needed": { "type": "array" }
      },
      "description": "适应建议"
    }
  }
}
```

## 苏格拉底问题类型

| 类型 | 目的 | 示例 |
|------|------|------|
| clarifying | 澄清含义 | "你说的...是什么意思？" |
| probing | 探究假设 | "你是基于什么假设？" |
| reason_evidence | 追问理由 | "你怎么知道这是真的？" |
| viewpoint | 探索视角 | "从另一个角度看呢？" |
| implication | 探究后果 | "如果...会怎样？" |
| about_question | 反思问题 | "为什么这个问题重要？" |

## 思维深度级别

| 级别 | 描述 | 问题特征 |
|------|------|---------|
| surface | 表面理解 | 记忆、识别 |
| conceptual | 概念理解 | 解释、比较 |
| deep | 深度理解 | 分析、评估 |
| synthesis | 综合创造 | 综合、创新 |

## 提问风格

| 风格 | 描述 | 适用情况 |
|------|------|---------|
| gentle | 温和引导 | 初学者、信心不足 |
| moderate | 适度挑战 | 一般情况 |
| challenging | 高强度挑战 | 高级学习者 |

## 执行流程

1. **状态分析**
   - 分析当前理解水平
   - 识别薄弱点
   - 回顾对话历史

2. **问题生成**
   - 选择问题类型
   - 针对薄弱点设计问题
   - 准备提示和后续问题

3. **序列优化**
   - 排列问题顺序
   - 从易到难递进
   - 确保逻辑连贯

4. **进度评估**
   - 评估学习者进步
   - 识别新的洞察
   - 更新理解状态

## 自适应策略

| 学习者表现 | 调整策略 |
|-----------|---------|
| 回答流畅 | 增加难度、减少提示 |
| 回答困难 | 提供提示、分解问题 |
| 存在误解 | 设计澄清问题 |
| 停滞不前 | 更换角度、提供新视角 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 针对性 | 问题针对薄弱点 | 100% |
| 递进性 | 难度逐步递进 | 是 |
| 启发性 | 引导自我发现 | 是 |
| 适应性 | 根据反馈调整 | 是 |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| self-explanation-validator | 配合验证理解 |
| analogy-explainer | 配合澄清概念 |
| verification-orchestrator | 由其调度 |

## 脚本

- `scripts/generate_questions.py` - 问题生成主脚本
- `scripts/progress_tracker.py` - 进度跟踪器
- `scripts/adaptation_engine.py` - 适应引擎

## 参考资料

- `references/question-patterns.md` - 问题模式库
- `references/scaffolding-levels.md` - 脚手架级别
- `references/socratic-method.md` - 苏格拉底方法指南
