---
name: body-worker
description: >
  正文生成 Worker (L2 Worker)。无状态纯函数式正文生成器，根据标题和主题生成结构化正文内容。
  支持多种内容结构（小红书流、公众号段落、Thread 系列等），Token 消耗低（<800）。
  由 adaptive-orchestrator 在蓝图执行中调用。
---

# Body Worker — 正文生成 Worker

## Worker 特性

| 特性 | 值 |
|------|-----|
| 状态 | 无状态 (Stateless) |
| 执行模式 | 纯函数 |
| Token 预算 | <800 tokens |
| 并行支持 | 不支持（依赖标题） |

## 触发条件

- 由 adaptive-orchestrator 调度
- 蓝图步骤指定 `component: body-worker`
- 标题已生成，需要生成正文时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["topic", "title"],
  "properties": {
    "topic": {
      "type": "string",
      "description": "写作主题/用户意图"
    },
    "title": {
      "type": "string",
      "description": "已确定的标题"
    },
    "platform": {
      "type": "string",
      "enum": ["xiaohongshu", "wechat", "twitter", "general"],
      "default": "general",
      "description": "目标平台"
    },
    "config": {
      "type": "object",
      "properties": {
        "word_count": {
          "type": "object",
          "properties": {
            "min": { "type": "integer", "default": 300 },
            "max": { "type": "integer", "default": 800 }
          }
        },
        "structure": {
          "type": "string",
          "enum": ["xiaohongshu_flow", "wechat_paragraphs", "tweet_series", "listicle", "story", "tutorial"],
          "default": "xiaohongshu_flow",
          "description": "内容结构"
        },
        "emoji_density": {
          "type": "string",
          "enum": ["none", "low", "medium", "medium-high", "high"],
          "default": "medium"
        },
        "paragraph_style": {
          "type": "string",
          "enum": ["short", "medium", "long"],
          "default": "short"
        },
        "include_sections": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["hook", "problem", "solution", "examples", "tips", "cta"]
          },
          "default": ["hook", "solution", "tips", "cta"]
        }
      }
    },
    "constraints": {
      "type": "object",
      "properties": {
        "must_include": {
          "type": "array",
          "items": { "type": "string" },
          "description": "必须包含的内容点"
        },
        "must_avoid": {
          "type": "array",
          "items": { "type": "string" },
          "description": "必须避免的内容"
        },
        "tone": {
          "type": "string",
          "description": "语气要求"
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
  "required": ["content", "word_count"],
  "properties": {
    "content": {
      "type": "string",
      "description": "生成的正文内容"
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "content": { "type": "string" }
        }
      },
      "description": "分段内容（如果适用）"
    },
    "key_points": {
      "type": "array",
      "items": { "type": "string" },
      "description": "核心要点"
    },
    "quotes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "金句/可摘录句"
    },
    "word_count": {
      "type": "integer",
      "description": "实际字数"
    },
    "emoji_count": {
      "type": "integer",
      "description": "emoji 数量"
    }
  }
}
```

## 内容结构模板

### 小红书流 (xiaohongshu_flow)
```
结构:
1. 开场钩子 (1-2句，直击痛点/引发好奇)
2. 问题共鸣 (2-3句，描述读者可能的困境)
3. 解决方案 (核心内容，分点列举)
4. 使用心得/案例 (增加可信度)
5. 总结+互动引导

特点:
- 短段落（每段2-4句）
- emoji 点缀（每100字2-4个）
- 口语化表达
- 适当换行增加可读性
```

### 公众号段落 (wechat_paragraphs)
```
结构:
1. 引入（背景/故事/问题）
2. 主体段落（论点+论据，3-5段）
3. 金句/观点升华
4. 结论/行动号召

特点:
- 完整段落（每段4-8句）
- 小标题分隔
- 逻辑递进
- 适合深度阅读
```

### Tweet 系列 (tweet_series)
```
结构:
1. 开篇推文（钩子）
2. 内容推文（2-8条，每条一个点）
3. 总结推文（CTA）

特点:
- 每条 ≤280 字符
- 独立成句
- 编号连贯
- 最后一条可不编号
```

### 列表体 (listicle)
```
结构:
1. 引入（为什么重要）
2. 列表项（3-10个）
   - 小标题
   - 简要说明
   - 实用建议
3. 总结

特点:
- 清晰的数字/符号列表
- 每项结构一致
- 便于快速浏览
```

### 故事体 (story)
```
结构:
1. 开场（设置场景）
2. 冲突/转折
3. 发展
4. 高潮/解决
5. 反思/启发

特点:
- 时间线清晰
- 情感起伏
- 有主角（作者或案例人物）
```

### 教程体 (tutorial)
```
结构:
1. 概述（学什么/能达到什么效果）
2. 准备工作（可选）
3. 步骤 1, 2, 3...
4. 常见问题/注意事项
5. 总结/下一步

特点:
- 步骤清晰
- 可操作性强
- 包含具体数据/参数
```

## 平台适配规则

### 小红书
```json
{
  "recommended_structure": "xiaohongshu_flow",
  "word_count": { "min": 500, "max": 1000 },
  "paragraph_length": "short",
  "emoji_density": "medium-high",
  "line_breaks": "frequent",
  "cta_style": "soft"
}
```

### 微信公众号
```json
{
  "recommended_structure": "wechat_paragraphs",
  "word_count": { "min": 1500, "max": 3000 },
  "paragraph_length": "medium",
  "emoji_density": "low",
  "line_breaks": "standard",
  "cta_style": "direct"
}
```

### Twitter
```json
{
  "recommended_structure": "tweet_series",
  "word_count": { "min": 500, "max": 2000 },
  "tweet_count": { "min": 3, "max": 15 },
  "emoji_density": "medium",
  "cta_style": "conversational"
}
```

## 执行流程

```
1. 解析输入
   └─ 提取 topic, title, platform, config

2. 确定结构
   └─ 根据 platform 和 config.structure 选择模板

3. 生成大纲
   └─ 确定各段落主题和要点

4. 填充内容
   └─ 按结构模板生成各部分内容

5. 应用风格
   └─ 添加 emoji、调整段落、语气润色

6. 检查约束
   └─ 验证字数、包含/排除关键词

7. 提取元数据
   └─ 识别 key_points 和 quotes

8. 输出结果
   └─ 组装输出对象
```

## 示例

### 输入
```json
{
  "topic": "AI工具提升工作效率",
  "title": "5个AI神器让你下班早2小时",
  "platform": "xiaohongshu",
  "config": {
    "word_count": { "min": 500, "max": 800 },
    "structure": "xiaohongshu_flow",
    "emoji_density": "medium-high"
  }
}
```

### 输出
```json
{
  "content": "姐妹们！今天必须来安利这几个AI工具...(正文内容)...",
  "sections": [
    { "type": "hook", "content": "姐妹们！今天必须来安利..." },
    { "type": "solution", "content": "1. ChatGPT - 万能助手..." },
    { "type": "tips", "content": "使用小技巧：..." },
    { "type": "cta", "content": "觉得有用记得点赞收藏..." }
  ],
  "key_points": [
    "ChatGPT 处理文字工作",
    "Midjourney 生成配图",
    "Notion AI 整理笔记"
  ],
  "quotes": [
    "效率提升的关键不是更努力，而是更聪明地工作"
  ],
  "word_count": 650,
  "emoji_count": 12
}
```

## 与黑板的交互

### 读取切片
```json
{
  "scope": ["meta.intent", "meta.constraints", "content.hook.selected"]
}
```

### 写入结果
```json
{
  "target": "content.body"
}
```

## 错误处理

| 错误类型 | 处理方式 |
|----------|---------|
| 标题缺失 | 返回错误，依赖未满足 |
| 字数超限 | 智能截断，保持完整性 |
| 结构不支持 | 使用 general 结构 |

## 性能指标

| 指标 | 目标值 |
|------|--------|
| Token 消耗 | <500 tokens |
| 执行延迟 | <1000ms |
| 字数达标率 | ≥95% |
