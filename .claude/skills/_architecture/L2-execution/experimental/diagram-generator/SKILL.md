---
name: diagram-generator
description: >
  图表生成器 Skill。将结构化数据转换为图表代码。当需要：(1) 生成流程图，
  (2) 生成关系图，(3) 生成各类图表时触发。支持 Mermaid、Graphviz、PlantUML
  等多种格式。作为实验性 Skill，具有灵活契约。
---

# Diagram Generator — 图表生成器

## 触发条件

- 需要生成可视化图表
- 由 knowledge-graph-orchestrator 调度
- 需要将数据转为图表代码

## 输入契约 (Flexible)

```json
{
  "type": "object",
  "required": ["data", "diagram_type"],
  "properties": {
    "data": {
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "nodes": { "type": "array" },
            "edges": { "type": "array" }
          },
          "description": "图结构数据"
        },
        {
          "type": "object",
          "properties": {
            "steps": { "type": "array" },
            "decisions": { "type": "array" }
          },
          "description": "流程数据"
        },
        {
          "type": "object",
          "properties": {
            "items": { "type": "array" },
            "hierarchy": { "type": "object" }
          },
          "description": "层次数据"
        },
        {
          "type": "object",
          "properties": {
            "events": { "type": "array" },
            "timeline": { "type": "object" }
          },
          "description": "时序数据"
        }
      ],
      "description": "结构化数据"
    },
    "diagram_type": {
      "type": "string",
      "enum": [
        "flowchart",
        "sequence",
        "class",
        "state",
        "er",
        "gantt",
        "pie",
        "mindmap",
        "graph",
        "tree"
      ],
      "description": "图表类型"
    },
    "output_format": {
      "type": "string",
      "enum": ["mermaid", "graphviz", "plantuml", "d3", "svg"],
      "default": "mermaid",
      "description": "输出格式"
    },
    "style": {
      "type": "object",
      "properties": {
        "theme": {
          "type": "string",
          "enum": ["default", "dark", "forest", "neutral"],
          "default": "default"
        },
        "direction": {
          "type": "string",
          "enum": ["TB", "BT", "LR", "RL"],
          "default": "TB"
        },
        "node_shape": { "type": "string" },
        "edge_style": { "type": "string" },
        "colors": { "type": "object" }
      },
      "description": "样式配置"
    }
  }
}
```

## 输出契约 (Flexible)

```json
{
  "type": "object",
  "required": ["code"],
  "properties": {
    "code": {
      "type": "string",
      "description": "生成的图表代码"
    },
    "format": {
      "type": "string",
      "description": "代码格式"
    },
    "preview_svg": {
      "type": "string",
      "description": "SVG 预览（如可生成）"
    },
    "render_instructions": {
      "type": "object",
      "properties": {
        "tool": { "type": "string" },
        "command": { "type": "string" },
        "online_renderer": { "type": "string" }
      },
      "description": "渲染说明"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "node_count": { "type": "integer" },
        "edge_count": { "type": "integer" },
        "complexity": { "type": "string" }
      }
    }
  }
}
```

## 支持的图表类型

| 类型 | 描述 | 推荐格式 |
|------|------|---------|
| flowchart | 流程图 | Mermaid |
| sequence | 时序图 | Mermaid, PlantUML |
| class | 类图 | Mermaid, PlantUML |
| state | 状态图 | Mermaid |
| er | ER 图 | Mermaid |
| gantt | 甘特图 | Mermaid |
| pie | 饼图 | Mermaid |
| mindmap | 思维导图 | Mermaid |
| graph | 通用图 | Graphviz |
| tree | 树状图 | D3 |

## 输出格式

### Mermaid
```
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
```

### Graphviz (DOT)
```
digraph G {
    A -> B;
    B -> C;
    B -> D;
}
```

### PlantUML
```
@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi
@enduml
```

## 执行流程

1. **数据解析**
   - 解析输入数据结构
   - 识别节点和边
   - 确定图表元素

2. **类型适配**
   - 根据图表类型转换数据
   - 处理特殊语法需求

3. **代码生成**
   - 生成图表代码
   - 应用样式配置

4. **验证优化**
   - 验证代码语法
   - 优化布局提示

## 样式主题

| 主题 | 适用场景 |
|------|---------|
| default | 一般用途 |
| dark | 深色背景 |
| forest | 自然主题 |
| neutral | 专业文档 |

## 布局方向

| 方向 | 描述 |
|------|------|
| TB | 上到下 |
| BT | 下到上 |
| LR | 左到右 |
| RL | 右到左 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 语法正确 | 代码可渲染 | 100% |
| 可读性 | 代码格式清晰 | 高 |
| 完整性 | 包含所有元素 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| spatial-mapper | 接收其布局数据 |
| knowledge-graph-orchestrator | 由其调度 |
| doc-gen | 可嵌入文档 |

## 脚本

- `scripts/generate_diagram.py` - 图表生成主脚本
- `scripts/mermaid_generator.py` - Mermaid 生成器
- `scripts/graphviz_generator.py` - Graphviz 生成器
- `scripts/plantuml_generator.py` - PlantUML 生成器

## 参考资料

- `references/diagram-types.md` - 图表类型说明
- `references/mermaid-syntax.md` - Mermaid 语法参考
- `references/graphviz-syntax.md` - Graphviz 语法参考

## 示例

### 输入
```json
{
  "data": {
    "nodes": [
      {"id": "A", "label": "Start"},
      {"id": "B", "label": "Process"},
      {"id": "C", "label": "End"}
    ],
    "edges": [
      {"from": "A", "to": "B"},
      {"from": "B", "to": "C"}
    ]
  },
  "diagram_type": "flowchart",
  "output_format": "mermaid"
}
```

### 输出
```
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```
