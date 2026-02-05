---
name: tiangong
description: >
  天工 Skills Cluster 主入口。多层级 AI Agent 技能系统，包含 38 个可调用技能。
  任何复杂任务都从这里开始分析和路由。
---

# 天工 TianGong — Skills Cluster

## 架构

```
L0: meta-commander | writing-commander | evaluation-commander* | learning-commander* (任务路由)
     ↓
L1: adaptive-orchestrator | code-orchestrator | doc-orchestrator | multi-agent
     ↓
L2: code-gen, hook-generator, narrative-builder, sensitive-filter...
     ↓
Workers: title-worker, body-worker, cta-worker (轻量无状态)
```

> 完整架构: [_architecture/](_architecture/)

## 可用 Skills (38个, 另有 23 个 planned)

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
| `/meta-commander` | 全局任务分析与路由 |
| `/writing-commander` | 写作域任务分析与路由 |
| `/evaluation-commander` | 评测域任务分析与路由 *(planned)* |
| `/learning-commander` | 学习域任务分析与路由 *(planned)* |

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
