---
name: ranking-synthesizer
description: >
  排名综合器。综合多个评审员的排名结果，支持 Borda/Schulze/加权平均算法，检测排名冲突。
  由 multi-round-eval-orchestrator 在 Round 2 调度。
---

# Ranking Synthesizer — 排名综合器

> 详细文档: [_architecture/L2-execution/extended/ranking-synthesizer/SKILL.md](_architecture/L2-execution/extended/ranking-synthesizer/SKILL.md)

## 排名算法

| 算法 | 适用场景 |
|------|---------|
| weighted_average (默认) | 按置信度加权，兼顾速度和公平 |
| borda | 等权重评审员 |
| schulze | 需要公平处理排名冲突 |

## 输出: 综合排名 + 冲突分析 (Kendall tau 系数)

## 用户任务

$ARGUMENTS
