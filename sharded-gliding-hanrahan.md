# 四阶段学习系统 - 原子化 Skills 规划

## 项目目标

将用户描述的四阶段学习系统转化为符合 v3.5.0 规范的原子化 Skills 体系。

---

## 原子化设计方案

### 三层架构

```
Layer 3: Composers (流程编排)
    └── full-learning-pipeline, phase1/2/3-orchestrators

Layer 2: Skills (用户交互)
    └── tutor-agent, socratic-agent, curator-agent, etc.

Layer 1: Primitives (原子能力)
    └── concept-explainer, question-generator, knowledge-validator, etc.
```

---

## 完整 Skills 清单

### Primitives (8个)

| 名称 | 触发词 | 职责 |
|------|--------|------|
| `concept-explainer` | `/explain-concept` | 概念分解与三级解释 |
| `analogy-generator` | `/generate-analogy` | 生成生活化类比 |
| `question-generator` | `/generate-questions` | Bloom分类法六级问题生成 |
| `knowledge-validator` | `/validate-knowledge` | 理解深度评分(0-100) |
| `difficulty-assessor` | `/assess-difficulty` | 难度评估+前置知识清单 |
| `memory-anchor-generator` | `/create-anchor` | 助记符+空间位置建议 |
| `progress-tracker` | `/track-progress` | 进度记录+遗忘曲线预测 |
| `feedback-synthesizer` | `/synthesize-feedback` | 多维反馈整合 |

### Core Skills (8个)

| 阶段 | 名称 | 触发词 | 职责 | 委托 |
|------|------|--------|------|------|
| 1 | `tutor-agent` | `/tutor` | 降维讲解+类比 | concept-explainer, analogy-generator, difficulty-assessor |
| 1 | `socratic-agent` | `/socratic` | 苏格拉底式对抗学习 | question-generator, knowledge-validator |
| 1 | `curator-agent` | `/curator` | 信息筛选去伪存真 | (subagent:browser) |
| 2 | `spatial-memory` | `/spatial` | 空间记忆法 | memory-anchor-generator |
| 2 | `speed-run` | `/speedrun` | 1小时极速概览 | concept-explainer, difficulty-assessor |
| 3 | `reverse-turing` | `/reverse-turing` | 反向图灵测试 | question-generator, knowledge-validator, feedback-synthesizer |
| 3 | `de-ai-review` | `/de-ai` | 离线复盘验证 | knowledge-validator, feedback-synthesizer |
| 4 | `micro-project` | `/micro-project` | 24小时MVP实战 | difficulty-assessor, progress-tracker, feedback-synthesizer |

### Composers (4个)

| 名称 | 触发词 | 编排 |
|------|--------|------|
| `phase1-input-orchestrator` | `/phase1` | tutor + socratic + curator |
| `phase2-multimodal-orchestrator` | `/phase2` | spatial-memory + speed-run |
| `phase3-validation-orchestrator` | `/phase3` | reverse-turing + de-ai-review |
| `full-learning-pipeline` | `/learn` | 全部四阶段 (conditional-composer) |

---

## 目录结构

```
D:\rag\mode\.claude\skills\
├── _primitives/
│   ├── concept-explainer/
│   │   ├── SKILL.md
│   │   ├── CHANGELOG.md
│   │   └── EVALUATION_LOG.md
│   ├── analogy-generator/
│   ├── question-generator/
│   ├── knowledge-validator/
│   ├── difficulty-assessor/
│   ├── memory-anchor-generator/
│   ├── progress-tracker/
│   └── feedback-synthesizer/
│
├── learning/
│   ├── tutor-agent/
│   ├── socratic-agent/
│   ├── curator-agent/
│   ├── spatial-memory/
│   ├── speed-run/
│   ├── reverse-turing/
│   ├── de-ai-review/
│   └── micro-project/
│
├── _composers/
│   ├── phase1-input-orchestrator/
│   ├── phase2-multimodal-orchestrator/
│   ├── phase3-validation-orchestrator/
│   └── full-learning-pipeline/
│
└── SKILLS_INDEX.md (更新)
```

---

## 实现步骤

### Phase 1: 核心Primitives (P0)
1. 创建 `concept-explainer` - 所有教学的基础
2. 创建 `question-generator` - 验证系统基础
3. 创建 `knowledge-validator` - 评估系统基础
4. 创建 `difficulty-assessor` - 自适应学习基础

### Phase 2: 第一阶段Skills (P1)
5. 创建 `tutor-agent` - 主要教学入口
6. 创建 `socratic-agent` - 对抗式深化
7. 创建 `analogy-generator` - 增强tutor效果

### Phase 3: 验证系统 (P2)
8. 创建 `feedback-synthesizer` - 反馈整合
9. 创建 `reverse-turing` - 核心验证机制
10. 创建 `de-ai-review` - 离线验证

### Phase 4: 增强功能 (P3)
11. 创建 `memory-anchor-generator` - 空间记忆支持
12. 创建 `spatial-memory` - 多模态学习
13. 创建 `speed-run` - 快速学习

### Phase 5: 实战与编排 (P4)
14. 创建 `progress-tracker` - 进度追踪
15. 创建 `micro-project` - MVP实战
16. 创建 `curator-agent` - 信息筛选(需browser subagent)

### Phase 6: Composers集成 (P5)
17. 创建 `phase1-input-orchestrator`
18. 创建 `phase2-multimodal-orchestrator`
19. 创建 `phase3-validation-orchestrator`
20. 创建 `full-learning-pipeline`

### Phase 7: 收尾
21. 更新 `SKILLS_INDEX.md`
22. 全局RLAIF评估

---

## 关键文件示例

### Primitive 示例: concept-explainer

```yaml
---
name: concept-explainer
type: skill
category: _primitives
trigger: "/explain-concept|解释概念"
description: "将复杂概念分解为可理解的组件"
version: 1.0.0
execution_modes:
  - instruction
---
```

### Core Skill 示例: tutor-agent

```yaml
---
name: tutor-agent
type: skill
category: learning
trigger: "/tutor|导师模式|teach me"
description: "降维打击式教学，用类比解释新概念"
version: 1.0.0
execution_modes:
  - instruction
  - delegate:concept-explainer
  - delegate:analogy-generator
  - delegate:difficulty-assessor
delegates_to:
  - concept-explainer
  - analogy-generator
  - difficulty-assessor
---
```

### Composer 示例: full-learning-pipeline

```yaml
---
name: full-learning-pipeline
type: conditional-composer
category: _composers
trigger: "/learn|完整学习|full pipeline"
description: "四阶段完整学习流水线"
version: 1.0.0
execution_modes:
  - delegate:phase1-input-orchestrator
  - delegate:phase2-multimodal-orchestrator
  - delegate:phase3-validation-orchestrator
  - delegate:micro-project
flags:
  - name: --phase
    description: "指定开始阶段 (1-4)"
    default: "1"
  - name: --skip-validation
    description: "跳过验证阶段"
    default: false
delegates_to:
  - phase1-input-orchestrator
  - phase2-multimodal-orchestrator
  - phase3-validation-orchestrator
  - micro-project
---
```

---

## 依赖关系图

```
                        full-learning-pipeline
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
   phase1-orch            phase2-orch            phase3-orch
         │                       │                       │
    ┌────┼────┐             ┌────┼────┐             ┌────┴────┐
    │    │    │             │         │             │         │
    ▼    ▼    ▼             ▼         ▼             ▼         ▼
 tutor socra cura       speed-run spatial     reverse  de-ai
    │    │                  │         │          │        │
    ├────┼──────────────────┼─────────┘          │        │
    │    │                  │                    │        │
    ▼    ▼                  ▼                    ▼        ▼
┌───────────────────────────────────────────────────────────────┐
│                        PRIMITIVES                              │
│  concept-explainer | analogy-gen | question-gen | validator   │
│  difficulty-assess | memory-anchor | progress | feedback      │
└───────────────────────────────────────────────────────────────┘
```

---

## 验证方法

### 单元验证
- 每个Primitive独立测试其触发词和输出格式
- 每个Skill测试委托链是否正确传递上下文

### 集成验证
1. 触发 `/tutor 量子计算` 测试导师模式
2. 触发 `/socratic` 测试苏格拉底对话
3. 触发 `/reverse-turing` 测试反向图灵
4. 触发 `/learn 机器学习` 测试完整流水线

### RLAIF 评估
- 每个Skill创建后调用 `/rlaif <skill-path>`
- 确保置信度 ≥ 80 分
- 不足则迭代修复

---

## 风险与决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| curator-agent 执行模式 | `subagent:browser` | 需要实时网络搜索验证 |
| progress-tracker | `api:python` | 需要持久化存储进度数据 |
| full-learning-pipeline | `conditional-composer` | 支持阶段跳转和验证回退 |

---

## 总计

- **Primitives**: 8 个
- **Core Skills**: 8 个
- **Composers**: 4 个
- **总计**: 20 个 Skills
