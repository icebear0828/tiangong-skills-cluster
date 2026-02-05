---
name: cta-worker
description: >
  CTA (Call-to-Action) 生成 Worker (L2 Worker)。无状态纯函数式行动号召生成器。
  专注于生成引导用户互动的结尾文案，支持关注、点赞、收藏、评论、分享等多种 CTA 类型。
  Token 消耗极低（<300），由 adaptive-orchestrator 在蓝图执行中调用。
---

# CTA Worker — 行动号召生成 Worker

## Worker 特性

| 特性 | 值 |
|------|-----|
| 状态 | 无状态 (Stateless) |
| 执行模式 | 纯函数 |
| Token 预算 | <300 tokens |
| 并行支持 | 不支持（依赖标题/正文） |

## 触发条件

- 由 adaptive-orchestrator 调度
- 蓝图步骤指定 `component: cta-worker`
- 标题/正文已生成，需要生成结尾 CTA 时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["platform"],
  "properties": {
    "platform": {
      "type": "string",
      "enum": ["xiaohongshu", "wechat", "twitter", "general"],
      "description": "目标平台"
    },
    "title": {
      "type": "string",
      "description": "内容标题（用于呼应）"
    },
    "content_summary": {
      "type": "string",
      "description": "内容摘要（可选，用于个性化 CTA）"
    },
    "config": {
      "type": "object",
      "properties": {
        "cta_types": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["follow", "like", "save", "comment", "share", "click", "subscribe", "reply", "retweet", "bookmark"]
          },
          "default": ["follow", "save", "comment"],
          "description": "期望的 CTA 类型"
        },
        "style": {
          "type": "string",
          "enum": ["soft_sell", "direct", "conversational", "playful", "professional"],
          "default": "soft_sell",
          "description": "CTA 风格"
        },
        "include_emoji": {
          "type": "boolean",
          "default": true,
          "description": "是否包含 emoji"
        },
        "max_length": {
          "type": "integer",
          "default": 100,
          "description": "最大字数"
        }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["primary", "type"],
  "properties": {
    "primary": {
      "type": "string",
      "description": "主要 CTA 文案"
    },
    "secondary": {
      "type": "string",
      "description": "次要 CTA 文案（可选）"
    },
    "type": {
      "type": "string",
      "description": "主要 CTA 类型"
    },
    "variants": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": { "type": "string" },
          "type": { "type": "string" },
          "style": { "type": "string" }
        }
      },
      "description": "其他 CTA 候选"
    },
    "placement_suggestion": {
      "type": "string",
      "enum": ["end_of_content", "separate_paragraph", "inline"],
      "description": "建议放置位置"
    }
  }
}
```

## CTA 类型库

### 关注型 (follow)
```
目的: 引导用户关注账号
小红书: "关注我，持续分享xxx干货~"
公众号: "点击关注，第一时间获取最新文章"
Twitter: "Follow for more insights on xxx"
```

### 点赞型 (like)
```
目的: 引导用户点赞
小红书: "觉得有用就点个赞吧~"
公众号: "如果觉得有收获，点个在看"
Twitter: "Like if this helped you!"
```

### 收藏型 (save)
```
目的: 引导用户收藏
小红书: "建议收藏慢慢看，下次用到就不慌了"
公众号: "收藏本文，随时查阅"
Twitter: "Bookmark this thread for later"
```

### 评论型 (comment)
```
目的: 引导用户评论互动
小红书: "你还知道哪些好用的？评论区告诉我~"
公众号: "你怎么看？留言区聊聊"
Twitter: "What's your experience with xxx? Reply below!"
```

### 分享型 (share)
```
目的: 引导用户分享
小红书: "分享给需要的朋友吧~"
公众号: "转发给需要的人，功德无量"
Twitter: "RT to share with your followers"
```

### 订阅型 (subscribe)
```
目的: 引导用户订阅
公众号: "长按识别二维码关注"
Twitter: "Turn on notifications to never miss a thread"
```

## 风格库

### 软性销售 (soft_sell)
```
特点: 温和引导，不强制
示例:
- "觉得有用的话..."
- "如果帮到你了..."
- "有需要的姐妹..."
```

### 直接型 (direct)
```
特点: 明确告知行动
示例:
- "现在就点击关注"
- "马上收藏这篇文章"
- "立即转发给朋友"
```

### 对话型 (conversational)
```
特点: 像朋友聊天
示例:
- "你们觉得呢？"
- "有什么想问的吗？"
- "下次想看什么内容？"
```

### 俏皮型 (playful)
```
特点: 活泼有趣
示例:
- "点赞的人运气都不会差~"
- "收藏不迷路，下次还能找到我"
- "评论区见！等你来撩~"
```

### 专业型 (professional)
```
特点: 正式专业
示例:
- "更多行业洞察，欢迎关注"
- "如需深入讨论，欢迎私信交流"
- "期待与您进一步探讨"
```

## 平台适配规则

### 小红书
```json
{
  "preferred_types": ["save", "follow", "comment"],
  "preferred_style": "soft_sell",
  "emoji_usage": "high",
  "max_length": 80,
  "avoid": ["点击链接", "私聊"]
}
```

### 微信公众号
```json
{
  "preferred_types": ["share", "like", "follow"],
  "preferred_style": "direct",
  "emoji_usage": "low",
  "max_length": 100,
  "include_qrcode_hint": true
}
```

### Twitter
```json
{
  "preferred_types": ["retweet", "reply", "follow"],
  "preferred_style": "conversational",
  "emoji_usage": "medium",
  "max_length": 100,
  "thread_aware": true
}
```

## 执行流程

```
1. 解析输入
   └─ 提取 platform, title, config

2. 确定 CTA 类型
   └─ 根据 config.cta_types 和平台偏好

3. 选择风格
   └─ 根据 config.style 和平台规则

4. 生成主 CTA
   └─ 组合类型+风格+平台规则

5. 生成次 CTA (可选)
   └─ 补充其他互动引导

6. 应用格式
   └─ 添加 emoji、调整长度

7. 输出结果
   └─ 组装输出对象
```

## 示例

### 输入
```json
{
  "platform": "xiaohongshu",
  "title": "5个AI神器让你下班早2小时",
  "config": {
    "cta_types": ["follow", "save", "comment"],
    "style": "soft_sell",
    "include_emoji": true
  }
}
```

### 输出
```json
{
  "primary": "觉得有用记得点赞收藏，下次需要就不用翻了~",
  "secondary": "还想看什么AI工具推荐？评论区告诉我",
  "type": "save",
  "variants": [
    {
      "text": "关注我，持续分享效率干货",
      "type": "follow",
      "style": "soft_sell"
    },
    {
      "text": "你在用哪些AI工具？评论区聊聊~",
      "type": "comment",
      "style": "conversational"
    }
  ],
  "placement_suggestion": "end_of_content"
}
```

## 组合 CTA 模板

### 小红书万能组合
```
[收藏] + [关注] + [评论互动]
"觉得有用记得收藏，关注我获取更多干货~ 你还用过什么好工具？评论区分享一下呀"
```

### 公众号标准组合
```
[点在看] + [转发] + [关注]
"如果觉得有收获，点个在看让更多人看到。欢迎转发给需要的朋友，关注我获取更多精彩内容。"
```

### Twitter Thread 结尾
```
[Follow] + [RT] + [Reply]
"If you found this helpful:
1. Follow @xxx for more threads
2. RT to share with your network
3. Reply with your thoughts!"
```

## 与黑板的交互

### 读取切片
```json
{
  "scope": ["meta.platform", "content.hook.selected"]
}
```

### 写入结果
```json
{
  "target": "content.cta"
}
```

## 错误处理

| 错误类型 | 处理方式 |
|----------|---------|
| 平台未知 | 使用 general 规则 |
| CTA 类型不支持 | 使用平台默认类型 |
| 生成失败 | 返回平台通用 CTA |

## 性能指标

| 指标 | 目标值 |
|------|--------|
| Token 消耗 | <200 tokens |
| 执行延迟 | <300ms |
| 适配准确率 | ≥95% |
