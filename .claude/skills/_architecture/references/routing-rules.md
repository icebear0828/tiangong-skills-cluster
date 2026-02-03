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

## S 级任务直接路由表

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

## M 级任务领域编排器路由

| 主要领域 | 目标编排器 | 典型子任务链 |
|---------|----------|------------|
| code | code-orchestrator | code-gen → test-gen → code-review |
| doc | doc-orchestrator | arch-explore → doc-gen → code-review |
| data | data-orchestrator | db-schema → code-gen → test-gen |

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
