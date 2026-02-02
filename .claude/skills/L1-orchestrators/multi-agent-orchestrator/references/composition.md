# Skill 组合规则

## 概述

定义 Skills 之间的有效组合模式和约束。

## 兼容性矩阵

### 输出→输入兼容性

| 输出 Skill | 兼容的输入 Skill | 传递数据 |
|-----------|-----------------|---------|
| arch-explore | api-design, db-schema, code-gen | 架构描述, 约束 |
| api-design | code-gen, doc-gen | API 规范 |
| db-schema | code-gen | DDL, 字段定义 |
| code-gen | test-gen, code-review, doc-gen | 代码文件 |
| test-gen | code-review | 测试文件 |
| code-review | refactor, debug | 审查报告 |
| refactor | test-gen, code-review | 修改后代码 |
| debug | test-gen | 修复后代码 |
| prototype | code-gen, arch-explore | 原型代码 |

### 不兼容组合

以下组合通常不合理：

| 组合 | 原因 |
|-----|------|
| debug → arch-explore | 粒度不匹配 |
| doc-gen → code-gen | 顺序错误 |
| test-gen → db-schema | 无关联 |

## 组合模板

### 完整功能开发

```yaml
name: full-feature
skills:
  - arch-explore (optional)
  - api-design (if API)
  - db-schema (if data)
  - code-gen
  - test-gen
  - code-review
  - doc-gen (optional)
constraints:
  - api-design before code-gen
  - db-schema before code-gen
  - code-gen before test-gen
  - code-gen before doc-gen
```

### 质量修复

```yaml
name: quality-fix
skills:
  - code-review (分析问题)
  - refactor or debug (根据问题类型)
  - test-gen (验证修复)
  - code-review (确认改进)
constraints:
  - code-review first
  - refactor/debug sequential
  - final code-review
```

### 探索性开发

```yaml
name: exploration
skills:
  - arch-explore
  - prototype
  - code-review (评估)
  - code-gen (if prototype good)
constraints:
  - prototype after arch-explore
  - code-gen only if eval > threshold
```

## 参数传递规则

### 必传参数

| 从 | 到 | 必传参数 |
|----|----|---------|
| arch-explore | code-gen | architecture_context |
| api-design | code-gen | api_spec |
| db-schema | code-gen | schema_definition |
| code-gen | test-gen | code_files, function_signatures |
| code-review | refactor | review_report, issues |

### 可选参数

| 参数 | 说明 | 默认 |
|-----|------|-----|
| language | 编程语言 | 从 context 推断 |
| framework | 使用框架 | 从 context 推断 |
| style_guide | 代码风格 | 项目默认 |
| test_framework | 测试框架 | 语言默认 |

## 冲突检测

### 资源冲突

当多个 Skill 需要修改同一文件时：
1. 检测文件路径重叠
2. 如有冲突，改为顺序执行
3. 后执行的 Skill 需要处理 merge

### 语义冲突

当多个 Skill 输出可能矛盾时：
1. api-design 和 db-schema 的字段定义
2. 多个 code-gen 的函数命名
3. 解决方案：设置主导 Skill

## 动态组合

### 根据分析结果组合

```python
def compose_skills(analysis):
    skills = []

    if analysis.needs_design:
        skills.append("arch-explore")

    if analysis.has_api:
        skills.append("api-design")

    if analysis.has_database:
        skills.append("db-schema")

    skills.append("code-gen")

    if analysis.needs_test:
        skills.append("test-gen")

    skills.append("code-review")

    if analysis.needs_doc:
        skills.append("doc-gen")

    return skills
```

### 条件组合

```yaml
conditions:
  - if: complexity > M
    add: arch-explore
  - if: domains contains "data"
    add: db-schema
  - if: quality_score < 0.8
    add: refactor after code-review
```

## 组合验证

验证组合有效性的检查：

1. **依赖完整性**: 每个 Skill 的必需输入都有来源
2. **无循环**: 组合中无循环依赖
3. **可终止**: 有明确的终止条件
4. **资源充足**: Context 预算足够
5. **Skill 可用**: 所有 Skill 状态为 active
