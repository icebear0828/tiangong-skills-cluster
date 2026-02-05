---
name: knowledge-extractor
description: >
  知识提取器。从文本中提取结构化知识项：概念、原则、事实、步骤、技能、模式。
  支持多种内容类型和提取深度。由 learning-orchestrator 调度。
---

# Knowledge Extractor — 知识提取器

> 详细文档: [_architecture/L2-execution/core/knowledge-extractor/SKILL.md](_architecture/L2-execution/core/knowledge-extractor/SKILL.md)

## 执行流程

1. **预处理**: 清洗文本，识别结构
2. **概念识别**: 提取实体和领域术语
3. **关系提取**: 识别 is_a / part_of / depends_on / related_to 等关系
4. **层次构建**: 构建概念树，确定根节点
5. **摘要生成**: 一句话摘要 + 段落摘要 + 关键要点

## 知识类型

| 类型 | 示例 |
|------|------|
| concept | "函数式编程" |
| principle | "单一职责原则" |
| fact | "JavaScript 是单线程的" |
| procedure | "创建 React 组件的步骤" |
| pattern | "观察者模式" |

## 用户任务

$ARGUMENTS
