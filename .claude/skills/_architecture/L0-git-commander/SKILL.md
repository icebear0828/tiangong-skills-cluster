---
name: git-commander
description: >
  Git 域总指挥 Skill (L0)。Git 管理和代码审查任务的第一入口点，负责意图解析、复杂度判定、
  路由到对应编排器或直连 L2 Skill。覆盖 4 大工作流：Smart Commit、PR Review、
  Branch Management、Changelog + Version。作为 L0 层 Skill，具有严格契约。
---

# Git Commander — Git 域总指挥

## 触发条件

- 用户任务包含 "commit"、"提交"、"pr"、"pull request"、"审查"、"branch"、"分支"、"release"、"发版"、"changelog" 等关键词
- 由 meta-commander 路由到 git 域
- 需要 git 操作管理时

## 蓝图选择机制

Git Commander 作为意图路由器，根据用户输入选择最合适的工作流：

```
用户输入 → Git Commander
              │
              ├─ 识别操作类型 + 复杂度
              │
              ▼
        ┌─────────────────────────────────────────────────┐
        │ 路由决策树                                        │
        │                                                 │
        │ commit/提交/暂存     → commit-orchestrator       │
        │ pr/pull request/审查  → pr-orchestrator          │
        │ branch/分支/清理/过期 → branch-orchestrator       │
        │ release/发版/changelog → release-orchestrator    │
        │                                                 │
        │ "写 commit message"  → commit-message-gen (直连) │
        │ "分析 diff"          → diff-analyzer (直连)      │
        │ "检查敏感文件"        → sensitive-file-detector   │
        │ "校验分支"           → branch-validator (直连)   │
        │ "检查 commit 格式"   → conventional-commit-validator │
        └─────────────────────────────────────────────────┘
```

### 蓝图映射规则

| 用户意图 | 工作流 | 推荐蓝图 | 预估 Token |
|---------|--------|---------|-----------|
| 智能提交 | Smart Commit | smart_commit | ~1500 |
| PR 创建/审查 | PR Review | pr_review | ~2000 |
| 分支管理/清理 | Branch Management | branch_management | ~1500 |
| 发版/Changelog | Release | release | ~1800 |
| 单一简单操作 | 直连 L2 | 无 | <500 |

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["task_description"],
  "properties": {
    "task_description": {
      "type": "string",
      "description": "Git 任务描述"
    },
    "git_context": {
      "type": "object",
      "properties": {
        "current_branch": { "type": "string", "description": "当前分支" },
        "has_staged_changes": { "type": "boolean", "description": "是否有暂存变更" },
        "has_unstaged_changes": { "type": "boolean", "description": "是否有未暂存变更" },
        "remote_url": { "type": "string", "description": "远程仓库 URL" },
        "last_tag": { "type": "string", "description": "最近的 tag" }
      },
      "description": "Git 仓库上下文信息"
    },
    "action": {
      "type": "string",
      "enum": ["commit", "pr", "review", "branch", "release", "auto"],
      "default": "auto",
      "description": "指定操作（auto 则自动检测意图）"
    },
    "options": {
      "type": "object",
      "properties": {
        "dry_run": { "type": "boolean", "default": false },
        "force": { "type": "boolean", "default": false },
        "interactive": { "type": "boolean", "default": true }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["task_analysis", "routing_decision"],
  "properties": {
    "task_analysis": {
      "type": "object",
      "properties": {
        "complexity": {
          "type": "string",
          "enum": ["S", "M", "L", "XL"],
          "description": "任务复杂度"
        },
        "task_type": {
          "type": "string",
          "enum": ["commit", "pr_create", "pr_review", "branch_check", "branch_cleanup", "release", "single_tool"],
          "description": "任务类型"
        },
        "skills_required": {
          "type": "array",
          "items": { "type": "string" },
          "description": "需要的 skill 列表"
        }
      },
      "description": "任务分析"
    },
    "routing_decision": {
      "type": "object",
      "properties": {
        "route_type": {
          "type": "string",
          "enum": ["direct_l2", "orchestrator"],
          "description": "路由类型"
        },
        "target": { "type": "string", "description": "目标 skill/orchestrator" },
        "blueprint_id": { "type": "string", "description": "蓝图 ID（如果走编排器）" },
        "rationale": { "type": "string", "description": "路由理由" }
      },
      "description": "路由决策"
    },
    "execution_result": {
      "type": "object",
      "description": "执行结果（如果直连 L2）或编排结果"
    },
    "safety_warnings": {
      "type": "array",
      "items": { "type": "string" },
      "description": "安全警告（破坏性操作提醒）"
    }
  }
}
```

## 复杂度判定

| 复杂度 | 条件 | 路由目标 |
|--------|------|---------|
| S | 单一工具操作（写 message / 分析 diff / 检查文件） | 直接 L2 skill |
| M | 完整工作流（smart commit / PR 创建 / 分支检查） | 对应 L1 编排器 |
| L | 跨工作流（commit + PR 创建 + review） | 多编排器串行 |
| XL | 完整发布流程（version + changelog + tag + release notes） | release-orchestrator |

## 四大工作流

### 1. Smart Commit (`/git-commander commit`)

```
Step 1: diff-analyzer (分析暂存变更)
Step 2: 并行 { sensitive-file-detector + conventional-commit-validator }
Gate 1: 敏感文件通过
Step 3: commit-message-gen
Gate 2: 格式校验通过
Step 4: 用户确认 → git commit
```

### 2. PR Review (`/git-commander pr|review`)

```
创建: diff-analyzer → pr-description-gen → gh pr create
审查: diff-analyzer → code-review → pr-comment-poster
Gate: review_score ≥ 0.7
```

### 3. Branch Management (`/git-commander branch`)

```
Step 1: branch-validator (命名/过期/冲突检查)
Step 2: conflict-resolver (仅当有冲突)
Step 3: commit-history-analyzer (健康报告)
```

### 4. Release (`/git-commander release`)

```
Step 1: version-bumper (计算版本号)
Gate: version sanity check
Step 2: changelog-gen (生成 CHANGELOG)
Step 3: release-notes-gen (生成 Release Notes)
Step 4: 用户确认 → git commit + git tag + git push
⚠️ 破坏性操作必须用户确认
```

## 路由规则

```
输入 → 意图解析 → 路由

| 关键词                    | 路由                          | 模式      |
|--------------------------|------------------------------|-----------|
| commit, 提交, 暂存        | commit-orchestrator          | L1 编排   |
| pr, pull request, 审查    | pr-orchestrator              | L1 编排   |
| branch, 分支, 清理, 过期  | branch-orchestrator          | L1 编排   |
| release, 发版, changelog  | release-orchestrator         | L1 编排   |
| "写 commit message"      | commit-message-gen           | 直连 L2   |
| "分析 diff"              | diff-analyzer                | 直连 L2   |
| "检查敏感文件"            | sensitive-file-detector      | 直连 L2   |
| "校验分支"               | branch-validator             | 直连 L2   |
| "检查 commit 格式"       | conventional-commit-validator | 直连 L2  |
```

**复杂度路由**: S 级 → 直连 L2（省 L1 开销）; M/L/XL 级 → L1 编排器

## 安全策略

### 破坏性操作保护

以下操作必须经用户明确确认：

| 操作 | 风险等级 | 确认方式 |
|------|---------|---------|
| `git push --force` | CRITICAL | 必须确认 + 显示影响 |
| `git branch -D` | HIGH | 必须确认 |
| `git reset --hard` | CRITICAL | 必须确认 + 备份提醒 |
| `git tag` (发版) | MEDIUM | 确认版本号 |
| `git push` (首次) | LOW | 确认远程分支 |

### 敏感文件保护

所有涉及 commit/push 的流程自动包含 `sensitive-file-detector` 检查。

## 已有 Skill 复用矩阵

| Git 功能 | 复用的已有 skill | 方式 |
|----------|-----------------|------|
| PR 代码审查 | `code-review` | 直接调用，传入 PR diff |
| 冲突解决中的代码重构 | `refactor` | conflict-resolver 内部调用 |
| 安全相关审查 | `security-audit` | pr-orchestrator 审查流程可选调用 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| meta-commander | 被调用 | 由其路由 git 任务 |
| commit-orchestrator | 调用 | M 级 commit 任务 |
| pr-orchestrator | 调用 | M 级 PR 任务 |
| branch-orchestrator | 调用 | M 级 branch 任务 |
| release-orchestrator | 调用 | M/L 级 release 任务 |
| diff-analyzer | 调用 | S 级直接调用 |
| commit-message-gen | 调用 | S 级直接调用 |
| sensitive-file-detector | 调用 | S 级直接调用 |
| branch-validator | 调用 | S 级直接调用 |
| conventional-commit-validator | 调用 | S 级直接调用 |
| code-review | 间接调用 | 通过 pr-orchestrator |
| refactor | 间接调用 | 通过 conflict-resolver |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 意图识别 | 正确识别 git 操作类型 | ≥95% |
| 路由准确 | 路由到正确执行层 | ≥95% |
| 安全合规 | 破坏性操作均有确认 | 100% |
| 敏感检测 | commit/push 流程含敏感检查 | 100% |

## 配置文件

- `.claude/git-config.json` — commit/pr/branch/release/sensitive 全局配置
- `_architecture/resources/blueprints/smart_commit.json` — Smart Commit 蓝图
- `_architecture/resources/blueprints/pr_review.json` — PR Review 蓝图
- `_architecture/resources/blueprints/branch_management.json` — Branch Management 蓝图
- `_architecture/resources/blueprints/release.json` — Release 蓝图

## 参考资料

- `references/capability-map.md` — 全局能力地图
- `references/routing-rules.md` — 路由规则
