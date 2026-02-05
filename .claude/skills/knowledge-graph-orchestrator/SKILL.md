---
name: knowledge-graph-orchestrator
description: >
  知识图谱编排器。编排 Phase 2 结构化阶段：关系增强→空间映射→聚类→可视化→学习路径推导。
  由 learning-commander 调度触发。
---

# Knowledge Graph Orchestrator — 知识图谱编排器

> 详细文档: [_architecture/L1-orchestrators/knowledge-graph-orchestrator/SKILL.md](_architecture/L1-orchestrators/knowledge-graph-orchestrator/SKILL.md)

## 编排流程 (Phase 2: 结构化)

### Step 1: 关系增强
- 补充隐含关系、验证合理性

### Step 2: 空间映射
- 调用 `/spatial-mapper` 确定节点位置

### Step 3: 聚类分析
- 识别概念群组、命名聚类

### Step 4: 可视化生成
- 调用 `/diagram-generator` 生成 Mermaid/Graphviz 代码

### Step 5: 学习路径推导
- 拓扑排序、生成建议学习顺序

## 图谱类型

| 类型 | 适用场景 |
|------|---------|
| concept_map | 概念关系理解 |
| mind_map | 头脑风暴、快速记忆 |
| knowledge_graph | 系统性知识组织 |
| learning_path | 学习路径规划 |

## 用户任务

$ARGUMENTS
