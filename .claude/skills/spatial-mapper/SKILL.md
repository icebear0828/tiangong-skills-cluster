---
name: spatial-mapper
description: >
  概念空间映射器。将概念列表映射到空间布局，识别聚类和关系。
  由 knowledge-graph-orchestrator 在 Phase 2 调度。
---

# Spatial Mapper — 概念空间映射器

> 详细文档: [_architecture/L2-execution/extended/spatial-mapper/SKILL.md](_architecture/L2-execution/extended/spatial-mapper/SKILL.md)

## 布局类型

| 布局 | 适用场景 |
|------|---------|
| hierarchical | 树形知识结构 |
| radial | 以核心概念为中心 |
| force_directed | 自由关系网络 |
| circular | 周期/循环结构 |

## 输出: 空间布局 + 聚类 + 可视化代码

## 用户任务

$ARGUMENTS
