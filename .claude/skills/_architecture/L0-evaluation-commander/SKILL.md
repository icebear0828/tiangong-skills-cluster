---
name: evaluation-commander
description: >
  评审总指挥 Skill (L0)。评审任务的第一入口点，负责任务路由、轮次调度、最终决策生成。
  当需要：(1) 多方案评审，(2) 对抗性评估，(3) 评审流程调度时触发。
  分析评审复杂度，选择评审模式，路由到对应编排器。作为 L0 层 Skill，具有严格契约。
---

# Evaluation Commander — 评审总指挥

## 触发条件

- 用户任务包含"评审"、"对比"、"选择最佳"、"评估方案"等关键词
- 输入包含多个候选方案
- 由 meta-commander 路由到评审域

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["task_description"],
  "properties": {
    "task_description": {
      "type": "string",
      "description": "评审任务描述"
    },
    "candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "path": { "type": "string" },
          "description": { "type": "string" }
        }
      },
      "description": "候选方案列表"
    },
    "evaluation_mode": {
      "type": "string",
      "enum": ["quick", "standard", "thorough", "adversarial"],
      "default": "standard",
      "description": "评审模式"
    },
    "criteria": {
      "type": "array",
      "items": { "type": "string" },
      "description": "评审维度"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "max_rounds": { "type": "integer" },
        "time_budget": { "type": "string" },
        "must_have": { "type": "array", "items": { "type": "string" } },
        "must_not_have": { "type": "array", "items": { "type": "string" } }
      },
      "description": "评审约束"
    },
    "context": {
      "type": "object",
      "properties": {
        "background": { "type": "string" },
        "stakeholders": { "type": "array", "items": { "type": "string" } },
        "decision_urgency": { "type": "string", "enum": ["low", "medium", "high"] }
      },
      "description": "评审上下文"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["evaluation_result", "decision"],
  "properties": {
    "task_analysis": {
      "type": "object",
      "properties": {
        "complexity": { "type": "string", "enum": ["S", "M", "L", "XL"] },
        "candidate_count": { "type": "integer" },
        "selected_mode": { "type": "string" },
        "estimated_rounds": { "type": "integer" }
      },
      "description": "任务分析结果"
    },
    "evaluation_result": {
      "type": "object",
      "properties": {
        "ranking": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "rank": { "type": "integer" },
              "candidate": { "type": "string" },
              "score": { "type": "number" },
              "summary": { "type": "string" }
            }
          }
        },
        "eliminated": {
          "type": "array",
          "items": { "type": "string" }
        },
        "detailed_reports": {
          "type": "array",
          "items": { "type": "string" },
          "description": "详细报告文件路径"
        }
      },
      "description": "评审结果"
    },
    "decision": {
      "type": "object",
      "required": ["recommendation", "confidence"],
      "properties": {
        "recommendation": {
          "type": "string",
          "description": "最终推荐方案"
        },
        "confidence": {
          "type": "string",
          "enum": ["Very High", "High", "Medium", "Low", "Very Low"]
        },
        "rationale": {
          "type": "string",
          "description": "推荐理由"
        },
        "caveats": {
          "type": "array",
          "items": { "type": "string" },
          "description": "注意事项"
        },
        "alternative": {
          "type": "string",
          "description": "备选推荐"
        }
      },
      "description": "最终决策"
    },
    "process_summary": {
      "type": "object",
      "properties": {
        "rounds_executed": { "type": "integer" },
        "total_evaluators": { "type": "integer" },
        "key_turning_points": { "type": "array", "items": { "type": "string" } },
        "decision_path": { "type": "string" }
      },
      "description": "流程摘要"
    }
  }
}
```

## 评审模式

| 模式 | 轮次 | 评审员 | 适用场景 |
|------|------|--------|---------|
| quick | 1 | 1 | 2个方案快速对比 |
| standard | 2 | 3 | 常规方案评审 |
| thorough | 4 | 5+ | 重要决策全面评审 |
| adversarial | 4 | 7+ | 高风险对抗评审 |

## 复杂度判定

| 复杂度 | 候选数 | 维度数 | 推荐模式 |
|--------|--------|--------|---------|
| S | 2 | ≤3 | quick |
| M | 3-4 | 3-5 | standard |
| L | 5-7 | 5-7 | thorough |
| XL | 8+ | 7+ | adversarial |

## 执行流程

1. **任务分析**
   - 解析任务描述
   - 识别候选方案
   - 提取评审维度
   - 判定复杂度

2. **模式选择**
   - 根据复杂度选择模式
   - 考虑用户指定的约束
   - 确定评审配置

3. **编排调度**
   - 调用 multi-round-eval-orchestrator
   - 传递配置和候选
   - 监控执行进度

4. **结果整合**
   - 接收编排器结果
   - 生成最终决策
   - 汇总流程摘要

5. **输出交付**
   - 格式化输出
   - 生成详细报告
   - 返回推荐决策

## 路由规则

```
评审任务 → evaluation-commander
    │
    ├─ 2个方案 + 无特殊要求 → quick 模式（直接对比）
    │
    ├─ 3-4个方案 + 标准要求 → standard 模式
    │   └─ multi-round-eval-orchestrator (Round 1-2)
    │
    ├─ 5+个方案 或 重要决策 → thorough 模式
    │   └─ multi-round-eval-orchestrator (Round 1-4)
    │
    └─ 高风险 或 adversarial 指定 → adversarial 模式
        └─ multi-round-eval-orchestrator (Round 1-4 + 增强)
```

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 任务理解 | 正确识别所有候选 | 100% |
| 模式适配 | 模式与复杂度匹配 | 正确 |
| 决策透明 | 理由可追溯 | 100% |
| 置信度准确 | 置信度与过程一致 | 合理 |

## 异常处理

| 异常 | 处理策略 |
|------|---------|
| 候选不足 | 要求补充或单方案评估 |
| 维度缺失 | 使用默认维度 |
| 编排失败 | 降级到 quick 模式 |
| 无法达成共识 | 输出分歧报告，建议人工决策 |

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| meta-commander | 被调用 | 由其路由评审任务 |
| multi-round-eval-orchestrator | 调用 | 编排多轮评审 |
| eval-engine | 集成 | 复用评分框架 |
| consensus-builder | 间接调用 | 通过编排器 |

## 能力边界

**能处理**:
- 方案对比评审
- 多维度评估
- 对抗性检验
- 共识决策

**不处理**:
- 方案生成（由其他 Skill 处理）
- 方案实施（评审后流程）
- 非方案类评审（如代码审查，由 code-review 处理）

## 脚本

- `scripts/analyze_task.py` - 任务分析脚本
- `scripts/select_mode.py` - 模式选择脚本
- `scripts/generate_report.py` - 报告生成脚本

## 参考资料

- `references/evaluation-routing-rules.md` - 评审路由规则
- `references/evaluation-capability-map.md` - 评审能力映射
- `references/evaluation-modes.md` - 评审模式详解
