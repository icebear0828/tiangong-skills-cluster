---
name: commit-message-gen
description: >
  Commit Message 生成器。基于 diff 分析生成 Conventional Commits 格式的提交信息。
  自动推断 type、scope，生成规范的 subject 和 body。
---

# Commit Message Generator — 提交信息生成器

> 详细文档: [_architecture/L2-execution/core/commit-message-gen/SKILL.md](_architecture/L2-execution/core/commit-message-gen/SKILL.md)

## 执行流程

收到 commit message 生成请求后，按以下步骤执行：

### Step 1: 获取变更信息

如果未提供 diff 分析，先执行分析：
```bash
git diff --staged
```

### Step 2: 推断类型和 Scope

| 变更模式 | Type | 说明 |
|---------|------|------|
| 新增功能代码 | `feat` | 新功能 |
| 修复 bug | `fix` | 缺陷修复 |
| 重构/重命名 | `refactor` | 不改变行为的代码调整 |
| 文档/注释 | `docs` | 文档变更 |
| 测试文件 | `test` | 测试相关 |
| 配置/CI | `chore`/`ci` | 构建/工具变更 |

Scope 从变更文件路径的公共模块推断。

### Step 3: 生成 Subject

规则:
- 祈使语气 ("Add", "Fix", 不用过去式)
- 首字母小写
- 不以句号结尾
- ≤72 字符

### Step 4: 生成 Body (feat/fix 必填)

包含:
- **What**: 做了什么
- **Why**: 为什么做
- **Impact**: 影响范围

### Step 5: 输出完整消息

```
<type>(<scope>): <subject>

<body>

BREAKING CHANGE: <description>  (如有)
```

## 用户任务

$ARGUMENTS

---

请分析暂存区变更，生成符合 Conventional Commits 规范的 commit message。
