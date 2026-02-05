---
name: version-bumper
description: >
  语义版本计算器 Skill。基于 Conventional Commits 规范分析 git 日志，自动计算下一版本号。
  当需要：(1) 确定版本升级类型，(2) 解析 breaking changes，(3) 生成提交摘要时触发。
  breaking → major, feat → minor, fix → patch。作为核心发布 Skill，具有严格契约。
---

# Version Bumper — 语义版本计算器

## 触发条件

- 发布流程启动时首先执行
- 由 release-orchestrator 调度
- 需要确定下一版本号时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["git_log", "current_version"],
  "properties": {
    "git_log": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["hash", "message"],
        "properties": {
          "hash": { "type": "string", "description": "提交哈希" },
          "message": { "type": "string", "description": "提交信息 (Conventional Commits 格式)" },
          "author": { "type": "string" },
          "date": { "type": "string", "format": "date-time" }
        }
      },
      "description": "自上个 tag 以来的提交列表"
    },
    "current_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+",
      "description": "当前版本号 (来自最新 git tag)"
    },
    "prerelease": {
      "type": "string",
      "enum": ["alpha", "beta", "rc", ""],
      "default": "",
      "description": "预发布标识 (可选)"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["current_version", "next_version", "bump_type", "breaking_changes", "commit_summary"],
  "properties": {
    "current_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+",
      "description": "当前版本号"
    },
    "next_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+",
      "description": "计算后的下一版本号"
    },
    "bump_type": {
      "type": "string",
      "enum": ["major", "minor", "patch"],
      "description": "版本升级类型"
    },
    "breaking_changes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "hash": { "type": "string" },
          "message": { "type": "string" },
          "description": { "type": "string" }
        }
      },
      "description": "破坏性变更列表"
    },
    "commit_summary": {
      "type": "object",
      "properties": {
        "total": { "type": "integer" },
        "feat": { "type": "integer" },
        "fix": { "type": "integer" },
        "breaking": { "type": "integer" },
        "chore": { "type": "integer" },
        "docs": { "type": "integer" },
        "refactor": { "type": "integer" },
        "other": { "type": "integer" }
      },
      "description": "按类型分组的提交统计"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "tag_prefix": { "type": "string", "default": "v" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}
```

## 执行流程

1. **解析提交日志**
   - 按 Conventional Commits 规范解析每条提交
   - 识别类型前缀: `feat`, `fix`, `chore`, `docs`, `refactor`, `perf`, `test`, `ci`
   - 检测 `BREAKING CHANGE:` 标记和 `!` 后缀

2. **计算升级类型**
   - 存在 `BREAKING CHANGE` 或 `!` → `major`
   - 存在 `feat` → `minor`
   - 仅 `fix` / `chore` / `docs` 等 → `patch`
   - 优先级: major > minor > patch

3. **版本号计算**
   - `major` → 主版本号 +1，次版本号和补丁号归零
   - `minor` → 次版本号 +1，补丁号归零
   - `patch` → 补丁号 +1
   - 处理预发布标识 (如有)

4. **生成摘要**
   - 统计各类型提交数量
   - 提取 breaking changes 详情
   - 计算置信度

## Conventional Commits 类型映射

| 提交类型 | 升级类型 | 说明 |
|---------|---------|------|
| `BREAKING CHANGE` / `!` | major | 不兼容的 API 变更 |
| `feat` | minor | 新增功能 |
| `fix` | patch | 缺陷修复 |
| `perf` | patch | 性能优化 |
| `refactor` | patch | 代码重构 |
| `docs` | patch | 文档更新 |
| `chore` | patch | 构建/工具变更 |
| `test` | patch | 测试相关 |
| `ci` | patch | CI/CD 变更 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 解析覆盖 | 所有提交已解析 | 100% |
| 规范符合 | 版本号符合 SemVer 2.0 | 100% |
| Breaking 检测 | 不遗漏破坏性变更 | 100% |
| 幂等性 | 相同输入给出相同输出 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| changelog-gen | 输出传递 | 版本确定后 |
| release-notes-gen | 间接依赖 | 通过 changelog-gen |
| release-orchestrator | 由其调度 | Step 1 |

## 脚本

- `scripts/bump.py` - 版本计算主脚本
- `scripts/commit_parser.py` - Conventional Commits 解析器

## 参考资料

- `references/semver-spec.md` - SemVer 2.0 规范
- `references/conventional-commits.md` - Conventional Commits 规范
