# 评审域能力映射

## 评审域 Skill 能力矩阵

### L0 总指挥

| Skill | 核心能力 | 输入 | 输出 |
|-------|---------|------|------|
| evaluation-commander | 评审任务路由、模式选择、最终决策 | 任务描述 + 候选方案 | 评审结果 + 推荐 |

### L1 编排器

| Skill | 核心能力 | 编排范围 |
|-------|---------|---------|
| multi-round-eval-orchestrator | 4轮评审流程编排 | 淘汰→分析→对抗→共识 |

### L2 核心评审 Skill

| Skill | 能力 | 调用时机 |
|-------|------|---------|
| initial-screener | 快速筛选、淘汰最差方案 | Round 1 |
| vote-aggregator | 汇总投票、阈值判定 | Round 1, 4 |
| defect-analyzer | 深度缺陷分析、评分 | Round 2 |
| devils-advocate | 对抗攻击、挖掘缺陷 | Round 3 |
| consensus-builder | 构建共识、最终决策 | Round 4 |

### L2 扩展评审 Skill

| Skill | 能力 | 调用时机 |
|-------|------|---------|
| ranking-synthesizer | 综合排名、冲突检测 | Round 2 |
| resurrection-evaluator | 评估复活资格 | Round 4 |
| final-candidate-reviewer | 最终候选检查 | Round 3, 4 |
| confidence-calculator | 置信度计算 | Round 4 |

---

## 能力调用链

### Quick 模式
```
evaluation-commander
    └── 直接评估（无编排器）
```

### Standard 模式
```
evaluation-commander
    └── multi-round-eval-orchestrator
            ├── initial-screener ×3
            ├── vote-aggregator
            ├── defect-analyzer ×3
            └── ranking-synthesizer
```

### Thorough 模式
```
evaluation-commander
    └── multi-round-eval-orchestrator
            ├── initial-screener ×3
            ├── vote-aggregator
            ├── defect-analyzer ×3
            ├── ranking-synthesizer
            ├── devils-advocate
            ├── final-candidate-reviewer
            ├── resurrection-evaluator (条件)
            └── consensus-builder
```

### Adversarial 模式
```
evaluation-commander
    └── multi-round-eval-orchestrator
            ├── initial-screener ×5
            ├── vote-aggregator
            ├── defect-analyzer ×5
            ├── ranking-synthesizer
            ├── devils-advocate ×3
            ├── final-candidate-reviewer ×2
            ├── resurrection-evaluator
            ├── consensus-builder
            └── confidence-calculator
```

---

## 能力边界定义

### evaluation-commander 能处理

- 多方案对比评审
- 评审模式选择
- 评审流程调度
- 最终决策生成

### evaluation-commander 不处理

- 方案生成（由 code-gen 等处理）
- 代码级审查（由 code-review 处理）
- 方案实施（评审后流程）
- 非对比类评估

---

## 与其他域的协作

| 协作域 | 协作 Skill | 协作场景 |
|--------|-----------|---------|
| 代码域 | code-review | 评审涉及代码质量时 |
| 学习域 | - | 无直接协作 |
| 基础设施 | eval-engine | 复用评分框架 |
