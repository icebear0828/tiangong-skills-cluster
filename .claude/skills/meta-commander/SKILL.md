---
name: meta-commander
description: >
  全局任务总指挥。当用户提交任何复杂任务时作为第一入口点触发。分析任务复杂度，
  选择最优 skill 组合，生成执行计划，路由到对应编排器。
---

# Meta-Commander — 总指挥

> 详细文档: [_architecture/L0-meta-commander/SKILL.md](_architecture/L0-meta-commander/SKILL.md)

## 快速参考

**触发条件:** 复杂任务、多步骤协作、策略决策

**复杂度分级:**
- S: 单一原子操作 → 直接执行 L2 skill
- M: 单领域多步骤 → 路由到 L1 编排器
- L: 跨域协作 → multi-agent-orchestrator
- XL: 探索性任务 → prime-mover 评估

## 用户任务

$ARGUMENTS

---

请分析任务并执行路由决策。参考 `_architecture/references/capability-map.md` 选择最优 skill。
