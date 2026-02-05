---
name: release-notes-gen
description: >
  发布说明生成器 Skill。生成面向用户的发布说明 (区别于面向开发者的 changelog)。
  当需要：(1) 生成用户友好的发布说明，(2) 高亮关键特性，(3) 提供迁移指南时触发。
  支持多受众 (developer/user/both)、自动生成迁移指南。作为扩展发布 Skill，具有标准契约。
---

# Release Notes Gen — 发布说明生成器

## 触发条件

- changelog 已生成 (changelog-gen 完成后)
- 由 release-orchestrator 调度
- 需要生成面向用户的发布说明时

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["changelog_entry", "version_info"],
  "properties": {
    "changelog_entry": {
      "type": "string",
      "description": "来自 changelog-gen 的 markdown 变更日志"
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
        "breaking_changes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "message": { "type": "string" },
              "description": { "type": "string" }
            }
          }
        }
      },
      "description": "版本信息 (来自 version-bumper)"
    },
    "audience": {
      "type": "string",
      "enum": ["developer", "user", "both"],
      "default": "both",
      "description": "目标受众"
    },
    "config": {
      "type": "object",
      "properties": {
        "project_name": { "type": "string", "description": "项目名称" },
        "include_migration_guide": {
          "type": "boolean",
          "default": true,
          "description": "是否包含迁移指南 (当有 breaking changes 时)"
        },
        "tone": {
          "type": "string",
          "enum": ["formal", "friendly", "technical"],
          "default": "friendly"
        }
      }
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["release_notes", "highlights"],
  "properties": {
    "release_notes": {
      "type": "string",
      "description": "完整的发布说明 markdown"
    },
    "highlights": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": { "type": "string", "maxLength": 80 },
          "description": { "type": "string" },
          "category": {
            "type": "string",
            "enum": ["feature", "improvement", "bugfix", "breaking", "security"]
          }
        }
      },
      "maxItems": 5,
      "description": "关键亮点 (最多 5 条)"
    },
    "migration_guide": {
      "type": "object",
      "properties": {
        "required": { "type": "boolean", "description": "是否需要迁移" },
        "steps": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": { "type": "string" },
              "before": { "type": "string", "description": "迁移前代码/配置" },
              "after": { "type": "string", "description": "迁移后代码/配置" },
              "notes": { "type": "string" }
            }
          }
        },
        "estimated_effort": {
          "type": "string",
          "enum": ["trivial", "small", "medium", "large"],
          "description": "预计迁移工作量"
        }
      },
      "description": "迁移指南 (当存在 breaking changes 时生成)"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "audience": { "type": "string" },
        "tone": { "type": "string" },
        "word_count": { "type": "integer" }
      }
    }
  }
}
```

## 执行流程

1. **内容分析**
   - 解析 changelog_entry 提取变更条目
   - 识别关键特性和重要修复
   - 评估 breaking changes 影响范围

2. **亮点提取**
   - 从变更列表中选择最具影响力的 Top 5
   - 按受众调整描述语言
   - feature > breaking > improvement > bugfix 优先级

3. **发布说明生成**
   - 按受众生成对应风格的发布说明
   - developer: 技术细节 + API 变更
   - user: 功能描述 + 使用示例
   - both: 综合版本，分段呈现

4. **迁移指南生成** (如有 breaking changes)
   - 列出所有破坏性变更
   - 提供 before/after 代码示例
   - 评估迁移工作量
   - 按优先级排列迁移步骤

## 受众适配策略

| 受众 | 语言风格 | 内容侧重 | 技术深度 |
|------|---------|---------|---------|
| developer | 技术术语 | API 变更、内部实现 | 高 |
| user | 通俗易懂 | 功能效果、使用方法 | 低 |
| both | 分层呈现 | 功能概要 + 技术细节 | 中高 |

## 发布说明输出格式

```markdown
# Release vX.Y.Z

> 一句话版本摘要

## Highlights
- Feature A: 简要描述
- Improvement B: 简要描述

## What's New
详细描述新功能...

## Improvements
详细描述改进...

## Bug Fixes
修复列表...

## Breaking Changes
破坏性变更说明...

## Migration Guide
迁移步骤...
```

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 覆盖所有 breaking changes | 100% |
| 可读性 | 非开发者可理解 (user 受众) | ≥85% |
| 准确性 | 描述与实际变更一致 | 100% |
| 迁移覆盖 | 每个 breaking change 有迁移步骤 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| changelog-gen | 接收输入 | changelog_entry |
| version-bumper | 间接依赖 | 通过 version_info |
| release-orchestrator | 由其调度 | Step 3 |

## 脚本

- `scripts/generate_notes.py` - 发布说明生成主脚本
- `scripts/highlight_extractor.py` - 亮点提取器
- `scripts/migration_guide_gen.py` - 迁移指南生成器

## 参考资料

- `references/release-notes-best-practices.md` - 发布说明最佳实践
- `references/migration-guide-template.md` - 迁移指南模板
