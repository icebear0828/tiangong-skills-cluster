---
name: title-worker
description: >
  标题生成 Worker。无状态轻量标题生成器，快速生成多候选标题，Token 消耗 <500。
  支持数字型、悬念型、痛点型等多种风格。
---

# Title Worker — 标题生成 (轻量)

> 详细文档: [_architecture/L2-execution/workers/title-worker/SKILL.md](_architecture/L2-execution/workers/title-worker/SKILL.md)

## Worker 规则

- 无状态, 纯函数执行
- Token 预算: <500
- 生成 3 个候选标题, 选最佳

**标题风格**: 数字型 / 悬念型 / 痛点型 / 对比型 / 疑问型

**平台限制**: 小红书≤20字, 公众号≤64字, Twitter≤100字

**输出**: 3个候选 (title, style, score) + 推荐选择

## 生成任务

$ARGUMENTS

---

快速生成 3 个候选标题，评分排序，输出最佳推荐。
