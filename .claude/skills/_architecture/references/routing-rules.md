# 任务路由决策树

## 概述

本文档定义了 Meta-Commander 将任务路由到正确 Skill 或编排器的决策规则。

## 路由决策树

```
任务输入
   │
   ▼
┌─────────────────────────┐
│ 1. 分析任务复杂度        │
│    (task_analyzer.py)   │
└─────────────────────────┘
   │
   ├── S (简单单一操作)
   │   └── 直接路由到 L2 执行层 Skill
   │
   ├── M (单领域多步骤)
   │   └── 路由到领域编排器
   │
   ├── L (跨域协作)
   │   └── 路由到 multi-agent-orchestrator
   │
   └── XL (探索性/无先例)
       └── 触发 prime-mover 评估
```

## 域级路由（第一级分流）

```
任务输入
   │
   ├── 代码相关 → 代码域
   │   └── meta-commander → code-orchestrator / L2 code skills
   │
   ├── 评审相关 → 评审域
   │   └── meta-commander → evaluation-commander → multi-round-eval-orchestrator
   │
   ├── 学习相关 → 学习域
   │   └── meta-commander → learning-commander → learning-orchestrator
   │
   ├── 写作相关 → 写作域
   │   └── meta-commander → writing-commander → writing-orchestrator
   │
   └── 跨域/复合 → 多代理
       └── meta-commander → multi-agent-orchestrator
```

---

## 代码域路由

### S 级任务直接路由表

| 任务特征关键词 | 目标 Skill | 置信度阈值 |
|--------------|-----------|-----------|
| 写函数、实现功能、生成代码 | code-gen | 0.8 |
| 审查、review、检查代码 | code-review | 0.85 |
| 写测试、单元测试、测试用例 | test-gen | 0.85 |
| 写文档、生成文档、README | doc-gen | 0.8 |
| 重构、优化结构、清理代码 | refactor | 0.8 |
| 调试、修复bug、排错 | debug | 0.85 |
| 设计API、接口设计 | api-design | 0.75 |
| 数据库设计、表结构、schema | db-schema | 0.8 |
| 性能优化、加速、提升性能 | perf-optimize | 0.75 |
| 安全审计、漏洞检查 | security-audit | 0.8 |
| 创意编程、实验性代码 | creative-code | 0.6 |
| 架构探索、方案对比 | arch-explore | 0.7 |
| 快速原型、MVP | prototype | 0.7 |

### M 级任务领域编排器路由

| 主要领域 | 目标编排器 | 典型子任务链 |
|---------|----------|------------|
| code | code-orchestrator | code-gen → test-gen → code-review |
| doc | doc-orchestrator | arch-explore → doc-gen → code-review |
| data | data-orchestrator | db-schema → code-gen → test-gen |

---

## 评审域路由

### 任务特征关键词

| 关键词 | 目标 | 说明 |
|--------|------|------|
| 评审、对比、选择最佳、评估方案 | evaluation-commander | 路由到评审总指挥 |
| 初筛、筛选 | initial-screener | 直接调用（由编排器） |
| 缺陷分析、风险评估 | defect-analyzer | 直接调用（由编排器） |
| 对抗评审、攻击方案 | devils-advocate | 直接调用（由编排器） |

### 评审模式选择

| 候选数 | 维度数 | 推荐模式 | 轮次 |
|--------|--------|---------|------|
| 2 | ≤3 | quick | 1-2 |
| 3-4 | 3-5 | standard | 2-3 |
| 5-7 | 5-7 | thorough | 4 |
| 8+ | 7+ | adversarial | 4+ |

### 四轮评审路由

```
Round 1 (初筛淘汰)
├── initial-screener ×3 (并行)
└── vote-aggregator

Round 2 (深度分析)
├── defect-analyzer ×3 (并行)
└── ranking-synthesizer

Round 3 (对抗评审)
├── devils-advocate
└── final-candidate-reviewer (条件触发)

Round 4 (复活与共识)
├── resurrection-evaluator (条件触发)
├── final-candidate-reviewer
└── consensus-builder
```

---

## 学习域路由

### 任务特征关键词

| 关键词 | 目标 | 说明 |
|--------|------|------|
| 学习、理解、掌握、教我 | learning-commander | 路由到学习总指挥 |
| 解释、讲解、比喻 | analogy-explainer | 直接调用 |
| 提取要点、总结、提炼 | knowledge-extractor | 直接调用 |
| 检验理解、测试掌握 | verification-orchestrator | 路由到验证编排器 |
| 做练习、实践 | micro-project-orchestrator | 路由到微项目编排器 |
| 生成图表、可视化 | diagram-generator | 直接调用 |

### 四阶段学习路由

```
Phase 1: 消化 (Digest)
├── content-curator
├── knowledge-extractor
└── analogy-explainer

Phase 2: 结构化 (Structure)
├── spatial-mapper
└── diagram-generator

Phase 3: 内化 (Internalize)
├── self-explanation-validator
├── socratic-questioner
└── analogy-explainer (澄清)

Phase 4: 应用 (Apply)
├── code-gen
├── test-gen
└── code-review
```

### 学习目标等级路由

| 目标等级 | 阶段数 | 路径 |
|---------|--------|------|
| awareness | 1 | Phase 1 only |
| understanding | 2 | Phase 1-2 |
| application | 3 | Phase 1-3 |
| mastery | 4 | Phase 1-4 |

---

## 写作域路由

### 任务特征关键词

| 关键词 | 目标 | 说明 |
|--------|------|------|
| 写文章、写内容、爆款、传播 | writing-commander | 路由到写作总指挥 |
| 写标题、起标题、钩子 | hook-generator | 直接调用 |
| 评分传播力、分析爆款 | virality-scorer | 直接调用 |
| 适配XX平台、转换格式 | platform-adapter | 直接调用 |
| 调整语气、改变风格 | tone-calibrator | 直接调用 |
| SEO优化、关键词优化 | seo-enhancer | 直接调用 |
| 热点追踪、趋势分析 | trend-tracker | 直接调用 |
| 小红书、公众号、Twitter | writing-commander | 根据平台路由 |

### 三阶段写作路由

```
Stage 1: 策划 (Planning)
├── content-curator (复用)
├── trend-tracker
└── 受众分析

Stage 2: 创作 (Creation) [迭代]
├── hook-generator
├── narrative-builder
└── virality-scorer (评估)
    └── 未达标 → 回到 hook-generator

Stage 3: 分发 (Distribution)
├── platform-adapter
├── seo-enhancer (可选)
└── tone-calibrator (可选)
```

### 写作复杂度路由

| 复杂度 | 条件 | 路由目标 |
|--------|------|---------|
| S | 单一任务（写标题/分析爆款） | 直接 L2 skill |
| M | 单平台深度内容 | writing-orchestrator |
| L | 多平台分发 | writing-orchestrator (multi_platform) |
| XL | 跨域复合任务 | multi-agent-orchestrator |

### 平台识别规则

| 关键词 | 识别为平台 |
|--------|-----------|
| 小红书、红书、xhs | xiaohongshu |
| 公众号、微信、公号 | wechat |
| twitter、推特、X | twitter |
| 通用、不限平台 | general |

---

## L 级任务 DAG 模式选择

| 任务模式 | DAG 模式 | 示例 |
|---------|---------|------|
| 严格顺序依赖 | sequential | 需求 → 设计 → 实现 → 测试 |
| 独立并行子任务 | parallel | 前端 ∥ 后端 ∥ 数据库 → 集成 |
| 质量迭代提升 | iterative | 生成 → 评测 → 修改 → 再评测 |
| 复杂混合依赖 | dag | 自定义 DAG 结构 |

## XL 级任务 Prime-Mover 触发条件

满足以下任一条件触发 Prime-Mover：

1. **能力缺口**: 任务需要的能力在 capability-map.md 中不存在
2. **低置信度匹配**: 所有 Skill 匹配置信度 < 0.5
3. **显式探索请求**: 任务包含"探索"、"创新"、"从零开始"等关键词
4. **多次失败**: 同一任务在 L/M 级已尝试 2 次失败

---

## 路由优化规则

### 1. 最小权限原则
- 能用 S 级解决的不升级到 M 级
- 能用 M 级解决的不升级到 L 级

### 2. Context 预算约束
- 单次执行计划的 Skill 数不超过 5 个
- 超过时拆分为多个独立执行计划

### 3. 快速失败与升级
- Skill 执行失败 1 次：重试（可能提供更多 context）
- Skill 执行失败 2 次：升级到更高层级编排
- 连续 3 个 Skill 失败：触发紧急制动

### 4. 历史模式学习
- 记录每次路由决策和最终结果
- 相似任务优先使用历史成功路由
- 失败路由加入负样本避免重复

## 路由验证检查点

在执行路由前，Meta-Commander 必须验证：

1. **Skill 可用性**: 目标 Skill 状态为 active
2. **契约兼容性**: 任务输入满足 Skill 输入 schema
3. **资源充足性**: Context window 有足够空间
4. **无循环依赖**: DAG 中无环
