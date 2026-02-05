---
name: pr-orchestrator
description: >
  PR Review 编排器 (L1)。编排完整的 PR 工作流：支持 Create 和 Review 两种子流程。
  Create: diff 分析→PR 描述生成→gh pr create。Review: diff 分析→代码审查→评论发布。
  通过黑板模式管理流程状态，含质量关卡。由 git-commander 调度。
---

# PR Orchestrator — PR Review 编排器

## 触发条件

- 由 `git-commander` 路由 PR/review/pull request 类请求
- 蓝图: `pr_review.json`

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["sub_flow"],
  "properties": {
    "sub_flow": {
      "type": "string",
      "enum": ["create", "review", "create_and_review"],
      "description": "子流程：创建 / 审查 / 创建+审查"
    },
    "pr_number": {
      "type": "integer",
      "description": "PR 编号（review 模式必需）"
    },
    "base_branch": {
      "type": "string",
      "default": "main",
      "description": "目标分支"
    },
    "repo": {
      "type": "object",
      "properties": {
        "owner": { "type": "string" },
        "name": { "type": "string" }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["status"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["pr_created", "review_posted", "review_blocked", "error"]
    },
    "pr_url": { "type": "string", "description": "创建的 PR URL" },
    "pr_description": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "body": { "type": "string" },
        "labels": { "type": "array", "items": { "type": "string" } }
      }
    },
    "review_result": {
      "type": "object",
      "properties": {
        "score": { "type": "number" },
        "passed": { "type": "boolean" },
        "issues": { "type": "array", "items": { "type": "object" } },
        "comment_url": { "type": "string" }
      }
    }
  }
}
```

## 编排流程

```
git-commander → pr-orchestrator (蓝图: pr_review.json)

  ┌─────────────────── Sub-flow: Create ───────────────────┐
  │                                                         │
  │  Step 1: diff-analyzer                                  │
  │    输入: git diff base...HEAD                           │
  │    输出: { files[], summary, risk_level, change_type }  │
  │                                                         │
  │  Step 2: pr-description-gen                             │
  │    输入: diff_analysis + commit_history + pr_template   │
  │    输出: { title, body, labels }                        │
  │                                                         │
  │  Step 3: gh pr create                                   │
  │    输入: title + body + labels                          │
  │    输出: PR URL                                         │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────── Sub-flow: Review ───────────────────┐
  │                                                         │
  │  Step 1: diff-analyzer                                  │
  │    输入: git diff base...HEAD (PR diff)                 │
  │    输出: { files[], summary, risk_level, change_type }  │
  │                                                         │
  │  Step 2: code-review                                    │
  │    输入: diff content + diff_analysis context           │
  │    输出: { issues[], summary, recommendations }         │
  │                                                         │
  │  ── 质量关卡: review_score ──                           │
  │  条件: code-review.summary.quality_score ≥ 0.7          │
  │  失败: 列出 blocking issues，建议修复后重新提交          │
  │                                                         │
  │  Step 3: pr-description-gen                             │
  │    输入: diff_analysis + commit_history                 │
  │    输出: { title, body, labels }                        │
  │                                                         │
  │  Step 4: pr-comment-poster                              │
  │    输入: review_findings + pr_number + repo             │
  │    输出: { comment_url, posted_count }                  │
  └─────────────────────────────────────────────────────────┘
```

## 黑板结构

```json
{
  "meta_zone": {
    "pr_number": null,
    "base_branch": "",
    "head_branch": "",
    "repo_owner": "",
    "repo_name": ""
  },
  "content_zone": {
    "diff_summary": null,
    "review_findings": null,
    "pr_description": null,
    "commit_history": null
  },
  "control_zone": {
    "review_score": 0,
    "review_passed": false,
    "sub_flow": "review",
    "comments_posted": false
  }
}
```

## 质量关卡

| 关卡 | 位置 | 检查 | 通过条件 | 失败处理 |
|------|------|------|---------|---------|
| review_score | Step 2 后 (Review flow) | 代码质量分数 | quality_score ≥ 0.7 | 列出 blocking issues，建议修复 |

## Skill 调用表

| Skill | 子流程 | 步骤 | 执行模式 | 必需 |
|-------|--------|------|---------|------|
| diff-analyzer | Create / Review | Step 1 | 串行 | 是 |
| pr-description-gen | Create | Step 2 | 串行 | 是 |
| pr-description-gen | Review | Step 3 | 串行 | 是 |
| code-review | Review | Step 2 | 串行 | 是 |
| pr-comment-poster | Review | Step 4 | 串行 | 是 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 审查覆盖 | 所有文件变更被审查 | 100% |
| 质量关卡 | review_score 达标才允许通过 | score ≥ 0.7 |
| 评论幂等 | 重复审查不产生重复评论 | 100% |
| PR 描述完整 | 包含 summary + test plan + breaking changes | ≥95% |

## 子流程选择

| 用户意图 | 子流程 | 说明 |
|---------|--------|------|
| "创建 PR" / "写 PR 描述" | Create | 生成 PR 标题和描述 |
| "审查 PR" / "review PR #123" | Review | 审查代码并发布评论 |
| "PR 全流程" | Create + Review | 先创建 PR，再自审 |

## 错误处理

| 场景 | 处理 |
|------|------|
| 无 diff (分支相同) | 提示无变更，终止流程 |
| review_score < 0.7 | 输出 blocking issues，建议修复 |
| gh api 调用失败 | 重试 1 次，失败后返回本地结果 |
| PR template 不存在 | 使用默认模板 |

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| git-commander | 被调用 | 接收路由 |
| diff-analyzer | 调用 | Step 1 (两种子流程) |
| code-review | 调用 | Review Step 2 |
| pr-description-gen | 调用 | Create Step 2 / Review Step 3 |
| pr-comment-poster | 调用 | Review Step 4 |
