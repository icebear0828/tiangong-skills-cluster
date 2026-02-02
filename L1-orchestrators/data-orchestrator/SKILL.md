---
name: data-orchestrator
description: >
  数据领域编排器。当数据相关的多步骤任务需要协调执行时触发。负责分解数据任务，
  协调 db-schema、code-gen（数据访问层）、test-gen（数据测试）等 skill 的执行，
  确保数据模型设计、实现和测试的一致性。支持顺序链和并行扇出模式。
---

# Data Orchestrator — 数据领域编排器

## 触发条件

由 Meta-Commander 路由触发，当任务满足以下条件时：
- 复杂度为 M 级
- 主要领域为 data
- 涉及数据库设计或数据处理

## 输入格式

```json
{
  "task_id": "...",
  "task_description": "...",
  "complexity": "M",
  "domains": ["data"],
  "context": {
    "database_type": "postgresql | mysql | mongodb | sqlite",
    "orm": "sqlalchemy | django-orm | prisma | none",
    "existing_schema": "path/to/schema.sql"
  }
}
```

## 编排模式

### 模式 1: Schema First（Schema 优先）

适用场景：新建数据模型

```
db-schema (设计 Schema)
    ↓
code-gen (生成 ORM 模型)
    ↓
code-gen (生成 Repository/DAO)
    ↓
test-gen (数据层测试)
```

### 模式 2: Migration（数据迁移）

适用场景：修改现有数据结构

```
db-schema (分析变更)
    ↓
code-gen (生成迁移脚本)
    ↓
code-gen (更新模型代码)
    ↓
test-gen (迁移测试)
```

### 模式 3: Parallel Processing（并行处理）

适用场景：多表/多模型独立设计

```
        ┌→ db-schema (表A) → code-gen (模型A) ─┐
需求分析 ┤→ db-schema (表B) → code-gen (模型B) ─┤→ 集成
        └→ db-schema (表C) → code-gen (模型C) ─┘
```

## 数据任务分解规则

参考 `references/data-patterns.md`：

| 任务类型 | 分解为 |
|---------|-------|
| 新建表/模型 | db-schema → code-gen (model) → test-gen |
| 修改表结构 | db-schema (diff) → code-gen (migration) → test-gen |
| 添加关联 | db-schema (FK) → code-gen (relations) → test-gen |
| 数据验证 | code-gen (validators) → test-gen |

## 质量门禁

参考 `references/quality-gates.md`：

### db-schema 门禁
- [ ] SQL 语法正确
- [ ] 主键定义存在
- [ ] 外键约束合理
- [ ] 索引设计合理

### 模型代码门禁
- [ ] 类型注解完整
- [ ] 关联关系正确
- [ ] 验证器存在

### 迁移脚本门禁
- [ ] 可逆（有 downgrade）
- [ ] 无数据丢失风险
- [ ] 版本号正确

## 输出结构

```json
{
  "task_id": "...",
  "status": "completed",
  "outputs": {
    "schema_files": ["path/to/schema.sql"],
    "model_files": ["path/to/models.py"],
    "migration_files": ["path/to/migration.py"],
    "test_files": ["path/to/test_models.py"]
  },
  "quality_scores": {
    "db-schema": 0.9,
    "code-gen": 0.85,
    "test-gen": 0.8
  }
}
```

## 数据库特定处理

### PostgreSQL
- 支持 JSONB 字段建议
- 支持数组类型
- 推荐使用 UUID 主键

### MySQL
- 注意字符集 (utf8mb4)
- 索引长度限制
- 外键约束名唯一

### MongoDB
- Schema 设计为 Collection 结构
- 嵌套文档 vs 引用建议
- 索引策略

## 与其他组件交互

- 调用 db-schema 设计数据结构
- 调用 code-gen 生成数据访问代码
- 调用 test-gen 生成数据测试
- 报告结果到 Meta-Commander
