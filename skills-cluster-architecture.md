# Claude Code 顶级 Skills 集群架构设计

## 迭代决策过程记录

---

## 第一轮：三大候选架构方向

### 方向 A：中心化指挥官模式（Centralized Conductor）
一个全能的 `orchestrator` skill 作为单一入口点，所有子 skill 通过它注册、调度、评测。采用严格的层级树状结构。

**优势**：控制流清晰，便于审计和回溯
**劣势**：单点瓶颈，context window 消耗巨大，orchestrator 本身复杂度爆炸

### 方向 B：联邦自治模式（Federated Autonomous）
每个 skill 是自治单元，拥有自己的评测、注册、废弃逻辑。通过一个轻量级 `skill-registry` 服务协调，无中心指挥。

**优势**：去中心化、可扩展、每个 skill 独立迭代
**劣势**：缺乏全局协调能力，复杂任务的跨 skill 编排困难，一致性难保证

### 方向 C：分层编排 + 事件驱动模式（Layered Orchestration + Event-Driven）
三层架构：Meta 层（策略决策）→ Orchestration 层（任务编排）→ Execution 层（原子 skill）。层间通过结构化事件通信，每层可独立评测和迭代。

**优势**：关注点分离、可组合性强、评测可在每层独立进行
**劣势**：架构复杂度高、需要精心设计层间协议

### 第一轮裁剪

**淘汰 A（置信度 0.35）**：中心化指挥官在 Claude Code 的 context window 约束下不可行。单一 orchestrator 的 SKILL.md 会膨胀到数千行，违反 progressive disclosure 原则。所有决策集中导致单点故障。

**淘汰 B（置信度 0.45）**：纯联邦模式缺乏"总指挥"能力，无法满足"操控一切的总指挥"需求。跨 skill 编排是核心需求，纯自治模式在这里断裂。

**保留 C（置信度 0.82）**：分层模式天然适配需求——Meta 层做总指挥，Orchestration 层做子代理编排，Execution 层做原子操作。继续深化。

---

## 第二轮：基于方向 C 的三个变体

### 变体 C1：静态分层 + JSON Schema 协议
层间通过固定的 JSON Schema 通信。每个 skill 在 SKILL.md 中声明自己的输入/输出 schema。编排层通过 schema 匹配选择 skill。

**优势**：类型安全，可验证，确定性强
**劣势**：灵活性差，新 skill 类型需要修改 schema，不适合探索性任务

### 变体 C2：动态分层 + Prompt Chain 协议
层间通过结构化 prompt 模板通信。Meta 层生成"任务描述 prompt"，Orchestration 层将其分解为子 prompt 序列，Execution 层执行单个 prompt。

**优势**：极度灵活，天然适配 LLM 的工作方式，新 skill 零成本接入
**劣势**：不确定性高，调试困难，评测需要更复杂的机制

### 变体 C3：混合分层 + 契约协议（Contract-Based）
核心 skill 使用严格 schema 契约（低自由度），扩展 skill 使用 prompt 模板（高自由度）。每个 skill 声明自己的"契约等级"。评测标准也根据契约等级分层。

**优势**：在确定性和灵活性之间取得平衡，渐进式可靠性
**劣势**：契约等级分类本身需要经验，存在"中间地带"的模糊性

### 第二轮裁剪

**淘汰 C1（置信度 0.40）**：静态 schema 在 skills 自我迭代的场景下是反模式。RLAIF 迭代意味着 skill 的行为会演化，固定 schema 会成为进化的天花板。

**淘汰 C2（置信度 0.55）**：纯 prompt chain 在评测环节无法提供足够的结构化信号。"完美评测"需要可量化的指标，纯 prompt 模板让评测变成了"评测一个 LLM 输出"——递归问题。

**保留 C3（置信度 0.88）**：混合契约模式精确匹配了需求矩阵的每一项。继续深化。

---

## 第三轮：基于 C3 的三个实现方案

### 方案 C3-α：Monorepo 单仓库实现
所有 skill 在一个巨型目录树中，通过路径约定区分层级。Registry 是一个 JSON 文件。

**优势**：简单直接，版本一致性好
**劣势**：skill 数量增长后目录臃肿，不利于独立 skill 的生命周期管理

### 方案 C3-β：模块化仓库 + 动态发现
每个 skill 是独立目录/包，Meta 层在运行时扫描所有可用 skill 的 frontmatter 来构建 registry。支持热插拔。

**优势**：skill 独立性强，生命周期管理清晰，运行时动态发现
**劣势**：首次扫描开销大，需要缓存策略

### 方案 C3-γ：元编程自举（Meta-Bootstrapping）
Meta 层本身也是一个 skill，它能创建、修改、废弃其他 skill。形成"skill 管理 skill"的自举闭环。

**优势**：真正的自我迭代能力，最高级别的自我改进
**劣势**：自举的安全边界需要极其严格的约束，避免"失控迭代"

### 第三轮裁剪

**淘汰 C3-α（置信度 0.38）**：Monorepo 在 skill 数量超过 20 个时会造成 Claude 在选择 skill 时的 context 爆炸。且无法支持"临时 skill"和"废弃 skill"的生命周期。

**保留 C3-β（置信度 0.85）**和 **C3-γ（置信度 0.90）**：这两个方向代表了两种哲学——β 是工程化优雅，γ 是自我进化优雅。两者可以融合。

---

## 最终方案：两套顶级架构

---

# 方案一：「天工」—— 工程化精密编排系统

> 设计哲学：如同精密钟表，每个齿轮精确咬合，可预测、可审计、可测量。

## 总体架构

```
天工 Skills Cluster
│
├── L0: Meta-Commander/          ← 总指挥（策略决策层）
│   ├── SKILL.md                  ← 任务分析、方案选择、全局调度
│   ├── references/
│   │   ├── routing-rules.md      ← 任务路由决策树
│   │   ├── capability-map.md     ← 全局能力地图
│   │   └── escalation-policy.md  ← 异常升级策略
│   └── scripts/
│       ├── task_analyzer.py      ← 任务复杂度评估
│       └── plan_generator.py     ← 执行计划生成
│
├── L1: Orchestrators/            ← 编排层（子代理编排）
│   ├── code-orchestrator/        ← 代码任务编排
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── patterns.md       ← 代码任务分解模式
│   │       └── quality-gates.md  ← 质量关卡定义
│   ├── doc-orchestrator/         ← 文档任务编排
│   ├── data-orchestrator/        ← 数据任务编排
│   ├── multi-agent-orchestrator/ ← 跨域复合任务编排
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── composition.md    ← 子代理组合模式
│   │       ├── dag-patterns.md   ← DAG 执行模式
│   │       └── conflict-resolution.md ← 冲突解决策略
│   └── eval-orchestrator/        ← 评测编排
│       ├── SKILL.md
│       └── references/
│           ├── metrics.md        ← 评测指标体系
│           └── benchmarks.md     ← 基准测试定义
│
├── L2: Execution Skills/         ← 执行层（原子 skill）
│   ├── core/                     ← 核心 skill（低自由度，严格契约）
│   │   ├── code-gen/
│   │   ├── code-review/
│   │   ├── test-gen/
│   │   ├── doc-gen/
│   │   ├── refactor/
│   │   └── debug/
│   ├── extended/                 ← 扩展 skill（中自由度）
│   │   ├── api-design/
│   │   ├── db-schema/
│   │   ├── perf-optimize/
│   │   └── security-audit/
│   └── experimental/             ← 实验 skill（高自由度）
│       ├── creative-code/
│       ├── arch-explore/
│       └── prototype/
│
├── L-infra: Infrastructure/      ← 基础设施层
│   ├── skill-registry/           ← skill 注册中心
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── register.py       ← 注册新 skill
│   │   │   ├── deprecate.py      ← 废弃 skill
│   │   │   ├── activate_temp.py  ← 激活临时 skill
│   │   │   ├── modify.py         ← 修改 skill 元数据
│   │   │   └── discover.py       ← 动态发现 skill
│   │   └── references/
│   │       └── registry-schema.md
│   │
│   ├── eval-engine/              ← 评测引擎
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── run_eval.py       ← 执行评测
│   │   │   ├── compare.py        ← A/B 对比
│   │   │   ├── score.py          ← 评分计算
│   │   │   └── report.py         ← 评测报告生成
│   │   └── references/
│   │       ├── rubrics.md        ← 评分 rubric 库
│   │       ├── test-cases.md     ← 测试用例模板
│   │       └── metrics-catalog.md ← 指标目录
│   │
│   ├── rlaif-engine/             ← RLAIF 自我迭代引擎
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── generate_feedback.py  ← 自动生成反馈
│   │   │   ├── propose_revision.py   ← 提议修订
│   │   │   ├── validate_revision.py  ← 验证修订
│   │   │   ├── apply_revision.py     ← 应用修订
│   │   │   └── rollback.py           ← 回滚修订
│   │   └── references/
│   │       ├── feedback-templates.md ← 反馈模板
│   │       ├── revision-policy.md    ← 修订策略
│   │       └── safety-bounds.md      ← 安全边界
│   │
│   └── lifecycle-manager/        ← 生命周期管理
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── promote.py        ← 晋升 skill（实验→扩展→核心）
│       │   ├── demote.py         ← 降级 skill
│       │   ├── archive.py        ← 归档废弃 skill
│       │   └── health_check.py   ← 健康检查
│       └── references/
│           └── lifecycle-policy.md
│
└── .tiangong/                    ← 全局状态
    ├── registry.json             ← skill 注册表
    ├── eval-history.jsonl        ← 评测历史
    ├── rlaif-log.jsonl           ← RLAIF 迭代日志
    └── contracts/                ← 契约定义
        ├── core-contract.json    ← 核心 skill 契约 schema
        ├── extended-contract.json
        └── experimental-contract.json
```

## 核心机制详解

### 1. 总指挥：Meta-Commander

Meta-Commander 是整个系统的大脑。当用户提交任何任务时，它首先介入：

```
用户任务 → Meta-Commander
    ├── 分析任务复杂度 (scripts/task_analyzer.py)
    ├── 查阅能力地图 (references/capability-map.md)
    ├── 确定编排策略:
    │   ├── 简单任务 → 直接路由到 L2 执行层
    │   ├── 中等任务 → 路由到 L1 单领域编排器
    │   └── 复杂任务 → 路由到 L1 multi-agent-orchestrator
    └── 生成执行计划 (scripts/plan_generator.py)
```

**Meta-Commander SKILL.md 核心内容**：

```markdown
# Meta-Commander — 天工总指挥

## 职责
作为全局入口，分析所有入站任务，制定执行策略，分配子代理。

## 决策流程
1. 接收任务描述
2. 运行 task_analyzer.py 评估复杂度等级 (S/M/L/XL)
3. 查阅 routing-rules.md 确定路由策略
4. 对于 L/XL 任务：
   a. 查阅 capability-map.md 确定所需 skill 集合
   b. 检查 .tiangong/registry.json 确认 skill 可用性
   c. 生成执行 DAG（有向无环图）
   d. 路由到对应编排器
5. 监控执行结果，根据 escalation-policy.md 处理异常
```

### 2. 子代理编排：multi-agent-orchestrator

这是处理复杂任务的核心编排器：

```markdown
# Multi-Agent Orchestrator

## 编排模式

### Sequential Chain（顺序链）
当任务有严格的依赖顺序时使用：
  Task A → Task B → Task C
  示例：需求分析 → 架构设计 → 代码生成 → 测试

### Parallel Fan-out（并行扇出）
当多个子任务可以独立执行时：
  Task A ─┬→ Task B1 ─┬→ Task C
          ├→ Task B2 ─┤
          └→ Task B3 ─┘
  示例：同时生成前端代码、后端 API、数据库 schema

### Iterative Refinement（迭代精炼）
当需要反复改进时：
  Task A → Eval → (pass? → Done) : (fail? → Refine → Task A)
  示例：代码生成 → 代码审查 → 修复 → 再审查

### DAG Composition（DAG 组合）
上述模式的自由组合，使用 dag-patterns.md 中的模板。
```

### 3. 评测体系：eval-engine

```markdown
# Eval Engine — 评测引擎

## 评测维度

### 功能正确性（权重 40%）
- 单元测试通过率
- 边界条件覆盖
- 异常处理完备性

### 代码质量（权重 25%）
- 可读性评分（命名、结构、注释）
- 复杂度指标（圈复杂度、认知复杂度）
- 一致性（风格统一性）

### 架构适配（权重 20%）
- 与现有代码库的一致性
- 设计模式适当性
- 耦合度/内聚度

### 效率（权重 15%）
- token 使用效率
- 执行步骤数
- 迭代次数

## 评测流程
1. 运行 scripts/run_eval.py 收集原始指标
2. 运行 scripts/score.py 按 rubrics.md 评分
3. 对于需要 A/B 对比的场景：scripts/compare.py
4. 生成评测报告：scripts/report.py → .tiangong/eval-history.jsonl
```

### 4. Skill 生命周期管理

```
                    ┌─────────────┐
                    │  Proposed    │  ← 新 skill 提议
                    └─────┬───────┘
                          │ register.py
                    ┌─────▼───────┐
                    │ Experimental │  ← 高自由度，宽松契约
                    └─────┬───────┘
                          │ promote.py (eval score > 0.7)
                    ┌─────▼───────┐
                    │  Extended    │  ← 中自由度，标准契约
                    └─────┬───────┘
                          │ promote.py (eval score > 0.9 + 50次调用)
                    ┌─────▼───────┐
                    │    Core      │  ← 低自由度，严格契约
                    └─────┬───────┘
                          │
                    ┌─────▼───────┐
              ┌────►│  Deprecated  │  ← 废弃标记
              │     └─────┬───────┘
              │           │ archive.py (30天后)
    demote.py │     ┌─────▼───────┐
              │     │  Archived    │  ← 归档（可恢复）
              │     └─────────────┘
              │
              └── 任何阶段均可触发降级或废弃
```

**临时 skill 策略**：
```python
# activate_temp.py 核心逻辑
# 临时 skill 有 TTL（生存时间），过期自动废弃
# 用于一次性任务或探索性实验
{
    "skill_id": "temp-xyz",
    "ttl_hours": 24,
    "auto_promote": false,  # 默认不晋升
    "cleanup_policy": "archive"  # 过期后归档而非删除
}
```

### 5. RLAIF 自我迭代引擎

这是整个系统最核心的"自我进化"机制：

```
RLAIF 迭代循环
│
├── Phase 1: 执行 & 观察
│   └── Skill 执行任务 → 收集执行轨迹
│
├── Phase 2: 生成反馈 (generate_feedback.py)
│   ├── 对比执行结果与预期
│   ├── 分析失败模式
│   ├── 使用 Claude 自身对输出打分（AI Feedback）
│   └── 生成结构化反馈报告
│
├── Phase 3: 提议修订 (propose_revision.py)
│   ├── 基于反馈识别改进点
│   ├── 生成 SKILL.md 修订 diff
│   ├── 生成 scripts/ 修订 diff
│   └── 估计改进幅度
│
├── Phase 4: 验证修订 (validate_revision.py)
│   ├── 在保留测试集上运行修订后的 skill
│   ├── 对比修订前后评测分数
│   ├── 检查安全边界 (safety-bounds.md)
│   └── 判定：accept / reject / need-human-review
│
├── Phase 5: 应用或回滚
│   ├── accept → apply_revision.py（应用修订）
│   ├── reject → 记录失败原因到 rlaif-log.jsonl
│   └── need-human-review → 暂存待人工确认
│
└── 安全约束 (safety-bounds.md)
    ├── 单次迭代最大修改幅度限制
    ├── 连续失败次数阈值（超过则冻结迭代）
    ├── 核心 skill 修订必须人工确认
    └── 所有修订可回滚 (rollback.py)
```

---

# 方案二：「造化」—— 自举进化系统

> 设计哲学：如同生物进化，系统能自我创造、自我评判、自我改良。skill 管理 skill，评测评测自身。

## 总体架构

```
造化 Skills Cluster
│
├── genesis/                      ← 创世层：自举内核
│   ├── prime-mover/              ← 元 skill：能创建一切 skill
│   │   ├── SKILL.md              ← 总指挥 + skill 工厂
│   │   ├── scripts/
│   │   │   ├── spawn_skill.py    ← 孵化新 skill
│   │   │   ├── mutate_skill.py   ← 变异现有 skill
│   │   │   ├── merge_skills.py   ← 融合两个 skill
│   │   │   └── speciate.py       ← 从一个 skill 分化出变体
│   │   └── references/
│   │       ├── skill-genome.md   ← skill 的 "基因组" 规范
│   │       └── fitness-func.md   ← 适应度函数定义
│   │
│   └── judge/                    ← 评判者：评测一切
│       ├── SKILL.md              ← 评测逻辑 + 自我评测
│       ├── scripts/
│       │   ├── evaluate.py       ← 通用评测
│       │   ├── self_evaluate.py  ← 评测评测自身
│       │   ├── tournament.py     ← 锦标赛选拔
│       │   └── fitness.py        ← 适应度计算
│       └── references/
│           ├── eval-genome.md    ← 评测标准的基因组
│           └── meta-rubrics.md   ← 元评分标准
│
├── species/                      ← 物种层：活跃 skill 族群
│   ├── apex/                     ← 顶级 skill（经过锦标赛胜出）
│   │   ├── [动态填充]
│   │   └── ...
│   ├── stable/                   ← 稳定 skill（通过适应度阈值）
│   │   ├── [动态填充]
│   │   └── ...
│   ├── evolving/                 ← 进化中 skill（正在迭代）
│   │   ├── [动态填充]
│   │   └── ...
│   └── incubating/               ← 孵化中 skill（新生/实验性）
│       ├── [动态填充]
│       └── ...
│
├── orchestration/                ← 编排层
│   ├── swarm-coordinator/        ← 群体智能协调器
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── assemble_team.py  ← 为任务组建最优 skill 团队
│   │   │   ├── negotiate.py      ← skill 间协商资源/顺序
│   │   │   └── synthesize.py     ← 综合多个 skill 输出
│   │   └── references/
│   │       ├── team-patterns.md  ← 团队组合模式
│   │       └── negotiation.md    ← 协商协议
│   │
│   └── evolution-scheduler/      ← 进化调度器
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── schedule_gen.py   ← 调度下一代进化
│       │   ├── select_parents.py ← 选择进化亲本
│       │   └── cull.py           ← 淘汰低适应度 skill
│       └── references/
│           └── evolution-policy.md
│
├── memory/                       ← 记忆层
│   ├── experience-bank/          ← 经验库
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── record.py         ← 记录执行经验
│   │   │   ├── retrieve.py       ← 检索相关经验
│   │   │   └── distill.py        ← 蒸馏经验为规则
│   │   └── references/
│   │       └── experience-schema.md
│   │
│   └── lineage-tracker/          ← 血统追踪器
│       ├── SKILL.md
│       └── scripts/
│           ├── trace.py          ← 追踪 skill 演化谱系
│           └── visualize.py      ← 可视化演化树
│
└── .zaohua/                      ← 全局状态
    ├── population.json           ← 当前种群状态
    ├── fitness-history.jsonl     ← 适应度历史
    ├── lineage.json              ← 演化谱系图
    ├── experience-bank.jsonl     ← 经验数据库
    └── genomes/                  ← skill 基因组快照
        ├── [skill-id]-v[n].json  ← 每个 skill 每个版本的基因组
        └── ...
```

## 核心机制详解

### 1. 总指挥：prime-mover

prime-mover 既是总指挥，又是创造者。它的独特之处在于它能创建新的 skill 来解决之前不存在解决方案的问题。

```markdown
# Prime Mover — 造化总指挥

## 核心能力
1. **任务分析与路由**：与天工的 Meta-Commander 类似
2. **Skill 孵化**：当现有 skill 无法解决问题时，即时创造新 skill
3. **Skill 进化**：驱动现有 skill 变异、融合、分化

## 决策流程
1. 接收任务 → 搜索 population.json 中的适配 skill
2. 找到匹配 → 组建团队 → 路由到 swarm-coordinator
3. 未找到匹配 → 决策：
   a. 可从现有 skill 变异得到？→ mutate_skill.py
   b. 可从两个 skill 融合得到？→ merge_skills.py
   c. 全新能力？→ spawn_skill.py 创建，放入 incubating/
4. 执行完成 → 记录经验 → 触发适应度评估
```

### 2. 自我评测的评测者：judge

judge 不仅评测其他 skill，还能评测自己的评测质量（元评测）：

```markdown
# Judge — 造化评判者

## 评测层级

### Level 1: 功能评测
- 任务完成度
- 输出正确性
- 边界覆盖

### Level 2: 质量评测
- 代码/文档质量
- 一致性
- 最佳实践遵循度

### Level 3: 进化评测
- 适应度变化趋势
- 泛化能力（在未见过的任务上的表现）
- 资源效率（token/步骤）

### Level 4: 元评测（自评测）
- 评测一致性（相同输入多次评测结果的方差）
- 评测区分度（能否区分好坏输出）
- 评测与人类判断的相关性
- 定期使用 self_evaluate.py 审计自身

## 锦标赛机制
对于同类 skill（如多个代码生成 skill），使用 tournament.py：
1. 随机抽取测试任务集
2. 每个 skill 独立完成
3. 对输出进行盲评
4. 胜者晋升 apex/，败者降级或淘汰
```

### 3. 群体智能编排：swarm-coordinator

与天工的编排器不同，造化的编排器更强调"涌现性"：

```markdown
# Swarm Coordinator — 群体协调器

## 编排哲学
不预设固定流程，而是让 skill 团队自组织。

## 工作流程

### 1. 团队组建 (assemble_team.py)
- 基于任务描述，从 population.json 中选择 top-k 适配 skill
- 考虑团队的多样性（避免冗余）
- 考虑历史协作数据（哪些 skill 搭配效果好）

### 2. 协商 (negotiate.py)
- 每个 skill 声明自己能处理任务的哪个部分
- 处理重叠区域：谁更擅长？查适应度分数
- 处理缺口区域：需要 prime-mover 补充？
- 确定执行顺序和依赖关系

### 3. 执行
- 按协商结果分配子任务
- 并行执行无依赖子任务
- 逐步汇总结果

### 4. 综合 (synthesize.py)
- 合并各 skill 输出
- 解决冲突（不同 skill 给出矛盾输出时）
- 质量检查 → 触发 judge 评测
```

### 4. RLAIF 进化循环

造化的 RLAIF 更像真正的进化算法：

```
进化循环（每 N 次任务执行后触发）
│
├── 选择 (Selection)
│   ├── 按适应度排序所有 skill
│   ├── 保留 top 70%
│   └── 标记 bottom 30% 为待淘汰/待进化
│
├── 变异 (Mutation) — mutate_skill.py
│   ├── 对中等适应度 skill 进行小变异
│   │   ├── 修改 SKILL.md 中的指令措辞
│   │   ├── 调整脚本参数
│   │   └── 增删 references
│   └── 对低适应度 skill 进行大变异
│       ├── 重写核心逻辑
│       ├── 改变策略方向
│       └── 或直接淘汰
│
├── 交叉 (Crossover) — merge_skills.py
│   ├── 选择两个高适应度 skill
│   ├── 提取各自的优势模块
│   └── 融合为新 skill，放入 incubating/
│
├── 分化 (Speciation) — speciate.py
│   ├── 对适应度极高但覆盖面广的 skill
│   ├── 分化出专注于子领域的变体
│   └── 各变体独立进化
│
├── 评测 (Fitness Evaluation)
│   ├── 所有新生/变异 skill 在测试集上评测
│   ├── 更新 fitness-history.jsonl
│   └── 更新 population.json
│
└── 淘汰 (Culling) — cull.py
    ├── 连续 3 代适应度低于阈值 → 归档
    ├── 被优势 skill 完全覆盖 → 废弃
    └── 种群超过上限 → 淘汰最低适应度
```

### 5. 经验蒸馏

造化独有的知识传承机制：

```markdown
# Experience Bank — 经验库

## 蒸馏流程 (distill.py)
1. 收集 > 100 条同类型任务的执行经验
2. 使用 Claude 自身分析模式：
   - 哪些策略反复成功？
   - 哪些错误反复出现？
   - 哪些边界条件特别重要？
3. 将分析结果凝缩为规则
4. 注入到相关 skill 的 references/ 中
5. 效果等同于"无需重新发现的集体智慧"
```

---

# 两套方案对比

| 维度 | 天工（方案一） | 造化（方案二） |
|------|---------------|---------------|
| **核心理念** | 精密工程 | 生物进化 |
| **总指挥** | Meta-Commander（分析-路由-监控） | prime-mover（分析-路由-创造） |
| **编排模式** | 预定义 DAG 模式 | 群体自组织 |
| **评测** | 固定维度加权评分 | 适应度函数 + 锦标赛 + 元评测 |
| **迭代** | 结构化 RLAIF（提议→验证→应用） | 进化算法（选择→变异→交叉→淘汰） |
| **Skill 管理** | 显式生命周期（注册→晋升→废弃） | 种群动力学（孵化→进化→顶级→淘汰） |
| **可预测性** | 高（确定性流程） | 中（涌现性行为） |
| **创新潜力** | 中（受限于预定义结构） | 高（能自我创造新 skill） |
| **安全性** | 高（严格契约+人工确认） | 中（需要严格的安全边界） |
| **最适场景** | 企业级生产环境 | 研究/前沿探索环境 |
| **实现复杂度** | 高 | 极高 |

---

# 推荐实施路径

## 混合策略：天工为骨，造化为魂

最佳实践是将两套方案融合：

1. **基础设施用天工**：注册、生命周期、契约体系用天工的工程化方案
2. **迭代进化用造化**：RLAIF 引擎用造化的进化算法思路
3. **编排用天工+造化**：核心任务用天工的 DAG 编排，探索性任务用造化的群体协调
4. **评测两者融合**：天工的结构化评分 + 造化的锦标赛 + 元评测

## 实施阶段

```
Phase 1 (Week 1-2): 基础骨架
├── 实现 skill-registry（天工）
├── 实现 Meta-Commander 基础版
├── 实现 eval-engine 基础版
└── 创建 3-5 个核心 L2 skill

Phase 2 (Week 3-4): 编排能力
├── 实现 code-orchestrator
├── 实现 multi-agent-orchestrator
├── 实现 DAG 执行引擎
└── 端到端测试复杂任务

Phase 3 (Week 5-6): 自我进化
├── 实现 RLAIF 引擎（造化的进化循环）
├── 实现 experience-bank
├── 实现 prime-mover 的 skill 孵化能力
└── 首次自动进化迭代

Phase 4 (Week 7-8): 精炼与评测
├── 实现完整评测体系（锦标赛 + 元评测）
├── 全面 A/B 测试
├── 安全边界验证
└── 文档与交付
```
