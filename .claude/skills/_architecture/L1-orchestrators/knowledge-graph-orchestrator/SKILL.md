---
name: knowledge-graph-orchestrator
description: >
  知识图谱编排器。编排知识提取+空间映射+图谱构建流程。当需要：(1) 构建知识图谱，
  (2) 可视化概念关系，(3) 生成学习地图时触发。支持多种图谱类型、链接策略、
  可视化输出。由 learning-commander 调度触发。
---

# Knowledge Graph Orchestrator — 知识图谱编排器

## 触发条件

- 进入 Phase 2 结构化阶段
- 由 learning-commander 调度
- 需要构建知识间关联结构

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["knowledge_base"],
  "properties": {
    "knowledge_base": {
      "type": "object",
      "properties": {
        "concepts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "definition": { "type": "string" },
              "importance": { "type": "string" }
            }
          }
        },
        "relationships": { "type": "array" },
        "hierarchy": { "type": "object" }
      },
      "description": "来自 Phase 1 的知识库"
    },
    "graph_config": {
      "type": "object",
      "properties": {
        "graph_type": {
          "type": "string",
          "enum": ["concept_map", "mind_map", "knowledge_graph", "learning_path"],
          "default": "concept_map"
        },
        "layout": {
          "type": "string",
          "enum": ["hierarchical", "radial", "force_directed", "circular"],
          "default": "hierarchical"
        },
        "include_visualization": {
          "type": "boolean",
          "default": true
        },
        "linking_strategy": {
          "type": "string",
          "enum": ["explicit", "semantic", "hybrid"],
          "default": "hybrid"
        },
        "max_depth": {
          "type": "integer",
          "default": 4
        }
      },
      "description": "图谱配置"
    },
    "external_connections": {
      "type": "object",
      "properties": {
        "link_to_existing": {
          "type": "boolean",
          "default": true
        },
        "existing_graphs": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "外部连接配置"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["graph", "visualization"],
  "properties": {
    "graph": {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "label": { "type": "string" },
              "type": { "type": "string" },
              "properties": { "type": "object" },
              "position": {
                "type": "object",
                "properties": {
                  "x": { "type": "number" },
                  "y": { "type": "number" }
                }
              }
            }
          }
        },
        "edges": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "source": { "type": "string" },
              "target": { "type": "string" },
              "type": { "type": "string" },
              "label": { "type": "string" },
              "weight": { "type": "number" }
            }
          }
        },
        "clusters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "members": { "type": "array" }
            }
          },
          "description": "概念聚类"
        }
      },
      "description": "图谱数据结构"
    },
    "visualization": {
      "type": "object",
      "properties": {
        "mermaid_code": { "type": "string" },
        "graphviz_code": { "type": "string" },
        "svg_path": { "type": "string" },
        "interactive_html_path": { "type": "string" }
      },
      "description": "可视化输出"
    },
    "analysis": {
      "type": "object",
      "properties": {
        "central_concepts": {
          "type": "array",
          "items": { "type": "string" }
        },
        "concept_importance": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "learning_sequence": {
          "type": "array",
          "items": { "type": "string" },
          "description": "建议学习顺序"
        },
        "dependency_chains": {
          "type": "array",
          "items": { "type": "array" }
        }
      },
      "description": "图谱分析"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "node_count": { "type": "integer" },
        "edge_count": { "type": "integer" },
        "avg_degree": { "type": "number" },
        "depth": { "type": "integer" }
      }
    }
  }
}
```

## 图谱类型

| 类型 | 适用场景 | 特点 |
|------|---------|------|
| concept_map | 概念关系理解 | 显示所有关系类型 |
| mind_map | 头脑风暴、快速记忆 | 放射状、单中心 |
| knowledge_graph | 系统性知识组织 | 严格类型、可查询 |
| learning_path | 学习路径规划 | 有向、显示依赖 |

## 链接策略

| 策略 | 描述 | 适用情况 |
|------|------|---------|
| explicit | 仅使用明确声明的关系 | 精确要求高 |
| semantic | 使用语义相似性推断关系 | 关系不完整 |
| hybrid | 结合两种策略 | 一般情况 |

## 编排流程

```
┌─────────────────────────────────────────────┐
│  Phase 2: 结构化 (Structure)                 │
│                                             │
│  Step 1: 关系增强                            │
│  ├─ 补充隐含关系                             │
│  └─ 验证关系合理性                           │
│                                             │
│  Step 2: 空间映射                            │
│  ├─ 调用 spatial-mapper                     │
│  └─ 确定节点位置                             │
│                                             │
│  Step 3: 聚类分析                            │
│  ├─ 识别概念群组                             │
│  └─ 命名聚类                                │
│                                             │
│  Step 4: 可视化生成                          │
│  ├─ 调用 diagram-generator                  │
│  └─ 生成多种格式                             │
│                                             │
│  Step 5: 学习路径推导                        │
│  ├─ 拓扑排序                                │
│  └─ 生成建议顺序                             │
│                                             │
│  输出 → verification-orchestrator (Phase 3)  │
└─────────────────────────────────────────────┘
```

## 质量关卡

| 检查点 | 标准 | 未通过处理 |
|--------|------|-----------|
| 连通性 | 图谱连通 | 补充关系 |
| 无环性 | 依赖图无环 | 移除错误边 |
| 中心性 | 有明确中心概念 | 重新分析 |
| 可视化 | 生成成功 | 简化图谱 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| knowledge-extractor | 接收输入 | 使用其提取结果 |
| spatial-mapper | 调用 | Step 2 |
| diagram-generator | 调用 | Step 4 |
| learning-orchestrator | 接收输入 | 来自 Phase 1 |
| verification-orchestrator | 输出传递 | 到 Phase 3 |

## 脚本

- `scripts/build_graph.py` - 图谱构建主脚本
- `scripts/cluster_analyzer.py` - 聚类分析器
- `scripts/path_calculator.py` - 路径计算器

## 参考资料

- `references/graph-patterns.md` - 图谱模式
- `references/linking-strategies.md` - 链接策略
- `references/layout-algorithms.md` - 布局算法
