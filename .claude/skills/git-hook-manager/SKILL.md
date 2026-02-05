---
name: git-hook-manager
description: >
  Git Hook 管理器。安装和管理 git hooks + Claude Code hooks。
  支持 Windows PowerShell 兼容方案。
---

# Git Hook Manager — Hook 管理器

> 详细文档: [_architecture/L2-execution/extended/git-hook-manager/SKILL.md](_architecture/L2-execution/extended/git-hook-manager/SKILL.md)

## 执行流程

### install — 安装 hooks

1. 创建 `.claude/git-hooks/` 目录
2. 生成以下 PowerShell 脚本:
   - `pre-commit.ps1` — 正则匹配敏感文件（.env, .pem, credentials 等）
   - `commit-msg.ps1` — 正则校验 Conventional Commits 格式
   - `prepare-commit-msg.ps1` — 从分支名预填充 type/scope
3. 在 `.git/hooks/` 生成 batch wrapper:
   ```batch
   @echo off
   powershell -ExecutionPolicy Bypass -File "%~dp0..\..\..\.claude\git-hooks\%~n0.ps1" %*
   exit /b %errorlevel%
   ```
4. 验证安装成功

### uninstall — 卸载 hooks

1. 删除 `.git/hooks/` 中的 wrapper 文件
2. 保留 `.claude/git-hooks/` 中的脚本（备用）

### status — 查看状态

列出所有 hook 的安装状态：
- Git hooks (pre-commit, commit-msg, prepare-commit-msg)
- Claude Code hooks (PreToolUse)

### configure — 配置

修改 hook 行为参数（如敏感文件模式、commit 格式规则）。

## 用户任务

$ARGUMENTS

---

请按指定操作管理 git hooks。
