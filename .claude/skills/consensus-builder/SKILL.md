---
name: consensus-builder
description: >
  共识构建器。综合所有轮次评审结果，构建最终推荐和置信度等级。
  追溯决策路径，记录异议。由 multi-round-eval-orchestrator 在 Round 4 调度。
---

# Consensus Builder — 共识构建器

> 详细文档: [_architecture/L2-execution/core/consensus-builder/SKILL.md](_architecture/L2-execution/core/consensus-builder/SKILL.md)

## 执行流程

1. **结果汇总**: 收集 Round 1-4 所有结果
2. **冲突检测**: 识别轮次间矛盾和异议
3. **路径分析**: 追溯决策路径 (A=早期胜出 / B=对抗后确认 / C=复活后胜出)
4. **置信度计算**: 综合评估影响因素
5. **最终推荐**: winner + runner_up + 置信度 + 理由

## 置信度等级

| 等级 | 分数 | 描述 |
|------|------|------|
| Very High | ≥0.9 | 高度确信 |
| High | 0.8-0.9 | 较有把握 |
| Medium | 0.6-0.8 | 中等确信 |
| Low | <0.6 | 存在疑虑 |

## 用户任务

$ARGUMENTS
