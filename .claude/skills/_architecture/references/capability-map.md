# 全局能力地图

## 能力矩阵

每个 skill 在此声明其核心能力、契约等级、适应度分数。
Meta-Commander 通过查阅此文件选择最优 skill 组合。

## 核心 Skill（低自由度，严格契约）

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 | 适应度 |
|----------|---------|---------|---------|---------|--------|
| code-gen | 根据需求描述生成代码 | 需求文本 + 语言 + 框架 | 代码文件 | strict | - |
| code-review | 审查代码质量/安全/性能 | 代码文件 | 审查报告 | strict | - |
| test-gen | 生成单元/集成测试 | 代码文件 + 框架 | 测试文件 | strict | - |
| doc-gen | 生成技术文档 | 代码/架构描述 | 文档文件 | strict | - |
| refactor | 重构代码（保持行为不变） | 代码文件 + 重构目标 | 重构后代码 | strict | - |
| debug | 诊断和修复 bug | 代码 + 错误信息 | 修复 patch | strict | - |

## 扩展 Skill（中自由度，标准契约）

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 | 适应度 |
|----------|---------|---------|---------|---------|--------|
| api-design | 设计 RESTful/GraphQL API | 需求描述 | API 规范 | standard | - |
| db-schema | 设计数据库 schema | 数据需求 | DDL/ERD | standard | - |
| perf-optimize | 性能分析和优化 | 代码 + 性能数据 | 优化方案 | standard | - |
| security-audit | 安全审计 | 代码/配置 | 审计报告 | standard | - |

## 实验 Skill（高自由度，宽松契约）

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 | 适应度 |
|----------|---------|---------|---------|---------|--------|
| creative-code | 创造性/探索性编程 | 灵感/目标描述 | 原型代码 | flexible | - |
| arch-explore | 架构探索与方案比较 | 约束条件 | 方案对比报告 | flexible | - |
| prototype | 快速原型开发 | 想法描述 | 可运行原型 | flexible | - |
| diagram-generator | 生成各类图表代码 | 结构化数据 | Mermaid/Graphviz 代码 | flexible | - |

---

## 写作域 Skill（Writing Domain）

### L0 总指挥

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| writing-commander | 写作任务路由、内容策略生成、多平台分发调度 | 写作任务描述 + 平台 + 受众 | 内容策略 + 路由决策 + 最终内容 | strict |

### L1 编排器

| Skill ID | 能力描述 | 编排范围 | 支持的模式 |
|----------|---------|---------|-----------|
| writing-orchestrator | 三阶段写作流程编排 | 策划→创作→分发 | single_pass, iterative, multi_platform |

### L2 核心写作

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| hook-generator | 生成标题、开头钩子、CTA | 主题 + 平台 + 配置 | 钩子列表 + 推荐 | strict |
| virality-scorer | 分析内容传播潜力，优化互动 | 内容 + 平台 | 综合评分 + 维度得分 + 优化建议 | strict |
| narrative-builder | 构建完整叙事结构 | 主题 + 结构类型 + 钩子 | 完整内容 + 分段 + 金句 | strict |
| platform-adapter | 将通用内容适配到特定平台 | 内容 + 目标平台 | 适配内容 + 适配报告 | strict |

### L2 扩展写作

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| tone-calibrator | 校准和调整内容语气风格 | 内容 + 目标语气 | 校准内容 + 语气分析 | standard |
| seo-enhancer | 优化内容搜索可见性 | 内容 + SEO配置 | 优化内容 + SEO报告 | standard |
| trend-tracker | 追踪热点趋势，发现内容机会 | 话题领域 + 平台 | 趋势列表 + 内容机会 | standard |

---

## 评审域 Skill（Evaluation Domain）

### L0 总指挥

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| evaluation-commander | 评审任务路由、轮次调度、最终决策 | 评审任务描述 + 候选方案 | 评审结果 + 推荐决策 | strict |

### L1 编排器

| Skill ID | 能力描述 | 编排范围 | 支持的模式 |
|----------|---------|---------|-----------|
| multi-round-eval-orchestrator | 多轮评审流程编排 | 4轮评审 + 复活 | sequential, parallel |

### L2 核心评审

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| initial-screener | 初筛评审，淘汰最差方案 | 候选列表 + 评审标准 | 淘汰决定 + 理由 | strict |
| vote-aggregator | 汇总多评审员投票 | 多个投票结果 | 汇总结果 + 阈值判定 | strict |
| defect-analyzer | 深度缺陷分析 | 方案 + 分析角度 | Top3 缺陷 + 评分 | strict |
| devils-advocate | 对抗评审攻击领先方案 | 目标方案 + 攻击问题 | Critical 缺陷 + 淘汰建议 | strict |
| consensus-builder | 构建最终共识决策 | 所有轮次结果 | 最终推荐 + 置信度 | strict |

### L2 扩展评审

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| ranking-synthesizer | 综合多评审员排名 | 多个排名结果 | 综合排名 + 冲突分析 | standard |
| resurrection-evaluator | 评估被淘汰方案复活 | 被淘汰方案 + 新缺陷 | 复活决定 + 理由 | standard |
| final-candidate-reviewer | 最终候选 Critical 检查 | 候选方案 + 检查项 | 检查结果 + 判定 | standard |
| confidence-calculator | 计算决策置信度 | 评审过程数据 | 置信度分数 + 不确定性来源 | standard |

---

## 学习域 Skill（Learning Domain）

### L0 总指挥

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| learning-commander | 学习任务路由、计划生成、阶段调度 | 学习任务描述 + 学习者画像 | 学习计划 + 执行结果 | strict |

### L1 编排器

| Skill ID | 能力描述 | 编排范围 | 支持的模式 |
|----------|---------|---------|-----------|
| learning-orchestrator | 消化阶段流程编排 | Phase 1 | sequential |
| knowledge-graph-orchestrator | 知识图谱构建编排 | Phase 2 | sequential, parallel |
| verification-orchestrator | 内化验证流程编排 | Phase 3 | iterative |
| micro-project-orchestrator | 微项目实践编排 | Phase 4 | sequential, iterative |

### L2 核心学习

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| knowledge-extractor | 从文本提取结构化知识 | 文本内容 + 内容类型 | 知识项 + 摘要 + 层次 | strict |
| analogy-explainer | 为概念生成类比解释 | 概念 + 学习者背景 | 类比映射 + 解释 + 局限性 | strict |
| self-explanation-validator | 验证学习者自我解释 | 学习者解释 + 参考解释 | 评分 + 误解识别 + 改进建议 | strict |

### L2 扩展学习

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 |
|----------|---------|---------|---------|---------|
| content-curator | 策展学习资源 | 主题 + 来源类型 + 质量标准 | 排序资源列表 + 学习路径 | standard |
| socratic-questioner | 苏格拉底式提问引导 | 主题 + 当前理解 + 对话历史 | 问题序列 + 进度评估 | standard |
| spatial-mapper | 概念空间映射 | 概念列表 + 关系 + 映射类型 | 空间布局 + 聚类 + 可视化代码 | standard |

---

## 编排器 Skill

| Skill ID | 编排范围 | 支持的 DAG 模式 |
|----------|---------|----------------|
| code-orchestrator | 代码领域多步骤任务 | sequential, iterative-refinement |
| doc-orchestrator | 文档领域多步骤任务 | sequential |
| data-orchestrator | 数据领域多步骤任务 | sequential, parallel |
| writing-orchestrator | 写作领域三阶段流程 | single_pass, iterative, multi_platform |
| multi-agent-orchestrator | 跨域复合任务 | all patterns |
| multi-round-eval-orchestrator | 多轮评审流程 | sequential, parallel |
| learning-orchestrator | 学习消化流程 | sequential |
| knowledge-graph-orchestrator | 知识图谱构建 | sequential, parallel |
| verification-orchestrator | 内化验证流程 | iterative |
| micro-project-orchestrator | 微项目实践 | sequential, iterative |

## 基础设施 Skill

| Skill ID | 职责 |
|----------|------|
| skill-registry | 注册、废弃、查询 skill |
| eval-engine | 执行评测、计算分数、生成报告 |
| rlaif-engine | RLAIF 自我迭代循环 |
| lifecycle-manager | skill 晋升、降级、归档 |

---

## 能力-任务映射规则

### 单任务直接映射（代码域）
- "写一个函数" → code-gen
- "写测试" → test-gen
- "review 这段代码" → code-review
- "写文档" → doc-gen
- "这个 bug 怎么修" → debug
- "重构这个模块" → refactor

### 单任务直接映射（评审域）
- "评审这些方案" → evaluation-commander
- "对比这些方案" → evaluation-commander
- "选择最佳方案" → evaluation-commander
- "攻击这个方案" → devils-advocate

### 单任务直接映射（学习域）
- "学习/理解/掌握 X" → learning-commander
- "解释/讲解 X" → analogy-explainer
- "提取要点" → knowledge-extractor
- "检验理解" → verification-orchestrator
- "做练习" → micro-project-orchestrator

### 单任务直接映射（写作域）
- "写文章/写内容/写爆款" → writing-commander
- "写标题/起标题" → hook-generator
- "评分传播力/分析爆款" → virality-scorer
- "适配X平台" → platform-adapter
- "调整语气" → tone-calibrator
- "SEO优化" → seo-enhancer
- "热点追踪" → trend-tracker

### 多步骤任务 → 编排器
- "实现这个功能并写测试" → code-orchestrator (code-gen → test-gen)
- "设计 API 并实现" → code-orchestrator (api-design → code-gen)
- "做性能分析并优化" → code-orchestrator (perf-optimize → refactor)
- "系统学习 X" → learning-commander (四阶段流程)
- "对比评审多个方案" → evaluation-commander (四轮评审)
- "写一篇完整文章" → writing-commander → writing-orchestrator (三阶段流程)
- "多平台内容分发" → writing-commander → writing-orchestrator (multi_platform)

### 跨域任务 → multi-agent-orchestrator
- "设计数据库、写 API、写前端" → multi-agent (db-schema ∥ api-design → code-gen)
- "完整项目：需求→设计→实现→测试→文档" → multi-agent (全链路)
