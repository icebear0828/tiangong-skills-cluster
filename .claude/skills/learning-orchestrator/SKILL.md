---
name: learning-orchestrator
description: >
  学习消化编排器。编排 Phase 1 消化阶段：内容获取→知识提取→类比生成。
  由 learning-commander 调度触发。
---

# Learning Orchestrator — 学习消化编排器

> 详细文档: [_architecture/L1-orchestrators/learning-orchestrator/SKILL.md](_architecture/L1-orchestrators/learning-orchestrator/SKILL.md)

## 编排流程 (Phase 1: 消化)

### Step 1: 内容获取
- 调用 `/content-curator` 策展学习资源
- 收集、排序相关资源

### Step 2: 知识提取
- 调用 `/knowledge-extractor` 提取结构化知识
- 输出概念、原则、事实、关系

### Step 3: 类比生成
- 调用 `/analogy-explainer` 为核心概念生成类比
- 适配学习者背景和水平

### Step 4: 质量检查
- 验证知识覆盖度 ≥80%
- 确保核心概念有类比

## 深度配置

| 深度 | 概念数 | 类比数 |
|------|--------|--------|
| overview | 5-8 | 2-3 |
| standard | 10-15 | 4-6 |
| comprehensive | 20-30 | 8-12 |

## 用户任务

$ARGUMENTS
