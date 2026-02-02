# 数据质量门禁

## 门禁定义

### db-schema 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| SQL 语法正确 | BLOCKER | 尝试解析 SQL |
| 主键存在 | CRITICAL | 检查 PRIMARY KEY |
| 字段类型合理 | CRITICAL | 检查类型匹配 |
| 命名规范 | MAJOR | 检查命名风格 |
| 外键约束 | MAJOR | 检查 FOREIGN KEY |
| 索引设计 | MINOR | 检查常用查询字段 |

**通过标准**: 无 BLOCKER，CRITICAL = 0

### code-gen (model) 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 代码可解析 | BLOCKER | 尝试 import |
| 与 Schema 一致 | CRITICAL | 对比字段 |
| 类型注解完整 | MAJOR | 检查 type hints |
| 关联正确 | MAJOR | 检查 relationship |
| 验证器存在 | MINOR | 检查 validator |

### code-gen (migration) 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 可正向执行 | BLOCKER | 语法检查 upgrade |
| 可逆执行 | CRITICAL | 语法检查 downgrade |
| 无数据丢失 | CRITICAL | 检查 DROP 语句 |
| 版本号唯一 | MAJOR | 检查版本号 |

### test-gen 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 测试可运行 | BLOCKER | 尝试解析 |
| 覆盖 CRUD | CRITICAL | 检查测试方法 |
| 使用 fixture | MAJOR | 检查测试隔离 |
| 边界测试 | MINOR | 检查 NULL/空 |

## 评分维度

### Schema 设计质量

```
schema_quality =
    0.3 * normalization_score +
    0.3 * index_score +
    0.2 * constraint_score +
    0.2 * naming_score
```

### 模型代码质量

```
model_quality =
    0.4 * consistency_score +
    0.3 * completeness_score +
    0.2 * type_safety_score +
    0.1 * style_score
```

## 数据安全检查

| 检查项 | 规则 |
|-------|------|
| 敏感字段 | password, token 等需加密 |
| 个人信息 | 需要加密或脱敏 |
| SQL 注入 | 不得拼接 SQL |
| 权限控制 | 检查访问控制 |

## 性能检查

| 检查项 | 阈值 |
|-------|------|
| 表字段数 | ≤ 30 |
| 索引数 | ≤ 10 |
| 外键深度 | ≤ 3 |
| JSON 字段 | 考虑索引需求 |
