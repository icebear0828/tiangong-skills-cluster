---
name: git-hook-manager
description: >
  Git Hook 管理器 (L2 Extended)。安装、配置和管理 git hooks 和 Claude Code hooks。
  支持 PowerShell 脚本 + batch wrapper 的 Windows 兼容方案。
  管理两层 hook：Git 原生 hooks（轻量校验）+ Claude Code PreToolUse hooks（skill 集成）。
---

# Git Hook Manager — Hook 管理器

## 触发条件

- 由 `git-commander` 路由 hook 管理请求
- 用户请求安装/卸载/配置 git hooks

## 核心能力

1. **安装 Git Hooks**: 生成 PowerShell 脚本 + batch wrapper
2. **配置 Claude Code Hooks**: 配置 PreToolUse hook 拦截 git 命令
3. **查看 Hook 状态**: 列出已安装的 hooks 及其状态
4. **卸载 Hooks**: 安全移除 hooks

## 两层 Hook 架构

### 层 1: Git Hooks（纯 shell，无 skill 依赖）

| Hook | 脚本 | 作用 | 性能 |
|------|------|------|------|
| `pre-commit` | `.claude/git-hooks/pre-commit.ps1` | 正则匹配敏感文件 | <1s |
| `commit-msg` | `.claude/git-hooks/commit-msg.ps1` | 正则校验 Conventional Commits | <0.5s |
| `prepare-commit-msg` | `.claude/git-hooks/prepare-commit-msg.ps1` | 预填充分支名/ticket | <0.5s |

**Windows 兼容方案**:
```
.git/hooks/pre-commit         ← batch wrapper
.git/hooks/commit-msg          ← batch wrapper
.git/hooks/prepare-commit-msg  ← batch wrapper
```

### 层 2: Claude Code Hooks (skill 集成)

通过 `.claude/settings.json` 的 `hooks.PreToolUse` 配置，在 Claude Code 中执行 git 命令时触发增强。

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["action"],
  "properties": {
    "action": {
      "type": "string",
      "enum": ["install", "uninstall", "status", "configure"],
      "description": "操作类型"
    },
    "hooks": {
      "type": "array",
      "items": { "type": "string", "enum": ["pre-commit", "commit-msg", "prepare-commit-msg", "all"] },
      "description": "目标 hook 列表"
    },
    "layer": {
      "type": "string",
      "enum": ["git", "claude-code", "both"],
      "default": "both",
      "description": "安装层"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "installed_hooks": { "type": "array", "items": { "type": "string" } },
    "status_report": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "hook": { "type": "string" },
          "installed": { "type": "boolean" },
          "layer": { "type": "string" },
          "script_path": { "type": "string" }
        }
      }
    },
    "messages": { "type": "array", "items": { "type": "string" } }
  }
}
```

## 执行流程

### install 操作

1. 创建 `.claude/git-hooks/` 目录
2. 生成 PowerShell 脚本
3. 生成 batch wrapper 到 `.git/hooks/`
4. 验证 hook 可执行

### status 操作

1. 检查 `.git/hooks/` 下已安装的 hooks
2. 检查 `.claude/git-hooks/` 下的脚本
3. 检查 Claude Code hooks 配置
4. 报告状态

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| git-commander | 被调用 | 接收路由 |
| sensitive-file-detector | 互补 | pre-commit hook 做轻量版敏感检测 |
| conventional-commit-validator | 互补 | commit-msg hook 做轻量版格式校验 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 安装成功 | hook 安装后可正确执行 | 100% |
| 兼容性 | Windows/macOS/Linux 均可运行 | 100% |
| 幂等安装 | 重复安装不产生副作用 | 100% |
| 卸载完整 | 卸载后无残留文件 | 100% |
