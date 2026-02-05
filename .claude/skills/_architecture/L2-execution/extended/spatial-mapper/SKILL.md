---
name: spatial-mapper
description: >
  空间映射器 Skill。将概念列表和关系映射到空间布局。当需要：(1) 可视化知识结构，
  (2) 生成概念地图，(3) 空间化信息组织时触发。支持多种布局算法、聚类分析、
  位置优化。作为扩展学习 Skill，具有标准契约。
---

# Spatial Mapper — 空间映射器

## 触发条件

- 需要将知识结构可视化
- 由 knowledge-graph-orchestrator 调度
- 需要生成空间布局

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["concepts", "relationships"],
  "properties": {
    "concepts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "importance": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "category": { "type": "string" },
          "level": { "type": "integer" }
        }
      },
      "description": "概念列表"
    },
    "relationships": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["from", "to", "type"],
        "properties": {
          "from": { "type": "string" },
          "to": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["is_a", "part_of", "depends_on", "related_to", "contrasts_with"]
          },
          "weight": {
            "type": "number",
            "default": 1
          }
        }
      },
      "description": "关系列表"
    },
    "mapping_type": {
      "type": "string",
      "enum": ["hierarchical", "radial", "force_directed", "grid", "circular", "tree"],
      "default": "force_directed",
      "description": "映射类型"
    },
    "config": {
      "type": "object",
      "properties": {
        "canvas_width": {
          "type": "integer",
          "default": 1000
        },
        "canvas_height": {
          "type": "integer",
          "default": 800
        },
        "node_spacing": {
          "type": "integer",
          "default": 100
        },
        "cluster_by": {
          "type": "string",
          "enum": ["category", "level", "importance", "none"],
          "default": "category"
        },
        "emphasize_central": {
          "type": "boolean",
          "default": true
        }
      },
      "description": "布局配置"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["layout", "clusters"],
  "properties": {
    "layout": {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "x": { "type": "number" },
              "y": { "type": "number" },
              "size": { "type": "number" },
              "color": { "type": "string" },
              "label": { "type": "string" },
              "cluster_id": { "type": "string" }
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
              "path": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "x": { "type": "number" },
                    "y": { "type": "number" }
                  }
                }
              },
              "style": { "type": "string" }
            }
          }
        },
        "bounds": {
          "type": "object",
          "properties": {
            "min_x": { "type": "number" },
            "max_x": { "type": "number" },
            "min_y": { "type": "number" },
            "max_y": { "type": "number" }
          }
        }
      },
      "description": "空间布局"
    },
    "clusters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "members": {
            "type": "array",
            "items": { "type": "string" }
          },
          "centroid": {
            "type": "object",
            "properties": {
              "x": { "type": "number" },
              "y": { "type": "number" }
            }
          },
          "bounds": { "type": "object" },
          "color": { "type": "string" }
        }
      },
      "description": "聚类结果"
    },
    "analysis": {
      "type": "object",
      "properties": {
        "central_nodes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "peripheral_nodes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "bridge_nodes": {
          "type": "array",
          "items": { "type": "string" }
        },
        "isolated_nodes": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "布局分析"
    },
    "visualization_code": {
      "type": "object",
      "properties": {
        "svg": { "type": "string" },
        "html_canvas": { "type": "string" },
        "d3_code": { "type": "string" }
      },
      "description": "可视化代码"
    }
  }
}
```

## 布局算法

| 算法 | 适用场景 | 特点 |
|------|---------|------|
| hierarchical | 层次结构 | 清晰的上下级关系 |
| radial | 中心辐射 | 突出核心概念 |
| force_directed | 通用关系 | 自然分布、自动聚类 |
| grid | 规整展示 | 整齐、便于扫描 |
| circular | 环形展示 | 无明显层次 |
| tree | 树状结构 | 严格的父子关系 |

## 聚类策略

| 策略 | 描述 | 适用情况 |
|------|------|---------|
| category | 按类别聚类 | 概念有明确分类 |
| level | 按层次聚类 | 层次关系明确 |
| importance | 按重要度聚类 | 突出核心概念 |
| none | 不聚类 | 概念间关系复杂 |

## 执行流程

1. **数据预处理**
   - 验证输入数据
   - 计算节点度数
   - 识别中心节点

2. **聚类分析**
   - 按配置策略聚类
   - 命名聚类
   - 分配颜色

3. **初始布局**
   - 应用布局算法
   - 计算初始位置

4. **布局优化**
   - 减少边交叉
   - 调整节点间距
   - 确保标签可读

5. **可视化生成**
   - 生成 SVG 代码
   - 生成交互式 HTML

## 节点大小映射

| 属性 | 节点大小 |
|------|---------|
| 高重要度 | 大 |
| 高度数 | 大 |
| 中心节点 | 大 |
| 边缘节点 | 小 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 边交叉 | 最小化交叉 | 减少 |
| 间距均匀 | 节点间距合理 | 是 |
| 聚类清晰 | 同类节点聚集 | 是 |
| 中心突出 | 核心概念居中 | 是 |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| knowledge-extractor | 接收其提取的概念 |
| diagram-generator | 配合生成图表 |
| knowledge-graph-orchestrator | 由其调度 |

## 脚本

- `scripts/create_map.py` - 空间映射主脚本
- `scripts/layout_algorithms.py` - 布局算法库
- `scripts/cluster_analyzer.py` - 聚类分析器

## 参考资料

- `references/mapping-algorithms.md` - 布局算法详解
- `references/visualization-best-practices.md` - 可视化最佳实践
