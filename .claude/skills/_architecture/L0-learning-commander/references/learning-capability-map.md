# 学习域能力映射

## 学习域 Skill 能力矩阵

### L0 总指挥

| Skill | 核心能力 | 输入 | 输出 |
|-------|---------|------|------|
| learning-commander | 学习任务路由、计划生成、阶段调度 | 任务描述 + 学习者画像 | 学习计划 + 执行结果 |

### L1 编排器

| Skill | 核心能力 | 编排范围 | 阶段 |
|-------|---------|---------|------|
| learning-orchestrator | 消化阶段流程编排 | 资源→提取→类比 | Phase 1 |
| knowledge-graph-orchestrator | 知识图谱构建编排 | 映射→聚类→可视化 | Phase 2 |
| verification-orchestrator | 内化验证流程编排 | 解释→对话→评估 | Phase 3 |
| micro-project-orchestrator | 微项目实践编排 | 项目→练习→评审 | Phase 4 |

### L2 核心学习 Skill

| Skill | 能力 | 调用时机 |
|-------|------|---------|
| knowledge-extractor | 从文本提取结构化知识 | Phase 1 |
| analogy-explainer | 生成类比解释 | Phase 1, 3 |
| self-explanation-validator | 验证学习者解释 | Phase 3 |

### L2 扩展学习 Skill

| Skill | 能力 | 调用时机 |
|-------|------|---------|
| content-curator | 策展学习资源 | Phase 1 |
| socratic-questioner | 苏格拉底式提问 | Phase 3 |
| spatial-mapper | 概念空间映射 | Phase 2 |

### L2 实验 Skill

| Skill | 能力 | 调用时机 |
|-------|------|---------|
| diagram-generator | 生成图表代码 | Phase 2 |

---

## 能力调用链

### 快速解释（单概念）
```
learning-commander
    └── analogy-explainer（直接调用）
```

### 知识提取（单文档）
```
learning-commander
    └── knowledge-extractor（直接调用）
```

### 理解验证
```
learning-commander
    └── verification-orchestrator
            ├── self-explanation-validator
            ├── socratic-questioner
            └── analogy-explainer (澄清)
```

### 系统学习（完整流程）
```
learning-commander
    │
    ├── Phase 1: learning-orchestrator
    │       ├── content-curator
    │       ├── knowledge-extractor
    │       └── analogy-explainer
    │
    ├── Phase 2: knowledge-graph-orchestrator
    │       ├── spatial-mapper
    │       └── diagram-generator
    │
    ├── Phase 3: verification-orchestrator
    │       ├── self-explanation-validator
    │       ├── socratic-questioner
    │       └── analogy-explainer (澄清)
    │
    └── Phase 4: micro-project-orchestrator
            ├── code-gen
            ├── test-gen
            └── code-review
```

---

## 能力边界定义

### learning-commander 能处理

- 学习任务分析
- 学习计划生成
- 阶段流程调度
- 掌握度评估
- 补救循环控制

### learning-commander 不处理

- 评审任务（由 evaluation-commander 处理）
- 代码开发任务（由 code-orchestrator 处理）
- 文档生成任务（由 doc-orchestrator 处理）

---

## 与其他域的协作

| 协作域 | 协作 Skill | 协作场景 |
|--------|-----------|---------|
| 代码域 | code-gen, test-gen, code-review | Phase 4 微项目实践 |
| 评审域 | - | 无直接协作 |
| 基础设施 | eval-engine | 掌握度评估评分 |

---

## 学习者画像适配

### 按水平调整
| 水平 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| beginner | 详细 | 简化 | 宽松 | 简单项目 |
| intermediate | 标准 | 标准 | 标准 | 标准项目 |
| advanced | 精简 | 深入 | 严格 | 挑战项目 |

### 按学习风格调整
| 风格 | 适配策略 |
|------|---------|
| visual | 增加图谱和可视化 |
| verbal | 增加文字解释和类比 |
| logical | 强调结构和推理 |
| experiential | 提前引入实践 |
