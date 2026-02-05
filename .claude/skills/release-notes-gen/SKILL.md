---
name: release-notes-gen
description: >
  发布说明生成器。生成面向用户的发布说明，高亮关键特性和 breaking changes。
  支持 developer/user/both 受众，自动生成迁移指南。由 release-orchestrator 在 Step 3 调度。
---

# Release Notes Gen — 发布说明生成器

> 详细文档: [_architecture/L2-execution/extended/release-notes-gen/SKILL.md](_architecture/L2-execution/extended/release-notes-gen/SKILL.md)

## 执行流程

1. **内容分析**: 解析 changelog 提取变更条目，评估 breaking 影响
2. **亮点提取**: Top 5 最具影响力变更，按受众调整描述
3. **发布说明生成**: 按受众风格生成 markdown (developer / user / both)
4. **迁移指南**: 为每个 breaking change 生成 before/after 示例

## 受众适配

| 受众 | 侧重 |
|------|------|
| developer | API 变更、技术细节 |
| user | 功能效果、使用方法 |
| both | 分层呈现 |

## 输出: release_notes (markdown) + highlights[] + migration_guide

## 用户任务

$ARGUMENTS
