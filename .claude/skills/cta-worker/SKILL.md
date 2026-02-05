---
name: cta-worker
description: >
  CTA 生成 Worker。无状态轻量行动号召生成器，Token 消耗 <300。
  支持关注、点赞、收藏、评论、分享等多种 CTA 类型。
---

# CTA Worker — 行动号召生成 (轻量)

> 详细文档: [_architecture/L2-execution/workers/cta-worker/SKILL.md](_architecture/L2-execution/workers/cta-worker/SKILL.md)

## Worker 规则

- 无状态, 纯函数执行
- Token 预算: <300

**CTA 类型**: follow / like / save / comment / share / subscribe / retweet / reply

**风格**: soft_sell (温和) / direct (直接) / conversational (对话) / playful (俏皮) / professional (专业)

**平台偏好**:
- 小红书: save + follow + comment, 风格 soft_sell
- 公众号: share + like + follow, 风格 direct
- Twitter: retweet + reply + follow, 风格 conversational

**输出**: 主CTA + 次CTA + 类型 + 放置建议

## 生成任务

$ARGUMENTS

---

根据平台和内容生成合适的 CTA 文案。
