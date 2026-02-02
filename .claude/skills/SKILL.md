---
name: tiangong
description: >
  天工 Skills Cluster 主入口。多层级 AI Agent 技能系统，包含：
  L0 Meta-Commander（任务路由）、L1 Orchestrators（领域编排）、L2 Execution（执行技能）、
  Genesis（技能进化）、Infra（基础设施）。任何复杂任务都从这里开始分析和路由。
---

# 天工 TianGong — Skills Cluster

## 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    L0: Meta-Commander                       │
│                      (任务分析与路由)                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   L1: Orchestrators                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │code-orch     │ │doc-orch      │ │multi-agent-orch      │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    L2: Execution Skills                     │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │
│  │code-gen│ │test-gen│ │debug   │ │refactor│ │doc-gen │    │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 可用 Skills

### L0 - 元指挥层
- [meta-commander](L0-meta-commander/SKILL.md) - 任务分析与路由

### L1 - 编排层
- [code-orchestrator](L1-orchestrators/code-orchestrator/SKILL.md) - 代码任务编排
- [doc-orchestrator](L1-orchestrators/doc-orchestrator/SKILL.md) - 文档任务编排
- [data-orchestrator](L1-orchestrators/data-orchestrator/SKILL.md) - 数据任务编排
- [multi-agent-orchestrator](L1-orchestrators/multi-agent-orchestrator/SKILL.md) - 多代理编排

### L2 - 执行层

**Core（核心）:**
- [code-gen](L2-execution/core/code-gen/SKILL.md) - 代码生成
- [code-review](L2-execution/core/code-review/SKILL.md) - 代码审查
- [test-gen](L2-execution/core/test-gen/SKILL.md) - 测试生成
- [debug](L2-execution/core/debug/SKILL.md) - 调试修复
- [refactor](L2-execution/core/refactor/SKILL.md) - 代码重构
- [doc-gen](L2-execution/core/doc-gen/SKILL.md) - 文档生成

**Extended（扩展）:**
- [api-design](L2-execution/extended/api-design/SKILL.md) - API 设计
- [db-schema](L2-execution/extended/db-schema/SKILL.md) - 数据库设计
- [perf-optimize](L2-execution/extended/perf-optimize/SKILL.md) - 性能优化
- [security-audit](L2-execution/extended/security-audit/SKILL.md) - 安全审计

**Experimental（实验）:**
- [prototype](L2-execution/experimental/prototype/SKILL.md) - 快速原型
- [arch-explore](L2-execution/experimental/arch-explore/SKILL.md) - 架构探索
- [creative-code](L2-execution/experimental/creative-code/SKILL.md) - 创意编程

### Genesis - 进化层
- [prime-mover](genesis/prime-mover/SKILL.md) - 技能进化与变异

### Infra - 基础设施
- [skill-registry](infra/skill-registry/SKILL.md) - 技能注册
- [lifecycle-manager](infra/lifecycle-manager/SKILL.md) - 生命周期管理
- [eval-engine](infra/eval-engine/SKILL.md) - 评估引擎
- [rlaif-engine](infra/rlaif-engine/SKILL.md) - RLAIF 引擎

## 使用方式

1. **直接调用 Skill**: `/code-gen 实现一个登录功能`
2. **通过入口路由**: `/tiangong 帮我重构这个模块并添加测试`
3. **指定编排器**: `/code-orchestrator 完成用户模块的完整开发`

## 参考文档

- [capability-map.md](references/capability-map.md) - 能力地图
- [routing-rules.md](references/routing-rules.md) - 路由规则
- [escalation-policy.md](references/escalation-policy.md) - 升级策略
- [registry.json](registry.json) - 技能注册表
