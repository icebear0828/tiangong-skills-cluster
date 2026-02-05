---
name: writing-orchestrator
description: >
  写作流程编排器 (L1)。编排三阶段写作流程（策划→创作→分发），协调多个 L2 写作 skill。
  当需要：(1) 创作完整内容，(2) 多平台分发，(3) 迭代优化内容时触发。
  支持单平台深度创作和多平台并行分发模式。由 writing-commander 调度触发。
---

# Writing Orchestrator — 写作流程编排器

## 触发条件

- 进入完整写作流程（非单一任务）
- 由 writing-commander 调度
- 需要编排多个写作 skill 协同工作

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["topic", "platform", "content_type"],
  "properties": {
    "topic": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string", "description": "写作主题" },
        "description": { "type": "string", "description": "主题描述" },
        "angle": { "type": "string", "description": "切入角度" },
        "keywords": {
          "type": "array",
          "items": { "type": "string" },
          "description": "关键词"
        }
      },
      "description": "写作主题"
    },
    "platform": {
      "type": "object",
      "required": ["primary"],
      "properties": {
        "primary": {
          "type": "string",
          "enum": ["xiaohongshu", "wechat", "twitter", "general"],
          "description": "主要发布平台"
        },
        "secondary": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["xiaohongshu", "wechat", "twitter"]
          },
          "description": "次要分发平台"
        }
      },
      "description": "目标平台"
    },
    "content_type": {
      "type": "string",
      "enum": ["article", "post", "thread", "story", "tutorial", "review", "listicle"],
      "description": "内容类型"
    },
    "audience": {
      "type": "object",
      "properties": {
        "demographic": { "type": "string" },
        "interests": { "type": "array", "items": { "type": "string" } },
        "pain_points": { "type": "array", "items": { "type": "string" } },
        "knowledge_level": {
          "type": "string",
          "enum": ["beginner", "intermediate", "expert"]
        }
      },
      "description": "目标受众"
    },
    "content_config": {
      "type": "object",
      "properties": {
        "tone": {
          "type": "string",
          "enum": ["professional", "casual", "humorous", "inspirational", "educational"],
          "default": "casual"
        },
        "length": {
          "type": "string",
          "enum": ["short", "medium", "long"],
          "default": "medium"
        },
        "virality_target": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "default": 75,
          "description": "目标传播力评分"
        },
        "iteration_limit": {
          "type": "integer",
          "default": 3,
          "description": "最大迭代次数"
        }
      },
      "description": "内容配置"
    },
    "reference_materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "content": { "type": "string" },
          "source": { "type": "string" }
        }
      },
      "description": "参考资料"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["stages", "final_output", "quality_gates"],
  "properties": {
    "stages": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "stage_id": {
            "type": "string",
            "enum": ["planning", "creation", "distribution"]
          },
          "status": {
            "type": "string",
            "enum": ["completed", "skipped", "failed"]
          },
          "skills_invoked": {
            "type": "array",
            "items": { "type": "string" }
          },
          "output_summary": { "type": "string" },
          "metrics": {
            "type": "object",
            "additionalProperties": { "type": "number" }
          }
        }
      },
      "description": "阶段执行记录"
    },
    "final_output": {
      "type": "object",
      "properties": {
        "primary_content": {
          "type": "object",
          "properties": {
            "title": { "type": "string" },
            "subtitle": { "type": "string" },
            "body": { "type": "string" },
            "hooks": {
              "type": "array",
              "items": { "type": "string" }
            },
            "cta": { "type": "string" }
          },
          "description": "主要内容"
        },
        "platform_versions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "platform": { "type": "string" },
              "title": { "type": "string" },
              "body": { "type": "string" },
              "hashtags": {
                "type": "array",
                "items": { "type": "string" }
              },
              "emoji_density": { "type": "string" },
              "word_count": { "type": "integer" }
            }
          },
          "description": "各平台版本"
        },
        "metadata": {
          "type": "object",
          "properties": {
            "keywords": { "type": "array", "items": { "type": "string" } },
            "seo_title": { "type": "string" },
            "meta_description": { "type": "string" }
          }
        }
      },
      "description": "最终输出"
    },
    "quality_gates": {
      "type": "object",
      "properties": {
        "virality_score": {
          "type": "object",
          "properties": {
            "overall": { "type": "number" },
            "hook_strength": { "type": "number" },
            "emotional_resonance": { "type": "number" },
            "social_currency": { "type": "number" },
            "practical_value": { "type": "number" },
            "discussion_potential": { "type": "number" }
          }
        },
        "platform_compliance": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "passed": { "type": "boolean" },
              "issues": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "iterations_used": { "type": "integer" },
        "passed": { "type": "boolean" }
      },
      "description": "质量关卡结果"
    },
    "improvement_suggestions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "area": { "type": "string" },
          "suggestion": { "type": "string" },
          "impact": { "type": "string", "enum": ["high", "medium", "low"] }
        }
      },
      "description": "改进建议"
    }
  }
}
```

## 编排流程

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: 策划阶段 (Planning)                                │
│                                                             │
│  Step 1.1: 素材收集                                          │
│  ├─ 调用 content-curator（复用）                             │
│  └─ 收集相关素材和案例                                       │
│                                                             │
│  Step 1.2: 热点分析                                          │
│  ├─ 调用 trend-tracker                                      │
│  └─ 识别热点话题和机会                                       │
│                                                             │
│  Step 1.3: 策略制定                                          │
│  ├─ 分析受众和平台                                          │
│  └─ 确定内容策略和角度                                       │
│                                                             │
│  输出 → Stage 2                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: 创作阶段 (Creation) [迭代循环]                     │
│                                                             │
│  Step 2.1: 钩子生成                                          │
│  ├─ 调用 hook-generator                                     │
│  └─ 生成标题候选和开头钩子                                   │
│                                                             │
│  Step 2.2: 叙事构建                                          │
│  ├─ 调用 narrative-builder                                  │
│  └─ 构建完整内容结构                                         │
│                                                             │
│  Step 2.3: 传播力评估                                        │
│  ├─ 调用 virality-scorer                                    │
│  └─ 评估传播潜力，识别改进点                                 │
│                                                             │
│  质量关卡: virality_score >= target?                         │
│  ├─ Yes → Stage 3                                           │
│  └─ No → 回到 Step 2.1 (最多 3 次迭代)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: 分发阶段 (Distribution) [可并行]                   │
│                                                             │
│  Step 3.1: 平台适配                                          │
│  ├─ 调用 platform-adapter                                   │
│  └─ 适配各目标平台格式                                       │
│                                                             │
│  Step 3.2: SEO优化 (可选)                                    │
│  ├─ 调用 seo-enhancer                                       │
│  └─ 优化搜索可见性                                          │
│                                                             │
│  Step 3.3: 语气校准 (可选)                                   │
│  ├─ 调用 tone-calibrator                                    │
│  └─ 确保语气一致性                                          │
│                                                             │
│  输出 → final_output                                        │
└─────────────────────────────────────────────────────────────┘
```

## 编排模式

### 单平台模式 (Single Platform)
```
Planning → Creation (iterate) → Distribution (single)
```
- 用于单一平台深度内容
- 创作阶段迭代优化
- 分发阶段仅适配一个平台

### 多平台模式 (Multi-Platform)
```
Planning → Creation (iterate) → Distribution (parallel)
                                    ├─ Platform A
                                    ├─ Platform B
                                    └─ Platform C
```
- 用于多平台分发
- 创作阶段产出通用版本
- 分发阶段并行适配各平台

## 质量关卡

| 阶段 | 检查点 | 标准 | 未通过处理 |
|------|--------|------|-----------|
| Planning | 素材充足 | ≥3 个参考 | 扩大搜索 |
| Creation | Hook 吸引力 | ≥70 分 | 重新生成 |
| Creation | 整体传播力 | ≥目标分 | 迭代优化 |
| Distribution | 平台合规 | 100% | 调整格式 |

## 平台规格参考

| 平台 | 标题长度 | 正文长度 | 特殊要求 |
|------|---------|---------|---------|
| 小红书 | ≤20字 | 500-1000字 | emoji密度中-高, 话题标签3-5个 |
| 公众号 | ≤64字 | 1500-3000字 | 段落分明, 小标题, 金句加粗 |
| Twitter/X | ≤280字/条 | Thread 3-10条 | Hook-first, 观点鲜明 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用阶段 |
|-------|------|---------|
| writing-commander | 被调用 | 由其调度 |
| content-curator | 调用 | Stage 1 |
| trend-tracker | 调用 | Stage 1 |
| hook-generator | 调用 | Stage 2 |
| narrative-builder | 调用 | Stage 2 |
| virality-scorer | 调用 | Stage 2 |
| platform-adapter | 调用 | Stage 3 |
| seo-enhancer | 调用 | Stage 3 |
| tone-calibrator | 调用 | Stage 3 |

## 迭代优化策略

当传播力评分未达标时，根据维度得分采取不同策略：

| 低分维度 | 优化策略 | 重点调用 |
|---------|---------|---------|
| Hook 吸引力 | 重新生成更有冲击力的标题 | hook-generator |
| 情感共鸣 | 加强故事性和情感元素 | narrative-builder |
| 社交货币 | 增加可分享的金句和观点 | hook-generator |
| 实用价值 | 补充具体方法和步骤 | narrative-builder |
| 话题性 | 关联热点话题 | trend-tracker |

## 脚本

- `scripts/orchestrate_writing.py` - 写作编排主脚本
- `scripts/quality_checker.py` - 质量检查器
- `scripts/iteration_manager.py` - 迭代管理器

## 参考资料

- `references/orchestration-patterns.md` - 编排模式
- `references/quality-gates.md` - 质量关卡定义
