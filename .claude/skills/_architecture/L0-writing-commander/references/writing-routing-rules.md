# 写作域路由规则

## 概述

本文档定义了 writing-commander 将写作任务路由到正确 Skill 或编排器的决策规则。

## 路由决策树

```
写作任务输入
   │
   ▼
┌─────────────────────────┐
│ 1. 分析任务复杂度        │
└─────────────────────────┘
   │
   ├── S (简单单一操作)
   │   └── 直接路由到 L2 执行层 Skill
   │
   ├── M (单平台深度内容)
   │   └── 路由到 writing-orchestrator
   │
   ├── L (多平台分发)
   │   └── 路由到 writing-orchestrator (multi-platform mode)
   │
   └── XL (跨域复合任务)
       └── 路由到 multi-agent-orchestrator
```

## S 级任务直接路由表

| 任务特征关键词 | 目标 Skill | 置信度阈值 |
|--------------|-----------|-----------|
| 写标题、起标题、取名 | hook-generator | 0.85 |
| 写开头、钩子、hook | hook-generator | 0.85 |
| 评分传播力、分析爆款 | virality-scorer | 0.85 |
| 适配XX平台、转换格式 | platform-adapter | 0.8 |
| 调整语气、改变风格 | tone-calibrator | 0.8 |
| SEO优化、关键词优化 | seo-enhancer | 0.8 |
| 热点追踪、趋势分析 | trend-tracker | 0.8 |
| 构建结构、写大纲 | narrative-builder | 0.8 |

## M 级任务编排器路由

### 触发条件

满足以下任一条件：
- 需要完整创作流程（标题+正文+优化）
- 明确指定单一目标平台
- 包含"写一篇"、"创作"、"完整内容"等关键词

### 路由目标

```
M 级任务 → writing-orchestrator (单平台模式)
    │
    └── 三阶段流程
        ├── Stage 1: 策划
        ├── Stage 2: 创作 (迭代)
        └── Stage 3: 分发 (单平台)
```

## L 级任务编排器路由

### 触发条件

满足以下任一条件：
- 多个目标平台
- 包含"多平台"、"分发到"、"同步发布"等关键词
- 明确列出多个平台名称

### 路由目标

```
L 级任务 → writing-orchestrator (多平台模式)
    │
    └── 三阶段流程
        ├── Stage 1: 策划
        ├── Stage 2: 创作 (迭代，产出通用版本)
        └── Stage 3: 分发 (并行适配各平台)
            ├── platform-adapter (Platform A)
            ├── platform-adapter (Platform B)
            └── platform-adapter (Platform C)
```

## XL 级任务路由

### 触发条件

满足以下任一条件：
- 写作+设计/代码等跨域需求
- 需要 diagram-generator 生成配图代码
- 包含"完整项目"、"从头到尾"等关键词

### 路由目标

```
XL 级任务 → multi-agent-orchestrator
    │
    ├── 写作子任务 → writing-commander
    ├── 设计子任务 → 相应 Skill
    └── 代码子任务 → 相应 Skill
```

## 平台识别规则

| 关键词 | 识别为平台 |
|--------|-----------|
| 小红书、红书、xhs | xiaohongshu |
| 公众号、微信、公号 | wechat |
| twitter、推特、X | twitter |
| 通用、不限平台 | general |

## 内容类型识别

| 关键词 | 内容类型 |
|--------|---------|
| 文章、深度 | article |
| 帖子、笔记 | post |
| 推文串、thread | thread |
| 故事、经历 | story |
| 教程、怎么做 | tutorial |
| 评测、对比 | review |
| 清单、X个方法 | listicle |

## 复杂度判定逻辑

```python
def determine_complexity(task):
    # S 级判定
    if is_single_operation(task):
        return 'S', get_direct_skill(task)

    # XL 级判定
    if involves_cross_domain(task):
        return 'XL', 'multi-agent-orchestrator'

    # L 级判定
    platforms = extract_platforms(task)
    if len(platforms) > 1:
        return 'L', 'writing-orchestrator'

    # M 级
    return 'M', 'writing-orchestrator'
```

## 可复用 Skill 调用规则

| 现有 Skill | 调用条件 | 调用阶段 |
|-----------|---------|---------|
| content-curator | 需要收集素材 | Stage 1 |
| knowledge-extractor | 有参考资料需要提取 | Stage 1 |
| socratic-questioner | 深化选题理解 | Stage 1 (可选) |
| diagram-generator | 需要生成配图 | Stage 3 |

## 质量关卡规则

### Stage 1 → Stage 2

- 必须有明确的内容策略
- 必须有目标受众定位

### Stage 2 迭代

```
迭代条件: virality_score < target_score AND iteration < max_iteration

迭代策略:
├── hook_score 低 → 重调 hook-generator
├── emotional_score 低 → 重调 narrative-builder (加强情感)
├── practical_score 低 → 重调 narrative-builder (补充干货)
└── social_currency 低 → 重调 hook-generator (金句优化)
```

### Stage 2 → Stage 3

- virality_score ≥ 目标分 (默认 75)
- 或已达最大迭代次数 (默认 3)

## 路由验证检查点

在执行路由前，writing-commander 必须验证：

1. **Skill 可用性**: 目标 Skill 状态为 active
2. **契约兼容性**: 任务输入满足 Skill 输入 schema
3. **平台支持**: 目标平台在支持列表中
4. **无循环依赖**: 任务流中无环

## 失败处理

| 失败场景 | 处理方式 |
|---------|---------|
| Skill 执行失败 1 次 | 重试，提供更多 context |
| Skill 执行失败 2 次 | 尝试替代方案 |
| 迭代优化无进展 | 提示用户调整需求 |
| 平台不支持 | 提示用户选择支持的平台 |
