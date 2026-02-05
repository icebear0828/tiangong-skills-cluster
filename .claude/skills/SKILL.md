---
name: tiangong
description: >
  天工 Skills Cluster 主入口。多层级 AI Agent 技能系统，包含 61 个可调用技能。
  任何复杂任务都从这里开始分析和路由。
---

# 天工 TianGong — Skills Cluster

## 架构

```
L0: meta-commander | writing-commander | evaluation-commander | learning-commander (任务路由)
     ↓
L1: adaptive-orchestrator | code-orchestrator | doc-orchestrator | multi-round-eval-orchestrator | learning-orchestrator | ...
     ↓
L2: code-gen, hook-generator, narrative-builder, initial-screener, knowledge-extractor...
     ↓
Workers: title-worker, body-worker, cta-worker (轻量无状态)
```

> 完整架构: [_architecture/](_architecture/)
> 总指挥快速上手: [_architecture/references/commander-quick-start.md](_architecture/references/commander-quick-start.md)

## 可用 Skills (61个)

### 写作域 — 创意内容
| Skill | 用途 | 类型 |
|-------|------|------|
| `/writing-commander` | **写作总入口** — 分析任务, 选蓝图, 编排执行 | L0 指挥 |
| `/adaptive-orchestrator` | 蓝图编排器 — 黑板+切片器+中间件 | L1 编排 |
| `/hook-generator` | 标题/钩子生成 (多风格) | L2 Core |
| `/narrative-builder` | 叙事结构构建 | L2 Core |
| `/virality-scorer` | 传播力评分 (5维度) | L2 Core |
| `/platform-adapter` | 平台适配 (小红书/公众号/Twitter) | L2 Core |
| `/sensitive-filter` | 敏感字审查 + 自动修复 | L2 Middleware |
| `/title-worker` | 标题生成 (轻量 <500 tokens) | Worker |
| `/body-worker` | 正文生成 (轻量 <800 tokens) | Worker |
| `/cta-worker` | CTA 生成 (轻量 <300 tokens) | Worker |
| `/tone-calibrator` | 语气校准 | L2 Extended |
| `/seo-enhancer` | SEO 增强 | L2 Extended |
| `/trend-tracker` | 热点追踪 | L2 Extended |

### 评审域 — 方案评审
| Skill | 用途 | 类型 |
|-------|------|------|
| `/evaluation-commander` | **评审总入口** — 分析评审任务, 选模式, 路由执行 | L0 指挥 |
| `/multi-round-eval-orchestrator` | 多轮评审编排 (4轮: 初筛→深度→对抗→共识) | L1 编排 |
| `/initial-screener` | 初筛评审 — 独立打分, 淘汰最差 | L2 Core |
| `/vote-aggregator` | 投票汇总 — 加权票数, 淘汰阈值 | L2 Core |
| `/defect-analyzer` | 缺陷分析 — Top 缺陷清单, 严重度评级 | L2 Core |
| `/devils-advocate` | 对抗评审 — 7个攻击问题, 挖掘风险 | L2 Core |
| `/consensus-builder` | 共识构建 — 最终推荐, 决策追溯 | L2 Core |
| `/ranking-synthesizer` | 排名综合 — Borda/Schulze 算法 | L2 Extended |
| `/resurrection-evaluator` | 复活评估 — Critical 缺陷时复活被淘汰方案 | L2 Extended |
| `/final-candidate-reviewer` | 最终审查 — Critical 级别检查 | L2 Extended |
| `/confidence-calculator` | 置信度计算 — 决策置信度和不确定性 | L2 Extended |

### 学习域 — 知识学习
| Skill | 用途 | 类型 |
|-------|------|------|
| `/learning-commander` | **学习总入口** — 分析需求, 生成计划, 路由阶段 | L0 指挥 |
| `/learning-orchestrator` | Phase 1 消化编排 (获取→提取→类比) | L1 编排 |
| `/knowledge-graph-orchestrator` | Phase 2 结构化编排 (图谱→映射→路径) | L1 编排 |
| `/verification-orchestrator` | Phase 3 内化编排 (验证→对话→评估) | L1 编排 |
| `/micro-project-orchestrator` | Phase 4 应用编排 (项目→练习→评审) | L1 编排 |
| `/knowledge-extractor` | 知识提取 — 概念/原则/事实/步骤 | L2 Core |
| `/analogy-explainer` | 类比解释 — 适配背景, 标注局限 | L2 Core |
| `/self-explanation-validator` | 自我解释验证 — 识别误解, 补救策略 | L2 Core |
| `/content-curator` | 内容策展 — 资源排序, 学习路径 | L2 Extended |
| `/socratic-questioner` | 苏格拉底提问 — 递进问题, 自适应难度 | L2 Extended |
| `/spatial-mapper` | 空间映射 — 概念聚类, 布局可视化 | L2 Extended |
| `/diagram-generator` | 图表生成 — Mermaid/Graphviz/PlantUML | L2 Experimental |

### 代码域
| Skill | 用途 |
|-------|------|
| `/code-gen` | 代码生成 |
| `/code-review` | 代码审查 |
| `/test-gen` | 测试生成 |
| `/debug` | 调试修复 |
| `/refactor` | 代码重构 |
| `/doc-gen` | 文档生成 |
| `/code-visualizer` | 代码可视化 (源码/文档 -> 工程图表) |
| `/api-design` | API 设计 |
| `/db-schema` | 数据库设计 |
| `/security-audit` | 安全审计 |
| `/perf-optimize` | 性能优化 |
| `/prototype` | 快速原型 |
| `/arch-explore` | 架构探索 |
| `/creative-code` | 创意编程 |

### 编排层 (L1)
| Skill | 用途 |
|-------|------|
| `/code-orchestrator` | 代码任务编排 |
| `/doc-orchestrator` | 文档任务编排 |
| `/data-orchestrator` | 数据任务编排 |
| `/multi-agent-orchestrator` | 多代理编排 |

### 指挥层 (L0)
| Skill | 用途 |
|-------|------|
| `/meta-commander` | 全局任务分析与路由 (代码域) |
| `/writing-commander` | 写作域任务分析与路由 |
| `/evaluation-commander` | 评审域任务分析与路由 |
| `/learning-commander` | 学习域任务分析与路由 |

### 基础设施
| Skill | 用途 |
|-------|------|
| `/skill-registry` | 技能注册表 |
| `/lifecycle-manager` | 生命周期管理 |
| `/eval-engine` | 评估引擎 |
| `/rlaif-engine` | RLAIF 引擎 |
| `/prime-mover` | 技能进化 |

## 用户任务

$ARGUMENTS

---

请分析任务并路由到合适的 skill。
