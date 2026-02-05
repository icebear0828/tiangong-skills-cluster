---
name: commit-message-gen
description: >
  Commit Message 生成器 (L2 Core)。基于 diff 分析结果生成 Conventional Commits 格式的提交信息。
  自动推断 type、scope、breaking change，生成清晰的 subject 和 body。
  由 commit-orchestrator 在 Smart Commit Step 3 调度。
---

# Commit Message Generator — 提交信息生成器

## 触发条件

- 由 `commit-orchestrator` 在 Smart Commit Step 3 调度
- 由 `git-commander` 直接路由（S 级 "写 commit message" 请求）

## 核心能力

1. **类型推断**: 从 diff 分析推断 feat/fix/docs/refactor/test/chore/ci 类型
2. **Scope 推断**: 从变更文件路径推断影响的模块/包
3. **Subject 生成**: 生成 ≤72 字符的简洁描述
4. **Body 生成**: 为 feat/fix 类型生成详细说明
5. **Breaking Change 标注**: 检测并标注破坏性变更

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["diff_analysis"],
  "properties": {
    "diff_analysis": {
      "type": "object",
      "description": "diff-analyzer 的输出结果",
      "properties": {
        "files": { "type": "array" },
        "summary": { "type": "object" },
        "risk_level": { "type": "string" },
        "change_type": { "type": "string" },
        "affected_modules": { "type": "array" },
        "breaking_changes": { "type": "boolean" }
      }
    },
    "project_conventions": {
      "type": "object",
      "description": "conventional-commit-validator 分析的项目惯例（可选）",
      "properties": {
        "suggested_type": { "type": "string" },
        "suggested_scope": { "type": "string" },
        "common_patterns": { "type": "array", "items": { "type": "string" } }
      }
    },
    "language": {
      "type": "string",
      "enum": ["en", "zh"],
      "default": "en",
      "description": "commit message 语言"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["subject", "type", "scope"],
  "properties": {
    "subject": {
      "type": "string",
      "maxLength": 72,
      "description": "commit 标题行"
    },
    "body": {
      "type": "string",
      "description": "commit 详细描述（feat/fix 必填）"
    },
    "type": {
      "type": "string",
      "enum": ["feat", "fix", "docs", "style", "refactor", "test", "chore", "ci"],
      "description": "变更类型"
    },
    "scope": {
      "type": "string",
      "description": "影响范围"
    },
    "breaking_change": {
      "type": "boolean",
      "description": "是否为破坏性变更"
    },
    "breaking_change_description": {
      "type": "string",
      "description": "破坏性变更说明"
    },
    "full_message": {
      "type": "string",
      "description": "完整的 commit message（直接可用）"
    }
  }
}
```

## 执行流程

### Step 1: 类型推断

```
从 diff_analysis.change_type 映射:
    feature → feat
    fix → fix
    refactor → refactor
    docs → docs
    test → test
    config → chore
    mixed → 按主要变更类型判定
```

### Step 2: Scope 推断

```
从 diff_analysis.affected_modules 推断:
    单模块 → scope = 模块名
    多模块有公共父 → scope = 公共父目录
    无公共父 → scope = 最主要模块
```

### Step 3: Subject 生成

遵循规则:
- 使用祈使语气 ("Add", "Fix", "Update", 不用 "Added", "Fixed")
- 首字母小写 (type 后的描述)
- 不以句号结尾
- ≤72 字符
- 概括核心变更

### Step 4: Body 生成

为 feat/fix 类型生成:
- **What**: 做了什么变更
- **Why**: 为什么需要这个变更
- **Impact**: 影响了哪些功能

### Step 5: 组装完整消息

```
<type>(<scope>): <subject>

<body>

BREAKING CHANGE: <description>  (仅当 breaking_change=true)
```

## Conventional Commits 格式参考

```
feat(auth): add OAuth2 login support

Implement Google and GitHub OAuth2 authentication.
Users can now sign in with their existing accounts.

- Add OAuth2 callback handlers
- Add provider configuration
- Update user model with provider fields

BREAKING CHANGE: User.login field renamed to User.email
```

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| commit-orchestrator | 被调用 | Smart Commit Step 3 |
| diff-analyzer | 上游数据源 | 提供变更分析 |
| conventional-commit-validator | 消费者 | 验证生成的 message 格式 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 类型准确 | type 与实际变更一致 | ≥95% |
| Subject 长度 | ≤72 字符 | 100% |
| 格式合规 | 符合 Conventional Commits | 100% |
| Body 完整 | feat/fix 包含 what/why | ≥90% |
