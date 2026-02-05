---
name: confidence-calculator
description: >
  置信度计算器。基于评审过程数据计算决策置信度，识别不确定性来源。
  由 multi-round-eval-orchestrator 在 Round 4 调度。
---

# Confidence Calculator — 置信度计算器

> 详细文档: [_architecture/L2-execution/extended/confidence-calculator/SKILL.md](_architecture/L2-execution/extended/confidence-calculator/SKILL.md)

## 置信度影响因素

| 因素 | 正向 | 负向 |
|------|------|------|
| 一致性 | 评审员高度一致 | 严重分歧 |
| 稳定性 | 排名稳定 | 排名波动大 |
| 对抗结果 | 经受住攻击 | 发现 Critical |
| 差距 | 领先明显 | 差距微小 |

## 输出: 置信度分数 + 等级 + 不确定性来源

## 用户任务

$ARGUMENTS
