---
name: body-worker
description: >
  正文生成 Worker。无状态轻量正文生成器，根据标题和主题快速生成结构化正文，
  Token 消耗 <800。支持多种内容结构。
---

# Body Worker — 正文生成 (轻量)

> 详细文档: [_architecture/L2-execution/workers/body-worker/SKILL.md](_architecture/L2-execution/workers/body-worker/SKILL.md)

## Worker 规则

- 无状态, 纯函数执行
- Token 预算: <800
- 依赖标题输入

**结构模板**: xiaohongshu_flow / wechat_paragraphs / tweet_series / listicle / story / tutorial

**平台适配**: 小红书(500-1000字,短段落,emoji多) / 公众号(1500-3000字,完整段落) / Twitter(每条≤280字)

**输出**: 正文内容 + 分段 + 核心要点 + 金句 + 实际字数

## 生成任务

$ARGUMENTS

---

根据标题和主题快速生成结构化正文。
