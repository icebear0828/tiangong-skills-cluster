---
name: changelog-gen
description: >
  变更日志生成器。基于提交历史生成 keepachangelog 格式的 CHANGELOG 条目。
  按 Added/Changed/Deprecated/Removed/Fixed/Security 分组。由 release-orchestrator 在 Step 2 调度。
---

# Changelog Gen — 变更日志生成器

> 详细文档: [_architecture/L2-execution/core/changelog-gen/SKILL.md](_architecture/L2-execution/core/changelog-gen/SKILL.md)

## 执行流程

1. **提交分类**: 解析 Conventional Commits 类型，映射到 keepachangelog 类别
2. **分组整理**: Added / Changed / Deprecated / Removed / Fixed / Security
3. **格式化输出**: keepachangelog 1.1.0 格式 markdown
4. **校验**: 确认 feat/fix 全部收录，验证格式正确性

## 类别映射

| 提交类型 | keepachangelog |
|---------|---------------|
| `feat` | Added |
| `fix` | Fixed |
| `refactor` / `perf` | Changed |
| `BREAKING CHANGE` | Changed (高亮) |
| `security` | Security |

## 输出: changelog_entry (markdown) + grouped_changes

## 用户任务

$ARGUMENTS
