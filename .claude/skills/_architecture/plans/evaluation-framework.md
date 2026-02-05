# 学习加速 Skills 方案评判框架

## 待评方案清单

| 代号 | 文件名 | 规模 | 核心特点 |
|------|--------|------|---------|
| **Plan-A** | optimized-painting-pancake.md | 23个 | 视频渲染集成，混合执行模式 |
| **Plan-B** | piped-moseying-dragon.md | 35个 | 最细粒度Primitive，完整数据契约 |
| **Plan-C** | sharded-gliding-hanrahan.md | 20个 | 简化实用，易于实施 |
| **Plan-D** | 2026-02-03-learning-acceleration-skills-plan.md | 12+配套 | 严格遵循TianGong三层架构 |

## 评判 Subagent 设计

### Subagent 1: 架构合规性评审员
**角度**: 与现有 TianGong/ZaoHua 架构的兼容性
**评分维度**:
- 三层架构遵循度 (L0/L1/L2)
- 契约等级应用合理性 (strict/standard/flexible)
- 与现有 Skills 集成复杂度
- registry.json 扩展难度

**打乱顺序**: B → D → A → C

---

### Subagent 2: 原子化纯度评审员
**角度**: Skills 的原子化程度和职责单一性
**评分维度**:
- 单一职责原则遵循度
- 输入/输出边界清晰度
- 可复用性（被多个上层调用的能力）
- 避免功能重叠

**打乱顺序**: C → A → D → B

---

### Subagent 3: 学习方法论覆盖评审员
**角度**: 对用户原始需求（四阶段学习）的覆盖完整度
**评分维度**:
- 导师Agent能力覆盖
- 苏格拉底Agent能力覆盖
- 策展Agent能力覆盖
- 空间记忆/极速概览覆盖
- 反向图灵测试覆盖
- 微项目驱动覆盖

**打乱顺序**: A → C → B → D

---

### Subagent 4: 实施可行性评审员
**角度**: 实际落地的工程可行性
**评分维度**:
- 文件数量/工作量
- 依赖链复杂度
- 外部API依赖风险
- 分阶段交付可行性
- 测试验证难度

**打乱顺序**: D → B → C → A

---

### Subagent 5: 可演进性评审员
**角度**: 长期维护和迭代能力
**评分维度**:
- 新增Skill扩展难度
- RLAIF自我迭代友好度
- 向后兼容性
- 文档自解释程度

**打乱顺序**: C → D → A → B

---

## 评分规则

### 分数范围
每个维度: 1-10 分
- 10: 卓越，行业最佳实践
- 8-9: 优秀，超出预期
- 6-7: 良好，满足要求
- 4-5: 及格，有明显不足
- 1-3: 不合格，需重做

### 权重分配
| 评审角度 | 权重 |
|---------|------|
| 架构合规性 | 25% |
| 原子化纯度 | 20% |
| 需求覆盖度 | 25% |
| 实施可行性 | 20% |
| 可演进性 | 10% |

### 最终得分公式
```
Final Score = Σ (角度得分 × 权重)
```

---

## 执行流程

```
1. 并行启动 5 个评审 Subagent
   ↓
2. 每个 Subagent 按打乱顺序阅读文档
   ↓
3. 每个 Subagent 独立打分（不知道其他Agent的评分）
   ↓
4. 汇总所有评分到矩阵
   ↓
5. 计算加权最终得分
   ↓
6. 生成对比报告
```

---

## 输出格式

每个 Subagent 返回:
```json
{
  "evaluator": "架构合规性评审员",
  "evaluation_order": ["Plan-B", "Plan-D", "Plan-A", "Plan-C"],
  "scores": {
    "Plan-A": { "dim1": 8, "dim2": 7, "dim3": 6, "dim4": 8, "total": 7.25 },
    "Plan-B": { "dim1": 9, "dim2": 8, "dim3": 7, "dim4": 6, "total": 7.5 },
    "Plan-C": { "dim1": 6, "dim2": 7, "dim3": 8, "dim4": 9, "total": 7.5 },
    "Plan-D": { "dim1": 10, "dim2": 9, "dim3": 8, "dim4": 7, "total": 8.5 }
  },
  "comments": {
    "Plan-A": "...",
    "Plan-B": "...",
    "Plan-C": "...",
    "Plan-D": "..."
  },
  "recommendation": "Plan-D"
}
```
