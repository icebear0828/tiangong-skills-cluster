---
name: platform-adapter
description: >
  平台内容适配 Skill。将通用内容适配到特定平台（小红书/公众号/Twitter），
  调整格式、长度、emoji、话题标签、CTA，确保符合平台规范。
---

# Platform Adapter — 平台适配

> 详细文档: [_architecture/L2-execution/core/platform-adapter/SKILL.md](_architecture/L2-execution/core/platform-adapter/SKILL.md)

## 执行协议

### 平台规格

| 平台 | 标题 | 正文 | 特殊要求 |
|------|------|------|---------|
| 小红书 | ≤20字 | 500-1000字 | emoji 每100字2-4个, 话题标签3-8个, 段落短 |
| 公众号 | ≤64字 | 1500-3000字 | 小标题分段, 金句加粗, 引导关注/分享 |
| Twitter | ≤280字/条 | 3-15条Thread | 编号连贯, 每条独立, 话题标签1-3个 |

### 适配检查清单

- [ ] 标题长度符合限制
- [ ] 正文字数在范围内
- [ ] emoji 密度合适
- [ ] 话题标签数量正确
- [ ] CTA 符合平台风格
- [ ] 无平台违禁词

### 输出格式

输出适配后的完整内容 + 适配报告 (调整了什么、为什么)。

## 适配任务

$ARGUMENTS

---

请将内容适配到目标平台，确保符合平台规范，输出适配版本和报告。
