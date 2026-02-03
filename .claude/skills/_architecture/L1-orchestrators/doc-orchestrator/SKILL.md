---
name: doc-orchestrator
description: >
  文档领域编排器。当文档相关的多步骤任务需要协调执行时触发。负责分解文档任务，
  协调 doc-gen、code-review（文档审查）、arch-explore（架构文档）等 skill 的执行，
  确保文档完整性、准确性和一致性。支持顺序链和并行扇出模式。
---

# Doc Orchestrator — 文档领域编排器

## 触发条件

由 Meta-Commander 路由触发，当任务满足以下条件时：
- 复杂度为 M 级
- 主要领域为 doc
- 需要生成多种类型的文档

## 输入格式

```json
{
  "task_id": "...",
  "task_description": "...",
  "complexity": "M",
  "domains": ["doc"],
  "context": {
    "doc_type": "api | readme | architecture | user-guide",
    "source_files": [],
    "target_audience": "developer | user | admin"
  }
}
```

## 编排模式

### 模式 1: Sequential Chain（顺序链）

适用场景：标准文档生成流程

```
arch-explore (理解结构)
    ↓
doc-gen (生成文档)
    ↓
code-review (文档审查)
```

### 模式 2: Parallel Fan-out（并行扇出）

适用场景：生成多种类型的文档

```
        ┌→ doc-gen (API 文档) ─┐
源分析 ─┤→ doc-gen (README) ───┤→ 汇总审查
        └→ doc-gen (架构文档) ─┘
```

## 文档类型模板

### API 文档

```
1. arch-explore: 分析 API 结构
2. doc-gen: 生成 OpenAPI/Swagger 规范
3. doc-gen: 生成 Markdown API 参考
4. code-review: 检查与代码一致性
```

### README 文档

```
1. arch-explore: 理解项目目的和结构
2. doc-gen: 生成 README 各部分
   - 项目简介
   - 安装指南
   - 快速开始
   - 配置说明
3. code-review: 检查示例代码正确性
```

### 架构文档

```
1. arch-explore: 深入分析架构
2. doc-gen: 生成架构概述
3. doc-gen: 生成组件说明
4. doc-gen: 生成数据流图描述
5. code-review: 验证与实际代码一致
```

## 质量门禁

参考 `references/quality-gates.md`：

### doc-gen 门禁
- [ ] 文档格式正确（Markdown/RST 可解析）
- [ ] 包含必要章节（标题、概述、详情）
- [ ] 代码示例可执行
- [ ] 无占位符残留

### 审查门禁
- [ ] 与源代码一致
- [ ] 术语使用一致
- [ ] 链接有效
- [ ] 图表清晰

## 输出结构

```json
{
  "task_id": "...",
  "status": "completed",
  "documents": {
    "readme": "path/to/README.md",
    "api_doc": "path/to/api.md",
    "architecture": "path/to/architecture.md"
  },
  "quality_scores": {
    "completeness": 0.9,
    "accuracy": 0.85,
    "readability": 0.88
  }
}
```

## 与其他组件交互

- 调用 code-gen 获取代码结构信息
- 调用 arch-explore 理解架构
- 调用 code-review 验证文档准确性
