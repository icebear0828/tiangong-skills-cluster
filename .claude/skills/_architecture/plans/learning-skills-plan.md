# 学习加速 Skills 集群实现计划

## 任务概述

将用户描述的四阶段学习加速方法论（导师Agent、苏格拉底Agent、策展Agent、空间记忆、极速概览、反向图灵测试、离线复盘、微项目驱动）原子化为符合现有 TianGong Skills Cluster 架构的 Skills 体系。

## 架构约束

- **三层架构**: L0(总指挥) → L1(编排器) → L2(原子Skill)
- **契约等级**: strict(核心) / standard(扩展) / flexible(实验)
- **文件结构**: SKILL.md + references/ + scripts/
- **位置**: `.claude/skills/_architecture/`

---

## 新增 Skills 清单

### L0 层（1个）
| ID | 名称 | 契约 | 职责 |
|----|------|------|------|
| learning-commander | 学习域总指挥 | strict | 学习任务路由、学习计划生成、阶段调度 |

### L1 层（4个编排器）
| ID | 名称 | 契约 | 职责 |
|----|------|------|------|
| learning-orchestrator | 学习流程编排 | strict | 四阶段学习流程编排（消化→结构→内化→验证） |
| knowledge-graph-orchestrator | 知识图谱编排 | standard | 知识提取+空间映射+图谱构建 |
| verification-orchestrator | 内化验证编排 | strict | 自我解释验证+苏格拉底对话+掌握度评估 |
| micro-project-orchestrator | 微项目编排 | standard | 项目生成+代码脚手架+评估反馈 |

### L2 层（7个原子Skill）

**Core（3个，strict契约）**
| ID | 名称 | 输入 | 输出 |
|----|------|------|------|
| knowledge-extractor | 知识提取器 | 文本内容+内容类型 | 结构化知识项+摘要+层次 |
| analogy-explainer | 类比解释器 | 概念+学习者背景 | 类比映射+解释文本+局限性 |
| self-explanation-validator | 自我解释验证器 | 学习者解释+参考解释 | 评分+误解识别+改进建议 |

**Extended（3个，standard契约）**
| ID | 名称 | 输入 | 输出 |
|----|------|------|------|
| content-curator | 内容策展器 | 主题+来源类型+质量标准 | 排序资源列表+学习路径建议 |
| socratic-questioner | 苏格拉底提问器 | 主题+当前理解+对话历史 | 问题序列+进度评估+适应建议 |
| spatial-mapper | 空间映射器 | 概念列表+关系+映射类型 | 空间布局+聚类+可视化代码 |

**Experimental（1个，flexible契约）**
| ID | 名称 | 输入 | 输出 |
|----|------|------|------|
| diagram-generator | 图表生成器 | 结构数据+图表类型 | Mermaid/Graphviz代码 |

---

## 目录结构

```
.claude/skills/_architecture/
├── L0-learning-commander/
│   ├── SKILL.md
│   ├── references/
│   │   ├── learning-routing-rules.md
│   │   ├── learning-capability-map.md
│   │   └── learning-phases.md
│   └── scripts/
│       ├── analyze_learning_task.py
│       └── select_learning_path.py
│
├── L1-orchestrators/
│   ├── learning-orchestrator/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── learning-patterns.md
│   │   │   └── quality-gates.md
│   │   └── scripts/
│   ├── knowledge-graph-orchestrator/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── graph-patterns.md
│   │   │   └── linking-strategies.md
│   │   └── scripts/
│   ├── verification-orchestrator/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── verification-rubrics.md
│   │   │   └── mastery-criteria.md
│   │   └── scripts/
│   └── micro-project-orchestrator/
│       ├── SKILL.md
│       ├── references/
│       │   ├── project-templates.md
│       │   └── scaffolding-patterns.md
│       └── scripts/
│
├── L2-execution/
│   ├── core/
│   │   ├── knowledge-extractor/
│   │   │   ├── SKILL.md
│   │   │   ├── references/extraction-patterns.md
│   │   │   └── scripts/extract.py
│   │   ├── analogy-explainer/
│   │   │   ├── SKILL.md
│   │   │   ├── references/
│   │   │   │   ├── analogy-bank.md
│   │   │   │   └── domain-mappings.md
│   │   │   └── scripts/generate_analogy.py
│   │   └── self-explanation-validator/
│   │       ├── SKILL.md
│   │       ├── references/validation-rubrics.md
│   │       └── scripts/validate.py
│   ├── extended/
│   │   ├── content-curator/
│   │   │   ├── SKILL.md
│   │   │   ├── references/
│   │   │   │   ├── source-quality-criteria.md
│   │   │   │   └── curation-strategies.md
│   │   │   └── scripts/curate.py
│   │   ├── socratic-questioner/
│   │   │   ├── SKILL.md
│   │   │   ├── references/
│   │   │   │   ├── question-patterns.md
│   │   │   │   └── scaffolding-levels.md
│   │   │   └── scripts/generate_questions.py
│   │   └── spatial-mapper/
│   │       ├── SKILL.md
│   │       ├── references/mapping-algorithms.md
│   │       └── scripts/create_map.py
│   └── experimental/
│       └── diagram-generator/
│           ├── SKILL.md
│           ├── references/diagram-types.md
│           └── scripts/generate_diagram.py
│
└── references/
    ├── learning-rubrics.md          # 新增：学习评估标准
    └── learning-domains.md          # 新增：学习领域定义
```

---

## 实现分阶段

### Phase 1: 核心基础（5个文件优先）

**目标**: 建立最小可用学习系统

1. `L2-execution/core/knowledge-extractor/SKILL.md`
2. `L2-execution/core/analogy-explainer/SKILL.md`
3. `L2-execution/core/self-explanation-validator/SKILL.md`
4. `L0-learning-commander/SKILL.md`
5. `L1-orchestrators/learning-orchestrator/SKILL.md`

**依赖链**: knowledge-extractor → analogy-explainer → learning-orchestrator → learning-commander

### Phase 2: 结构化增强（4个文件）

**目标**: 增加知识图谱和可视化

1. `L2-execution/extended/spatial-mapper/SKILL.md`
2. `L1-orchestrators/knowledge-graph-orchestrator/SKILL.md`
3. `L2-execution/experimental/diagram-generator/SKILL.md`
4. `L2-execution/extended/content-curator/SKILL.md`

### Phase 3: 交互验证（3个文件）

**目标**: 完善苏格拉底对话和微项目

1. `L2-execution/extended/socratic-questioner/SKILL.md`
2. `L1-orchestrators/verification-orchestrator/SKILL.md`
3. `L1-orchestrators/micro-project-orchestrator/SKILL.md`

### Phase 4: 集成更新（3个文件）

**目标**: 更新全局配置

1. `_architecture/registry.json` - 添加12个新skill注册
2. `_architecture/references/capability-map.md` - 添加学习域能力映射
3. `_architecture/references/routing-rules.md` - 添加学习任务路由规则

---

## 依赖关系 DAG

```
                    learning-commander (L0)
                           │
          ┌────────────────┼────────────────┬─────────────────┐
          ▼                ▼                ▼                 ▼
learning-orchestrator  knowledge-graph   verification    micro-project
    (L1)              -orchestrator(L1)  -orchestrator(L1) -orchestrator(L1)
    │                      │                  │                │
    ├─→ knowledge-extractor │                  │                │
    ├─→ analogy-explainer   ├─→ knowledge-extractor             │
    ├─→ content-curator     ├─→ spatial-mapper                  │
    │                       ├─→ diagram-generator               │
    │                       │                  ├─→ self-explanation-validator
    │                       │                  ├─→ socratic-questioner
    │                       │                  ├─→ analogy-explainer
    │                       │                  │                │
    └───────────────────────┴──────────────────┴────────────────┤
                                                                │
                                                   ┌────────────┴────────────┐
                                                   ▼            ▼            ▼
                                               code-gen    test-gen    code-review
                                               (现有)      (现有)       (现有)
```

---

## 与现有 Skills 的集成

| 现有 Skill | 调用者 | 场景 |
|-----------|--------|------|
| code-gen | micro-project-orchestrator | 生成项目代码 |
| test-gen | micro-project-orchestrator | 生成练习测试 |
| code-review | micro-project-orchestrator | 评审学习者代码 |
| doc-gen | knowledge-graph-orchestrator | 生成知识文档 |
| eval-engine | learning-orchestrator, verification-orchestrator | 评估学习进度/掌握度 |
| debug | micro-project-orchestrator | 辅助学习者调试 |

---

## 关键文件修改清单

### registry.json 新增条目（12个）
```json
"learning-commander", "learning-orchestrator", "knowledge-graph-orchestrator",
"verification-orchestrator", "micro-project-orchestrator", "knowledge-extractor",
"analogy-explainer", "self-explanation-validator", "content-curator",
"socratic-questioner", "spatial-mapper", "diagram-generator"
```

### capability-map.md 新增表格
- 学习 Skill 能力表（7个L2）
- 学习编排器表（4个L1）
- 学习任务映射规则

### routing-rules.md 新增路由
- "学习/理解/掌握" → learning-commander
- "解释/讲解" → analogy-explainer
- "提取要点" → knowledge-extractor
- "检验理解" → verification-orchestrator
- "做练习" → micro-project-orchestrator

---

## 实现规范

### SKILL.md 完整契约要求
每个 SKILL.md 必须包含：
- **Frontmatter**: name, description (含触发条件)
- **输入契约**: 完整 JSON Schema，包含 required/optional 字段
- **输出契约**: 完整 JSON Schema，定义所有返回字段
- **执行流程**: 分步骤描述处理逻辑
- **质量标准**: 评分维度和阈值表格
- **与其他 Skill 的关系**: 上下游依赖说明

### 外部 API 接口设计（content-curator）
采用模拟接口模式：
```python
# 定义标准接口
class ContentSource(Protocol):
    def search(self, query: str, filters: dict) -> List[Resource]: ...
    def fetch(self, url: str) -> Content: ...

# 实际调用由 MCP 工具或用户配置完成
# SKILL.md 中定义接口契约，不实现具体 API 调用
```

支持的数据源类型（通过 MCP 扩展）：
- `arxiv`: 学术论文检索
- `github`: 代码仓库搜索
- `web`: 通用网页抓取（WebFetch）

---

## 验证计划

### 单元测试
- 每个 L2 Skill：输入契约验证 + 输出格式验证
- 每个 L1 编排器：流程完整性测试

### 集成测试
1. **简单学习流程**: 给定概念 → knowledge-extractor → analogy-explainer → 输出解释
2. **知识图谱构建**: 给定文档 → knowledge-extractor → spatial-mapper → diagram-generator
3. **完整四阶段**: learning-commander 路由 → 四阶段流程 → eval-engine 评估

### 端到端测试
- 输入："帮我学习 React Hooks"
- 预期：内容策展 → 知识提取 → 类比解释 → 图谱可视化 → 苏格拉底问答 → 微项目生成

---

## 文件总数统计

| 类型 | 数量 |
|------|------|
| SKILL.md | 12 |
| references/*.md | ~20 |
| scripts/*.py | ~15 |
| 全局配置更新 | 3 |
| **总计** | ~50 |

---

## 用户需求到 Skill 映射

### 原始需求 → Skills 映射表

| 用户描述 | 对应 Skill | 层级 |
|----------|-----------|------|
| 导师 Agent - 降维打击解释 | analogy-explainer | L2 Core |
| 苏格拉底 Agent - 对抗性学习 | socratic-questioner | L2 Extended |
| 策展 Agent - 信息过滤降噪 | content-curator | L2 Extended |
| 空间记忆 - 概念可视化 | spatial-mapper + diagram-generator | L2 Extended/Experimental |
| 极速概览 - 技能树生成 | knowledge-extractor + spatial-mapper | L2 Core/Extended |
| 反向图灵测试 - 你教AI | self-explanation-validator | L2 Core |
| 离线复盘 - 逻辑框架 | knowledge-graph-orchestrator | L1 |
| 微项目驱动 - 24h MVP | micro-project-orchestrator | L1 |

### 四阶段学习流程映射

```
第一阶段 (输入优化)
├── content-curator → 精选内容
├── knowledge-extractor → 提取要点
└── analogy-explainer → 类比解释

第二阶段 (多模态输入)
├── spatial-mapper → 概念映射
├── diagram-generator → 可视化
└── knowledge-graph-orchestrator → 图谱构建

第三阶段 (内化)
├── self-explanation-validator → 反向图灵测试
├── socratic-questioner → 苏格拉底问答
└── verification-orchestrator → 综合验证

第四阶段 (实战)
├── micro-project-orchestrator → 项目生成
├── code-gen (现有) → 代码生成
├── test-gen (现有) → 测试生成
└── eval-engine (现有) → 评估反馈
```
