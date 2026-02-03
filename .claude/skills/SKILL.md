---
name: tiangong
description: >
  天工 Skills Cluster 主入口。多层级 AI Agent 技能系统，包含 22 个可调用技能。
  任何复杂任务都从这里开始分析和路由。
---

# 天工 TianGong — Skills Cluster

## 架构

```
L0: meta-commander (任务路由)
     ↓
L1: code-orchestrator | doc-orchestrator | data-orchestrator | multi-agent
     ↓
L2: code-gen, debug, test-gen, refactor, api-design, security-audit...
```

> 完整架构: [_architecture/](_architecture/)

## 可用 Skills (22个)

### 执行层 (L2)
| Skill | 用途 |
|-------|------|
| `/code-gen` | 代码生成 |
| `/code-review` | 代码审查 |
| `/test-gen` | 测试生成 |
| `/debug` | 调试修复 |
| `/refactor` | 代码重构 |
| `/doc-gen` | 文档生成 |
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
| `/meta-commander` | 任务分析与路由 |

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
