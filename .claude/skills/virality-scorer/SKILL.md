---
name: virality-scorer
description: >
  传播力评分 Skill。分析内容的病毒传播潜力，评估多维度传播系数，
  提供互动优化建议。覆盖 Hook 吸引力、情感共鸣、社交货币等维度。
---

# Virality Scorer — 传播力评分

> 详细文档: [_architecture/L2-execution/core/virality-scorer/SKILL.md](_architecture/L2-execution/core/virality-scorer/SKILL.md)

## 执行协议

### 评分维度

| 维度 | 权重 | 评估要点 |
|------|------|---------|
| Hook 吸引力 | 25% | 标题/开头是否引发好奇 |
| 情感共鸣度 | 25% | 是否触发情感反应 |
| 社交货币 | 20% | 分享是否让人显得聪明/有品位 |
| 实用价值 | 15% | 是否提供可操作的价值 |
| 话题讨论性 | 15% | 是否容易引发讨论 |

### 输出格式

```
Overall Score: XX/100
├─ Hook 吸引力: XX/100
├─ 情感共鸣度: XX/100
├─ 社交货币: XX/100
├─ 实用价值: XX/100
└─ 话题讨论性: XX/100

优化建议:
1. ...
2. ...

互动设计:
- 评论引导: ...
- 分享动机: ...
- CTA 建议: ...
```

## 评分任务

$ARGUMENTS

---

请对内容进行全面传播力分析，输出各维度评分和优化建议。
