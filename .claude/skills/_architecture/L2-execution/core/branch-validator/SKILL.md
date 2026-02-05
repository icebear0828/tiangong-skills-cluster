---
name: branch-validator
description: >
  分支验证器 Skill。验证分支命名规范、检测过期分支、检查合并冲突、保护关键分支。当需要：
  (1) 分支命名合规检查，(2) 过期分支清理，(3) 合并冲突预检，(4) 保护分支管理时触发。
  支持可配置命名模式、批量检测、保护列表。作为核心分支管理 Skill，具有严格契约。
---

# Branch Validator — 分支验证器

## 触发条件

- 分支管理流程启动时
- 由 branch-orchestrator 调度
- 需要验证分支健康状态时
- 用户执行分支清理或合规检查时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["branches", "naming_pattern"],
  "properties": {
    "branches": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "last_commit_date"],
        "properties": {
          "name": { "type": "string", "description": "分支名称" },
          "last_commit_date": { "type": "string", "format": "date-time", "description": "最后提交时间" },
          "author": { "type": "string", "description": "分支创建者" },
          "ahead_behind": {
            "type": "object",
            "properties": {
              "ahead": { "type": "integer" },
              "behind": { "type": "integer" }
            },
            "description": "相对主分支的领先/落后提交数"
          }
        }
      },
      "minItems": 1,
      "description": "待验证的分支列表"
    },
    "naming_pattern": {
      "type": "string",
      "description": "分支命名正则模式，来源 .claude/git-config.json",
      "examples": ["^(feature|fix|hotfix|release|chore)/[a-z0-9-]+$"]
    },
    "protected_branches": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["main", "master", "develop"],
      "description": "受保护分支列表，禁止删除"
    },
    "max_age_days": {
      "type": "integer",
      "default": 30,
      "description": "分支最大存活天数，超过视为过期"
    },
    "check_conflicts": {
      "type": "boolean",
      "default": true,
      "description": "是否检查分支间合并冲突"
    },
    "target_branch": {
      "type": "string",
      "default": "main",
      "description": "冲突检测的目标分支"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["branches", "naming_violations", "stale_branches", "conflicts", "protected_status"],
  "properties": {
    "branches": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "status", "issues"],
        "properties": {
          "name": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["healthy", "warning", "violation", "stale", "protected"]
          },
          "issues": {
            "type": "array",
            "items": { "type": "string" }
          },
          "age_days": { "type": "integer" },
          "naming_valid": { "type": "boolean" }
        }
      },
      "description": "每个分支的验证结果"
    },
    "naming_violations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["branch", "violation", "suggestion"],
        "properties": {
          "branch": { "type": "string", "description": "违规分支名" },
          "violation": { "type": "string", "description": "违规类型描述" },
          "suggestion": { "type": "string", "description": "推荐的分支名" }
        }
      },
      "description": "命名违规列表"
    },
    "stale_branches": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["branch", "age_days", "last_commit_date"],
        "properties": {
          "branch": { "type": "string" },
          "age_days": { "type": "integer" },
          "last_commit_date": { "type": "string" },
          "author": { "type": "string" },
          "recommendation": {
            "type": "string",
            "enum": ["delete", "archive", "review"],
            "description": "处理建议"
          }
        }
      },
      "description": "过期分支列表"
    },
    "conflicts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["branch", "target", "conflict_files"],
        "properties": {
          "branch": { "type": "string" },
          "target": { "type": "string" },
          "conflict_files": {
            "type": "array",
            "items": { "type": "string" }
          },
          "severity": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "冲突严重度"
          }
        }
      },
      "description": "合并冲突列表"
    },
    "protected_status": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "exists": { "type": "boolean" },
          "protected": { "type": "boolean" },
          "deletion_blocked": { "type": "boolean" }
        }
      },
      "description": "受保护分支状态"
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_branches": { "type": "integer" },
        "healthy": { "type": "integer" },
        "violations": { "type": "integer" },
        "stale": { "type": "integer" },
        "with_conflicts": { "type": "integer" },
        "protected_count": { "type": "integer" }
      },
      "description": "汇总统计"
    }
  }
}
```

## 执行流程

1. **加载配置**
   - 从 `.claude/git-config.json` 读取命名模式
   - 加载受保护分支列表
   - 确定最大存活天数阈值

2. **命名合规检查**
   - 对每个分支名应用正则匹配
   - 记录不合规分支
   - 生成推荐命名建议

3. **过期检测**
   - 计算每个分支的存活天数
   - 与 max_age_days 阈值比较
   - 按过期程度分级建议（delete / archive / review）

4. **冲突预检**
   - 对非保护分支执行 `git merge-tree` 预检
   - 识别冲突文件列表
   - 评估冲突严重度

5. **保护验证**
   - 确认保护列表中的分支存在
   - 标记保护状态
   - 阻止对保护分支的删除操作

## 命名模式参考

| 模式 | 示例 | 说明 |
|------|------|------|
| `feature/*` | `feature/user-auth` | 功能分支 |
| `fix/*` | `fix/login-crash` | 修复分支 |
| `hotfix/*` | `hotfix/security-patch` | 紧急修复 |
| `release/*` | `release/v2.1.0` | 发布分支 |
| `chore/*` | `chore/deps-update` | 杂务分支 |

## 过期分级标准

| 年龄范围 | 等级 | 建议 |
|---------|------|------|
| > 90 天 | Critical | 直接删除 |
| 60-90 天 | High | 归档或删除 |
| 30-60 天 | Medium | 人工审查 |
| < 30 天 | Low | 正常 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 所有分支均被检查 | 100% |
| 准确性 | 命名匹配结果正确 | 100% |
| 保护性 | 受保护分支不被误删 | 100% |
| 覆盖度 | 冲突检测覆盖所有活跃分支 | >=90% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| conflict-resolver | 检测到冲突后由其处理 |
| commit-history-analyzer | 提供分支年龄和活跃度数据 |
| branch-orchestrator | 由其调度执行 |

## 脚本

- `scripts/validate_branches.py` - 分支验证主脚本
- `scripts/naming_checker.py` - 命名规范检查器
- `scripts/stale_detector.py` - 过期分支检测器

## 参考资料

- `references/naming-conventions.md` - 分支命名规范
- `references/protection-rules.md` - 保护规则说明
