---
name: pr-description-gen
description: >
  PR Description Generator. Auto-generates PR title and body from diff analysis and commit history.
  Produces summary, test plan, breaking changes. By pr-orchestrator in PR workflow.
---

# PR Description Generator — PR 描述生成器

> 详细文档: [_architecture/L2-execution/extended/pr-description-gen/SKILL.md](_architecture/L2-execution/extended/pr-description-gen/SKILL.md)

## 执行流程

### Step 1: 收集 Commits

从 `git log base...HEAD` 提取所有 commit subjects，归类变更类型和意图。

### Step 2: 分析 Diff

从 diff-analyzer 输出提取：变更文件、受影响模块、风险等级、破坏性变更标记。

### Step 3: 生成 Title

- ≤70 字符
- 使用祈使语气 ("Add", "Fix", "Update")
- 概括核心变更意图
- 格式: `<动词> <描述>`

### Step 4: 生成 Body

```markdown
## Summary
- <1-3 bullet points summarizing changes>

## Test plan
- [ ] <test item 1>
- [ ] <test item 2>

## Breaking changes (if any)
- <breaking change + migration guide>
```

### Step 5: 建议 Labels

| 变更类型 | Label |
|---------|-------|
| feature | `feature`, `enhancement` |
| fix | `bugfix` |
| refactor | `refactor` |
| docs | `documentation` |
| breaking | `breaking-change` |
| high risk | `needs-review` |

## 输出

- **title**: PR 标题 (≤70 chars)
- **body**: 结构化 markdown (summary + test plan + breaking changes)
- **labels**: 建议的 label 列表

## 用户任务

$ARGUMENTS
