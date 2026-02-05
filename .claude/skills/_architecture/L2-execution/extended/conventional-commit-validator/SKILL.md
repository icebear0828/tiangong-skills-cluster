---
name: conventional-commit-validator
description: >
  Conventional Commits 校验器 (L2 Extended)。校验 commit message 是否符合 Conventional Commits 规范。
  分析项目历史 commit 模式，推荐 type/scope。作为 Smart Commit 流程的质量关卡。
  由 commit-orchestrator 在 Step 2b 并行调度，或在 Step 4 作为格式校验。
---

# Conventional Commit Validator — 提交格式校验器

## 触发条件

- 由 `commit-orchestrator` 在 Step 2b 并行调度（分析历史模式）
- 由 `commit-orchestrator` 在质量关卡 2 调度（校验生成的 message）
- 由 `git-commander` 直接路由（S 级 "检查 commit 格式" 请求）

## 核心能力

1. **格式校验**: 校验 message 是否符合 `<type>(<scope>): <subject>` 格式
2. **历史分析**: 分析项目最近的 commit 模式，推荐惯例
3. **Type 校验**: 验证 type 是否在允许列表中
4. **长度校验**: 验证 subject ≤72 字符，body 行宽 ≤100 字符

## 输入契约 (Standard)

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "待校验的 commit message"
    },
    "mode": {
      "type": "string",
      "enum": ["validate", "analyze_history"],
      "default": "validate",
      "description": "模式：校验单条 / 分析历史"
    },
    "history_count": {
      "type": "integer",
      "default": 20,
      "description": "分析历史 commit 的数量"
    },
    "config": {
      "type": "object",
      "description": "覆盖默认配置",
      "properties": {
        "types": { "type": "array", "items": { "type": "string" } },
        "max_subject_length": { "type": "integer" },
        "require_body_for": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "properties": {
    "valid": {
      "type": "boolean",
      "description": "格式是否有效"
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rule": { "type": "string" },
          "message": { "type": "string" },
          "severity": { "type": "string", "enum": ["error", "warning"] }
        }
      }
    },
    "project_conventions": {
      "type": "object",
      "description": "项目惯例分析（analyze_history 模式）",
      "properties": {
        "common_types": { "type": "array", "items": { "type": "string" } },
        "common_scopes": { "type": "array", "items": { "type": "string" } },
        "avg_subject_length": { "type": "integer" },
        "suggested_type": { "type": "string" },
        "suggested_scope": { "type": "string" }
      }
    }
  }
}
```

## 校验规则

| 规则 | 说明 | 严重度 |
|------|------|--------|
| type_required | type 不能为空 | error |
| type_valid | type 必须在允许列表中 | error |
| subject_required | subject 不能为空 | error |
| subject_max_length | subject ≤72 字符 | error |
| subject_no_period | subject 不以句号结尾 | warning |
| subject_imperative | subject 使用祈使语气 | warning |
| scope_format | scope 使用小写字母 + 短横线 | warning |
| body_required | feat/fix 类型需要 body | warning |
| body_line_length | body 每行 ≤100 字符 | warning |
| breaking_change_format | BREAKING CHANGE 格式正确 | error |

## 执行流程

### validate 模式

1. **解析 message**: 按 `<type>(<scope>): <subject>\n\n<body>\n\n<footer>` 拆分
2. **校验 type**: 检查是否在允许列表中（从 `.claude/git-config.json` 或 config 参数）
3. **校验 scope**: 格式为小写字母 + 短横线
4. **校验 subject**: 非空、≤72 字符、不以句号结尾、祈使语气
5. **校验 body**: feat/fix 类型检查 body 存在性、行宽 ≤100 字符
6. **校验 footer**: BREAKING CHANGE 格式、Closes/Fixes 引用格式
7. **汇总结果**: 输出 valid + errors 数组

### analyze_history 模式

1. **获取历史**: `git log --oneline -N`（N = history_count）
2. **解析 commits**: 提取 type、scope、subject
3. **统计模式**: 计算 common_types、common_scopes、avg_subject_length
4. **生成建议**: suggested_type、suggested_scope（基于频率和当前上下文）

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| commit-orchestrator | 被调用 | Step 2b 和质量关卡 2 |
| commit-message-gen | 上游 | 校验其生成的 message |
| git-hook-manager | 相关 | commit-msg hook 做轻量校验 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 格式检测 | 正确识别格式错误 | ≥98% |
| 历史分析 | 模式推荐准确 | ≥85% |
