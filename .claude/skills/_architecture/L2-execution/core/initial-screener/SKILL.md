---
name: initial-screener
description: >
  初筛评审员 Skill。独立评审多个方案，选择最差方案淘汰。当需要：(1) 方案初筛淘汰，
  (2) 快速筛选候选列表，(3) 多方案比较评估时触发。支持打乱阅读顺序、独立评分、
  淘汰投票。作为核心评审 Skill，具有严格契约。
---

# Initial Screener — 初筛评审员

## 触发条件

- 评审任务中包含"初筛"、"淘汰"、"筛选"等关键词
- 由 multi-round-eval-orchestrator 调度
- Round 1 初筛阶段

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["candidates", "reading_order", "evaluation_criteria", "max_elimination"],
  "properties": {
    "candidates": {
      "type": "array",
      "items": { "type": "string" },
      "description": "候选方案路径/名称列表",
      "minItems": 2
    },
    "reading_order": {
      "type": "array",
      "items": { "type": "string" },
      "description": "打乱后的阅读顺序（消除顺序偏差）"
    },
    "evaluation_criteria": {
      "type": "array",
      "items": { "type": "string" },
      "description": "评审维度列表，如 ['架构设计', '实施可行性', '兼容性']"
    },
    "max_elimination": {
      "type": "integer",
      "default": 1,
      "description": "本轮最多淘汰方案数"
    },
    "evaluator_id": {
      "type": "string",
      "description": "评审员标识（如 Alpha, Beta, Gamma）"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["evaluator_id", "reading_order_confirmed", "quick_assessments", "elimination_decision"],
  "properties": {
    "evaluator_id": {
      "type": "string",
      "description": "评审员标识"
    },
    "reading_order_confirmed": {
      "type": "array",
      "items": { "type": "string" },
      "description": "确认的阅读顺序"
    },
    "quick_assessments": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "summary": { "type": "string", "description": "一句话评价" },
          "score": { "type": "number", "minimum": 1, "maximum": 10 },
          "strengths": { "type": "array", "items": { "type": "string" } },
          "weaknesses": { "type": "array", "items": { "type": "string" } }
        }
      },
      "description": "每个方案的快速评估"
    },
    "elimination_decision": {
      "type": "object",
      "required": ["eliminated", "reason", "confidence"],
      "properties": {
        "eliminated": {
          "type": "string",
          "description": "被淘汰的方案名"
        },
        "reason": {
          "type": "string",
          "description": "2-3句话淘汰理由"
        },
        "confidence": {
          "type": "string",
          "enum": ["High", "Medium", "Low"],
          "description": "淘汰决定的置信度"
        },
        "margin": {
          "type": "number",
          "description": "与次差方案的分差"
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "evaluation_duration": { "type": "string" },
        "criteria_weights_used": { "type": "object" }
      }
    }
  }
}
```

## 执行流程

1. **确认阅读顺序**
   - 按指定的打乱顺序阅读方案
   - 避免首位效应和近因效应

2. **快速扫描**
   - 每个方案用 1-2 分钟快速浏览
   - 记录第一印象和关键特征

3. **维度评分**
   - 按评审维度逐个打分
   - 使用 1-10 分制

4. **淘汰决策**
   - 识别最低分方案
   - 撰写淘汰理由
   - 评估决策置信度

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 独立性 | 评审不受其他评审员影响 | 100% |
| 全面性 | 覆盖所有评审维度 | ≥90% |
| 一致性 | 评分与理由逻辑一致 | 100% |
| 区分度 | 不同方案分数有区分 | 方差 ≥1.5 |

## 评分维度参考

### 架构设计
- 层次清晰度
- 模块解耦程度
- 可扩展性

### 实施可行性
- 工作量估算
- 技术栈匹配
- 资源依赖

### 兼容性
- 与现有系统的兼容
- 向后兼容性
- 迁移成本

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| vote-aggregator | 输出投票被其汇总 |
| multi-round-eval-orchestrator | 由其调度执行 |
| eval-engine | 可复用其评分框架 |

## 脚本

- `scripts/evaluate.py` - 评审主脚本
- `scripts/score_calculator.py` - 分数计算器

## 参考资料

- `references/screening-rubrics.md` - 初筛评分标准
