---
name: commit-history-analyzer
description: >
  提交历史分析器。分析提交历史趋势、识别代码热点、生成贡献者统计和分支健康报告。
  由 branch-orchestrator 在 Step 3 调度。
---

# Commit History Analyzer — 提交历史分析器

> 详细文档: [_architecture/L2-execution/extended/commit-history-analyzer/SKILL.md](_architecture/L2-execution/extended/commit-history-analyzer/SKILL.md)

## 执行流程

1. **历史数据采集**: 执行 `git log` 获取指定范围内提交记录，解析元数据
2. **趋势分析**: 按时间段聚合提交频率，计算代码翻转率，识别提交规模趋势
3. **热点识别**: 统计文件变更频次，评估风险等级（critical / high / medium / low）
4. **贡献者分析**: 统计提交量/代码量，计算巴士因子，评估知识分布
5. **健康评估**: 综合指标生成分支健康等级（excellent ~ critical）和改进建议

## 分析维度

| 维度 | 输出 |
|------|------|
| trends | 提交频率、文件变更、规模趋势、时间线 |
| hotspots[] | 高频变更文件、风险等级、改进建议 |
| contributor_stats | 贡献者排名、巴士因子、知识分布 |
| branch_health_report | 健康等级、合并频率、过期比率、冲突率 |

## 热点风险分级

| 等级 | 条件 |
|------|------|
| critical | 变更 >50 次，单人维护 |
| high | 变更 >30 次，<=2 人维护 |
| medium | 变更 >10 次 |
| low | 变更 <=10 次 |

## 用户任务

$ARGUMENTS
