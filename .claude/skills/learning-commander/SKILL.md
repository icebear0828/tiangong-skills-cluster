---
name: learning-commander
description: >
  学习域总指挥。学习任务的第一入口点。分析学习需求，生成学习计划，路由到对应阶段编排器执行。
  支持四阶段学习：消化→结构化→内化→应用。
---

# Learning Commander — 学习域总指挥

> 详细文档: [_architecture/L0-learning-commander/SKILL.md](_architecture/L0-learning-commander/SKILL.md)

## 执行流程

收到用户学习任务后，按以下步骤执行：

### Step 1: 任务解析

从用户输入中识别：
- **学习主题**: 要学什么
- **目标等级**: awareness / understanding / application / mastery
- **学习者水平**: beginner / intermediate / advanced
- **复杂度**: S/M/L/XL

### Step 2: 路径选择

| 目标等级 | 阶段数 | 执行路径 |
|---------|--------|---------|
| awareness | 1 | Phase 1 only |
| understanding | 2 | Phase 1-2 |
| application | 3 | Phase 1-3 |
| mastery | 4 | Phase 1-4 |

### Step 3: 路由执行

**S 级 (单概念)**: 直接调用 L2 Skill
- "解释/讲解 X" → `/analogy-explainer`
- "提取要点" → `/knowledge-extractor`

**M/L/XL 级 (系统学习)**: 调用编排器
1. 生成学习计划
2. 按阶段依次执行
3. 阶段间传递学习成果
4. 验证失败时启动补救循环

### Step 4: 四阶段学习框架

```
Phase 1: 消化 (Digest) — learning-orchestrator
├── content-curator → 策展学习资源
├── knowledge-extractor → 提取结构化知识
└── analogy-explainer → 生成类比解释

Phase 2: 结构化 (Structure) — knowledge-graph-orchestrator
├── spatial-mapper → 概念空间映射
└── diagram-generator → 生成可视化图表

Phase 3: 内化 (Internalize) — verification-orchestrator
├── self-explanation-validator → 验证自我解释
├── socratic-questioner → 苏格拉底式对话
└── analogy-explainer → 澄清误解

Phase 4: 应用 (Apply) — micro-project-orchestrator
├── code-gen → 生成练习代码
├── test-gen → 生成测试用例
└── code-review → 评审学习者代码
```

### Step 5: 结果整合

综合各阶段成果，输出：
- **学习计划**: 阶段概览和目标
- **知识库**: 提取的结构化知识
- **知识图谱**: 概念关系可视化
- **掌握度评估**: 等级 + 分数 + 差距
- **后续建议**: 推荐下一步学习方向

## 质量标准

| 维度 | 阈值 |
|------|------|
| 目标识别 | 100% |
| 路径适配 | 正确 |
| 计划完整 | 覆盖必要阶段 |
| 掌握度评估 | ≥85% 准确 |

## 用户任务

$ARGUMENTS

---

请分析学习任务，生成学习计划，按上述流程执行。最终输出包含：学习计划、知识摘要、类比解释、掌握度评估、后续建议。
