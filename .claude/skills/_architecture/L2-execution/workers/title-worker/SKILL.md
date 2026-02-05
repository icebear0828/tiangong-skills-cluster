---
name: title-worker
description: >
  标题生成 Worker (L2 Worker)。无状态纯函数式标题生成器，专注于生成高吸引力标题。
  支持多种标题风格（数字型、悬念型、痛点型等），Token 消耗极低（<500）。
  由 adaptive-orchestrator 在蓝图执行中调用。
---

# Title Worker — 标题生成 Worker

## Worker 特性

| 特性 | 值 |
|------|-----|
| 状态 | 无状态 (Stateless) |
| 执行模式 | 纯函数 |
| Token 预算 | <500 tokens |
| 并行支持 | 支持多实例竞争生成 |

## 触发条件

- 由 adaptive-orchestrator 调度
- 蓝图步骤指定 `component: title-worker`
- 需要快速生成标题候选时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["topic", "platform"],
  "properties": {
    "topic": {
      "type": "string",
      "description": "写作主题/用户意图"
    },
    "platform": {
      "type": "string",
      "enum": ["xiaohongshu", "wechat", "twitter", "general"],
      "description": "目标平台"
    },
    "style": {
      "type": "string",
      "enum": ["professional", "casual", "humorous", "inspirational", "educational"],
      "default": "casual",
      "description": "内容风格"
    },
    "config": {
      "type": "object",
      "properties": {
        "variants": {
          "type": "integer",
          "default": 3,
          "minimum": 1,
          "maximum": 5,
          "description": "生成候选数量"
        },
        "title_styles": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["numeric", "suspense", "pain_point", "contrast", "question", "benefit", "urgency"]
          },
          "default": ["numeric", "suspense", "pain_point"],
          "description": "标题风格"
        },
        "length_limit": {
          "type": "integer",
          "description": "标题长度限制"
        },
        "must_include": {
          "type": "array",
          "items": { "type": "string" },
          "description": "必须包含的关键词"
        },
        "must_avoid": {
          "type": "array",
          "items": { "type": "string" },
          "description": "必须避免的词语"
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
  "required": ["variants", "selected"],
  "properties": {
    "variants": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["title", "style", "score"],
        "properties": {
          "title": {
            "type": "string",
            "description": "标题内容"
          },
          "style": {
            "type": "string",
            "description": "标题风格"
          },
          "score": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "description": "预估吸引力分数"
          },
          "rationale": {
            "type": "string",
            "description": "选择理由"
          }
        }
      },
      "description": "标题候选列表"
    },
    "selected": {
      "type": "string",
      "description": "推荐的最佳标题"
    },
    "selection_reason": {
      "type": "string",
      "description": "选择原因"
    }
  }
}
```

## 标题风格库

### 数字型 (numeric)
```
模式: [数字] + [关键词] + [利益点]
示例:
- "5个让你效率翻倍的AI工具"
- "3分钟学会的早餐食谱"
- "10条职场潜规则"
```

### 悬念型 (suspense)
```
模式: [悬念引子] + [意外结果]
示例:
- "用了这个方法后，我再也不..."
- "结果让我没想到..."
- "直到看到这个，我才明白..."
```

### 痛点型 (pain_point)
```
模式: [痛点描述] + [解决暗示]
示例:
- "还在为xxx烦恼？"
- "总是xxx？试试这个"
- "xxx的人一定要看"
```

### 对比型 (contrast)
```
模式: [Before] vs [After] / [旧认知] vs [新发现]
示例:
- "从月薪3k到年薪30w，我只做了这一件事"
- "以前xxx，现在xxx"
- "别人还在xxx，聪明人已经xxx"
```

### 疑问型 (question)
```
模式: [引发好奇的问题]
示例:
- "为什么xxx总是xxx？"
- "xxx真的有用吗？"
- "你知道xxx的秘密吗？"
```

### 利益型 (benefit)
```
模式: [直接利益承诺]
示例:
- "让你xxx的终极方法"
- "一招解决xxx问题"
- "xxx必备指南"
```

### 紧迫型 (urgency)
```
模式: [时间/数量限制] + [行动号召]
示例:
- "2024年最值得xxx"
- "错过这个再等一年"
- "最后xxx的机会"
```

## 平台适配规则

### 小红书
```json
{
  "max_length": 20,
  "preferred_styles": ["numeric", "pain_point", "suspense"],
  "emoji_usage": "moderate",
  "avoid": ["最好的", "第一", "绝对"]
}
```

### 微信公众号
```json
{
  "max_length": 64,
  "preferred_styles": ["question", "contrast", "benefit"],
  "emoji_usage": "minimal",
  "avoid": ["震惊", "不转不是"]
}
```

### Twitter
```json
{
  "max_length": 100,
  "preferred_styles": ["suspense", "contrast", "numeric"],
  "emoji_usage": "moderate",
  "include_thread_indicator": true
}
```

## 执行流程

```
1. 解析输入
   └─ 提取 topic, platform, style, config

2. 加载平台规则
   └─ 获取长度限制、偏好风格

3. 生成候选
   └─ 根据指定 styles 生成 variants 个候选

4. 评分排序
   └─ 对每个候选进行吸引力评分

5. 选择最佳
   └─ 返回最高分候选作为 selected

6. 输出结果
   └─ 组装输出对象
```

## 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 吸引力 | 30% | 是否引发好奇/点击欲望 |
| 清晰度 | 25% | 主题是否清晰表达 |
| 平台适配 | 20% | 是否符合平台风格 |
| 长度适当 | 15% | 是否在最佳长度范围 |
| 独特性 | 10% | 是否有差异化 |

## 示例

### 输入
```json
{
  "topic": "AI工具提升工作效率",
  "platform": "xiaohongshu",
  "style": "casual",
  "config": {
    "variants": 3,
    "title_styles": ["numeric", "pain_point", "suspense"],
    "length_limit": 20
  }
}
```

### 输出
```json
{
  "variants": [
    {
      "title": "5个AI神器让你下班早2小时",
      "style": "numeric",
      "score": 88,
      "rationale": "数字+具体利益，吸引力强"
    },
    {
      "title": "还在手动做表？这些AI太香了",
      "style": "pain_point",
      "score": 82,
      "rationale": "痛点共鸣+口语化"
    },
    {
      "title": "用了这些AI后我被老板表扬了",
      "style": "suspense",
      "score": 79,
      "rationale": "故事性+好奇心"
    }
  ],
  "selected": "5个AI神器让你下班早2小时",
  "selection_reason": "数字型标题在小红书表现最佳，具体利益点明确"
}
```

## 与黑板的交互

### 读取切片
```json
{
  "scope": ["meta.intent", "meta.platform", "meta.style"]
}
```

### 写入结果
```json
{
  "target": "content.hook.variants",
  "select_best_target": "content.hook.selected"
}
```

## 错误处理

| 错误类型 | 处理方式 |
|----------|---------|
| 输入不完整 | 返回错误，要求补充 |
| 平台未知 | 使用 general 规则 |
| 生成失败 | 重试一次，仍失败则返回空 |

## 性能指标

| 指标 | 目标值 |
|------|--------|
| Token 消耗 | <300 tokens |
| 执行延迟 | <500ms |
| 候选质量 | 平均分 ≥75 |
