---
name: meta-commander
description: >
  全局任务总指挥。当用户提交任何复杂任务时作为第一入口点触发。职责包括：(1) 分析任务复杂度和类型，
  (2) 查阅全局能力地图选择最优 skill 组合，(3) 生成执行计划（DAG），(4) 路由到对应编排器，
  (5) 监控执行结果并处理异常升级。对于简单单一任务直接路由到执行层 skill，对于复合任务启动子代理编排。
  当任务涉及多个领域、需要多步骤协作、或需要策略决策时触发此 skill。
---

# Meta-Commander — 总指挥

## 决策流程

1. 接收任务描述
2. 运行 `scripts/task_analyzer.py <task_description>` 评估：
   - 复杂度等级：S（单一原子操作）/ M（单领域多步骤）/ L（跨域协作）/ XL（探索性/无先例）
   - 涉及领域标签：`[code, doc, data, design, test, deploy, ...]`
   - 预估步骤数
3. 路由决策：
   - **S 级** → 直接查阅 `references/capability-map.md`，选择单个 L2 skill 执行
   - **M 级** → 路由到对应领域编排器（如 code-orchestrator）
   - **L 级** → 路由到 multi-agent-orchestrator，附带执行计划
   - **XL 级** → 触发 prime-mover 评估是否需要创建新 skill
4. 生成执行计划：`scripts/plan_generator.py`
5. 监控：执行完成后检查结果，按 `references/escalation-policy.md` 处理异常

## 关键原则

- **最小权限路由**：能用 S 级解决的不升级到 M 级
- **快速失败**：如果 skill 执行 2 次仍失败，立即升级到更高编排层
- **Context 预算**：总执行计划的 skill 数不超过 5 个（避免 context 爆炸）
- 简单任务不需要编排层介入，直接选择执行层 skill

## 与其他组件的交互

- 查阅 `../state/registry.json` 获取可用 skill 列表
- 查阅 `references/capability-map.md` 了解每个 skill 的能力范围
- 查阅 `references/routing-rules.md` 了解详细路由规则
- 复杂场景查阅 `references/escalation-policy.md`
