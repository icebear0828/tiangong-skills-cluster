# DAG 执行模式

## 概述

本文档定义了 multi-agent-orchestrator 支持的 DAG（有向无环图）执行模式。

## 基础模式

### 1. Sequential Chain（顺序链）

最简单的 DAG，所有节点依次执行。

```
A → B → C → D
```

**适用场景**:
- 任务有严格的前后依赖
- 每步输出是下一步的输入
- 需要逐步积累 context

**配置示例**:
```json
{
  "pattern": "sequential",
  "nodes": [
    {"id": "A", "skill": "arch-explore"},
    {"id": "B", "skill": "api-design", "depends_on": ["A"]},
    {"id": "C", "skill": "code-gen", "depends_on": ["B"]},
    {"id": "D", "skill": "test-gen", "depends_on": ["C"]}
  ]
}
```

### 2. Parallel Fan-out（并行扇出）

多个独立任务并行执行后汇合。

```
        ┌→ B ─┐
    A ──┤→ C ─┼→ E
        └→ D ─┘
```

**适用场景**:
- 多个子任务相互独立
- 可以并行加速
- 最后需要汇总结果

**配置示例**:
```json
{
  "pattern": "parallel",
  "nodes": [
    {"id": "A", "skill": "arch-explore"},
    {"id": "B", "skill": "code-gen", "depends_on": ["A"], "parallel_group": 1},
    {"id": "C", "skill": "code-gen", "depends_on": ["A"], "parallel_group": 1},
    {"id": "D", "skill": "db-schema", "depends_on": ["A"], "parallel_group": 1},
    {"id": "E", "skill": "code-gen", "depends_on": ["B", "C", "D"]}
  ]
}
```

### 3. Diamond（菱形）

常见的分叉-汇合模式。

```
      ┌→ B ─┐
  A ──┤     ├→ D
      └→ C ─┘
```

**适用场景**:
- 前端和后端可并行开发
- 多个方案并行探索后选择
- 独立组件开发后集成

### 4. Iterative Refinement（迭代精炼）

带有反馈循环的执行模式。

```
A → B → eval → pass? → D
         ↓
        fail → A (loop, max N)
```

**适用场景**:
- 质量驱动开发
- 需要多轮优化
- 评测分数未达标时重试

**配置示例**:
```json
{
  "pattern": "iterative",
  "nodes": [
    {"id": "A", "skill": "code-gen"},
    {"id": "B", "skill": "code-review", "depends_on": ["A"]},
    {"id": "eval", "type": "gate", "depends_on": ["B"], "threshold": 0.8},
    {"id": "D", "skill": "doc-gen", "depends_on": ["eval"]}
  ],
  "max_iterations": 3,
  "retry_from": "A"
}
```

### 5. Conditional（条件分支）

根据运行时条件选择执行路径。

```
        ┌→ B (if condition)
    A ──┤
        └→ C (else)
```

**适用场景**:
- 根据分析结果选择不同策略
- 处理不同类型的输入
- 错误恢复路径

## 复合模式

### Full Stack Development

```
                    ┌→ db-schema ──┐
arch-explore ───────┤              ├→ code-gen (integration) → test-gen → doc-gen
                    └→ api-design ─┘
```

### Quality-Driven Development

```
                                ┌────────────────┐
                                ↓                │
code-gen → code-review → eval → (pass) → test-gen
                          ↓
                        (fail) → refactor ─┘
```

### Exploration & Implementation

```
arch-explore → prototype → eval → (good) → code-gen → test-gen
                           ↓
                         (bad) → arch-explore (retry)
```

## 节点类型

| 类型 | 描述 | 示例 |
|-----|------|-----|
| skill | 执行一个 skill | code-gen, test-gen |
| gate | 质量门禁检查点 | eval, threshold |
| merge | 合并多个输出 | combine outputs |
| split | 拆分任务 | fan out |
| transform | 数据转换 | format, filter |

## 执行策略

### 并行度控制

```json
{
  "max_parallel": 3,
  "parallel_strategy": "greedy"  // greedy | conservative
}
```

- **greedy**: 尽可能多地并行执行
- **conservative**: 保守并行，优先完成依赖链

### 失败处理

```json
{
  "on_failure": "retry_then_skip",  // retry_then_skip | retry_then_fail | fail_fast
  "max_retries": 2
}
```

### Context 传递

```json
{
  "context_strategy": "summary",  // full | summary | selective
  "summary_max_tokens": 500
}
```

## DAG 验证规则

1. **无环检测**: DAG 必须无循环（除了显式的迭代模式）
2. **可达性**: 所有节点必须从起始节点可达
3. **终止性**: 必须有明确的终止节点
4. **依赖完整**: 所有 depends_on 引用的节点必须存在
