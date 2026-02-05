---
name: resurrection-evaluator
description: >
  复活评估器。当 Round 3 发现领先方案有 Critical 缺陷时，评估被淘汰方案是否应复活。
  由 multi-round-eval-orchestrator 在 Round 4 条件触发。
---

# Resurrection Evaluator — 复活评估器

> 详细文档: [_architecture/L2-execution/extended/resurrection-evaluator/SKILL.md](_architecture/L2-execution/extended/resurrection-evaluator/SKILL.md)

## 复活条件评估

1. 被淘汰方案的原始缺陷是否被新发现覆盖
2. 相对于新第一名的优势
3. 重新评估后的排名

## 输出: 复活决定 + 理由 + 新排名

## 用户任务

$ARGUMENTS
