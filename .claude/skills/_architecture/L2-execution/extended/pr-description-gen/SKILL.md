---
name: pr-description-gen
description: >
  PR Description Generator (L2 Extended). Auto-generates PR title and body from diff analysis and commit history.
  Produces structured PR descriptions with summary, test plan, and breaking changes sections.
  Called by pr-orchestrator in PR Create/Review flows. Standard contract.
---

# PR Description Generator — PR 描述生成器

## 触发条件

- 由 `pr-orchestrator` 在 PR Create 流程 Step 3 调度
- 由 `pr-orchestrator` 在 PR Review 流程 Step 3 调度
- 由 `git-commander` 直接路由（S 级 "生成 PR 描述" 请求）

## 核心能力

1. **Commit 聚合**: 从 commit history 提取变更意图和范围
2. **Title 生成**: 生成 ≤70 字符的简洁 PR 标题
3. **Body 生成**: 生成结构化 PR body（summary + test plan + breaking changes）
4. **Label 建议**: 基于变更类型和风险等级建议 PR labels
5. **Template 适配**: 适配项目 PR template（如有）

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["diff_analysis", "commit_history"],
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
    "commit_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "hash": { "type": "string" },
          "subject": { "type": "string" },
          "body": { "type": "string" },
          "author": { "type": "string" },
          "date": { "type": "string" }
        }
      },
      "description": "分支上的 commit 列表（git log base...HEAD）"
    },
    "pr_template": {
      "type": "string",
      "description": "项目 PR template 内容（来自 .github/PULL_REQUEST_TEMPLATE.md，可选）"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["title", "body", "labels"],
  "properties": {
    "title": {
      "type": "string",
      "maxLength": 70,
      "description": "PR 标题，≤70 字符"
    },
    "body": {
      "type": "object",
      "required": ["summary", "test_plan"],
      "properties": {
        "summary": {
          "type": "string",
          "description": "变更摘要，1-3 个要点"
        },
        "test_plan": {
          "type": "string",
          "description": "测试计划，Markdown checklist 格式"
        },
        "breaking_changes": {
          "type": "string",
          "description": "破坏性变更说明（仅当存在时）"
        }
      },
      "description": "PR body 结构化内容"
    },
    "labels": {
      "type": "array",
      "items": { "type": "string" },
      "description": "建议的 PR labels（如 feature, bugfix, breaking-change, docs）"
    },
    "full_body_markdown": {
      "type": "string",
      "description": "完整的 PR body markdown（直接可用于 gh pr create --body）"
    }
  }
}
```

## 执行流程

### Step 1: 收集 Commit 信息

```
git log base...HEAD --oneline
    │
    ├─ 提取所有 commit subjects
    ├─ 归类 commit 类型 (feat/fix/refactor/docs/test)
    └─ 识别主要变更意图
```

### Step 2: 分析 Diff 上下文

```
从 diff_analysis 提取:
    │
    ├─ 变更文件数和范围
    ├─ 受影响模块
    ├─ 风险等级
    └─ 破坏性变更标记
```

### Step 3: 生成 Title

规则:
- ≤70 字符
- 概括核心变更意图
- 使用祈使语气 ("Add", "Fix", "Update")
- 不含 PR 编号或分支名
- 格式: `<动词> <描述>` 或 `<type>: <描述>`

### Step 4: 生成 Body

```
## Summary
- <bullet point 1: what changed>
- <bullet point 2: why>
- <bullet point 3: impact (optional)>

## Test plan
- [ ] <test item 1>
- [ ] <test item 2>
- [ ] <test item 3>

## Breaking changes (仅当有时)
- <breaking change description>
- <migration guide>
```

### Step 5: 建议 Labels

| 变更类型 | 建议 Label |
|---------|-----------|
| feature | `feature`, `enhancement` |
| fix | `bugfix`, `fix` |
| refactor | `refactor` |
| docs | `docs`, `documentation` |
| breaking_changes=true | `breaking-change` |
| risk_level=high/critical | `needs-review` |
| test | `test` |

### Step 6: Template 适配

如果提供了 `pr_template`，将生成的内容填充到 template 对应位置。

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| Title 长度 | ≤70 字符 | 100% |
| Summary 准确性 | 准确反映变更内容 | ≥90% |
| Test Plan 完整性 | 覆盖主要变更点 | ≥85% |
| Breaking Changes | 正确识别并标注 | 100% |
| Label 准确性 | 与变更类型匹配 | ≥90% |

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| pr-orchestrator | 被调用 | PR Create/Review Step 3 |
| diff-analyzer | 上游数据源 | 提供结构化的变更分析 |
| code-review | 下游协作 | Review 流程中 review 结果可补充 PR 描述 |
