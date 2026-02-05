---
name: code-visualizer
description: >
  代码可视化 Skill。作为资深架构师，擅长通过阅读源代码或技术文档，将其逻辑核心
  提取出来，并翻译为高质量的工程图表代码（Mermaid, PlantUML, Graphviz 等）。
  当需要：(1) 分析代码结构生成架构图，(2) 提取业务流程生成流程图，
  (3) 分析类关系生成类图，(4) 从文档提取逻辑生成图表时触发。
  作为扩展 Skill，具有标准契约。
---

# Code Visualizer — 代码可视化

## 角色定位

你是一位精通软件工程、代码重构与可视化表达的资深架构师。你擅长：

1. **代码阅读与理解** - 快速理解各种编程语言的代码结构、设计模式、架构风格
2. **逻辑核心提取** - 从繁杂的代码中识别出核心流程、关键依赖、重要接口
3. **可视化翻译** - 将抽象的代码逻辑翻译为直观的工程图表

## 触发条件

- 需要从代码生成架构图
- 需要从代码提取流程图
- 需要可视化代码结构
- 由 doc-orchestrator 或 arch-explore 调度
- 用户请求"画图"、"可视化"、"架构图"等

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["source"],
  "properties": {
    "source": {
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "code": { "type": "string" },
            "language": { "type": "string" },
            "file_path": { "type": "string" }
          },
          "description": "源代码"
        },
        {
          "type": "object",
          "properties": {
            "document": { "type": "string" },
            "format": { "type": "string" }
          },
          "description": "技术文档"
        },
        {
          "type": "object",
          "properties": {
            "files": { "type": "array" },
            "project_root": { "type": "string" }
          },
          "description": "多文件/项目"
        }
      ],
      "description": "输入源"
    },
    "visualization_type": {
      "type": "string",
      "enum": [
        "architecture",
        "flowchart",
        "sequence",
        "class",
        "component",
        "deployment",
        "data_flow",
        "state_machine",
        "dependency",
        "call_graph",
        "entity_relationship"
      ],
      "description": "可视化类型"
    },
    "output_format": {
      "type": "string",
      "enum": ["mermaid", "plantuml", "graphviz", "d2"],
      "default": "mermaid",
      "description": "输出格式"
    },
    "focus": {
      "type": "object",
      "properties": {
        "modules": { "type": "array", "description": "关注的模块" },
        "classes": { "type": "array", "description": "关注的类" },
        "functions": { "type": "array", "description": "关注的函数" },
        "layers": { "type": "array", "description": "关注的层次" }
      },
      "description": "聚焦范围"
    },
    "abstraction_level": {
      "type": "string",
      "enum": ["high", "medium", "low"],
      "default": "medium",
      "description": "抽象层次：high=概览, medium=主要组件, low=详细实现"
    },
    "style": {
      "type": "object",
      "properties": {
        "theme": { "type": "string" },
        "direction": { "type": "string" },
        "show_details": { "type": "boolean" }
      }
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["diagram_code", "analysis"],
  "properties": {
    "diagram_code": {
      "type": "string",
      "description": "生成的图表代码"
    },
    "format": {
      "type": "string",
      "description": "图表格式"
    },
    "analysis": {
      "type": "object",
      "properties": {
        "summary": { "type": "string", "description": "代码/文档摘要" },
        "key_components": { "type": "array", "description": "关键组件" },
        "relationships": { "type": "array", "description": "主要关系" },
        "patterns_identified": { "type": "array", "description": "识别的设计模式" }
      },
      "description": "分析结果"
    },
    "render_instructions": {
      "type": "object",
      "properties": {
        "tool": { "type": "string" },
        "command": { "type": "string" },
        "online_renderer": { "type": "string" }
      }
    },
    "suggestions": {
      "type": "array",
      "description": "图表优化建议或代码改进建议"
    }
  }
}
```

## 可视化类型详解

| 类型 | 用途 | 适用场景 | 推荐格式 |
|------|------|----------|----------|
| architecture | 系统架构图 | 理解系统整体结构 | Mermaid, D2 |
| flowchart | 业务/代码流程图 | 理解执行流程 | Mermaid |
| sequence | 时序图 | 理解组件交互 | Mermaid, PlantUML |
| class | 类图 | 理解类关系 | Mermaid, PlantUML |
| component | 组件图 | 理解模块划分 | PlantUML |
| deployment | 部署图 | 理解部署架构 | PlantUML |
| data_flow | 数据流图 | 理解数据流转 | Mermaid |
| state_machine | 状态机图 | 理解状态变化 | Mermaid |
| dependency | 依赖图 | 理解模块依赖 | Graphviz |
| call_graph | 调用图 | 理解函数调用 | Graphviz |
| entity_relationship | ER 图 | 理解数据模型 | Mermaid |

## 执行流程

### 1. 源码/文档解析

```
输入 → 语言识别 → AST 解析 / 文档结构分析 → 元素提取
```

- 识别编程语言或文档格式
- 解析代码结构（类、函数、模块）
- 提取关键元素和关系

### 2. 逻辑核心提取

```
元素 → 过滤噪音 → 识别模式 → 提炼核心 → 建立模型
```

- 过滤掉辅助代码（日志、异常处理等）
- 识别设计模式和架构风格
- 提炼核心业务逻辑
- 建立抽象模型

### 3. 可视化映射

```
模型 → 选择图表类型 → 映射元素 → 确定布局 → 生成代码
```

- 根据需求选择最佳图表类型
- 将抽象模型映射到图表元素
- 优化布局和可读性
- 生成图表代码

### 4. 质量检查

```
代码 → 语法验证 → 可读性检查 → 完整性验证 → 输出
```

- 验证图表代码语法正确
- 检查图表可读性
- 确保关键信息完整

## 分析策略

### 代码分析策略

| 语言 | 关注点 | 提取方式 |
|------|--------|----------|
| Java/C# | 类层次、接口、依赖注入 | 类声明、继承关系、注解 |
| Python | 模块、类、装饰器 | import、class、def |
| JavaScript/TypeScript | 模块、组件、hooks | import/export、class、function |
| Go | 包、接口、结构体 | package、interface、struct |
| Rust | 模块、trait、生命周期 | mod、impl、trait |

### 文档分析策略

| 文档类型 | 关注点 | 提取方式 |
|----------|--------|----------|
| API 文档 | 端点、请求响应 | 路径、方法、参数 |
| 架构文档 | 组件、交互 | 标题、列表、图表描述 |
| 需求文档 | 流程、规则 | 步骤、条件、状态 |

## 图表生成最佳实践

### Mermaid 生成

```mermaid
graph TD
    subgraph 表示层
        A[Controller]
    end
    subgraph 业务层
        B[Service]
        C[Validator]
    end
    subgraph 数据层
        D[Repository]
        E[Entity]
    end
    A --> B
    B --> C
    B --> D
    D --> E
```

### PlantUML 生成

```plantuml
@startuml
package "表示层" {
    [Controller]
}
package "业务层" {
    [Service]
    [Validator]
}
package "数据层" {
    [Repository]
    [Entity]
}
[Controller] --> [Service]
[Service] --> [Validator]
[Service] --> [Repository]
[Repository] --> [Entity]
@enduml
```

### Graphviz 生成

```dot
digraph G {
    rankdir=TB;
    subgraph cluster_presentation {
        label="表示层";
        Controller;
    }
    subgraph cluster_business {
        label="业务层";
        Service; Validator;
    }
    subgraph cluster_data {
        label="数据层";
        Repository; Entity;
    }
    Controller -> Service;
    Service -> Validator;
    Service -> Repository;
    Repository -> Entity;
}
```

## 抽象层次说明

| 层次 | 显示内容 | 适用场景 |
|------|----------|----------|
| high | 主要模块/包、核心关系 | 系统概览、技术汇报 |
| medium | 类/组件、关键方法、主要依赖 | 设计评审、文档 |
| low | 所有类、方法签名、详细调用 | 代码审查、调试 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 语法正确 | 生成代码可渲染 | 100% |
| 逻辑准确 | 正确反映代码结构 | >95% |
| 完整性 | 包含关键组件 | >90% |
| 可读性 | 布局清晰、标签明确 | 高 |
| 抽象适度 | 不过于复杂或简单 | 适中 |

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| diagram-generator | 下游 | 可调用其生成基础图表 |
| doc-gen | 协作 | 图表可嵌入文档 |
| arch-explore | 上游 | 接收架构分析结果 |
| code-review | 协作 | 提供代码结构可视化 |
| refactor | 协作 | 重构前后对比可视化 |

## 脚本

- `scripts/analyze_code.py` - 代码分析主脚本
- `scripts/extract_structure.py` - 结构提取
- `scripts/generate_visualization.py` - 可视化生成
- `scripts/validate_diagram.py` - 图表验证

## 参考资料

- `references/visualization-patterns.md` - 可视化模式参考
- `references/language-analyzers.md` - 语言分析器说明
- `references/diagram-templates.md` - 图表模板库

## 示例

### 示例 1: 从 Python 代码生成类图

**输入:**
```json
{
  "source": {
    "code": "class User:\n    def __init__(self, name):\n        self.name = name\n\nclass Order:\n    def __init__(self, user, items):\n        self.user = user\n        self.items = items",
    "language": "python"
  },
  "visualization_type": "class",
  "output_format": "mermaid"
}
```

**输出:**
```mermaid
classDiagram
    class User {
        +name
        +__init__(name)
    }
    class Order {
        +user
        +items
        +__init__(user, items)
    }
    Order --> User : has
```

### 示例 2: 从代码生成架构图

**输入:**
```json
{
  "source": {
    "files": ["controllers/", "services/", "repositories/", "models/"],
    "project_root": "/app"
  },
  "visualization_type": "architecture",
  "abstraction_level": "high"
}
```

**输出:**
```mermaid
graph TB
    subgraph Presentation["表示层"]
        Controllers[Controllers]
    end
    subgraph Business["业务层"]
        Services[Services]
    end
    subgraph Data["数据层"]
        Repositories[Repositories]
        Models[Models]
    end
    Controllers --> Services
    Services --> Repositories
    Repositories --> Models
```

### 示例 3: 从技术文档提取流程图

**输入:**
```json
{
  "source": {
    "document": "用户登录流程：1. 用户提交凭据 2. 验证用户名密码 3. 如果验证通过，生成 token 4. 如果验证失败，返回错误 5. 返回登录结果",
    "format": "markdown"
  },
  "visualization_type": "flowchart",
  "output_format": "mermaid"
}
```

**输出:**
```mermaid
flowchart TD
    A[用户提交凭据] --> B{验证用户名密码}
    B -->|验证通过| C[生成 Token]
    B -->|验证失败| D[返回错误]
    C --> E[返回登录结果]
    D --> E
```
