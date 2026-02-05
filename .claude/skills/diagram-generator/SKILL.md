---
name: diagram-generator
description: >
  图表生成器。根据结构化数据生成 Mermaid/Graphviz/PlantUML 图表代码。
  支持流程图、类图、序列图、知识图谱等多种类型。
---

# Diagram Generator — 图表生成器

> 详细文档: [_architecture/L2-execution/experimental/diagram-generator/SKILL.md](_architecture/L2-execution/experimental/diagram-generator/SKILL.md)

## 支持的图表类型

| 类型 | 格式 | 适用场景 |
|------|------|---------|
| flowchart | Mermaid | 流程和决策 |
| class_diagram | Mermaid | 类结构和关系 |
| sequence | Mermaid | 交互时序 |
| knowledge_graph | Graphviz | 知识图谱 |
| mind_map | Mermaid | 思维导图 |
| state_diagram | Mermaid | 状态机 |

## 输出: 图表代码 + 渲染说明

## 用户任务

$ARGUMENTS
