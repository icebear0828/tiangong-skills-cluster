---
name: commit-orchestrator
description: >
  Smart Commit 编排器 (L1)。编排完整的智能提交流程：diff 分析→敏感检测→消息生成→格式校验。
  通过黑板模式管理流程状态，含两个质量关卡。由 git-commander 调度。
---

# Commit Orchestrator — Smart Commit 编排器

## 触发条件

- 由 `git-commander` 路由 commit/提交/暂存 类请求
- 蓝图: `smart_commit.json`

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["staged_diff"],
  "properties": {
    "staged_diff": {
      "type": "string",
      "description": "git diff --staged 输出"
    },
    "git_context": {
      "type": "object",
      "properties": {
        "current_branch": { "type": "string" },
        "staged_files": { "type": "array", "items": { "type": "string" } },
        "repo_root": { "type": "string" }
      }
    },
    "options": {
      "type": "object",
      "properties": {
        "dry_run": { "type": "boolean", "default": false },
        "auto_commit": { "type": "boolean", "default": false }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["status", "commit_message"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["committed", "pending_confirmation", "blocked", "error"]
    },
    "commit_message": {
      "type": "object",
      "properties": {
        "subject": { "type": "string" },
        "body": { "type": "string" },
        "type": { "type": "string" },
        "scope": { "type": "string" },
        "breaking_change": { "type": "boolean" }
      }
    },
    "safety_report": {
      "type": "object",
      "properties": {
        "sensitive_passed": { "type": "boolean" },
        "violations": { "type": "array", "items": { "type": "string" } }
      }
    },
    "format_validation": {
      "type": "object",
      "properties": {
        "valid": { "type": "boolean" },
        "errors": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

## 编排流程

```
git-commander → commit-orchestrator (蓝图: smart_commit.json)

  Step 1: diff-analyzer
    输入: git diff --staged
    输出: { files[], insertions, deletions, risk_level, summary, change_type }

  Step 2: 并行 {
    2a: sensitive-file-detector
        输入: staged file list + content patterns
        输出: { passed: bool, violations[], auto_fixable: bool }
    2b: conventional-commit-validator (分析历史 commit 模式)
        输入: git log --oneline -20
        输出: { project_conventions, suggested_scope, suggested_type }
  }

  ── 质量关卡 1: sensitive_check ──
  条件: sensitive-file-detector.passed == true
  失败: 阻止并报告违规文件，建议 .gitignore

  Step 3: commit-message-gen
    输入: diff-analyzer.output + validator.conventions
    输出: { subject, body, type, scope, breaking_change }

  ── 质量关卡 2: format_check ──
  条件: conventional-commit-validator(message) == valid
  失败: retry_from Step 3 (max 2 次)

  Step 4: 用户确认 → git commit -m "{message}"
```

## 黑板结构

```json
{
  "meta_zone": {
    "repo_root": "",
    "current_branch": "",
    "staged_files": []
  },
  "content_zone": {
    "diff_summary": null,
    "commit_message": null
  },
  "control_zone": {
    "sensitive_passed": false,
    "format_valid": false,
    "retries": 0,
    "max_retries": 2
  }
}
```

## 质量关卡

| 关卡 | 位置 | 检查 | 通过条件 | 失败处理 |
|------|------|------|---------|---------|
| sensitive_check | Step 2 后 | 敏感文件检测 | passed == true | 阻止，报告违规 |
| format_check | Step 3 后 | commit message 格式 | valid == true | 从 Step 3 重试 (max 2) |

## Skill 调用表

| Skill | 步骤 | 执行模式 | 必需 |
|-------|------|---------|------|
| diff-analyzer | Step 1 | 串行 | 是 |
| sensitive-file-detector | Step 2a | 并行 | 是 |
| conventional-commit-validator | Step 2b | 并行 | 是 |
| commit-message-gen | Step 3 | 串行 | 是 |
| conventional-commit-validator | 质量关卡 2 | 串行 | 是 |

## 错误处理

| 场景 | 处理 |
|------|------|
| 无 staged changes | 提示用户先 git add |
| 敏感文件检测失败 | 阻止提交，报告违规文件和修复建议 |
| 格式校验失败 (重试耗尽) | 返回部分结果，展示 message 和错误 |
| diff 分析失败 | 降级为手动输入 commit message |

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| git-commander | 被调用 | 接收路由 |
| diff-analyzer | 调用 | Step 1 |
| sensitive-file-detector | 调用 | Step 2a |
| conventional-commit-validator | 调用 | Step 2b + 质量关卡 |
| commit-message-gen | 调用 | Step 3 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 敏感检测 | commit/push 流程含敏感检查 | 100% |
| 格式合规 | 生成的 message 符合 Conventional Commits | ≥95% |
| 流程完整 | 所有步骤按序执行 | 100% |
| 重试成功率 | 格式校验重试后通过 | ≥80% |
