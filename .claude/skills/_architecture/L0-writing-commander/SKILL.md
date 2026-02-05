---
name: writing-commander
description: >
  写作域总指挥 Skill (L0)。写作任务的第一入口点，负责创意内容写作任务路由、内容策略生成、
  多平台分发调度。当需要：(1) 创作高传播力内容，(2) 多平台内容分发，(3) 爆款内容策划时触发。
  分析写作任务复杂度，选择蓝图并路由到 adaptive-orchestrator。作为 L0 层 Skill，具有严格契约。
---

# Writing Commander — 写作域总指挥

## 触发条件

- 用户任务包含"写文章"、"写内容"、"爆款"、"传播"、"小红书"、"公众号"、"Twitter"等关键词
- 由 meta-commander 路由到写作域
- 需要创作高传播力内容时

## 蓝图选择机制

Writing Commander 作为意图路由器，根据用户输入选择最合适的蓝图：

```
用户输入 → Writing Commander
              │
              ├─ 识别平台 + 内容类型 + 复杂度
              │
              ▼
        ┌─────────────────────────────────────────────┐
        │ 蓝图选择决策树                                │
        │                                             │
        │ 小红书 + 短内容 → xiaohongshu_viral (省钱模式) │
        │ 公众号 + 长文   → wechat_longform (质量模式)  │
        │ Twitter + Thread → twitter_thread (平衡模式) │
        │ 深度分析需求    → deep_analysis (质量模式)    │
        │ 简单任务       → 直接 L2 Skill              │
        └─────────────────────────────────────────────┘
              │
              ▼
        adaptive-orchestrator (执行蓝图)
```

### 蓝图映射规则

| 用户意图 | 平台 | 推荐蓝图 | 预估 Token |
|---------|------|---------|-----------|
| 短文案/种草/推荐 | 小红书 | xiaohongshu_viral | ~1000 |
| 深度文章/专题 | 公众号 | wechat_longform | ~3500 |
| Thread/观点 | Twitter | twitter_thread | ~2000 |
| 行业分析/研究 | 通用 | deep_analysis | ~4000 |
| 写标题/分析 | 任意 | 直接 L2 | <500 |

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["task_description"],
  "properties": {
    "task_description": {
      "type": "string",
      "description": "写作任务描述"
    },
    "content_request": {
      "type": "object",
      "properties": {
        "topic": { "type": "string", "description": "写作主题" },
        "content_type": {
          "type": "string",
          "enum": ["article", "post", "thread", "story", "tutorial", "review"],
          "description": "内容类型"
        },
        "platform": {
          "type": "string",
          "enum": ["xiaohongshu", "wechat", "twitter", "general", "multi"],
          "description": "目标平台"
        },
        "goal": {
          "type": "string",
          "enum": ["viral", "engagement", "conversion", "education", "brand"],
          "description": "内容目标"
        },
        "reference_materials": {
          "type": "array",
          "items": { "type": "string" },
          "description": "参考资料"
        }
      },
      "description": "内容请求"
    },
    "audience": {
      "type": "object",
      "properties": {
        "demographic": { "type": "string" },
        "interests": { "type": "array", "items": { "type": "string" } },
        "pain_points": { "type": "array", "items": { "type": "string" } },
        "tone_preference": {
          "type": "string",
          "enum": ["professional", "casual", "humorous", "inspirational", "educational"]
        }
      },
      "description": "目标受众"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "word_count": { "type": "object", "properties": { "min": { "type": "integer" }, "max": { "type": "integer" } } },
        "must_include": { "type": "array", "items": { "type": "string" } },
        "must_avoid": { "type": "array", "items": { "type": "string" } },
        "deadline": { "type": "string" }
      },
      "description": "写作约束"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["task_analysis", "routing_decision", "final_content"],
  "properties": {
    "task_analysis": {
      "type": "object",
      "properties": {
        "complexity": {
          "type": "string",
          "enum": ["S", "M", "L", "XL"],
          "description": "任务复杂度"
        },
        "task_type": {
          "type": "string",
          "enum": ["title_only", "single_platform", "multi_platform", "cross_domain"]
        },
        "platforms_involved": {
          "type": "array",
          "items": { "type": "string" }
        },
        "estimated_stages": { "type": "integer" },
        "skills_required": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "任务分析"
    },
    "routing_decision": {
      "type": "object",
      "properties": {
        "route_type": {
          "type": "string",
          "enum": ["direct_l2", "writing_orchestrator", "multi_agent"]
        },
        "target_skill": { "type": "string" },
        "orchestration_mode": {
          "type": "string",
          "enum": ["single_pass", "iterative", "multi_platform"]
        },
        "rationale": { "type": "string" }
      },
      "description": "路由决策"
    },
    "content_strategy": {
      "type": "object",
      "properties": {
        "core_message": { "type": "string" },
        "hook_angle": { "type": "string" },
        "narrative_approach": { "type": "string" },
        "platform_adaptations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "platform": { "type": "string" },
              "key_adjustments": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      },
      "description": "内容策略"
    },
    "final_content": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "body": { "type": "string" },
        "platform_versions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "platform": { "type": "string" },
              "adapted_content": { "type": "string" }
            }
          }
        },
        "virality_score": { "type": "number" },
        "metadata": {
          "type": "object",
          "properties": {
            "hashtags": { "type": "array", "items": { "type": "string" } },
            "keywords": { "type": "array", "items": { "type": "string" } },
            "cta": { "type": "string" }
          }
        }
      },
      "description": "最终内容"
    },
    "quality_report": {
      "type": "object",
      "properties": {
        "virality_assessment": {
          "type": "object",
          "properties": {
            "overall_score": { "type": "number" },
            "hook_strength": { "type": "number" },
            "emotional_resonance": { "type": "number" },
            "shareability": { "type": "number" }
          }
        },
        "platform_fit": { "type": "number" },
        "improvement_suggestions": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "质量报告"
    }
  }
}
```

## 复杂度判定

| 复杂度 | 条件 | 路由目标 |
|--------|------|---------|
| S | 单一任务（写标题/分析爆款） | 直接 L2 skill |
| M | 单平台深度内容 | writing-orchestrator |
| L | 多平台分发 | writing-orchestrator (多平台模式) |
| XL | 跨域复合任务 | multi-agent-orchestrator |

## 三阶段写作框架

### Phase 1: 策划阶段 (Planning)
**目标**: 确定内容策略和方向

**执行**:
1. 调用 `content-curator` 收集素材（复用）
2. 调用 `trend-tracker` 追踪热点
3. 分析受众和平台特性

**产出**:
- 内容策略
- 选题方向
- 受众定位

### Phase 2: 创作阶段 (Creation)
**目标**: 生成高质量内容

**执行**:
1. 调用 `hook-generator` 生成标题和开头钩子
2. 调用 `narrative-builder` 构建叙事结构
3. 调用 `virality-scorer` 评估传播力
4. 迭代优化直到达标

**产出**:
- 完整内容
- 传播力评分
- 优化建议

### Phase 3: 分发阶段 (Distribution)
**目标**: 适配和优化各平台

**执行**:
1. 调用 `platform-adapter` 适配目标平台
2. 调用 `seo-enhancer` SEO优化（可选）
3. 调用 `tone-calibrator` 语气校准（可选）

**产出**:
- 平台适配版本
- SEO优化内容
- 发布建议

## 路由规则

```
写作任务 → writing-commander
    │
    ├─ "写标题/起标题" → 直接调用 hook-generator
    │
    ├─ "分析爆款/评分传播力" → 直接调用 virality-scorer
    │
    ├─ "适配X平台" → 直接调用 platform-adapter
    │
    ├─ "小红书短文案" → adaptive-orchestrator + xiaohongshu_viral 蓝图
    │   └─ Worker 链，省钱模式
    │
    ├─ "公众号深度文章" → adaptive-orchestrator + wechat_longform 蓝图
    │   └─ Skill 链，质量模式
    │
    ├─ "Twitter Thread" → adaptive-orchestrator + twitter_thread 蓝图
    │   └─ 混合模式
    │
    ├─ "深度分析/行业报告" → adaptive-orchestrator + deep_analysis 蓝图
    │   └─ 完整研究流程
    │
    ├─ "多平台分发" → adaptive-orchestrator (多蓝图串行)
    │   └─ 生成通用版 → 并行适配各平台
    │
    └─ "跨域任务（内容+设计+代码）" → multi-agent-orchestrator
```

### 敏感字审查集成

所有路径都会经过 sensitive-filter-middleware 检查：

```
任意内容生成 → sensitive-filter-middleware
    │
    ├─ passed=true → 继续流程
    │
    └─ passed=false
        ├─ auto_fix=true → 自动修复 → 重新检查
        └─ auto_fix=false → 返回问题列表 → 人工处理
```

## 平台策略矩阵

| 平台 | 核心特征 | 关键成功因素 |
|------|---------|-------------|
| 小红书 | 图文并茂、种草风格 | 首图、标题、前3行、emoji、话题标签 |
| 公众号 | 深度长文、逻辑性强 | 标题、开篇、金句、分享裂变动机 |
| Twitter/X | 简短有力、金句频出 | 前15字、Thread结构、话题互动 |

## 与 doc-gen 的边界

| 维度 | writing-commander | doc-gen |
|------|------------------|---------|
| 内容类型 | 创意内容、营销文案 | 技术文档、API文档 |
| 目标 | 传播、互动、转化 | 准确、清晰、完整 |
| 风格 | 吸引力、情感共鸣 | 专业、严谨 |
| 平台 | 社交媒体 | 开发者文档站 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| meta-commander | 被调用 | 由其路由写作任务 |
| adaptive-orchestrator | 调用 | 执行蓝图 (M/L 级任务) |
| writing-orchestrator | 调用 | **已废弃**，迁移到 adaptive-orchestrator |
| sensitive-filter-middleware | 调用 | 所有内容生成后的审查 |
| title-worker | 调用 | Worker 模式标题生成 |
| body-worker | 调用 | Worker 模式正文生成 |
| cta-worker | 调用 | Worker 模式 CTA 生成 |
| hook-generator | 调用 | S 级直接调用或 Skill 模式 |
| virality-scorer | 调用 | S 级直接调用或验证阶段 |
| platform-adapter | 调用 | S 级直接调用或分发阶段 |
| content-curator | 调用 | 策划阶段（复用） |
| multi-agent-orchestrator | 调用 | XL 级跨域任务 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 任务理解 | 正确识别写作目标 | 100% |
| 路由准确 | 路由到正确执行层 | ≥95% |
| 传播力评分 | 内容传播潜力 | ≥75 |
| 平台适配 | 符合平台规范 | 100% |

## 可复用的现有 Skill

| 现有 Skill | 复用场景 | 调用阶段 |
|-----------|---------|---------|
| content-curator | 写作素材收集 | 策划阶段 |
| knowledge-extractor | 从参考资料提取要点 | 策划阶段 |
| socratic-questioner | 深化选题理解 | 策划阶段（可选）|
| diagram-generator | 生成配图代码 | 分发阶段 |

## 参考资料

- `references/platform-strategies.md` - 各平台策略详解
- `references/writing-routing-rules.md` - 写作域路由规则
- `references/virality-patterns.md` - 爆款模式库
