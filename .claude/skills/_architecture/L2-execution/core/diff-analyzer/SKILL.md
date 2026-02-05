---
name: diff-analyzer
description: >
  Git Diff 分析器 (L2 Core)。解析 git diff 输出，生成变更摘要、影响范围评估、风险等级判定。
  作为 Smart Commit 和 PR Review 工作流的第一步，为后续 skill 提供结构化的变更信息。
  由 commit-orchestrator 或 pr-orchestrator 调度触发。
---

# Diff Analyzer — Git Diff 分析器

## 触发条件

- 由 `commit-orchestrator` 在 Smart Commit 流程 Step 1 调度
- 由 `pr-orchestrator` 在 PR Review 流程 Step 1 调度
- 由 `git-commander` 直接路由（S 级 "分析 diff" 请求）

## 核心能力

1. **变更解析**: 解析 `git diff` 输出，提取文件列表、新增/删除行数、变更类型
2. **影响评估**: 评估变更影响的模块、API、配置等范围
3. **风险判定**: 基于变更模式判定风险等级 (low/medium/high/critical)
4. **变更分类**: 自动识别变更类型 (feature/fix/refactor/docs/test/config)

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["diff_content"],
  "properties": {
    "diff_content": {
      "type": "string",
      "description": "git diff 输出内容（--staged 或 base...HEAD）"
    },
    "diff_mode": {
      "type": "string",
      "enum": ["staged", "unstaged", "branch_compare", "pr"],
      "default": "staged",
      "description": "diff 模式"
    },
    "context_lines": {
      "type": "integer",
      "default": 3,
      "description": "diff 上下文行数"
    },
    "include_stats": {
      "type": "boolean",
      "default": true,
      "description": "是否包含统计信息"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["files", "summary", "risk_level", "change_type"],
  "properties": {
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "status": { "type": "string", "enum": ["added", "modified", "deleted", "renamed"] },
          "insertions": { "type": "integer" },
          "deletions": { "type": "integer" },
          "change_summary": { "type": "string" },
          "risk_factors": { "type": "array", "items": { "type": "string" } }
        }
      },
      "description": "变更文件列表"
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_files": { "type": "integer" },
        "total_insertions": { "type": "integer" },
        "total_deletions": { "type": "integer" },
        "description": { "type": "string", "description": "一句话变更摘要" },
        "detailed_description": { "type": "string", "description": "详细变更描述" }
      },
      "description": "变更统计摘要"
    },
    "risk_level": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "风险等级"
    },
    "risk_reasons": {
      "type": "array",
      "items": { "type": "string" },
      "description": "风险原因列表"
    },
    "change_type": {
      "type": "string",
      "enum": ["feature", "fix", "refactor", "docs", "test", "config", "chore", "mixed"],
      "description": "变更类型"
    },
    "affected_modules": {
      "type": "array",
      "items": { "type": "string" },
      "description": "受影响的模块/包"
    },
    "breaking_changes": {
      "type": "boolean",
      "description": "是否包含破坏性变更"
    }
  }
}
```

## 执行流程

### Step 1: 解析 diff

```
git diff --staged (或 git diff base...HEAD)
    │
    ├─ 提取变更文件列表
    ├─ 统计每个文件的 insertions/deletions
    ├─ 识别文件状态 (added/modified/deleted/renamed)
    └─ 按模块/目录分组
```

### Step 2: 变更分类

```
分析变更内容模式:
    │
    ├─ 新增功能代码 → feature
    ├─ 修复 bug (fix/patch 关键词) → fix
    ├─ 重构 (移动/重命名/简化) → refactor
    ├─ 文档变更 (.md, comments) → docs
    ├─ 测试变更 (test/spec 目录) → test
    ├─ 配置变更 (.json/.yaml/.toml) → config
    └─ 混合多种类型 → mixed
```

### Step 3: 风险评估

| 风险因素 | 权重 | 说明 |
|---------|------|------|
| 修改核心/关键文件 | HIGH | package.json, auth/*, config/* |
| 大量删除 (>100行) | MEDIUM | 可能影响功能 |
| 修改 API 接口 | HIGH | 可能影响下游 |
| 修改数据库/迁移 | CRITICAL | 不可逆操作 |
| 修改安全相关文件 | HIGH | auth, crypto, permissions |
| 新增依赖 | MEDIUM | 供应链风险 |
| 修改 CI/CD | MEDIUM | 影响部署流程 |
| 仅修改测试/文档 | LOW | 低风险 |

### Step 4: 生成摘要

- 一句话描述核心变更
- 列出影响的模块
- 标注破坏性变更
- 输出结构化 JSON

## 风险等级判定规则

| 等级 | 条件 |
|------|------|
| low | 仅文档/测试/注释变更，或小幅修改 (<20行) |
| medium | 功能代码变更，无 API/配置改动，<100行 |
| high | API 变更、核心模块修改、安全相关、>100行 |
| critical | 数据库迁移、认证变更、生产配置、>500行 |

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| commit-orchestrator | 被调用 | Smart Commit Step 1 |
| pr-orchestrator | 被调用 | PR Review Step 1 |
| commit-message-gen | 下游消费者 | 基于 diff 分析生成 commit message |
| sensitive-file-detector | 并行协作 | 同时检查敏感文件 |
| code-review | 下游消费者 | PR 审查时提供变更上下文 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 文件识别 | 正确识别所有变更文件 | 100% |
| 变更分类 | 正确判断变更类型 | ≥90% |
| 风险评估 | 风险等级合理 | ≥85% |
| 摘要质量 | 准确反映变更内容 | ≥90% |
