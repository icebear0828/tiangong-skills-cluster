# 全局能力地图

## 能力矩阵

每个 skill 在此声明其核心能力、契约等级、适应度分数。
Meta-Commander 通过查阅此文件选择最优 skill 组合。

## 核心 Skill（低自由度，严格契约）

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 | 适应度 |
|----------|---------|---------|---------|---------|--------|
| code-gen | 根据需求描述生成代码 | 需求文本 + 语言 + 框架 | 代码文件 | strict | - |
| code-review | 审查代码质量/安全/性能 | 代码文件 | 审查报告 | strict | - |
| test-gen | 生成单元/集成测试 | 代码文件 + 框架 | 测试文件 | strict | - |
| doc-gen | 生成技术文档 | 代码/架构描述 | 文档文件 | strict | - |
| refactor | 重构代码（保持行为不变） | 代码文件 + 重构目标 | 重构后代码 | strict | - |
| debug | 诊断和修复 bug | 代码 + 错误信息 | 修复 patch | strict | - |

## 扩展 Skill（中自由度，标准契约）

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 | 适应度 |
|----------|---------|---------|---------|---------|--------|
| api-design | 设计 RESTful/GraphQL API | 需求描述 | API 规范 | standard | - |
| db-schema | 设计数据库 schema | 数据需求 | DDL/ERD | standard | - |
| perf-optimize | 性能分析和优化 | 代码 + 性能数据 | 优化方案 | standard | - |
| security-audit | 安全审计 | 代码/配置 | 审计报告 | standard | - |

## 实验 Skill（高自由度，宽松契约）

| Skill ID | 能力描述 | 输入类型 | 输出类型 | 契约等级 | 适应度 |
|----------|---------|---------|---------|---------|--------|
| creative-code | 创造性/探索性编程 | 灵感/目标描述 | 原型代码 | flexible | - |
| arch-explore | 架构探索与方案比较 | 约束条件 | 方案对比报告 | flexible | - |
| prototype | 快速原型开发 | 想法描述 | 可运行原型 | flexible | - |

## 编排器 Skill

| Skill ID | 编排范围 | 支持的 DAG 模式 |
|----------|---------|----------------|
| code-orchestrator | 代码领域多步骤任务 | sequential, iterative-refinement |
| doc-orchestrator | 文档领域多步骤任务 | sequential |
| data-orchestrator | 数据领域多步骤任务 | sequential, parallel |
| multi-agent-orchestrator | 跨域复合任务 | all patterns |
| eval-orchestrator | 评测流程 | sequential, parallel |

## 基础设施 Skill

| Skill ID | 职责 |
|----------|------|
| skill-registry | 注册、废弃、查询 skill |
| eval-engine | 执行评测、计算分数、生成报告 |
| rlaif-engine | RLAIF 自我迭代循环 |
| lifecycle-manager | skill 晋升、降级、归档 |

## 能力-任务映射规则

### 单任务直接映射
- "写一个函数" → code-gen
- "写测试" → test-gen
- "review 这段代码" → code-review
- "写文档" → doc-gen
- "这个 bug 怎么修" → debug
- "重构这个模块" → refactor

### 多步骤任务 → 编排器
- "实现这个功能并写测试" → code-orchestrator (code-gen → test-gen)
- "设计 API 并实现" → code-orchestrator (api-design → code-gen)
- "做性能分析并优化" → code-orchestrator (perf-optimize → refactor)

### 跨域任务 → multi-agent-orchestrator
- "设计数据库、写 API、写前端" → multi-agent (db-schema ∥ api-design → code-gen)
- "完整项目：需求→设计→实现→测试→文档" → multi-agent (全链路)
