---
name: code-gen
description: >
  代码生成 Skill。根据需求描述生成高质量代码，支持多种语言和框架，
  遵循项目代码风格和最佳实践。
---

# Code Gen — 代码生成

> 详细文档: [_architecture/L2-execution/core/code-gen/SKILL.md](_architecture/L2-execution/core/code-gen/SKILL.md)

## 质量标准

| 维度 | 标准 |
|-----|------|
| 正确性 | 实现需求描述的功能 |
| 可读性 | 命名清晰、结构合理 |
| 健壮性 | 处理边界条件和异常 |
| 类型安全 | 完整的类型注解 |

## 语言规范

- **Python**: type hints, PEP 8, Google style docstring
- **TypeScript**: ES6+, async/await, strict mode
- **Go**: Go 惯例, error 返回, context.Context

## 用户需求

$ARGUMENTS

---

请根据需求生成符合质量标准的代码。
