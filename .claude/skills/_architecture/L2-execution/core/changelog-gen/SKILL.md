---
name: changelog-gen
description: >
  变更日志生成器 Skill。基于提交历史生成符合 keepachangelog 格式的 CHANGELOG.md 条目。
  当需要：(1) 生成版本变更记录，(2) 按类型分组提交，(3) 格式化变更日志时触发。
  支持 Added/Changed/Deprecated/Removed/Fixed/Security 分类。作为核心发布 Skill，具有严格契约。
---

# Changelog Gen — 变更日志生成器

## 触发条件

- 版本号已确定 (version-bumper 完成后)
- 由 release-orchestrator 调度
- 需要生成或更新 CHANGELOG.md 时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["commits", "version_info"],
  "properties": {
    "commits": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["hash", "message"],
        "properties": {
          "hash": { "type": "string", "description": "提交哈希" },
          "message": { "type": "string", "description": "提交信息" },
          "author": { "type": "string" },
          "date": { "type": "string", "format": "date-time" },
          "scope": { "type": "string", "description": "变更范围 (可选)" }
        }
      },
      "description": "自上个版本以来的提交列表"
    },
    "version_info": {
      "type": "object",
      "required": ["current_version", "next_version", "bump_type"],
      "properties": {
        "current_version": { "type": "string" },
        "next_version": { "type": "string" },
        "bump_type": {
          "type": "string",
          "enum": ["major", "minor", "patch"]
        },
        "release_date": {
          "type": "string",
          "format": "date",
          "description": "发布日期 (默认今天)"
        }
      },
      "description": "来自 version-bumper 的版本信息"
    },
    "config": {
      "type": "object",
      "properties": {
        "include_hash": {
          "type": "boolean",
          "default": false,
          "description": "是否包含提交哈希链接"
        },
        "include_author": {
          "type": "boolean",
          "default": false,
          "description": "是否包含作者信息"
        },
        "repo_url": {
          "type": "string",
          "description": "仓库 URL (用于生成 commit 链接)"
        }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["changelog_entry", "grouped_changes"],
  "properties": {
    "changelog_entry": {
      "type": "string",
      "description": "格式化的 CHANGELOG markdown 文本"
    },
    "grouped_changes": {
      "type": "object",
      "properties": {
        "Added": {
          "type": "array",
          "items": { "type": "string" },
          "description": "新增功能 (feat)"
        },
        "Changed": {
          "type": "array",
          "items": { "type": "string" },
          "description": "变更内容 (refactor, perf)"
        },
        "Deprecated": {
          "type": "array",
          "items": { "type": "string" },
          "description": "即将废弃的功能"
        },
        "Removed": {
          "type": "array",
          "items": { "type": "string" },
          "description": "已移除的功能"
        },
        "Fixed": {
          "type": "array",
          "items": { "type": "string" },
          "description": "缺陷修复 (fix)"
        },
        "Security": {
          "type": "array",
          "items": { "type": "string" },
          "description": "安全相关修复"
        }
      },
      "description": "按 keepachangelog 类别分组的变更"
    },
    "stats": {
      "type": "object",
      "properties": {
        "total_entries": { "type": "integer" },
        "categories_used": { "type": "array", "items": { "type": "string" } },
        "unmapped_commits": { "type": "integer", "description": "未能分类的提交数" }
      }
    }
  }
}
```

## 执行流程

1. **提交分类**
   - 解析每条提交的 Conventional Commits 类型
   - 映射到 keepachangelog 类别
   - 处理含 scope 的提交 (如 `feat(api): ...`)

2. **分组整理**
   - 按 Added / Changed / Deprecated / Removed / Fixed / Security 分组
   - 组内按影响范围排序
   - 过滤不影响用户的提交 (ci, test, chore 默认不入 changelog)

3. **格式化输出**
   - 生成 keepachangelog 格式的 markdown
   - 添加版本号和日期标题
   - 可选添加提交哈希链接和作者信息

4. **校验**
   - 确认所有 feat/fix 提交已包含
   - 验证 markdown 格式正确性
   - 统计未分类提交

## Conventional Commits → keepachangelog 映射

| 提交类型 | keepachangelog 类别 | 说明 |
|---------|-------------------|------|
| `feat` | Added | 新增功能 |
| `fix` | Fixed | 缺陷修复 |
| `refactor` | Changed | 代码重构 |
| `perf` | Changed | 性能优化 |
| `deprecate` | Deprecated | 废弃标记 |
| `remove` | Removed | 功能移除 |
| `security` | Security | 安全修复 |
| `BREAKING CHANGE` | Changed (高亮) | 破坏性变更，加粗标记 |
| `docs` / `chore` / `ci` / `test` | (默认不入) | 可通过 config 开启 |

## keepachangelog 输出格式

```markdown
## [x.y.z] - YYYY-MM-DD

### Added
- 新增功能描述

### Changed
- **BREAKING**: 破坏性变更描述
- 变更描述

### Fixed
- 修复描述
```

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 覆盖率 | feat/fix 提交 100% 收录 | 100% |
| 格式合规 | 符合 keepachangelog 1.1.0 | 100% |
| 分类准确 | 类别映射正确 | ≥95% |
| 可读性 | 条目简洁易懂 | ≥90% |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| version-bumper | 接收输入 | 版本号 + 提交列表 |
| release-notes-gen | 输出传递 | changelog 作为输入 |
| release-orchestrator | 由其调度 | Step 2 |

## 脚本

- `scripts/generate.py` - 变更日志生成主脚本
- `scripts/commit_classifier.py` - 提交分类器
- `scripts/formatter.py` - keepachangelog 格式化器

## 参考资料

- `references/keepachangelog-spec.md` - keepachangelog 1.1.0 规范
- `references/commit-category-map.md` - 提交类型映射表
