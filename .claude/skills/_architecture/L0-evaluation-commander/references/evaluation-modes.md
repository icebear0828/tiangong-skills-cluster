# 评审模式详解

## 模式概览

| 模式 | 轮次 | 评审员 | 耗时 | 适用场景 |
|------|------|--------|------|---------|
| quick | 1 | 1 | 短 | 2方案快速对比 |
| standard | 2 | 3 | 中 | 常规方案评审 |
| thorough | 4 | 5+ | 长 | 重要决策评审 |
| adversarial | 4+ | 7+ | 很长 | 高风险对抗评审 |

---

## Quick 模式

### 特点
- 单轮快速对比
- 无淘汰机制
- 直接输出排名

### 流程
```
输入 → 快速评估 → 输出排名
```

### 适用场景
- 2个方案的简单对比
- 时间紧迫
- 低风险决策

### 输出
- 简单排名
- 关键差异点
- 快速推荐

---

## Standard 模式

### 特点
- 2轮评审
- 3个评审员
- 有初筛淘汰

### 流程
```
Round 1: 初筛淘汰
├── 3个 initial-screener 并行
└── vote-aggregator 汇总

Round 2: 深度分析
├── 3个 defect-analyzer 并行
└── ranking-synthesizer 综合排名

输出: 排名 + 推荐
```

### 适用场景
- 3-4个候选方案
- 常规技术决策
- 中等重要性

### 输出
- 综合排名
- 缺陷报告
- 推荐理由

---

## Thorough 模式

### 特点
- 完整4轮评审
- 5+评审员
- 包含对抗评审和复活

### 流程
```
Round 1: 初筛淘汰
├── 3个 initial-screener 并行
└── vote-aggregator 汇总

Round 2: 深度分析
├── 3个 defect-analyzer 并行
└── ranking-synthesizer 综合排名

Round 3: 对抗评审
├── devils-advocate 攻击第一名
└── 条件触发 final-candidate-reviewer

Round 4: 复活与共识
├── resurrection-evaluator (条件触发)
├── final-candidate-reviewer
└── consensus-builder 最终决策

输出: 最终推荐 + 置信度
```

### 适用场景
- 5+个候选方案
- 重要技术决策
- 需要高置信度

### 输出
- 详细评审报告
- 完整决策路径
- 高置信度推荐

---

## Adversarial 模式

### 特点
- 4+轮评审
- 7+评审员
- 增强对抗强度
- 多轮攻击

### 流程
```
Round 1-2: 同 thorough

Round 3: 增强对抗
├── 2个 devils-advocate 攻击第一名
├── 1个 devils-advocate 攻击第二名
└── final-candidate-reviewer 检查所有存活方案

Round 4: 复活与共识
├── resurrection-evaluator (更宽松触发)
├── 二次对抗检查
└── consensus-builder + confidence-calculator

可选 Round 5: 人工介入
└── 当置信度 < Medium 时建议

输出: 最终推荐 + 详细置信度分析
```

### 适用场景
- 高风险决策
- 候选方案差距小
- 需要极高置信度

### 输出
- 完整攻击报告
- 置信度详细分析
- 风险缓解建议

---

## 模式升降级规则

### 自动升级
- quick → standard: 发现方案差距小
- standard → thorough: Round 1 无淘汰
- thorough → adversarial: Round 3 发现 Critical

### 手动降级
- 时间不足时可手动指定降级
- 降级会影响置信度评分
