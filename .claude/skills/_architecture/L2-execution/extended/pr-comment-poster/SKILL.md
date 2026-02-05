---
name: pr-comment-poster
description: >
  PR Comment Poster (L2 Extended). Formats review findings and posts as PR comments via gh api.
  Supports idempotent posting: queries existing comments before creating or updating.
  Called by pr-orchestrator in PR Review flow. Standard contract.
---

# PR Comment Poster — PR 评论发布器

## 触发条件

- 由 `pr-orchestrator` 在 PR Review 流程 Step 4 调度
- 需要将 code-review 结果发布到 PR 评论时

## 核心能力

1. **Findings 格式化**: 将 code-review 结构化结果转换为 Markdown 评论
2. **幂等发布**: 查询已有评论，更新而非重复创建
3. **Inline 评论**: 支持在特定文件行号发布 inline review comments
4. **Summary 评论**: 发布汇总评论到 PR conversation

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["review_findings", "pr_number", "repo"],
  "properties": {
    "review_findings": {
      "type": "object",
      "description": "code-review 的输出结果",
      "properties": {
        "issues": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "severity": { "type": "string", "enum": ["critical", "major", "minor", "suggestion"] },
              "category": { "type": "string" },
              "line_number": { "type": "integer" },
              "file_path": { "type": "string" },
              "code_snippet": { "type": "string" },
              "description": { "type": "string" },
              "suggestion": { "type": "string" }
            }
          }
        },
        "summary": {
          "type": "object",
          "properties": {
            "total_issues": { "type": "integer" },
            "critical_count": { "type": "integer" },
            "quality_score": { "type": "number" }
          }
        },
        "recommendations": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "pr_number": {
      "type": "integer",
      "description": "PR 编号"
    },
    "repo": {
      "type": "object",
      "required": ["owner", "name"],
      "properties": {
        "owner": { "type": "string", "description": "仓库 owner" },
        "name": { "type": "string", "description": "仓库名" }
      },
      "description": "仓库信息"
    },
    "comment_mode": {
      "type": "string",
      "enum": ["summary_only", "inline_only", "both"],
      "default": "both",
      "description": "评论模式：仅汇总 / 仅 inline / 两者"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["success", "posted_count"],
  "properties": {
    "success": {
      "type": "boolean",
      "description": "发布是否成功"
    },
    "posted_count": {
      "type": "integer",
      "description": "成功发布的评论数"
    },
    "comment_url": {
      "type": "string",
      "description": "汇总评论的 URL"
    },
    "inline_comments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file": { "type": "string" },
          "line": { "type": "integer" },
          "url": { "type": "string" }
        }
      },
      "description": "已发布的 inline 评论列表"
    },
    "errors": {
      "type": "array",
      "items": { "type": "string" },
      "description": "发布失败的错误信息"
    }
  }
}
```

## 执行流程

### Step 1: 查询已有评论（幂等性保障）

```
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
gh api repos/{owner}/{repo}/issues/{pr_number}/comments
    │
    ├─ 过滤 bot/自动化 评论
    ├─ 检查是否存在本工具的标记 (<!-- tiangong-review -->)
    └─ 存在 → 更新模式；不存在 → 创建模式
```

### Step 2: 格式化 Summary 评论

```markdown
<!-- tiangong-review -->
## Code Review Summary

**Quality Score**: {quality_score}/1.0
**Issues Found**: {total_issues} ({critical_count} critical)

### Critical Issues
| # | File | Line | Description |
|---|------|------|-------------|
| 1 | path/to/file | 42 | Description... |

### Recommendations
- recommendation 1
- recommendation 2

---
*Automated review by TianGong Skills*
```

### Step 3: 格式化 Inline 评论

对每个有 `file_path` 和 `line_number` 的 issue 生成 inline comment:

```markdown
**{severity}**: {description}

> Suggestion: {suggestion}
```

### Step 4: 发布评论

```
创建模式:
    gh api repos/{owner}/{repo}/issues/{pr_number}/comments \
      -f body="{summary_markdown}"

更新模式:
    gh api repos/{owner}/{repo}/issues/comments/{comment_id} \
      -X PATCH -f body="{summary_markdown}"

Inline 评论:
    gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
      -f body="{inline_markdown}" \
      -f path="{file_path}" \
      -f line={line_number} \
      -f commit_id="{head_sha}"
```

### Step 5: 验证发布结果

- 确认每个评论的 HTTP 状态码为 200/201
- 收集所有评论 URL
- 统计成功/失败数量

## 幂等性机制

| 场景 | 处理 |
|------|------|
| 首次运行 | 创建新 summary comment + inline comments |
| 重复运行 | 检测 `<!-- tiangong-review -->` 标记，更新已有 comment |
| 部分失败 | 记录失败项，返回 partial success |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 幂等性 | 重复运行不产生重复评论 | 100% |
| 格式正确 | Markdown 渲染正常 | 100% |
| 完整性 | 所有 findings 都被发布 | ≥95% |
| 错误处理 | 失败时有明确错误信息 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| pr-orchestrator | 被调用 | PR Review Step 4 |
| code-review | 上游数据源 | 提供 review findings |
| diff-analyzer | 间接上游 | 通过 code-review 传递变更上下文 |
