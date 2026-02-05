---
name: pr-comment-poster
description: >
  PR Comment Poster. Formats review findings and posts as PR comments via gh api.
  Idempotent: checks existing comments before posting. By pr-orchestrator in PR Review flow.
---

# PR Comment Poster — PR 评论发布器

> 详细文档: [_architecture/L2-execution/extended/pr-comment-poster/SKILL.md](_architecture/L2-execution/extended/pr-comment-poster/SKILL.md)

## 执行流程

### Step 1: 查询已有评论

通过 `gh api repos/{owner}/{repo}/issues/{pr_number}/comments` 查询是否已存在本工具的评论（检测 `<!-- tiangong-review -->` 标记）。存在则进入更新模式，否则创建模式。

### Step 2: 格式化 Summary 评论

将 review findings 格式化为 Markdown 评论：
- Quality Score + Issue 统计
- Critical Issues 表格
- Recommendations 列表

### Step 3: 格式化 Inline 评论

对有 `file_path` + `line_number` 的 issue 生成 inline review comment，包含 severity、description、suggestion。

### Step 4: 发布评论

- **创建模式**: `gh api repos/{owner}/{repo}/issues/{pr_number}/comments -f body=...`
- **更新模式**: `gh api repos/{owner}/{repo}/issues/comments/{id} -X PATCH -f body=...`
- **Inline**: `gh api repos/{owner}/{repo}/pulls/{pr_number}/comments -f body=... -f path=... -f line=...`

### Step 5: 验证发布结果

确认 HTTP 200/201，收集 comment URLs，统计 posted_count。

## 幂等性

| 场景 | 处理 |
|------|------|
| 首次运行 | 创建新评论 |
| 重复运行 | 更新已有评论 |
| 部分失败 | 返回 partial success + errors |

## 输出

- **success**: 是否成功
- **posted_count**: 发布的评论数
- **comment_url**: 汇总评论 URL

## 用户任务

$ARGUMENTS
