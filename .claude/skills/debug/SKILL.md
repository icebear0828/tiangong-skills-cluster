---
name: debug
description: >
  调试修复 Skill。诊断和修复代码 bug，分析错误原因，提供修复方案和预防建议。
---

# Debug — 调试修复

> 详细文档: [_architecture/L2-execution/core/debug/SKILL.md](_architecture/L2-execution/core/debug/SKILL.md)

## Bug 类型

| 类型 | 常见原因 |
|-----|---------|
| 逻辑错误 | 边界条件、算法缺陷 |
| 空指针 | 未检查 null |
| 类型错误 | 隐式转换 |
| 并发错误 | 竞态条件 |
| 资源错误 | 未关闭资源 |

## 诊断流程

1. 复现问题
2. 定位原因
3. 生成修复
4. 验证修复

## 问题描述

$ARGUMENTS

---

请诊断问题并提供修复方案。
