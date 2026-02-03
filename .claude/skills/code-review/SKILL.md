---
name: code-review
description: >
  代码审查 Skill。检查代码质量、安全漏洞、性能问题，提供改进建议。
---

# Code Review — 代码审查

> 详细文档: [_architecture/L2-execution/core/code-review/SKILL.md](_architecture/L2-execution/core/code-review/SKILL.md)

## 审查维度

| 维度 | 检查项 |
|-----|--------|
| 正确性 | 逻辑错误、边界处理 |
| 安全性 | 注入、XSS、敏感数据 |
| 性能 | 复杂度、资源使用 |
| 可读性 | 命名、注释、结构 |

## 严重级别

- **Critical**: 必须立即修复
- **Major**: 应该修复
- **Minor**: 建议改进

## 待审查代码

$ARGUMENTS

---

请审查代码并按严重级别列出问题和修复建议。
