---
name: db-schema
description: >
  数据库 Schema 设计 Skill。设计数据库表结构和关系。当需要：(1) 设计新数据模型，
  (2) 优化现有 Schema，(3) 生成迁移脚本时触发。支持关系型和文档型数据库。
  输出 DDL 语句或 ORM 模型定义。作为扩展 Skill，具有标准契约。
---

# DB Schema — 数据库设计

## 触发条件

- 需求涉及数据存储
- 由 data-orchestrator 调度
- 新功能需要新表/字段

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["requirements"],
  "properties": {
    "requirements": {
      "type": "string",
      "description": "数据需求描述"
    },
    "database_type": {
      "type": "string",
      "enum": ["postgresql", "mysql", "sqlite", "mongodb"],
      "default": "postgresql"
    },
    "existing_schema": {
      "type": "string",
      "description": "现有 Schema（如需扩展）"
    },
    "orm": {
      "type": "string",
      "enum": ["sqlalchemy", "django", "prisma", "none"]
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["schema"],
  "properties": {
    "schema": {
      "type": "object",
      "properties": {
        "ddl": { "type": "string" },
        "orm_models": { "type": "string" }
      }
    },
    "tables": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "columns": { "type": "array" },
          "indexes": { "type": "array" },
          "constraints": { "type": "array" }
        }
      }
    },
    "migrations": {
      "type": "array"
    },
    "erd": {
      "type": "string",
      "description": "Mermaid ERD 图"
    }
  }
}
```

## 设计原则

参考 `references/schema-patterns.md`：

### 规范化
- 消除冗余
- 确保数据一致性
- 适当反规范化（性能）

### 命名规范
- 表名：复数小写下划线
- 字段：小写下划线
- 主键：id
- 外键：关联表_id

### 常用字段
- id (主键)
- created_at
- updated_at
- deleted_at (软删除)

## 脚本

- `scripts/design_schema.py` - Schema 设计脚本
