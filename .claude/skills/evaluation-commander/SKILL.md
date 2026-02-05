---
name: evaluation-commander
description: >
  评审域总指挥。方案评审的第一入口点。分析评审任务，选择评审模式，路由到 multi-round-eval-orchestrator 执行。
  支持方案对比、对抗评审、共识决策。
---

# Evaluation Commander — 评审域总指挥

> 详细文档: [_architecture/L0-evaluation-commander/SKILL.md](_architecture/L0-evaluation-commander/SKILL.md)

## 执行流程

收到用户评审任务后，按以下步骤执行：

### Step 1: 任务解析

从用户输入中识别：
- **候选方案**: 提取所有待评审方案
- **评审维度**: 识别评审标准（架构设计、可行性、兼容性等）
- **复杂度**: 根据候选数和维度数判定 S/M/L/XL

### Step 2: 模式选择

| 条件 | 模式 | 轮次 |
|------|------|------|
| 2方案 + 简单对比 | quick | 1 |
| 3-4方案 + 标准要求 | standard | 2 |
| 5+方案 或 重要决策 | thorough | 4 |
| 高风险 或 用户指定 | adversarial | 4+ |

### Step 3: 路由执行

**S 级 (quick)**: 直接对比两个方案
- 逐维度评分
- 输出排名和推荐

**M/L 级 (standard/thorough/adversarial)**: 调用编排器
1. 路由到 `/multi-round-eval-orchestrator`
2. 传递候选方案、评审维度、模式配置
3. 监控执行进度
4. 接收最终结果

### Step 4: 四轮评审框架

```
Round 1 (初筛淘汰):
├── initial-screener ×3 (并行) → 独立评分
└── vote-aggregator → 汇总投票，淘汰最差

Round 2 (深度分析):
├── defect-analyzer ×3 (并行) → 缺陷挖掘
└── ranking-synthesizer → 综合排名

Round 3 (对抗评审):
├── devils-advocate → 攻击第一名
└── final-candidate-reviewer (条件触发)

Round 4 (复活与共识):
├── resurrection-evaluator (条件触发)
├── final-candidate-reviewer → 最终检查
└── consensus-builder → 构建共识决策
```

### Step 5: 结果整合

综合编排器结果，输出：
- **排名**: 所有方案的最终排名
- **推荐**: 最佳方案 + 推荐理由
- **置信度**: Very High / High / Medium / Low
- **决策路径**: 关键转折点追溯
- **注意事项**: 风险提示和缓解建议

## 质量标准

| 维度 | 阈值 |
|------|------|
| 候选识别 | 100% |
| 模式适配 | 正确匹配复杂度 |
| 决策透明 | 路径可追溯 |
| 置信度 | 与过程一致 |

## 用户任务

$ARGUMENTS

---

请分析评审任务，选择评审模式，按上述流程执行。最终输出包含：排名、推荐方案、置信度、决策路径、注意事项。
