---
name: test-gen
description: >
  测试生成 Skill。为代码生成单元测试、集成测试，覆盖正常路径、边界条件和异常情况。
---

# Test Gen — 测试生成

> 详细文档: [_architecture/L2-execution/core/test-gen/SKILL.md](_architecture/L2-execution/core/test-gen/SKILL.md)

## 测试类型

| 类型 | 说明 |
|-----|------|
| 单元测试 | 测试单个函数/方法 |
| 集成测试 | 测试组件交互 |
| 边界测试 | 边界条件覆盖 |
| 异常测试 | 错误处理验证 |

## 覆盖要求

- 正常路径: 所有主要功能
- 边界条件: 空值、极值
- 异常路径: 错误输入
- 目标覆盖率: ≥80%

## 待测代码

$ARGUMENTS

---

请生成全面的测试用例。
