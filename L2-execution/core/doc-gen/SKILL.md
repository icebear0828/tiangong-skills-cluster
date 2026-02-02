---
name: doc-gen
description: >
  文档生成 Skill。为代码、API、项目生成技术文档。当需要：(1) 生成 API 文档，
  (2) 创建 README，(3) 生成代码注释，(4) 编写架构文档时触发。支持多种文档格式，
  自动提取代码结构和类型信息。作为核心 Skill，具有严格契约。
---

# Doc Gen — 文档生成

## 触发条件

- 代码生成后自动触发（如配置）
- 需求包含"文档"关键词
- 由 doc-orchestrator 调度

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["source"],
  "properties": {
    "source": {
      "type": "string",
      "description": "源代码或需求描述"
    },
    "doc_type": {
      "type": "string",
      "enum": ["api", "readme", "docstring", "architecture", "user_guide"]
    },
    "language": {
      "type": "string"
    },
    "target_audience": {
      "type": "string",
      "enum": ["developer", "user", "admin", "all"]
    },
    "format": {
      "type": "string",
      "enum": ["markdown", "rst", "html", "docstring"]
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["document", "files"],
  "properties": {
    "document": {
      "type": "string",
      "description": "生成的文档内容"
    },
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "content": { "type": "string" }
        }
      }
    },
    "sections": {
      "type": "array",
      "description": "文档章节列表"
    },
    "quality_score": {
      "type": "number"
    }
  }
}
```

## 文档类型

参考 `references/doc-templates.md`：

### 1. API 文档
- 端点描述
- 参数说明
- 响应格式
- 示例

### 2. README
- 项目简介
- 安装指南
- 快速开始
- 使用示例

### 3. Docstring
- 函数描述
- 参数说明
- 返回值
- 异常

### 4. 架构文档
- 系统概述
- 组件说明
- 数据流
- 部署架构

## 执行流程

1. **分析源码**
   - 提取函数/类结构
   - 识别参数类型
   - 理解代码逻辑

2. **确定文档结构**
   - 选择模板
   - 规划章节
   - 确定详细程度

3. **生成内容**
   - 编写描述
   - 添加示例
   - 格式化

4. **质量检查**
   - 完整性检查
   - 格式验证
   - 术语一致性

## 脚本

- `scripts/generate_doc.py` - 文档生成主脚本
