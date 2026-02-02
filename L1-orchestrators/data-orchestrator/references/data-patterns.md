# 数据任务模式

## 模式分类

### 1. 新建模型 (Create Model)

**输入**: 数据需求描述
**输出**: Schema + 模型代码 + 测试

```
需求分析
    ↓
db-schema (设计表结构)
    ↓
code-gen (ORM 模型)
    ↓
code-gen (Repository 层)
    ↓
test-gen (单元测试)
```

**示例任务**: "创建用户表，包含用户名、邮箱、密码"

### 2. 修改模型 (Alter Model)

**输入**: 变更需求 + 现有 Schema
**输出**: 迁移脚本 + 更新后模型

```
分析现有 Schema
    ↓
db-schema (设计变更)
    ↓
code-gen (迁移脚本)
    ↓
code-gen (更新模型)
    ↓
test-gen (回归测试)
```

**示例任务**: "给用户表添加手机号字段"

### 3. 建立关联 (Add Relation)

**输入**: 关联需求
**输出**: 外键 + 关联代码

```
分析实体关系
    ↓
db-schema (设计外键)
    ↓
code-gen (关联属性)
    ↓
test-gen (关联测试)
```

**关联类型**:
- 一对一 (1:1)
- 一对多 (1:N)
- 多对多 (M:N)

### 4. 数据查询 (Query Design)

**输入**: 查询需求
**输出**: 查询方法 + 索引建议

```
分析查询模式
    ↓
db-schema (索引设计)
    ↓
code-gen (查询方法)
    ↓
test-gen (查询测试)
```

### 5. 数据验证 (Validation)

**输入**: 验证规则
**输出**: 验证器代码

```
code-gen (字段验证器)
    ↓
code-gen (模型验证器)
    ↓
test-gen (验证测试)
```

## 数据类型映射

### Python SQLAlchemy

| 概念类型 | SQLAlchemy 类型 |
|---------|----------------|
| 字符串 | String, Text |
| 整数 | Integer, BigInteger |
| 浮点数 | Float, Numeric |
| 布尔 | Boolean |
| 日期时间 | DateTime, Date |
| JSON | JSON, JSONB |
| UUID | UUID |

### TypeScript Prisma

| 概念类型 | Prisma 类型 |
|---------|------------|
| 字符串 | String |
| 整数 | Int, BigInt |
| 浮点数 | Float, Decimal |
| 布尔 | Boolean |
| 日期时间 | DateTime |
| JSON | Json |

## 常见模式

### 软删除

```python
class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
```

### 审计字段

```python
class AuditMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
```

### 乐观锁

```python
class VersionMixin:
    version = Column(Integer, default=1)
```

## 步骤间数据传递

| 从 | 到 | 传递内容 |
|----|----|---------|
| db-schema | code-gen (model) | DDL, 字段定义 |
| db-schema | code-gen (migration) | ALTER 语句 |
| code-gen (model) | code-gen (repo) | 模型类名, 字段 |
| code-gen (model) | test-gen | 模型类, 工厂 |
