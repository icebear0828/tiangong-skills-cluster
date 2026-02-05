---
name: multi-round-eval-orchestrator
description: >
  多轮评审编排器。编排4轮评审流程，管理复活机制和共识投票。当需要：
  (1) 多方案对比评审，(2) 对抗性评估，(3) 共识决策时触发。
  支持并行评审、淘汰机制、复活投票。由 evaluation-commander 调度触发。
---

# Multi-Round Eval Orchestrator — 多轮评审编排器

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["candidates", "candidate_paths"],
  "properties": {
    "candidates": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 2,
      "maxItems": 10,
      "description": "候选方案名称列表"
    },
    "candidate_paths": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "候选名称到文件路径的映射"
    },
    "config": {
      "type": "object",
      "properties": {
        "round1_screeners": {
          "type": "integer",
          "default": 3,
          "description": "Round 1 评审员数量"
        },
        "elimination_threshold": {
          "type": "integer",
          "default": 2,
          "description": "淘汰所需票数"
        },
        "round2_analyzers": {
          "type": "integer",
          "default": 3,
          "description": "Round 2 分析员数量"
        },
        "round3_devils_advocates": {
          "type": "integer",
          "default": 1,
          "description": "Round 3 对抗评审员数量"
        },
        "consensus_threshold": {
          "type": "integer",
          "default": 5,
          "description": "共识投票票数"
        },
        "enable_resurrection": {
          "type": "boolean",
          "default": true,
          "description": "是否启用复活机制"
        },
        "max_iterations": {
          "type": "integer",
          "default": 1,
          "description": "每轮最大迭代次数"
        }
      },
      "description": "评审配置"
    },
    "evaluation_criteria": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["架构设计", "实施可行性", "兼容性", "可扩展性", "维护成本"],
      "description": "评审维度"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["rounds", "final_recommendation"],
  "properties": {
    "rounds": {
      "type": "object",
      "properties": {
        "round1": {
          "type": "object",
          "properties": {
            "eliminated": { "type": "array", "items": { "type": "string" } },
            "survivors": { "type": "array", "items": { "type": "string" } },
            "votes": { "type": "array" },
            "consensus_level": { "type": "string" }
          }
        },
        "round2": {
          "type": "object",
          "properties": {
            "ranking": { "type": "array", "items": { "type": "string" } },
            "scores": { "type": "object" },
            "conflicts": { "type": "boolean" },
            "defect_summary": { "type": "object" }
          }
        },
        "round3": {
          "type": "object",
          "properties": {
            "attacked": { "type": "array", "items": { "type": "string" } },
            "critical_found": { "type": "boolean" },
            "attack_results": { "type": "array" }
          }
        },
        "round4": {
          "type": "object",
          "properties": {
            "resurrected": { "type": "array", "items": { "type": "string" } },
            "final_eliminated": { "type": "array", "items": { "type": "string" } },
            "final_ranking": { "type": "array" }
          }
        }
      }
    },
    "final_recommendation": {
      "type": "object",
      "required": ["winner", "confidence"],
      "properties": {
        "winner": { "type": "string" },
        "runner_up": { "type": "string" },
        "confidence": { "type": "string", "enum": ["Very High", "High", "Medium", "Low"] },
        "decision_path": { "type": "string", "enum": ["A", "B", "C"] },
        "summary": { "type": "string" }
      }
    },
    "execution_log": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "round": { "type": "string" },
          "action": { "type": "string" },
          "result": { "type": "object" },
          "timestamp": { "type": "string" }
        }
      }
    }
  }
}
```

## 四轮评审流程

### Round 1: 初筛淘汰

```
┌─────────────────────────────────────────────┐
│  输入: 全部候选方案                           │
│                                             │
│  1. 为每个评审员生成打乱的阅读顺序            │
│  2. 并行启动 N 个 initial-screener           │
│  3. 收集所有投票                             │
│  4. 调用 vote-aggregator 汇总               │
│  5. 达到阈值的方案被淘汰                      │
│                                             │
│  输出: 存活方案列表                           │
└─────────────────────────────────────────────┘
```

**质量关卡**:
- 至少淘汰 1 个方案
- 投票一致性 ≥ 60%

### Round 2: 深度缺陷分析

```
┌─────────────────────────────────────────────┐
│  输入: Round 1 存活方案                       │
│                                             │
│  1. 为每个方案分配 defect-analyzer           │
│  2. 并行执行深度分析                          │
│  3. 收集缺陷报告和评分                        │
│  4. 调用 ranking-synthesizer 综合排名        │
│  5. 检测排名冲突                             │
│                                             │
│  输出: 综合排名 + 缺陷清单                    │
└─────────────────────────────────────────────┘
```

**质量关卡**:
- 每个方案至少 3 个缺陷被识别
- 排名冲突已记录

### Round 3: 对抗评审

```
┌─────────────────────────────────────────────┐
│  输入: Round 2 排名第一的方案                 │
│                                             │
│  1. 调用 devils-advocate 攻击第一名          │
│  2. 如发现 Critical 缺陷:                    │
│     a. 调用 final-candidate-reviewer         │
│        检查第二名                            │
│     b. 可能触发排名调整                       │
│  3. 记录攻击报告                             │
│                                             │
│  输出: 攻击结果 + 是否需要调整                │
└─────────────────────────────────────────────┘
```

**质量关卡**:
- 7 个攻击问题全部回答
- Critical 缺陷有确认

### Round 4: 复活与共识

```
┌─────────────────────────────────────────────┐
│  输入: Round 3 结果 + Round 1 被淘汰方案      │
│                                             │
│  1. 如果 Round 3 发现 Critical:              │
│     a. 调用 resurrection-evaluator           │
│        评估被淘汰方案是否复活                 │
│  2. 调用 final-candidate-reviewer            │
│     对所有存活方案最终检查                    │
│  3. 调用 consensus-builder 构建共识          │
│                                             │
│  输出: 最终推荐 + 置信度                      │
└─────────────────────────────────────────────┘
```

**质量关卡**:
- 共识等级 ≥ moderate
- 置信度 ≥ Medium

## 复活机制

当 Round 3 对第一名发现 Critical 缺陷时触发:

1. **复活条件评估**
   - Round 1 被淘汰方案的缺陷是否已被新发现覆盖
   - 相对于新第一名的优势

2. **复活投票**
   - 重新评估被淘汰方案
   - 与当前存活方案比较

3. **决策路径变更**
   - 路径类型变为 "C"
   - 置信度降低

## 并行执行策略

| 阶段 | 可并行任务 |
|------|-----------|
| Round 1 | N 个 initial-screener 并行 |
| Round 2 | M 个 defect-analyzer 并行 |
| Round 3 | 顺序执行（依赖 Round 2 结果）|
| Round 4 | resurrection + final-review 可并行 |

## Context 管理

- 每轮之间只传递结构化摘要
- 完整报告通过文件路径引用
- 编排器 context 预算: ≤20% 总 context

## 错误处理

| 错误类型 | 处理策略 |
|---------|---------|
| 评审员超时 | 重试 1 次，然后用剩余评审员结果 |
| 投票不足 | 降低阈值或增加评审员 |
| 共识失败 | 记录分歧，人工介入 |
| 复活冲突 | 使用加权投票决定 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| initial-screener | 调用 | Round 1 |
| vote-aggregator | 调用 | Round 1, 4 |
| defect-analyzer | 调用 | Round 2 |
| ranking-synthesizer | 调用 | Round 2 |
| devils-advocate | 调用 | Round 3 |
| final-candidate-reviewer | 调用 | Round 3, 4 |
| resurrection-evaluator | 调用 | Round 4 |
| consensus-builder | 调用 | Round 4 |
| evaluation-commander | 被调用 | 由其调度 |

## 脚本

- `scripts/orchestrate.py` - 编排主脚本
- `scripts/shuffle.py` - 随机打乱工具
- `scripts/aggregate_results.py` - 结果汇总器

## 参考资料

- `references/orchestration-patterns.md` - 编排模式
- `references/quality-gates.md` - 质量关卡定义
