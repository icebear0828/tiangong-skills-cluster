---
name: conventional-commit-validator
description: >
  Conventional Commits 校验器。校验 commit message 格式，分析项目 commit 历史模式。
  支持校验模式和历史分析模式。
---

# Conventional Commit Validator — 提交格式校验器

> 详细文档: [_architecture/L2-execution/extended/conventional-commit-validator/SKILL.md](_architecture/L2-execution/extended/conventional-commit-validator/SKILL.md)

## 执行流程

### 模式 1: 校验 (validate)

校验单条 commit message：

```
输入: "feat(auth): add OAuth2 login"
    │
    ├─ 检查 type 是否在允许列表 ✓
    ├─ 检查 scope 格式 ✓
    ├─ 检查 subject 长度 ≤72 ✓
    ├─ 检查 subject 不以句号结尾 ✓
    ├─ 检查 feat 类型是否有 body (warning)
    └─ 输出: { valid: true, errors: [] }
```

### 模式 2: 分析历史 (analyze_history)

分析项目最近 20 条 commit：
```bash
git log --oneline -20
```

提取:
- 常用 type 分布
- 常用 scope 列表
- 平均 subject 长度
- 推荐的 type 和 scope

### 校验规则

| 规则 | 说明 | 严重度 |
|------|------|--------|
| type 必填且有效 | feat/fix/docs/style/refactor/test/chore/ci | error |
| subject 必填 | 不能为空 | error |
| subject ≤72 字符 | 保证日志可读 | error |
| 不以句号结尾 | Conventional Commits 惯例 | warning |
| feat/fix 需要 body | 重要变更需详细说明 | warning |

## 用户任务

$ARGUMENTS

---

请校验 commit message 格式或分析项目 commit 历史模式。
