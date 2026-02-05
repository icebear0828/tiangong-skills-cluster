# 学习域路由规则

## 概述

本文档定义了 learning-commander 将学习任务路由到正确 Skill 或编排器的决策规则。

## 一级分流：任务类型判断

```
学习任务输入
    │
    ├── 单概念快速解释 → 直接调用 analogy-explainer
    │
    ├── 知识点提取 → 直接调用 knowledge-extractor
    │
    ├── 理解验证 → verification-orchestrator
    │
    ├── 实践练习 → micro-project-orchestrator
    │
    └── 系统性学习 → 完整四阶段流程
            ├── Phase 1: learning-orchestrator
            ├── Phase 2: knowledge-graph-orchestrator
            ├── Phase 3: verification-orchestrator
            └── Phase 4: micro-project-orchestrator
```

## 关键词触发规则

| 关键词 | 路由目标 | 说明 |
|--------|---------|------|
| 学习、理解、掌握、教我 | learning-commander | 启动学习流程 |
| 解释、讲解、比喻、类比 | analogy-explainer | 直接调用 |
| 提取要点、总结、提炼 | knowledge-extractor | 直接调用 |
| 检验理解、测试掌握 | verification-orchestrator | 编排验证 |
| 做练习、实践、项目 | micro-project-orchestrator | 编排实践 |
| 画图、可视化、图谱 | knowledge-graph-orchestrator | 编排图谱 |

## 目标等级路由

| 目标等级 | 描述 | 阶段数 | 路径 |
|---------|------|--------|------|
| awareness | 知道是什么 | 1 | Phase 1 only |
| understanding | 理解原理 | 2 | Phase 1-2 |
| application | 能够应用 | 3 | Phase 1-3 |
| mastery | 精通掌握 | 4 | Phase 1-4 |

## 复杂度判定

| 复杂度 | 主题特征 | 阶段数 | 示例 |
|--------|---------|--------|------|
| S | 单一概念、基础知识 | 1-2 | "什么是变量" |
| M | 多概念关联、中等难度 | 2-3 | "理解闭包" |
| L | 复杂主题、系统性 | 3-4 | "学习 React" |
| XL | 深度主题、需要实践 | 4+ | "精通微服务架构" |

## 编排器选择规则

### Phase 1: learning-orchestrator
触发条件：
- 需要消化新知识
- 需要内容策展
- 需要生成类比解释

### Phase 2: knowledge-graph-orchestrator
触发条件：
- 需要构建知识结构
- 需要可视化概念关系
- 目标等级 ≥ understanding

### Phase 3: verification-orchestrator
触发条件：
- 需要验证学习效果
- 需要苏格拉底对话
- 目标等级 ≥ application

### Phase 4: micro-project-orchestrator
触发条件：
- 需要实践巩固
- 需要微项目练习
- 目标等级 = mastery

## 自适应调整规则

| 学习者表现 | 调整策略 |
|-----------|---------|
| Phase 1 理解快 | 跳过部分类比，加速到 Phase 2 |
| Phase 3 验证失败 | 返回 Phase 1/2 补救 |
| Phase 4 实践困难 | 返回 Phase 3 加强 |
| 全程优秀 | 提升难度，减少阶段 |

## 质量关卡

| 阶段 | 检查内容 | 未通过处理 |
|------|---------|-----------|
| Phase 1 | 知识覆盖度 ≥80% | 增加资源 |
| Phase 2 | 图谱连通性 | 补充关系 |
| Phase 3 | 掌握度 ≥目标 | 返回补救 |
| Phase 4 | 项目完成度 | 简化项目 |

## 异常处理

| 异常 | 处理策略 |
|------|---------|
| 主题过大 | 拆分为子主题 |
| 资源不足 | 使用生成式内容 |
| 验证多次失败 | 降低目标等级 |
| 学习者放弃 | 保存进度，允许续学 |
