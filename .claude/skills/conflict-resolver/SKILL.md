---
name: conflict-resolver
description: >
  冲突解决器。分析分支间合并冲突，提供智能解决方案，区分自动可解决和需人工介入的冲突。
  可调用 refactor skill 处理复杂结构冲突。由 branch-orchestrator 条件调度。
---

# Conflict Resolver — 冲突解决器

> 详细文档: [_architecture/L2-execution/core/conflict-resolver/SKILL.md](_architecture/L2-execution/core/conflict-resolver/SKILL.md)

## 执行流程

1. **冲突分类**: 解析冲突文件类型（content / rename / delete / mode / structural）
2. **逐文件分析**: 对比三方内容（base / ours / theirs），分析冲突根因和严重度
3. **解决方案生成**: trivial 自动合并，低复杂度智能合并，高复杂度标记人工或调用 refactor
4. **结构冲突检测**: 识别大规模重构导致的冲突，评估是否需 refactor skill
5. **风险评估**: 综合评估解决方案风险，输出置信度评分

## 冲突严重度

| 等级 | 示例 |
|------|------|
| trivial | 空白差异、注释变更 |
| low | 不同区域的独立修改 |
| medium | 同一函数的不同参数修改 |
| high | 同一逻辑的不同实现 |
| critical | 大规模重构 vs 功能添加 |

## 输出结构

| 字段 | 说明 |
|------|------|
| conflicts[] | 冲突详细分析（文件、类型、严重度） |
| resolutions[] | 解决方案（策略、合并内容、置信度） |
| auto_resolvable | 是否所有冲突均可自动解决 |
| refactor_needed | 是否需要调用 refactor skill |

## 用户任务

$ARGUMENTS
