---
name: multi-round-eval-orchestrator
description: >
  多轮评审编排器。编排4轮评审流程：初筛淘汰→深度分析→对抗评审→复活与共识。
  管理并行评审员、淘汰机制、复活投票。由 evaluation-commander 调度。
---

# Multi-Round Eval Orchestrator — 多轮评审编排器

> 详细文档: [_architecture/L1-orchestrators/multi-round-eval-orchestrator/SKILL.md](_architecture/L1-orchestrators/multi-round-eval-orchestrator/SKILL.md)

## 编排流程

### Round 1: 初筛淘汰
1. 为每个评审员生成打乱的阅读顺序
2. 并行启动 N 个 `/initial-screener`
3. 调用 `/vote-aggregator` 汇总投票
4. 达到淘汰阈值的方案被淘汰

### Round 2: 深度缺陷分析
1. 为每个存活方案分配 `/defect-analyzer`
2. 并行执行深度分析
3. 调用 `/ranking-synthesizer` 综合排名
4. 检测排名冲突

### Round 3: 对抗评审
1. 调用 `/devils-advocate` 攻击排名第一方案
2. 如发现 Critical 缺陷，调用 `/final-candidate-reviewer` 检查第二名
3. 记录攻击报告

### Round 4: 复活与共识
1. 如 Round 3 发现 Critical，调用 `/resurrection-evaluator` 评估复活
2. 调用 `/final-candidate-reviewer` 最终检查
3. 调用 `/consensus-builder` 构建最终共识

## 并行策略

| 阶段 | 并行任务 |
|------|---------|
| Round 1 | N 个 initial-screener 并行 |
| Round 2 | M 个 defect-analyzer 并行 |
| Round 3 | 顺序执行 |
| Round 4 | resurrection + final-review 可并行 |

## 用户任务

$ARGUMENTS
