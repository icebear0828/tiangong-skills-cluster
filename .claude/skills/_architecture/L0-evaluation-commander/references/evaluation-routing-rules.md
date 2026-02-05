# 评审域路由规则

## 概述

本文档定义了 evaluation-commander 将评审任务路由到正确 Skill 的决策规则。

## 一级分流：任务类型判断

```
评审任务输入
    │
    ├── 单方案评估 → 直接返回评估报告
    │
    ├── 2方案快速对比 → quick 模式
    │   └── 直接对比，不启动编排器
    │
    ├── 3-4方案标准评审 → standard 模式
    │   └── multi-round-eval-orchestrator (Round 1-2)
    │
    ├── 5+方案深度评审 → thorough 模式
    │   └── multi-round-eval-orchestrator (Round 1-4)
    │
    └── 高风险对抗评审 → adversarial 模式
        └── multi-round-eval-orchestrator (Round 1-4 + 增强)
```

## 关键词触发规则

| 关键词 | 路由目标 | 模式 |
|--------|---------|------|
| 评审、对比、选择最佳 | evaluation-commander | 自动选择 |
| 快速对比、简单评审 | evaluation-commander | quick |
| 深度评审、全面评估 | evaluation-commander | thorough |
| 对抗评审、压力测试 | evaluation-commander | adversarial |
| 初筛、筛选 | initial-screener | - |
| 缺陷分析、风险评估 | defect-analyzer | - |
| 攻击、挑战方案 | devils-advocate | - |

## 模式选择矩阵

| 候选数 | 维度数 | 时间约束 | 推荐模式 |
|--------|--------|---------|---------|
| 2 | ≤3 | 紧急 | quick |
| 2 | ≤3 | 充裕 | standard |
| 3-4 | 3-5 | 任意 | standard |
| 5-7 | 5-7 | 任意 | thorough |
| 8+ | 7+ | 任意 | adversarial |
| 任意 | 任意 | 高风险决策 | adversarial |

## 编排器调度规则

### 何时启动编排器

- 候选方案 ≥3 个
- 需要多轮评审
- 需要多评审员并行
- 需要淘汰/复活机制

### 何时跳过编排器

- 2 个方案简单对比
- 单维度快速判断
- 时间极度紧张

## 质量关卡

| 关卡 | 检查内容 | 未通过处理 |
|------|---------|-----------|
| 输入验证 | 候选方案 ≥2 | 要求补充 |
| 维度验证 | 评审维度 ≥1 | 使用默认维度 |
| 模式验证 | 模式与复杂度匹配 | 自动调整 |
| 结果验证 | 有明确推荐 | 请求人工介入 |

## 异常处理

| 异常 | 处理策略 |
|------|---------|
| 候选方案不足 | 返回错误，要求补充 |
| 维度缺失 | 使用默认维度集 |
| 编排器超时 | 降级到 quick 模式 |
| 共识失败 | 输出分歧报告 |
