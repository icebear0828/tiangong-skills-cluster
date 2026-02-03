---
name: code-orchestrator
description: >
  代码编排器。协调代码相关的多步骤任务，组合 code-gen、test-gen、review 等 skill。
---

# Code Orchestrator — 代码编排器

> 详细文档: [_architecture/L1-orchestrators/code-orchestrator/SKILL.md](_architecture/L1-orchestrators/code-orchestrator/SKILL.md)

## 可编排 Skills

- code-gen → code-review → test-gen
- debug → refactor → code-review
- 自定义组合

## 编排模式

- 顺序: A → B → C
- 并行: A | B → C
- 条件: if(x) A else B

## 编排任务

$ARGUMENTS

---

请分解任务并编排执行。
