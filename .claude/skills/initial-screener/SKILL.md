---
name: initial-screener
description: >
  初筛评审员。独立评审多个方案，按维度打分，选择最差方案淘汰。
  支持打乱阅读顺序消除偏差。由 multi-round-eval-orchestrator 在 Round 1 调度。
---

# Initial Screener — 初筛评审员

> 详细文档: [_architecture/L2-execution/core/initial-screener/SKILL.md](_architecture/L2-execution/core/initial-screener/SKILL.md)

## 执行流程

1. **按打乱顺序阅读**所有候选方案
2. **逐维度评分** (1-10分)：架构设计、实施可行性、兼容性等
3. **识别最差方案**并撰写淘汰理由
4. **输出**: 每个方案的快速评估 + 淘汰决定 + 置信度

## 输出格式

```json
{
  "evaluator_id": "Alpha",
  "quick_assessments": { "方案A": { "score": 8, "summary": "..." }, ... },
  "elimination_decision": { "eliminated": "方案C", "reason": "...", "confidence": "High" }
}
```

## 用户任务

$ARGUMENTS
