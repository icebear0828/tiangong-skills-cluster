---
name: learning-commander
description: >
  学习域总指挥 Skill (L0)。学习任务的第一入口点，负责学习任务路由、学习计划生成、
  阶段调度。当需要：(1) 学习新知识，(2) 掌握技能，(3) 理解概念时触发。
  分析学习任务复杂度，选择最优学习路径，路由到对应编排器。作为 L0 层 Skill，具有严格契约。
---

# Learning Commander — 学习域总指挥

## 触发条件

- 用户任务包含"学习"、"理解"、"掌握"、"教我"等关键词
- 由 meta-commander 路由到学习域
- 需要系统性学习某个主题时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["task_description"],
  "properties": {
    "task_description": {
      "type": "string",
      "description": "学习任务描述"
    },
    "learning_goal": {
      "type": "object",
      "properties": {
        "topic": { "type": "string" },
        "target_level": {
          "type": "string",
          "enum": ["awareness", "understanding", "application", "mastery"]
        },
        "time_available": { "type": "string" },
        "specific_objectives": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "学习目标"
    },
    "learner_profile": {
      "type": "object",
      "properties": {
        "current_level": {
          "type": "string",
          "enum": ["beginner", "intermediate", "advanced"]
        },
        "background": {
          "type": "array",
          "items": { "type": "string" }
        },
        "preferred_style": {
          "type": "string",
          "enum": ["visual", "verbal", "logical", "experiential"]
        },
        "available_time": { "type": "string" }
      },
      "description": "学习者画像"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "max_phases": { "type": "integer" },
        "focus_areas": { "type": "array", "items": { "type": "string" } },
        "skip_areas": { "type": "array", "items": { "type": "string" } }
      },
      "description": "学习约束"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["learning_plan", "execution_result"],
  "properties": {
    "task_analysis": {
      "type": "object",
      "properties": {
        "topic_complexity": { "type": "string", "enum": ["S", "M", "L", "XL"] },
        "estimated_phases": { "type": "integer" },
        "prerequisite_check": {
          "type": "object",
          "properties": {
            "met": { "type": "array", "items": { "type": "string" } },
            "missing": { "type": "array", "items": { "type": "string" } }
          }
        },
        "selected_path": { "type": "string" }
      },
      "description": "任务分析"
    },
    "learning_plan": {
      "type": "object",
      "properties": {
        "overview": { "type": "string" },
        "phases": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "phase_id": { "type": "string" },
              "name": { "type": "string" },
              "description": { "type": "string" },
              "skills_used": { "type": "array", "items": { "type": "string" } },
              "expected_outcome": { "type": "string" },
              "dependencies": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "success_criteria": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "学习计划"
    },
    "execution_result": {
      "type": "object",
      "properties": {
        "phases_completed": { "type": "integer" },
        "knowledge_gained": {
          "type": "array",
          "items": { "type": "string" }
        },
        "mastery_assessment": {
          "type": "object",
          "properties": {
            "level_achieved": { "type": "string" },
            "confidence": { "type": "number" },
            "gaps_identified": { "type": "array", "items": { "type": "string" } }
          }
        },
        "artifacts_produced": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "path": { "type": "string" }
            }
          }
        }
      },
      "description": "执行结果"
    },
    "next_steps": {
      "type": "array",
      "items": { "type": "string" },
      "description": "后续学习建议"
    }
  }
}
```

## 四阶段学习框架

### Phase 1: 消化 (Digest)
**目标**: 将外部知识转化为内部表征

**执行**:
1. 调用 `content-curator` 获取优质资源
2. 调用 `knowledge-extractor` 提取知识点
3. 调用 `analogy-explainer` 生成易懂解释

**产出**:
- 结构化知识项
- 概念摘要
- 类比解释

### Phase 2: 结构化 (Structure)
**目标**: 构建知识间的关联结构

**执行**:
1. 调用 `knowledge-graph-orchestrator`
2. 构建概念图谱
3. 生成可视化表示

**产出**:
- 知识图谱
- 概念地图
- 关系图

### Phase 3: 内化 (Internalize)
**目标**: 通过验证确保深度理解

**执行**:
1. 调用 `verification-orchestrator`
2. 苏格拉底式对话
3. 自我解释验证

**产出**:
- 掌握度评估
- 误解纠正
- 理解确认

### Phase 4: 应用 (Apply)
**目标**: 通过实践巩固学习

**执行**:
1. 调用 `micro-project-orchestrator`
2. 生成练习项目
3. 评估应用能力

**产出**:
- 微项目代码
- 练习结果
- 能力评估

## 学习路径选择

| 复杂度 | 阶段数 | 路径描述 |
|--------|--------|---------|
| S | 1-2 | 快速消化 + 基础验证 |
| M | 2-3 | 消化 + 结构化 + 验证 |
| L | 3-4 | 完整四阶段 |
| XL | 4+ | 多轮迭代 + 深度验证 |

## 目标等级定义

| 等级 | 定义 | 验证方式 |
|------|------|---------|
| awareness | 知道是什么 | 能识别 |
| understanding | 理解原理 | 能解释 |
| application | 能够应用 | 能使用 |
| mastery | 精通掌握 | 能教授 |

## 路由规则

```
学习任务 → learning-commander
    │
    ├─ "解释/讲解X" → 直接调用 analogy-explainer
    │
    ├─ "提取要点" → 直接调用 knowledge-extractor
    │
    ├─ "检验理解" → verification-orchestrator
    │
    ├─ "做练习" → micro-project-orchestrator
    │
    └─ "系统学习" → 完整四阶段流程
        ├─ Phase 1: learning-orchestrator
        ├─ Phase 2: knowledge-graph-orchestrator
        ├─ Phase 3: verification-orchestrator
        └─ Phase 4: micro-project-orchestrator
```

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| meta-commander | 被调用 | 由其路由学习任务 |
| learning-orchestrator | 调用 | Phase 1 |
| knowledge-graph-orchestrator | 调用 | Phase 2 |
| verification-orchestrator | 调用 | Phase 3 |
| micro-project-orchestrator | 调用 | Phase 4 |
| eval-engine | 调用 | 掌握度评估 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 任务理解 | 正确识别学习目标 | 100% |
| 路径适配 | 路径与目标匹配 | 正确 |
| 计划完整 | 覆盖必要阶段 | 100% |
| 评估准确 | 掌握度评估准确 | ≥85% |

## 脚本

- `scripts/analyze_learning_task.py` - 任务分析脚本
- `scripts/select_learning_path.py` - 路径选择脚本
- `scripts/generate_plan.py` - 计划生成脚本

## 参考资料

- `references/learning-routing-rules.md` - 学习路由规则
- `references/learning-capability-map.md` - 学习能力映射
- `references/learning-phases.md` - 学习阶段详解
