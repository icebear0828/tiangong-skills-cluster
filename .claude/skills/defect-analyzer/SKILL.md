---
name: defect-analyzer
description: >
  缺陷分析器。深度分析方案缺陷，生成 Top 缺陷清单和严重度评级。
  支持多角度分析。由 multi-round-eval-orchestrator 在 Round 2 调度。
---

# Defect Analyzer — 缺陷分析器

> 详细文档: [_architecture/L2-execution/core/defect-analyzer/SKILL.md](_architecture/L2-execution/core/defect-analyzer/SKILL.md)

## 执行流程

1. **深度阅读**方案文档，理解核心设计
2. **多角度分析**: architecture / implementation / scalability / security / performance / compatibility / cost
3. **缺陷分级**: Critical / High / Medium / Low
4. **综合评分**: 各维度评分 + 总分 + 排名建议

## 严重度定义

| 等级 | 影响 |
|------|------|
| Critical | 使方案完全无法工作 |
| High | 需要重大修改 |
| Medium | 需要一定工作量修复 |
| Low | 可接受或易修复 |

## 用户任务

$ARGUMENTS
