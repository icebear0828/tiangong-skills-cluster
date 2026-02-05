---
name: hook-generator
description: >
  标题钩子生成器 Skill (L2 Core)。生成高吸引力的标题、开头钩子和 CTA。
  当需要：(1) 生成爆款标题，(2) 创作开头钩子，(3) 设计行动召唤时触发。
  支持多平台适配、多种标题公式、A/B测试候选生成。作为核心写作 Skill，具有严格契约。
---

# Hook Generator — 标题钩子生成器

## 触发条件

- 写作任务中包含"写标题"、"起标题"、"开头"、"钩子"等关键词
- 由 writing-orchestrator 调度（Stage 2）
- 需要生成吸引注意力的内容开头

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["topic", "platform"],
  "properties": {
    "topic": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string", "description": "主题名称" },
        "description": { "type": "string", "description": "主题描述" },
        "keywords": {
          "type": "array",
          "items": { "type": "string" },
          "description": "关键词"
        },
        "angle": { "type": "string", "description": "切入角度" }
      },
      "description": "写作主题"
    },
    "platform": {
      "type": "string",
      "enum": ["xiaohongshu", "wechat", "twitter", "general"],
      "description": "目标平台"
    },
    "hook_config": {
      "type": "object",
      "properties": {
        "title_count": {
          "type": "integer",
          "default": 5,
          "description": "生成标题数量"
        },
        "opening_count": {
          "type": "integer",
          "default": 3,
          "description": "生成开头数量"
        },
        "style_preferences": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["number", "suspense", "pain_point", "contrast", "question", "statement", "story"]
          },
          "description": "偏好的标题风格"
        },
        "include_emoji": {
          "type": "boolean",
          "default": true,
          "description": "是否包含emoji"
        },
        "tone": {
          "type": "string",
          "enum": ["professional", "casual", "humorous", "urgent", "inspirational"],
          "default": "casual"
        }
      },
      "description": "钩子配置"
    },
    "audience": {
      "type": "object",
      "properties": {
        "demographic": { "type": "string" },
        "pain_points": { "type": "array", "items": { "type": "string" } },
        "desires": { "type": "array", "items": { "type": "string" } }
      },
      "description": "目标受众"
    },
    "context": {
      "type": "object",
      "properties": {
        "content_summary": { "type": "string" },
        "key_value_props": { "type": "array", "items": { "type": "string" } },
        "competitor_titles": { "type": "array", "items": { "type": "string" } }
      },
      "description": "内容上下文"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["hooks", "recommendation"],
  "properties": {
    "hooks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "content", "score"],
        "properties": {
          "id": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["title", "opening", "cta"]
          },
          "content": { "type": "string" },
          "formula_used": { "type": "string" },
          "style": {
            "type": "string",
            "enum": ["number", "suspense", "pain_point", "contrast", "question", "statement", "story"]
          },
          "score": {
            "type": "object",
            "properties": {
              "overall": { "type": "number", "minimum": 0, "maximum": 100 },
              "curiosity_gap": { "type": "number" },
              "emotional_trigger": { "type": "number" },
              "clarity": { "type": "number" },
              "platform_fit": { "type": "number" }
            }
          },
          "platform_compliance": {
            "type": "object",
            "properties": {
              "length_ok": { "type": "boolean" },
              "style_fit": { "type": "boolean" },
              "issues": { "type": "array", "items": { "type": "string" } }
            }
          },
          "variations": {
            "type": "array",
            "items": { "type": "string" },
            "description": "A/B测试变体"
          }
        }
      },
      "description": "生成的钩子列表"
    },
    "recommendation": {
      "type": "object",
      "properties": {
        "best_title": { "type": "string" },
        "best_opening": { "type": "string" },
        "best_cta": { "type": "string" },
        "rationale": { "type": "string" },
        "ab_test_suggestion": {
          "type": "object",
          "properties": {
            "variant_a": { "type": "string" },
            "variant_b": { "type": "string" },
            "hypothesis": { "type": "string" }
          }
        }
      },
      "description": "推荐选择"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "formulas_applied": { "type": "array", "items": { "type": "string" } },
        "platform_rules_checked": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

## 标题公式库

### 数字型 (Number)
- "X个方法让你..." - 具体化、可预期
- "X%的人不知道的..." - 稀缺性、好奇心
- "从X到Y，只用了Z天" - 转变、时间框架

### 悬念型 (Suspense)
- "结果让我没想到..." - 好奇心驱动
- "直到我发现了这个..." - 转折暗示
- "这一点改变了一切" - 关键发现

### 痛点型 (Pain Point)
- "还在为...烦恼？" - 共鸣+解决方案
- "别再...了，试试这个" - 否定+替代
- "为什么你的...总是失败" - 问题诊断

### 对比型 (Contrast)
- "从A到B，我只做了这一件事" - 简单方法
- "普通人vs高手的X个区别" - 差距对比
- "以前...现在..." - 时间对比

### 提问型 (Question)
- "你知道...吗？" - 知识测试
- "为什么...？" - 原因探究
- "如何在X天内...？" - How-to

### 陈述型 (Statement)
- "这是我见过最..." - 极致评价
- "终于找到了..." - 解决方案
- "必须收藏的..." - 价值声明

### 故事型 (Story)
- "当我第一次..." - 个人经历
- "3年前，我还是..." - 转变历程
- "昨天发生了一件事..." - 即时故事

## 平台特化规则

| 平台 | 标题长度 | 特殊要求 |
|------|---------|---------|
| 小红书 | ≤20字 | emoji开头，口语化，种草感 |
| 公众号 | ≤22字（推荐）/64字（上限） | 金句感，引发好奇 |
| Twitter/X | ≤50字（推荐） | 观点鲜明，可引战 |

## 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 好奇心缺口 | 30% | 是否激发想要知道更多的欲望 |
| 情感触发 | 25% | 是否引发情感反应（惊讶、共鸣、焦虑等）|
| 清晰度 | 20% | 是否清楚传达主题和价值 |
| 平台适配 | 25% | 是否符合平台风格和规范 |

## 执行流程

1. **分析输入**
   - 解析主题和关键词
   - 识别受众痛点和欲望
   - 确定平台规范

2. **公式选择**
   - 根据主题匹配适合的公式
   - 考虑偏好设置
   - 确保多样性

3. **批量生成**
   - 应用多个公式生成候选
   - 生成开头钩子
   - 生成 CTA

4. **评分排序**
   - 计算各维度得分
   - 检查平台合规
   - 排序并推荐

5. **变体生成**
   - 为最佳候选生成 A/B 变体
   - 提供测试假设

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| writing-orchestrator | 由其调度 |
| narrative-builder | 为其提供标题和开头 |
| virality-scorer | 评估其输出 |
| platform-adapter | 可能需要其适配 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 生成数量 | 满足配置要求 | 100% |
| 平台合规 | 符合平台规范 | 100% |
| 最佳得分 | 推荐标题质量 | ≥75 |
| 多样性 | 使用不同公式 | ≥3种 |

## 脚本

- `scripts/generate_hooks.py` - 钩子生成主脚本
- `scripts/formula_library.py` - 公式库
- `scripts/scorer.py` - 评分器

## 参考资料

- `references/title-formulas.md` - 标题公式详解
- `references/platform-rules.md` - 平台规则
