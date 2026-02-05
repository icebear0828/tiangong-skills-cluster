---
name: self-explanation-validator
description: >
  自我解释验证器。验证学习者解释是否正确，识别误解，提供改进建议和补救策略。
  由 verification-orchestrator 调度。
---

# Self-Explanation Validator — 自我解释验证器

> 详细文档: [_architecture/L2-execution/core/self-explanation-validator/SKILL.md](_architecture/L2-execution/core/self-explanation-validator/SKILL.md)

## 执行流程

1. **解析输入**: 提取学习者解释的关键点
2. **对比分析**: 逐点比较准确性、完整性、清晰度
3. **误解检测**: 匹配常见误解模式，分析错误根源
4. **评分计算**: 各维度评分 → 加权汇总 → 掌握等级
5. **反馈生成**: 改进建议 + 推荐资源 + 后续问题

## 掌握等级

| 等级 | 分数 | 描述 |
|------|------|------|
| mastered | ≥90 | 完全掌握 |
| proficient | 75-89 | 熟练 |
| developing | 60-74 | 发展中 |
| beginning | 40-59 | 初步理解 |
| misconceived | <40 | 存在严重误解 |

## 用户任务

$ARGUMENTS
