# 总指挥快速上手指南

## 四大总指挥概览

TianGong Skills 架构采用**四总指挥制**，每个总指挥负责一个独立领域：

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                L0 总指挥层                                           │
├────────────────┬────────────────┬─────────────────────┬─────────────────────────────┤
│ meta-commander │writing-commander│evaluation-commander│  learning-commander         │
│  代码域总指挥   │  写作域总指挥    │    评审域总指挥      │      学习域总指挥            │
│                │                │                     │                             │
│ "帮我写代码"   │ "帮我写文章"    │  "帮我评审方案"       │  "帮我学习 X"               │
│ "实现功能"     │ "写小红书笔记"  │  "对比这些方案"       │  "解释 X 概念"              │
│ "修复 bug"    │ "写公众号文章"  │  "选择最佳方案"       │  "检验我的理解"             │
└────────────────┴────────────────┴─────────────────────┴─────────────────────────────┘
```

---

## 快速判断：该用哪个总指挥？

### 30秒决策流程图

```
你的任务是什么？
    │
    ├── 涉及代码开发/修改 ──────────▶ meta-commander
    │   • 写代码、写测试、写文档
    │   • 修 bug、重构
    │   • API 设计、数据库设计
    │
    ├── 涉及创意内容写作 ──────────▶ writing-commander
    │   • 小红书笔记、公众号文章
    │   • Twitter/社交媒体帖子
    │   • 标题优化、SEO、传播力
    │
    ├── 涉及方案对比/评审 ──────────▶ evaluation-commander
    │   • 多方案对比
    │   • 选择最佳方案
    │   • 对抗性评估
    │
    └── 涉及学习/理解知识 ──────────▶ learning-commander
        • 学习新技术
        • 理解概念
        • 检验掌握程度
```

### 关键词速查表

| 关键词 | 总指挥 | 示例 |
|--------|--------|------|
| 写代码、实现、生成代码、创建功能 | meta-commander | "写一个登录功能" |
| 修复、debug、调试 | meta-commander | "修复这个 bug" |
| 测试、test | meta-commander | "写单元测试" |
| 重构、优化代码 | meta-commander | "重构这个模块" |
| 写文章、写笔记、写帖子 | writing-commander | "写一篇小红书笔记" |
| 标题、文案、内容创作 | writing-commander | "帮我起个标题" |
| SEO、传播、平台适配 | writing-commander | "优化这篇文章的SEO" |
| 评审、对比、选择 | evaluation-commander | "评审这三个方案" |
| 哪个更好、最佳方案 | evaluation-commander | "哪个方案更好" |
| 攻击、挑战、压力测试 | evaluation-commander | "攻击这个方案" |
| 学习、理解、掌握 | learning-commander | "学习 React" |
| 解释、讲解、教我 | learning-commander | "解释闭包" |
| 检验、测试掌握 | learning-commander | "检验我对 X 的理解" |

---

## 总指挥详细对比

### 1. meta-commander（代码域总指挥）

**职责**: 处理所有代码相关任务

**触发条件**:
- 需要生成/修改代码
- 需要写测试/文档
- 需要调试/重构

**下游编排器**:
- `code-orchestrator` - 代码开发流程
- `doc-orchestrator` - 文档生成流程
- `data-orchestrator` - 数据库相关流程
- `multi-agent-orchestrator` - 跨域复杂任务

**典型任务示例**:
```
O "实现一个用户注册功能"
O "为这个函数写单元测试"
O "重构这个模块，提高可读性"
O "设计用户表的数据库 schema"
O "优化这段代码的性能"
```

**不处理**:
```
X "写一篇小红书笔记" → writing-commander
X "评审这三个架构方案" → evaluation-commander
X "教我学习 TypeScript" → learning-commander
```

---

### 2. writing-commander（写作域总指挥）

**职责**: 处理所有创意内容写作任务

**触发条件**:
- 需要创作社交媒体内容
- 需要优化文案/标题
- 需要平台适配或SEO

**下游编排器**:
- `adaptive-orchestrator` - 蓝图编排 (黑板+切片器+中间件)

**支持平台**:
| 平台 | 特点 |
|------|------|
| 小红书 | 种草风格、emoji丰富 |
| 公众号 | 深度长文、金句导向 |
| Twitter | 简洁有力、话题标签 |

**典型任务示例**:
```
O "帮我写一篇关于AI的小红书笔记"
O "优化这个标题的吸引力"
O "写一篇公众号爆款文章"
O "分析这篇文章的传播力"
```

**不处理**:
```
X "写一个 Python 脚本" → meta-commander
X "对比这两篇文章哪个更好" → evaluation-commander
X "学习内容营销" → learning-commander
```

---

### 3. evaluation-commander（评审域总指挥）

**职责**: 处理所有方案评审任务

**触发条件**:
- 需要对比多个方案
- 需要选择最佳方案
- 需要对抗性评估

**下游编排器**:
- `multi-round-eval-orchestrator` - 多轮评审流程

**评审模式**:
| 模式 | 轮次 | 适用场景 |
|------|------|---------|
| quick | 1 | 2方案快速对比 |
| standard | 2 | 常规方案评审 |
| thorough | 4 | 重要决策评审 |
| adversarial | 4+ | 高风险对抗评审 |

**典型任务示例**:
```
O "对比 React 和 Vue 哪个更适合我们的项目"
O "评审这三个架构方案，选出最佳"
O "对这个方案做对抗性评估"
O "这两个实现方案哪个更好"
```

**不处理**:
```
X "实现选中的方案" → meta-commander
X "写一篇方案分析文章" → writing-commander
X "学习 React" → learning-commander
```

---

### 4. learning-commander（学习域总指挥）

**职责**: 处理所有学习相关任务

**触发条件**:
- 需要学习新知识
- 需要理解概念
- 需要验证掌握程度

**下游编排器**:
- `learning-orchestrator` - Phase 1 消化
- `knowledge-graph-orchestrator` - Phase 2 结构化
- `verification-orchestrator` - Phase 3 内化
- `micro-project-orchestrator` - Phase 4 应用

**学习目标等级**:
| 等级 | 描述 | 阶段数 |
|------|------|--------|
| awareness | 知道是什么 | 1 |
| understanding | 理解原理 | 2 |
| application | 能够应用 | 3 |
| mastery | 精通掌握 | 4 |

**典型任务示例**:
```
O "学习 TypeScript 泛型"
O "解释什么是闭包，用类比说明"
O "检验我对依赖注入的理解"
O "帮我系统性掌握 React Hooks"
```

**不处理**:
```
X "用 TypeScript 写一个工具函数" → meta-commander
X "写一篇 TypeScript 教程文章" → writing-commander
X "对比 TypeScript 和 Flow" → evaluation-commander
```

---

## 边界场景处理

### 场景 1：学习后实践

```
用户: "学习 React，然后写一个 Todo 应用"

处理方式:
1. learning-commander 负责 "学习 React" 部分
2. 学习完成后，meta-commander 负责 "写 Todo 应用" 部分
```

### 场景 2：评审后实施

```
用户: "评审这三个方案，然后实现最佳方案"

处理方式:
1. evaluation-commander 负责 "评审" 部分
2. 选出最佳方案后，meta-commander 负责 "实现" 部分
```

### 场景 3：学习中的代码练习

```
用户: "学习 React Hooks，包括动手练习"

处理方式:
learning-commander 全程负责，其中:
- Phase 1-3: 学习和验证
- Phase 4: micro-project-orchestrator 调用 code-gen 等生成练习
```

### 场景 4：内容创作前的学习

```
用户: "学习内容营销，然后写一篇推广文"

处理方式:
1. learning-commander 负责 "学习内容营销" 部分
2. 学习完成后，writing-commander 负责 "写推广文" 部分
```

### 场景 5：评审写作方案

```
用户: "写三个版本的标题，帮我选最好的"

处理方式:
1. writing-commander 负责生成三个标题版本
2. evaluation-commander 负责对比选择最佳标题
```

---

## 总指挥协作模式

### 串行协作
```
用户大任务
    │
    ├── 阶段1: learning-commander (学习)
    │
    ├── 阶段2: evaluation-commander (方案评审)
    │
    ├── 阶段3: writing-commander (内容创作) 或 meta-commander (代码实施)
    │
    └── 完成
```

### 独立调用
```
用户单一任务 ──▶ 对应总指挥 ──▶ 完成
```

### 跨域复杂任务
```
用户跨域任务
    │
    └── meta-commander
            └── multi-agent-orchestrator
                    ├── 代码子任务 → code-orchestrator
                    ├── 数据子任务 → data-orchestrator
                    └── 文档子任务 → doc-orchestrator
```

---

## 常见问题

### Q: 如果任务同时涉及多个域怎么办？

**A**: 拆分为多个子任务，分别路由到对应总指挥。例如：
- "学习 React 并写一个项目" → learning-commander + meta-commander
- "写三版标题并选最好的" → writing-commander + evaluation-commander

### Q: 我不确定该用哪个总指挥？

**A**: 看任务的**核心目标**：
- 核心是产出代码 → meta-commander
- 核心是产出内容 → writing-commander
- 核心是做决策 → evaluation-commander
- 核心是获取知识 → learning-commander

### Q: 可以直接调用下游 Skill 吗？

**A**: 可以，但建议通过总指挥路由，以获得：
- 自动模式选择
- 质量关卡检查
- 统一的输出格式

### Q: meta-commander 和原来的用法有什么区别？

**A**: 没有区别。meta-commander 是原有的代码域总指挥，写作域、评审域和学习域是新增的专业化总指挥。

### Q: writing-commander 和 meta-commander 都能写文档？

**A**: 关键区别：
- `meta-commander` → 技术文档 (API doc, README, 代码注释)
- `writing-commander` → 创意内容 (社交媒体, 营销文案, 爆款文章)

---

## 一图总结

```
┌────────────────────────────────────────────────────────────────────┐
│                          用户任务                                   │
└────────────────────────────────────────────────────────────────────┘
                                │
               ┌────────────────┼────────────────┐
               │                │                │                │
               ▼                ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │meta-commander│ │  writing-    │ │ evaluation-  │ │  learning-   │
      │   代码域      │ │  commander   │ │  commander   │ │  commander   │
      │              │ │   写作域      │ │   评审域      │ │   学习域      │
      └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                │                │                │
      ┌──────┴──────┐        │               │         ┌──────┴──────┐
      ▼             ▼        ▼               ▼         ▼             ▼
 ┌────────┐   ┌────────┐ ┌────────┐   ┌────────┐ ┌────────┐  ┌────────┐
 │ code-  │   │ doc-   │ │adaptive│   │multi-  │ │learning│  │verifi- │
 │orchestr│   │orchestr│ │-orchestr│  │round-  │ │-orchestr│ │cation- │
 │        │   │        │ │        │   │eval-   │ │        │  │orchestr│
 └────────┘   └────────┘ └────────┘   │orchestr│ └────────┘  └────────┘
                                       └────────┘
                                           │
                              ┌─────────────┼─────────────┐
                              ▼             ▼             ▼
                        L2 评审 Skills  L2 学习 Skills  L2 写作 Skills
```
