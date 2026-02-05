---
name: branch-validator
description: >
  分支验证器。验证分支命名规范、检测过期分支、检查合并冲突、保护关键分支。
  由 branch-orchestrator 调度，配置来源 .claude/git-config.json。
---

# Branch Validator — 分支验证器

> 详细文档: [_architecture/L2-execution/core/branch-validator/SKILL.md](_architecture/L2-execution/core/branch-validator/SKILL.md)

## 执行流程

1. **加载配置**: 从 `.claude/git-config.json` 读取命名模式和保护列表
2. **命名合规检查**: 对每个分支名匹配 `naming_pattern` 正则，记录违规并生成建议
3. **过期检测**: 计算存活天数，与 `max_age_days` 比较，分级建议 delete / archive / review
4. **冲突预检**: 对活跃分支执行 merge-tree 预检，识别冲突文件和严重度
5. **保护验证**: 确认保护分支存在，标记保护状态，阻止删除操作

## 输出结构

| 字段 | 说明 |
|------|------|
| branches[] | 每个分支的验证结果和状态 |
| naming_violations[] | 命名违规详情和推荐名称 |
| stale_branches[] | 过期分支及处理建议 |
| conflicts[] | 合并冲突列表及严重度 |
| protected_status | 受保护分支状态映射 |

## 过期分级

| 年龄 | 建议 |
|------|------|
| > 90 天 | 直接删除 |
| 60-90 天 | 归档或删除 |
| 30-60 天 | 人工审查 |
| < 30 天 | 正常 |

## 用户任务

$ARGUMENTS
