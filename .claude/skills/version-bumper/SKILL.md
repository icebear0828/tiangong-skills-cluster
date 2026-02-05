---
name: version-bumper
description: >
  语义版本计算器。基于 Conventional Commits 分析 git 日志，自动计算下一版本号。
  breaking → major, feat → minor, fix → patch。由 release-orchestrator 在 Step 1 调度。
---

# Version Bumper — 语义版本计算器

> 详细文档: [_architecture/L2-execution/core/version-bumper/SKILL.md](_architecture/L2-execution/core/version-bumper/SKILL.md)

## 执行流程

1. **解析提交日志**: 按 Conventional Commits 规范解析 `feat`, `fix`, `BREAKING CHANGE` 等
2. **计算升级类型**: major > minor > patch 优先级
3. **版本号计算**: SemVer 2.0 规则递增
4. **生成摘要**: 按类型统计 + breaking changes 清单

## 版本映射

| 提交类型 | 升级类型 |
|---------|---------|
| `BREAKING CHANGE` / `!` | major |
| `feat` | minor |
| `fix` / `chore` / `docs` | patch |

## 输出: current_version + next_version + bump_type + breaking_changes[] + commit_summary

## 用户任务

$ARGUMENTS
