---
name: diff-analyzer
description: >
  Git Diff 分析器。解析 git diff 输出，生成变更摘要、影响范围、风险等级。
  Smart Commit 和 PR Review 的第一步。
---

# Diff Analyzer — Git Diff 分析器

> 详细文档: [_architecture/L2-execution/core/diff-analyzer/SKILL.md](_architecture/L2-execution/core/diff-analyzer/SKILL.md)

## 执行流程

收到 diff 分析请求后，按以下步骤执行：

### Step 1: 获取 diff

根据请求模式获取 diff 内容：
- **staged**: `git diff --staged`
- **unstaged**: `git diff`
- **branch_compare**: `git diff base...HEAD`
- **pr**: `git diff origin/main...HEAD`

### Step 2: 解析变更

对每个变更文件分析：
- **路径**: 文件完整路径
- **状态**: added / modified / deleted / renamed
- **统计**: insertions / deletions 行数
- **摘要**: 该文件的核心变更内容

### Step 3: 分类变更类型

| 模式 | 分类 |
|------|------|
| 新增功能代码 | `feature` |
| 修复 bug | `fix` |
| 重构/重命名 | `refactor` |
| 文档/注释变更 | `docs` |
| 测试文件变更 | `test` |
| 配置文件变更 | `config` |
| 混合多种 | `mixed` |

### Step 4: 风险评估

| 风险等级 | 触发条件 |
|---------|---------|
| `low` | 仅文档/测试/注释，或 <20行 |
| `medium` | 功能代码变更 <100行，无 API 改动 |
| `high` | API 变更、核心模块、安全相关、>100行 |
| `critical` | 数据库迁移、认证变更、生产配置、>500行 |

### Step 5: 输出结构化结果

```json
{
  "files": [{ "path": "...", "status": "modified", "insertions": 10, "deletions": 3 }],
  "summary": { "total_files": 3, "total_insertions": 25, "total_deletions": 8, "description": "..." },
  "risk_level": "medium",
  "change_type": "feature",
  "affected_modules": ["auth", "api"],
  "breaking_changes": false
}
```

## 用户任务

$ARGUMENTS

---

请分析提供的 git diff 内容，输出结构化的变更分析报告。
