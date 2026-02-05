---
name: micro-project-orchestrator
description: >
  微项目编排器。编排项目生成+代码脚手架+评估反馈流程。当需要：(1) 实践应用所学知识，
  (2) 生成练习项目，(3) 评估应用能力时触发。支持项目生成、代码脚手架、
  评估反馈循环。由 learning-commander 调度触发。
---

# Micro-Project Orchestrator — 微项目编排器

## 触发条件

- 进入 Phase 4 应用阶段
- 由 learning-commander 调度
- 需要通过实践巩固学习

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["knowledge_base", "mastery_assessment"],
  "properties": {
    "knowledge_base": {
      "type": "object",
      "properties": {
        "concepts": { "type": "array" },
        "relationships": { "type": "array" }
      },
      "description": "已学习的知识库"
    },
    "mastery_assessment": {
      "type": "object",
      "properties": {
        "overall_score": { "type": "number" },
        "by_concept": { "type": "object" },
        "gaps": { "type": "array" }
      },
      "description": "来自 Phase 3 的掌握度评估"
    },
    "learner_profile": {
      "type": "object",
      "properties": {
        "level": { "type": "string" },
        "preferred_language": { "type": "string" },
        "available_time": { "type": "string" }
      },
      "description": "学习者画像"
    },
    "project_config": {
      "type": "object",
      "properties": {
        "difficulty": {
          "type": "string",
          "enum": ["starter", "intermediate", "advanced", "challenge"],
          "default": "intermediate"
        },
        "project_type": {
          "type": "string",
          "enum": ["exercise", "mini_app", "refactor", "debug", "extend"],
          "default": "mini_app"
        },
        "time_budget": {
          "type": "string",
          "enum": ["15min", "30min", "1hour", "2hours"],
          "default": "30min"
        },
        "include_tests": {
          "type": "boolean",
          "default": true
        },
        "include_hints": {
          "type": "boolean",
          "default": true
        }
      },
      "description": "项目配置"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["project", "evaluation"],
  "properties": {
    "project": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "title": { "type": "string" },
        "description": { "type": "string" },
        "objectives": {
          "type": "array",
          "items": { "type": "string" }
        },
        "concepts_practiced": {
          "type": "array",
          "items": { "type": "string" }
        },
        "difficulty": { "type": "string" },
        "estimated_time": { "type": "string" },
        "scaffolding": {
          "type": "object",
          "properties": {
            "starter_code": { "type": "string" },
            "file_structure": { "type": "object" },
            "dependencies": { "type": "array" },
            "setup_instructions": { "type": "string" }
          }
        },
        "requirements": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "description": { "type": "string" },
              "acceptance_criteria": { "type": "string" }
            }
          }
        },
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
        "tests": {
          "type": "object",
          "properties": {
            "test_file": { "type": "string" },
            "test_cases": { "type": "array" }
          }
        },
        "solution": {
          "type": "object",
          "properties": {
            "code": { "type": "string" },
            "explanation": { "type": "string" }
          }
        }
      },
      "description": "生成的微项目"
    },
    "evaluation": {
      "type": "object",
      "properties": {
        "submission_received": { "type": "boolean" },
        "tests_passed": {
          "type": "object",
          "properties": {
            "total": { "type": "integer" },
            "passed": { "type": "integer" },
            "failed": { "type": "integer" }
          }
        },
        "code_review": {
          "type": "object",
          "properties": {
            "quality_score": { "type": "number" },
            "concept_application": { "type": "object" },
            "feedback": { "type": "array" }
          }
        },
        "learning_outcome": {
          "type": "object",
          "properties": {
            "concepts_reinforced": { "type": "array" },
            "skills_demonstrated": { "type": "array" },
            "areas_for_improvement": { "type": "array" }
          }
        }
      },
      "description": "项目评估"
    },
    "next_recommendations": {
      "type": "object",
      "properties": {
        "continue_learning": { "type": "boolean" },
        "suggested_next_project": { "type": "string" },
        "review_topics": { "type": "array" }
      },
      "description": "后续建议"
    }
  }
}
```

## 项目类型

| 类型 | 描述 | 适用场景 |
|------|------|---------|
| exercise | 针对性练习 | 巩固单一概念 |
| mini_app | 小型应用 | 综合多个概念 |
| refactor | 重构练习 | 理解设计模式 |
| debug | 调试练习 | 加深理解原理 |
| extend | 扩展功能 | 应用到实际场景 |

## 难度级别

| 级别 | 提示量 | 脚手架量 | 时间 |
|------|--------|---------|------|
| starter | 多 | 高 | 15min |
| intermediate | 中 | 中 | 30min |
| advanced | 少 | 低 | 1hour |
| challenge | 无 | 最小 | 2hours |

## 编排流程

```
┌─────────────────────────────────────────────┐
│  Phase 4: 应用 (Apply)                       │
│                                             │
│  Step 1: 项目生成                            │
│  ├─ 根据掌握度选择难度                       │
│  ├─ 确定练习的概念                           │
│  └─ 生成项目描述和要求                       │
│                                             │
│  Step 2: 脚手架创建                          │
│  ├─ 调用 code-gen 生成 starter 代码         │
│  ├─ 调用 test-gen 生成测试用例              │
│  └─ 准备文件结构                             │
│                                             │
│  Step 3: 提示生成                            │
│  ├─ 生成分级提示                             │
│  └─ 准备参考解答                             │
│                                             │
│  Step 4: 学习者完成项目                      │
│  ├─ 提供项目材料                             │
│  └─ 等待提交                                │
│                                             │
│  Step 5: 评估与反馈                          │
│  ├─ 运行测试用例                             │
│  ├─ 调用 code-review 审查代码               │
│  └─ 生成学习成果报告                         │
│                                             │
│  Step 6: 迭代（可选）                        │
│  ├─ 根据反馈调整                             │
│  └─ 生成后续项目建议                         │
│                                             │
│  输出 → 返回 learning-commander              │
└─────────────────────────────────────────────┘
```

## 与现有 Skills 的集成

| 现有 Skill | 调用时机 | 用途 |
|-----------|---------|------|
| code-gen | Step 2 | 生成脚手架代码 |
| test-gen | Step 2 | 生成测试用例 |
| code-review | Step 5 | 评审学习者代码 |
| debug | Step 5 | 辅助学习者调试 |

## 质量关卡

| 检查点 | 标准 | 未通过处理 |
|--------|------|-----------|
| 项目生成 | 覆盖目标概念 | 重新生成 |
| 脚手架有效 | 可运行 | 修复脚手架 |
| 测试可用 | 测试能运行 | 修复测试 |
| 评估完成 | 给出反馈 | 补充反馈 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| code-gen | 调用 | Step 2 |
| test-gen | 调用 | Step 2 |
| code-review | 调用 | Step 5 |
| debug | 调用 | Step 5（可选）|
| verification-orchestrator | 接收输入 | 来自 Phase 3 |
| learning-commander | 返回结果 | 完成时 |

## 脚本

- `scripts/generate_project.py` - 项目生成主脚本
- `scripts/scaffold_builder.py` - 脚手架构建器
- `scripts/evaluate_submission.py` - 提交评估器

## 参考资料

- `references/project-templates.md` - 项目模板库
- `references/scaffolding-patterns.md` - 脚手架模式
- `references/evaluation-rubrics.md` - 评估标准
