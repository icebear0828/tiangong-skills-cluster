---
name: git-commander
description: >
  Git 域总指挥。Git 管理和代码审查的第一入口点。分析 git 任务，路由到对应工作流。
  覆盖 Smart Commit、PR Review、Branch Management、Release 四大工作流。
---

# Git Commander — Git 域总指挥

> 详细文档: [_architecture/L0-git-commander/SKILL.md](_architecture/L0-git-commander/SKILL.md)

## 执行流程

收到 git 任务后，按以下步骤执行：

### Step 1: 收集 Git 上下文

```bash
git status                    # 工作区状态
git branch --show-current     # 当前分支
git diff --staged --stat      # 暂存变更概览
git describe --tags --abbrev=0 2>/dev/null  # 最近 tag
```

### Step 2: 意图解析

从用户输入中识别：
- **操作类型**: commit / pr / branch / release
- **复杂度**: S (单一工具) / M (完整工作流) / L (跨工作流)

### Step 3: 路由执行

**S 级 (简单)**: 直接调用对应 L2 skill
- "写 commit message" → `/commit-message-gen`
- "分析 diff" → `/diff-analyzer`
- "检查敏感文件" → `/sensitive-file-detector`
- "校验分支" → `/branch-validator`
- "检查 commit 格式" → `/conventional-commit-validator`

**M 级 (完整工作流)**: 调用对应 L1 编排器

| 操作 | 编排器 | 蓝图 |
|------|--------|------|
| commit/提交 | commit-orchestrator | `smart_commit.json` |
| pr/审查 | pr-orchestrator | `pr_review.json` |
| branch/分支 | branch-orchestrator | `branch_management.json` |
| release/发版 | release-orchestrator | `release.json` |

### Step 4: 安全检查

所有涉及 commit/push 的操作自动包含：
- `sensitive-file-detector` 敏感文件检查
- 破坏性操作（force push, branch delete, reset）必须用户确认

### Step 5: 执行与输出

**Smart Commit** (`/git-commander commit`):
1. 分析 staged diff
2. 检查敏感文件 + 分析历史惯例（并行）
3. 生成 Conventional Commits 消息
4. 校验格式
5. 用户确认 → `git commit`

**PR Review** (`/git-commander pr|review`):
- 创建: 分析 diff → 生成 PR 描述 → `gh pr create`
- 审查: 分析 diff → `code-review` → 发布评论
- 质量关卡: review_score ≥ 0.7

**Branch Management** (`/git-commander branch`):
1. 分支命名/过期/冲突检查
2. 冲突解决建议（如有）
3. 提交历史健康报告

**Release** (`/git-commander release`):
1. 计算语义化版本号
2. 生成 CHANGELOG.md
3. 生成 Release Notes
4. 用户确认 → `git commit` + `git tag` + `git push`

## 安全保护

| 操作 | 保护 |
|------|------|
| `git push --force` | **必须确认** + 显示影响范围 |
| `git branch -D` | **必须确认** |
| `git reset --hard` | **必须确认** + 建议备份 |
| commit/push | 自动敏感文件检测 |

## 用户任务

$ARGUMENTS

---

请分析 git 任务，收集仓库上下文，按上述流程执行。对破坏性操作必须请求用户确认。
