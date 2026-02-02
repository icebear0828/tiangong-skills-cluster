---
name: multi-agent-orchestrator
description: >
  跨域复合任务编排器。当任务涉及多个领域（如代码+测试+文档）、需要多个 skill 协作、
  或需要复杂的 DAG 执行流程时触发。支持四种编排模式：Sequential Chain（顺序链）、
  Parallel Fan-out（并行扇出）、Iterative Refinement（迭代精炼）、DAG Composition（DAG 组合）。
  由 Meta-Commander 路由触发，不直接由用户任务触发。
---

# Multi-Agent Orchestrator — 跨域编排器

## 输入格式

从 Meta-Commander 接收执行计划：
```json
{
  "task_id": "...",
  "complexity": "L",
  "domains": ["code", "test", "doc"],
  "plan": {
    "pattern": "sequential | parallel | iterative | dag",
    "steps": [...]
  }
}
```

## 编排模式

### 1. Sequential Chain（顺序链）

适用场景：任务有严格依赖顺序。

```
Step1 → Step2 → Step3 → Output
```

执行逻辑：
1. 按顺序执行每个 step
2. 前一个 step 的输出是后一个 step 的输入
3. 任一 step 失败 → 根据 quality-gates 决定：重试 / 回退 / 升级

示例：
```
需求分析 (arch-explore)
  → API 设计 (api-design)
    → 代码生成 (code-gen)
      → 测试生成 (test-gen)
```

### 2. Parallel Fan-out（并行扇出）

适用场景：多个子任务可独立执行，最终汇合。

```
        ┌→ TaskB1 ─┐
TaskA ──┤→ TaskB2 ──┤→ TaskC (merge)
        └→ TaskB3 ──┘
```

执行逻辑：
1. 执行前置任务 TaskA
2. 识别可并行的子任务（无相互依赖的）
3. "并行"执行（Claude Code 中实际为快速交替执行）
4. 汇合：merge 多个输出，解决冲突
5. 执行后续任务 TaskC

示例：
```
需求确认
  ├→ 前端代码 (code-gen: frontend)
  ├→ 后端 API (code-gen: backend)
  └→ 数据库 Schema (db-schema)
  → 集成 (code-gen: integration)
```

### 3. Iterative Refinement（迭代精炼）

适用场景：输出质量需要逐步提升。

```
Task → Eval → Pass? ─YES→ Done
              │
              NO → Refine → Task (loop, max 3 iterations)
```

执行逻辑：
1. 执行任务 skill
2. 调用 eval-engine 评测输出
3. 评分 ≥ 阈值 → 完成
4. 评分 < 阈值 → 将评测反馈注入到 skill 的下一次执行中
5. 最多迭代 3 次，超过则升级到人工 / 换 skill

示例：
```
代码生成 (code-gen)
  → 代码审查 (code-review) → 评分 0.6 (< 0.8 阈值)
    → 基于审查反馈修复 (debug) → 再审查 → 评分 0.85 → 通过
```

### 4. DAG Composition（DAG 组合）

适用场景：前三种模式的自由组合。

参考 `references/dag-patterns.md` 中的常用 DAG 模板。

执行逻辑：
1. 解析 DAG 结构，识别所有节点和边
2. 拓扑排序确定执行顺序
3. 同一拓扑层的节点可并行
4. 每个节点完成后检查后继节点的所有前置是否满足
5. 全部节点完成 → 汇总最终输出

## 质量关卡

每个 step 完成后检查：

1. **输出完整性**：是否产出了预期的文件/结果
2. **契约符合性**：输出是否符合 skill 声明的契约
3. **质量阈值**：如果配置了 eval-engine，检查评分是否达标

关卡未通过的处理策略见 `references/quality-gates.md`。

## Context 管理

跨 skill 编排时的 context 策略：

- 每个 step 之间只传递**结构化摘要**，不传递完整 context
- 摘要格式：`{step_id, status, output_summary, output_files[], key_decisions[]}`
- 大文件通过文件路径引用，不嵌入 context
- 编排器自身的 context 预算：不超过总 context window 的 20%
