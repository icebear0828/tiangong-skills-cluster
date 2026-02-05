---
name: micro-project-orchestrator
description: >
  微项目实践编排器。编排 Phase 4 应用阶段：项目生成→练习指导→代码评审→能力评估。
  由 learning-commander 调度触发。
---

# Micro-Project Orchestrator — 微项目实践编排器

> 详细文档: [_architecture/L1-orchestrators/micro-project-orchestrator/SKILL.md](_architecture/L1-orchestrators/micro-project-orchestrator/SKILL.md)

## 编排流程 (Phase 4: 应用)

### Step 1: 项目生成
- 根据学习内容设计微项目
- 调用 `/code-gen` 生成项目骨架

### Step 2: 练习指导
- 提供分步指导和提示

### Step 3: 代码评审
- 调用 `/code-review` 检查概念应用正确性
- 调用 `/test-gen` 生成测试验证

### Step 4: 能力评估
- 评估应用能力和知识迁移
- 确定最终掌握等级

## 用户任务

$ARGUMENTS
