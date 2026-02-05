---
name: release-orchestrator
description: >
  发布编排器。编排完整的语义化发布流程：版本计算→变更日志→发布说明→用户确认。
  当需要：(1) 创建新版本发布，(2) 生成完整发布产物，(3) 自动化 tag + push 时触发。
  采用黑板模式共享版本/发布数据。破坏性操作 (git tag, git push) 必须用户确认。
---

# Release Orchestrator — 发布编排器

## 触发条件

- 用户请求创建新版本发布
- 手动调用 `/release-orchestrator`
- 存在未发布的提交需要版本化

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["repo_root"],
  "properties": {
    "repo_root": {
      "type": "string",
      "description": "仓库根目录路径"
    },
    "force_bump_type": {
      "type": "string",
      "enum": ["major", "minor", "patch"],
      "description": "强制指定版本升级类型 (覆盖自动计算)"
    },
    "prerelease": {
      "type": "string",
      "enum": ["alpha", "beta", "rc", ""],
      "default": "",
      "description": "预发布标识"
    },
    "audience": {
      "type": "string",
      "enum": ["developer", "user", "both"],
      "default": "both",
      "description": "发布说明目标受众"
    },
    "dry_run": {
      "type": "boolean",
      "default": false,
      "description": "仅预览，不执行 git 操作"
    },
    "config": {
      "type": "object",
      "properties": {
        "tag_prefix": { "type": "string", "default": "v" },
        "changelog_file": { "type": "string", "default": "CHANGELOG.md" },
        "auto_push": { "type": "boolean", "default": false }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["version", "changelog_entry", "release_notes", "actions_taken"],
  "properties": {
    "version": {
      "type": "object",
      "properties": {
        "current": { "type": "string" },
        "next": { "type": "string" },
        "bump_type": { "type": "string" },
        "tag": { "type": "string" }
      },
      "description": "版本信息"
    },
    "changelog_entry": {
      "type": "string",
      "description": "生成的 CHANGELOG 条目"
    },
    "release_notes": {
      "type": "string",
      "description": "生成的发布说明"
    },
    "actions_taken": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "action": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["success", "skipped", "failed", "pending_confirmation"]
          },
          "details": { "type": "string" }
        }
      },
      "description": "已执行的操作列表"
    },
    "dry_run": { "type": "boolean" }
  }
}
```

## 黑板模型

```
Blackboard:
├── Meta Zone
│   ├── repo_root: 仓库根目录
│   ├── tag_prefix: "v"
│   ├── changelog_file: "CHANGELOG.md"
│   └── audience: "both"
│
├── Version Zone
│   ├── current_version: "1.2.3"
│   ├── next_version: "1.3.0"
│   ├── bump_type: "minor"
│   ├── breaking_changes: [...]
│   └── commit_summary: {...}
│
├── Content Zone
│   ├── git_log: [...提交列表]
│   ├── changelog_entry: "## [1.3.0] - 2026-02-05\n..."
│   ├── release_notes: "# Release v1.3.0\n..."
│   └── highlights: [...]
│
└── Control Zone
    ├── step_status: { version_bump: "done", changelog: "done", ... }
    ├── quality_gates: { version_sanity: "passed", ... }
    ├── user_confirmed: false
    └── actions_log: [...]
```

## 编排流程

```
┌──────────────────────────────────────────────────────┐
│  Release Orchestrator — 发布编排                      │
│                                                      │
│  Step 0: 环境准备                                     │
│  ├─ 获取最新 git tag → current_version               │
│  ├─ 获取 git log since last tag → commits            │
│  └─ 写入黑板 Meta Zone + Content Zone                │
│                                                      │
│  Step 1: 版本计算                                     │
│  ├─ 调用 version-bumper                              │
│  ├─ 输入: git_log, current_version                   │
│  ├─ 输出: next_version, bump_type, breaking_changes  │
│  └─ 写入黑板 Version Zone                             │
│                                                      │
│  ── Quality Gate: version_sanity ──                   │
│  │  检查: bump_type 与提交类型匹配                     │
│  │  检查: next_version > current_version              │
│  │  检查: breaking changes → 必须 major               │
│  │  未通过 → 中止并报告                                │
│  └─────────────────────────────────                   │
│                                                      │
│  Step 2: 变更日志生成                                  │
│  ├─ 调用 changelog-gen                               │
│  ├─ 输入: commits, version_info                      │
│  ├─ 输出: changelog_entry, grouped_changes           │
│  └─ 写入黑板 Content Zone                             │
│                                                      │
│  Step 3: 发布说明生成                                  │
│  ├─ 调用 release-notes-gen                           │
│  ├─ 输入: changelog_entry, version_info, audience    │
│  ├─ 输出: release_notes, highlights, migration_guide │
│  └─ 写入黑板 Content Zone                             │
│                                                      │
│  Step 4: 用户确认 + 执行                               │
│  ├─ 展示: 版本号 + changelog + release notes          │
│  ├─ 展示: 即将执行的 git 操作列表                      │
│  │                                                   │
│  ── Quality Gate: user_confirmation ──                │
│  │  ⚠ 以下操作需要用户确认:                            │
│  │  1. 更新 CHANGELOG.md                             │
│  │  2. git commit (changelog 更新)                   │
│  │  3. git tag vX.Y.Z                                │
│  │  4. git push (如 auto_push=true)                  │
│  │  dry_run=true → 仅预览，跳过执行                    │
│  └─────────────────────────────────                   │
│                                                      │
│  用户确认后:                                           │
│  ├─ 写入 CHANGELOG.md (prepend 到文件头部)            │
│  ├─ git add CHANGELOG.md                             │
│  ├─ git commit -m "chore(release): vX.Y.Z"          │
│  ├─ git tag -a vX.Y.Z -m "Release vX.Y.Z"          │
│  └─ git push + git push --tags (如 auto_push)       │
│                                                      │
│  输出 → 完整发布报告                                   │
└──────────────────────────────────────────────────────┘
```

## 质量关卡

### Gate 1: version_sanity (Step 1 后)

| 检查项 | 规则 | 未通过处理 |
|--------|------|-----------|
| bump_type 匹配 | breaking → major, feat → minor, fix → patch | 中止 + 报告不一致 |
| 版本递增 | next_version > current_version | 中止 + 报告错误 |
| Breaking 约束 | 有 breaking changes 时 bump_type 必须为 major | 中止 + 建议修正 |
| 版本格式 | 符合 SemVer 2.0 格式 | 中止 + 格式错误 |

### Gate 2: user_confirmation (Step 4)

| 检查项 | 规则 | 未通过处理 |
|--------|------|-----------|
| 用户同意 | 所有 git 操作需明确确认 | 等待确认或取消 |
| dry_run | dry_run=true 时跳过所有 git 写操作 | 仅返回预览 |
| push 确认 | push 操作额外确认 (不可逆) | 单独确认 |

## 破坏性操作保护

| 操作 | 危险等级 | 保护措施 |
|------|---------|---------|
| 更新 CHANGELOG.md | 低 | 预览 diff |
| git commit | 低 | 展示提交内容 |
| git tag | 中 | 展示 tag 名称，确认 |
| git push | 高 | 单独确认，展示远程信息 |
| git push --tags | 高 | 单独确认，不可逆警告 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| version-bumper | 调用 | Step 1 |
| changelog-gen | 调用 | Step 2 |
| release-notes-gen | 调用 | Step 3 |

## 脚本

- `scripts/orchestrate_release.py` - 发布编排主脚本
- `scripts/git_ops.py` - Git 操作封装 (tag, commit, push)
- `scripts/changelog_updater.py` - CHANGELOG.md 更新器

## 参考资料

- `references/release-workflow.md` - 发布工作流详解
- `references/semver-decision-tree.md` - SemVer 决策树
- `references/git-tag-conventions.md` - Git Tag 命名规范
