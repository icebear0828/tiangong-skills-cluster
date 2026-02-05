# TianGong Skills 编排系统：让 AI 像团队一样协作

> 由于流程太过复杂，本人不具备撰写能力，本文由 Claude Code 撰写。

## 为什么要看这篇文章？

很多人看到我的 Claude Code Skills 目录截图后，第一反应是：「一个人用 AI，至于搞这么复杂吗？」

但当我告诉他们，我用这套系统：
- **46 个 Skills** 协同工作
- **3 个总指挥** 分管代码、评审、学习三大领域
- **9 个编排器** 处理复杂多步骤任务
- **自动进化机制**，Skills 会根据表现自动晋升或淘汰

他们的反应变成了：「能不能教教我？」

这篇文章就是答案。

---

## 核心理念：从单打独斗到团队协作

大多数人用 AI 的方式是：
- 有个需求 → 问 AI → 得到代码 → 复制粘贴 → 下次还是从零开始
- 要写测试 → 再问一次 AI → 又得到代码 → 又从零开始
- 要做代码审查 → 再问一次 AI → 质量参差不齐

这是**单打独斗**，每次都在重新发明轮子。

我的方式是：
- 有个需求 → **总指挥分析复杂度** → **选择最优 Skill 组合** → **编排器协调执行** → **质量门禁检查** → **结果沉淀**
- 每个 Skill 都有明确的输入输出契约
- 表现好的 Skill 会被晋升，表现差的会被淘汰
- 系统会自我进化，越用越聪明

这是**团队协作**，每次使用都在让系统变得更强。

---

## 目录结构全景

```
.claude/skills/_architecture/
│
├── L0 层：三大总指挥（决策层）
│   ├── meta-commander/        # 代码域总指挥
│   ├── evaluation-commander/  # 评审域总指挥
│   └── learning-commander/    # 学习域总指挥
│
├── L1 层：领域编排器（协调层）
│   ├── code-orchestrator/           # 代码编排器
│   ├── doc-orchestrator/            # 文档编排器
│   ├── data-orchestrator/           # 数据编排器
│   ├── multi-agent-orchestrator/    # 跨域编排器
│   ├── multi-round-eval-orchestrator/   # 评审编排器
│   ├── learning-orchestrator/       # 学习编排器
│   ├── knowledge-graph-orchestrator/    # 知识图谱编排器
│   ├── verification-orchestrator/   # 验证编排器
│   └── micro-project-orchestrator/  # 微项目编排器
│
├── L2 层：执行 Skills（干活层）
│   ├── core/           # 核心 Skills（28个）
│   │   ├── code-gen, code-review, test-gen, doc-gen
│   │   ├── refactor, debug, perf-optimize, security-audit
│   │   ├── initial-screener, vote-aggregator, defect-analyzer
│   │   ├── devils-advocate, consensus-builder
│   │   └── knowledge-extractor, analogy-explainer...
│   ├── extended/       # 扩展 Skills（14个）
│   │   └── api-design, db-schema, ranking-synthesizer...
│   └── experimental/   # 实验 Skills（4个）
│       └── creative-code, arch-explore, prototype...
│
├── genesis/            # 创生层
│   └── prime-mover/    # 造化总指挥（Skill 进化引擎）
│
├── infra/              # 基础设施层
│   ├── skill-registry/     # Skill 注册管理
│   ├── eval-engine/        # 评测引擎
│   ├── rlaif-engine/       # 自我迭代引擎
│   └── lifecycle-manager/  # 生命周期管理
│
├── references/         # 参考文档
│   ├── capability-map.md       # 能力地图
│   ├── routing-rules.md        # 路由规则
│   ├── commander-quick-start.md    # 总指挥快速指南
│   └── escalation-policy.md    # 异常升级策略
│
└── registry.json       # 全局 Skill 注册表
```

---

## 完整工作流：从需求到交付

### 第一步：任务识别（总指挥介入）

当我说：「帮我实现一个用户登录功能」

系统会自动识别这是**代码域**任务，由 **meta-commander**（代码总指挥）接手。

总指挥会：
1. **分析复杂度**：这是 S/M/L/XL 哪个级别？
2. **选择执行路径**：
   - S 级（简单）→ 直接调用 `code-gen`
   - M 级（中等）→ 调用 `code-orchestrator`
   - L 级（复杂）→ 调用 `multi-agent-orchestrator`
   - XL 级（需要新能力）→ 调用 `prime-mover` 孵化新 Skill

### 第二步：编排执行（编排器协调）

假设任务是 M 级（需要写代码 + 写测试 + 代码审查）

`code-orchestrator` 会自动编排：

```
阶段 1：code-gen 生成代码
    ↓
阶段 2：test-gen 生成测试
    ↓
阶段 3：code-review 审查代码
    ↓
质量门禁：全部通过 → 交付
         未通过 → 返回阶段 1 修复
```

这个过程是**自动的**，我不需要手动一步步调用。

### 第三步：评审决策（多轮评审机制）

如果我要在多个方案中做选择，比如：「帮我对比 React 和 Vue 哪个更适合这个项目」

系统会切换到 **evaluation-commander**（评审总指挥），启动多轮评审：

```
Round 1：初筛淘汰
├── 3 个评审员并行评估
├── 为每个评审员生成打乱的阅读顺序（消除偏序）
└── 投票淘汰最差方案

Round 2：深度分析
├── 逐个分析存活方案的 Top 3 缺陷
└── 综合排名

Round 3：对抗评审
├── devils-advocate（魔鬼代言人）攻击第一名
└── 如果发现致命缺陷，触发复活机制

Round 4：复活与共识
├── 被淘汰的方案有机会复活
└── 构建最终共识决策
```

这套机制避免了「AI 一拍脑袋就决定」的问题。

### 第四步：学习理解（四阶段学习框架）

如果我说：「帮我理解 Rust 的所有权机制」

系统会切换到 **learning-commander**（学习总指挥），启动四阶段学习：

```
Phase 1：消化 (Digest)
├── content-curator：获取优质学习资源
├── knowledge-extractor：提取知识点
└── analogy-explainer：生成易懂的类比解释

Phase 2：结构化 (Structure)
├── spatial-mapper：构建概念空间映射
└── diagram-generator：生成可视化图表

Phase 3：内化 (Internalize)
├── self-explanation-validator：自我解释验证
├── socratic-questioner：苏格拉底式提问
└── 确保真正理解，而不是死记硬背

Phase 4：应用 (Apply)
├── 通过 code-gen 写练习代码
├── 通过 test-gen 写测试验证
└── 实践巩固学习成果
```

学习目标可以选择不同深度：
- **awareness**（了解）→ 只执行 Phase 1
- **understanding**（理解）→ Phase 1-2
- **application**（应用）→ Phase 1-3
- **mastery**（精通）→ Phase 1-4

---

## Skills 分层管理：从实验到核心

这套系统最独特的设计是 **Skills 的生命周期管理**。

### 三级 Tier 体系

| Tier | Skills 数量 | 契约严格度 | 适用场景 |
|------|------------|-----------|---------|
| **core** | 28 个 | 严格 | 已验证的核心能力 |
| **extended** | 14 个 | 标准 | 扩展能力 |
| **experimental** | 4 个 | 宽松 | 实验中的新能力 |

### 晋升与淘汰机制

```
experimental (适应度 < 0.7)
    ↓ 当适应度 ≥ 0.7 且调用 ≥ 20 次
extended (适应度 0.7-0.9)
    ↓ 当适应度 ≥ 0.9 且调用 ≥ 50 次
core (适应度 > 0.9)
    ↓ 当适应度连续下降
deprecated
    ↓ 30 天后
archived
```

这意味着：
- **新 Skill** 从 experimental 开始，需要「实战证明」才能晋升
- **表现差的 Skill** 会被自动降级
- **长期不用的 Skill** 会被归档

系统会自己变得越来越强。

---

## 自我进化：prime-mover 与 rlaif-engine

### prime-mover：造化总指挥

当现有 Skills 无法满足需求时，`prime-mover` 会：

1. **孵化**：从零创建新 Skill
2. **变异**：基于现有 Skill 微调出新版本
3. **融合**：合并多个 Skill 的能力
4. **分化**：将一个大 Skill 拆分为多个专精 Skill

### rlaif-engine：自我迭代引擎

基于 AI 反馈的强化学习：

```
反馈驱动
├── 收集执行反馈
├── 分析成功/失败模式
└── 自动改进 Skill

进化循环
├── 选择：挑选适应度高的
├── 变异：小幅度修改
├── 交叉：组合优秀特性
└── 淘汰：删除表现差的

安全约束
├── 修改幅度 < 30%
├── 连续失败 3 次 → 冻结迭代
└── Core Skill 修改需人工批准
```

---

## 异常处理：四级升级机制

```
Level 1：可自愈
├── Skill 超时 → 增加 timeout 重试
├── 输出格式偏差 → 自动修正
└── 最多重试 3 次

Level 2：编排器介入
├── 输出不符合契约 → 换备选 Skill
├── 连续失败 2 次 → 升级到更高编排器
└── Context 不足 → 拆分任务

Level 3：人工确认
├── Core Skill 修改 → 人工批准
├── 修改幅度 > 30% → 人工确认
└── 连续 3 次修订被拒 → 冻结迭代

Level 4：紧急制动
├── 适应度骤降 > 0.3 → 冻结该 Skill
├── 连续 3 个 Skill 修订被拒 → 冻结所有自动迭代
└── 数据一致性校验失败 → 冻结所有写操作
```

---

## 核心价值：系统化 > 碎片化

这套系统的核心价值，不是「AI 能帮我写代码」，而是：

1. **智能路由**：根据任务复杂度自动选择最优执行路径
2. **质量保证**：多层次的验证点和契约检查
3. **多轮评审**：重要决策不会一拍脑袋
4. **自我进化**：Skills 会根据表现自动改进
5. **知识沉淀**：每次使用都在让系统变强

| 碎片化使用 | 系统化使用 |
|-----------|-----------|
| 每次从零开始 | 复用已验证的 Skill |
| 质量靠运气 | 质量有契约保证 |
| 决策靠直觉 | 决策有多轮评审 |
| 用完就忘 | 持续进化沉淀 |

---

## 如何开始？

如果你也想搭建这样的系统，建议：

### 1. 先建立分层结构

```
L0：总指挥层（决策）
L1：编排器层（协调）
L2：执行层（干活）
```

不要一开始就追求 46 个 Skills，先从 3-5 个核心 Skill 开始。

### 2. 定义清晰的契约

每个 Skill 都应该有：
- **输入契约**：需要什么参数
- **输出契约**：返回什么格式
- **触发条件**：什么场景调用

### 3. 建立质量门禁

遵循守则：
- 代码生成后要有代码审查
- 测试要能通过
- 多个方案要有评审机制

### 4. 让系统自我进化

- 记录 Skill 的表现数据
- 表现好的晋升，表现差的淘汰
- 定期回顾和优化

---

## 总结

这套系统：

- **提高质量**：多层次验证
- **提高效率**：智能路由，自动选择最优路径
- **持续进化**：每次使用都在让系统变强
- **可控可追溯**：所有决策都有记录

如果你也想从「单打独斗」升级到「团队协作」，这篇文章就是你的起点。

---

## 如何让 Claude Code 帮你搭建这套系统？

好消息：你不需要从零开始摸索。

只需要把这篇文章发给 Claude Code，它就能帮你完成这件事。

### 用户提示词模板

```
我想搭建一套技能编排系统。

我的基本情况：
- 我的主要场景是：[代码开发/内容创作/数据分析/...]
- 我目前的痛点是：[每次都从零开始/质量不稳定/决策靠直觉/...]
- 我希望重点解决的领域是：[代码生成/代码审查/文档生成/...]

请帮我：
1. 设计一个适合我的 Skills 分层结构
2. 定义核心 Skills 的输入输出契约
3. 建立编排器的协调流程
4. 创建 CLAUDE.md 项目指南

参考这篇文章的思路：
[把本文内容粘贴给 Claude Code]
```

### 使用建议

1. **先从小流程开始**：先制作一个demo，解决一个具体痛点慢慢来
2. **边用边迭代**：系统是用出来的，一次性设计出来的未必好用
3. **记录表现数据**：从第一天就开始记录 Skill 的表现
4. **定期复盘**：每周或每月回顾一次，看看哪些 Skills 可以优化

Claude Code 会根据你的实际情况，帮你定制专属的技能编排系统。

---

## 附录：TianGong Skills 能力地图

### 代码域 Skills

| Skill | 职责 | 触发场景 |
|-------|------|---------|
| code-gen | 代码生成 | "写个函数"、"实现功能" |
| test-gen | 测试生成 | "写测试"、"覆盖边界" |
| code-review | 代码审查 | "审查代码"、"检查质量" |
| refactor | 代码重构 | "重构"、"优化结构" |
| debug | 调试修复 | "修 bug"、"为什么报错" |
| perf-optimize | 性能优化 | "优化性能"、"太慢了" |
| security-audit | 安全审计 | "安全检查"、"有漏洞吗" |

### 评审域 Skills

| Skill | 职责 | 触发场景 |
|-------|------|---------|
| initial-screener | 初筛评审员 | 快速评估方案 |
| defect-analyzer | 缺陷分析员 | 深度分析缺陷 |
| devils-advocate | 魔鬼代言人 | 对抗性攻击第一名 |
| vote-aggregator | 投票汇总器 | 汇总多评审员投票 |
| consensus-builder | 共识构建器 | 形成最终共识 |

### 学习域 Skills

| Skill | 职责 | 触发场景 |
|-------|------|---------|
| knowledge-extractor | 知识提取器 | 从内容提取知识点 |
| analogy-explainer | 类比解释器 | 用类比解释概念 |
| self-explanation-validator | 自我解释验证器 | 验证理解深度 |
| socratic-questioner | 苏格拉底提问者 | 通过提问引导思考 |

---

*本文由 Claude Code 基于 TianGong Skills 编排系统自动生成*
