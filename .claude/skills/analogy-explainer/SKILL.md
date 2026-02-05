---
name: analogy-explainer
description: >
  类比解释器。为复杂概念生成易懂的类比解释，适配学习者背景。
  标注类比局限性，避免误导。由 learning-orchestrator / verification-orchestrator 调度。
---

# Analogy Explainer — 类比解释器

> 详细文档: [_architecture/L2-execution/core/analogy-explainer/SKILL.md](_architecture/L2-execution/core/analogy-explainer/SKILL.md)

## 执行流程

1. **概念分析**: 提取核心属性和关键特征
2. **学习者适配**: 根据熟悉领域和水平选择类比域
3. **类比生成**: 从类比库匹配，生成元素映射
4. **质量检查**: 验证映射准确性，标注局限性
5. **解释输出**: 简化解释 + 详细解释 + 引导问题

## 类比来源域

| 领域 | 适用 | 示例 |
|------|------|------|
| 日常生活 | 基础概念 | 变量 → 盒子 |
| 建筑/工程 | 架构/结构 | 软件架构 → 建筑设计 |
| 生物/自然 | 系统/演化 | 神经网络 → 大脑神经元 |
| 交通/物流 | 流程/传输 | 数据流 → 物流系统 |

## 用户任务

$ARGUMENTS
