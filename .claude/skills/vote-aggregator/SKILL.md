---
name: vote-aggregator
description: >
  投票汇总器。汇总多个评审员投票，计算加权票数，判断淘汰阈值，分析共识程度。
  由 multi-round-eval-orchestrator 在 Round 1/4 调度。
---

# Vote Aggregator — 投票汇总器

> 详细文档: [_architecture/L2-execution/core/vote-aggregator/SKILL.md](_architecture/L2-execution/core/vote-aggregator/SKILL.md)

## 执行流程

1. **收集投票**: 验证所有评审员已提交
2. **票数统计**: 原始票数 + 置信度加权
3. **阈值判定**: 加权票数 vs 淘汰阈值
4. **共识分析**: 一致性比例、冲突检测

## 共识等级

| 等级 | 一致性 | 描述 |
|------|--------|------|
| unanimous | 100% | 全票一致 |
| strong | ≥80% | 强共识 |
| moderate | ≥60% | 中等共识 |
| weak | ≥40% | 弱共识 |
| split | <40% | 分裂 |

## 用户任务

$ARGUMENTS
