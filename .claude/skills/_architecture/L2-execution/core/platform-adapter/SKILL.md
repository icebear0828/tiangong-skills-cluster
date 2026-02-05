---
name: platform-adapter
description: >
  平台内容适配器 Skill (L2 Core)。将通用内容适配到特定平台的格式和规范。
  当需要：(1) 适配不同平台，(2) 调整内容格式，(3) 优化平台表现时触发。
  支持小红书、公众号、Twitter/X 等主流平台。作为核心写作 Skill，具有严格契约。
---

# Platform Adapter — 平台内容适配器

## 触发条件

- 写作任务中包含"适配"、"发到X平台"、"转换格式"等关键词
- 由 writing-orchestrator 调度（Stage 3）
- 需要将通用内容转换为平台特定格式

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["content", "target_platform"],
  "properties": {
    "content": {
      "type": "object",
      "required": ["title", "body"],
      "properties": {
        "title": { "type": "string", "description": "原标题" },
        "subtitle": { "type": "string", "description": "副标题" },
        "body": { "type": "string", "description": "正文内容" },
        "cta": { "type": "string", "description": "行动召唤" },
        "key_points": {
          "type": "array",
          "items": { "type": "string" },
          "description": "关键要点"
        },
        "golden_sentences": {
          "type": "array",
          "items": { "type": "string" },
          "description": "金句"
        }
      },
      "description": "原始内容"
    },
    "target_platform": {
      "type": "string",
      "enum": ["xiaohongshu", "wechat", "twitter"],
      "description": "目标平台"
    },
    "adaptation_config": {
      "type": "object",
      "properties": {
        "preserve_core": {
          "type": "boolean",
          "default": true,
          "description": "是否保留核心信息"
        },
        "emoji_level": {
          "type": "string",
          "enum": ["none", "low", "medium", "high"],
          "default": "medium"
        },
        "hashtag_strategy": {
          "type": "string",
          "enum": ["trending", "niche", "mixed"],
          "default": "mixed"
        },
        "image_suggestions": {
          "type": "boolean",
          "default": true
        }
      },
      "description": "适配配置"
    },
    "context": {
      "type": "object",
      "properties": {
        "account_type": {
          "type": "string",
          "enum": ["personal", "brand", "media"]
        },
        "follower_count": { "type": "string" },
        "content_category": { "type": "string" }
      },
      "description": "账号上下文"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["adapted_content", "adaptation_report"],
  "properties": {
    "adapted_content": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "body": { "type": "string" },
        "hashtags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "emojis_used": {
          "type": "array",
          "items": { "type": "string" }
        },
        "word_count": { "type": "integer" },
        "character_count": { "type": "integer" },
        "cta": { "type": "string" },
        "thread_parts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "part_number": { "type": "integer" },
              "content": { "type": "string" },
              "character_count": { "type": "integer" }
            }
          },
          "description": "仅 Twitter Thread 时使用"
        }
      },
      "description": "适配后内容"
    },
    "adaptation_report": {
      "type": "object",
      "properties": {
        "platform": { "type": "string" },
        "changes_made": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "original": { "type": "string" },
              "adapted": { "type": "string" },
              "reason": { "type": "string" }
            }
          }
        },
        "compliance_check": {
          "type": "object",
          "properties": {
            "title_length": { "type": "boolean" },
            "body_length": { "type": "boolean" },
            "hashtag_count": { "type": "boolean" },
            "emoji_density": { "type": "boolean" },
            "all_passed": { "type": "boolean" },
            "issues": { "type": "array", "items": { "type": "string" } }
          }
        },
        "platform_fit_score": { "type": "number" }
      },
      "description": "适配报告"
    },
    "publishing_guide": {
      "type": "object",
      "properties": {
        "best_posting_time": {
          "type": "array",
          "items": { "type": "string" }
        },
        "cover_image_suggestion": { "type": "string" },
        "first_comment_strategy": { "type": "string" },
        "engagement_tips": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "发布指南"
    },
    "alternative_versions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "version_name": { "type": "string" },
          "title": { "type": "string" },
          "body_preview": { "type": "string" },
          "use_case": { "type": "string" }
        }
      },
      "description": "备选版本"
    }
  }
}
```

## 平台规则详解

### 小红书 (Xiaohongshu)

| 元素 | 规范 | 最佳实践 |
|------|------|---------|
| 标题 | ≤20字 | emoji开头，口语化 |
| 正文 | 500-1000字最佳 | 分段落，每段2-4行 |
| emoji | 每100字2-4个 | 段首段尾，强调词 |
| 话题 | 3-8个 | 混合热门+精准 |
| 首图 | 必须有 | 清晰、有吸引力 |

**特色适配**:
```
格式: 软糯口语 + 种草感
开头: "姐妹们！" / "宝子们注意了！"
结尾: "码住！" / "姐妹们冲！"
emoji: 🔥 💕 ✨ 🌟 💯 👀 ❗
```

### 公众号 (WeChat Official Account)

| 元素 | 规范 | 最佳实践 |
|------|------|---------|
| 标题 | ≤64字(显示22字) | 金句感，引发好奇 |
| 正文 | 1500-3000字 | 段落分明，有小标题 |
| 金句 | 加粗/引用框 | 方便截图分享 |
| 引导 | 文末必有 | 关注/在看/分享 |

**特色适配**:
```
格式: 逻辑清晰 + 深度感
开头: 先抛观点或故事
正文: 小标题分段，逻辑递进
金句: 加粗突出，适合截图
结尾: 引导互动 + 关注
```

### Twitter/X

| 元素 | 规范 | 最佳实践 |
|------|------|---------|
| 单条 | ≤280字符 | 简洁有力 |
| Thread | 3-10条 | 结构清晰，每条独立 |
| 话题 | 1-3个 | 精准为主 |
| 互动 | 开放式 | 引发讨论 |

**Thread 结构**:
```
1/ 钩子（最重要！决定是否展开）
2-4/ 背景/问题描述
5-8/ 核心观点/方法
9/ 总结
10/ CTA + 转发邀请
```

## 适配策略

### 标题适配
```
原始: "高效学习的5个方法，让你事半功倍"
       ↓
小红书: "🔥 学霸都在用的学习法 | 后悔没早知道"
公众号: "为什么别人学得快？这5个方法是关键"
Twitter: "5 methods that 2x'd my learning speed 🧵"
```

### 内容压缩/展开

| 转换方向 | 策略 |
|---------|------|
| 长→短 (公众号→小红书) | 提取核心点，增加口语化 |
| 短→长 (小红书→公众号) | 补充论据，增加深度 |
| 中→Thread | 每点一条，保持独立 |

### Emoji 策略

| 平台 | 密度 | 位置 | 推荐emoji |
|------|------|------|----------|
| 小红书 | 高 | 标题、段首、强调 | 🔥💕✨🌟💯👀❗ |
| 公众号 | 低 | 仅小标题 | 📌🔹💡 |
| Twitter | 中 | Thread开头、强调 | 🧵✅❌💡🔥 |

### 话题标签策略

**混合策略 (推荐)**:
```
话题组成:
├─ 热门话题 (30%) - 获取曝光
├─ 精准话题 (50%) - 精准触达
└─ 品牌话题 (20%) - 建立认知
```

## 执行流程

1. **平台规则加载**
   - 获取目标平台规范
   - 确定适配边界

2. **内容分析**
   - 计算原始长度
   - 识别核心元素

3. **结构适配**
   - 调整段落结构
   - 适配长度

4. **风格转换**
   - 调整语气
   - 添加/调整emoji

5. **合规检查**
   - 验证各项规范
   - 修复问题

6. **指南生成**
   - 发布时间建议
   - 互动策略

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| writing-orchestrator | 由其调度 |
| narrative-builder | 接收其完整内容 |
| hook-generator | 可能需要重新生成标题 |
| seo-enhancer | 协同优化 |
| tone-calibrator | 协同调整语气 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 规范合规 | 符合平台规范 | 100% |
| 核心保留 | 保留关键信息 | ≥90% |
| 平台适配度 | 符合平台风格 | ≥80分 |
| 可用性 | 可直接发布 | 100% |

## 脚本

- `scripts/adapt_platform.py` - 平台适配主脚本
- `scripts/platform_rules.py` - 平台规则库
- `scripts/compliance_checker.py` - 合规检查器

## 参考资料

- `references/platform-guides.md` - 平台指南
- `references/emoji-library.md` - Emoji 库
- `references/hashtag-strategy.md` - 话题策略
