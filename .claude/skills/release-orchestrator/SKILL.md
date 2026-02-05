---
name: release-orchestrator
description: >
  发布编排器。编排完整发布流程：版本计算→变更日志→发布说明→用户确认。
  采用黑板模式。破坏性 git 操作 (tag, push) 需要用户确认。
---

# Release Orchestrator — 发布编排器

> 详细文档: [_architecture/L1-orchestrators/release-orchestrator/SKILL.md](_architecture/L1-orchestrators/release-orchestrator/SKILL.md)

## 编排流程

### Step 0: 环境准备
- 获取最新 git tag → current_version
- 获取 git log since last tag → commits

### Step 1: 版本计算
- 调用 `/version-bumper` → next_version, bump_type
- Quality Gate: version_sanity (bump_type 匹配提交类型)

### Step 2: 变更日志
- 调用 `/changelog-gen` → keepachangelog 格式条目

### Step 3: 发布说明
- 调用 `/release-notes-gen` → 用户友好的发布说明 + 迁移指南

### Step 4: 用户确认
- 展示: 版本号 + changelog + release notes
- 确认后执行: CHANGELOG.md 更新 → git commit → git tag → git push
- dry_run=true → 仅预览，不执行 git 操作

## 破坏性操作保护

| 操作 | 需确认 |
|------|-------|
| git tag | 是 |
| git push | 是 (单独确认) |
| git push --tags | 是 (不可逆警告) |

## 用户任务

$ARGUMENTS
