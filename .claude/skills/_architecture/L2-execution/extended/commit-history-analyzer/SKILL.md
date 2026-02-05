---
name: commit-history-analyzer
description: >
  提交历史分析器 Skill。分析 Git 提交历史趋势、识别代码热点、生成贡献者统计和分支健康报告。
  当需要：(1) 提交趋势分析，(2) 代码热点识别，(3) 贡献者统计，(4) 分支健康评估时触发。
  支持时间范围过滤和多维度分析。作为扩展分支管理 Skill，具有标准契约。
---

# Commit History Analyzer — 提交历史分析器

## 触发条件

- 分支管理流程的第三步
- 由 branch-orchestrator 调度
- 需要了解仓库活跃度和健康状态时
- 代码审计或团队效能分析时

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["branch"],
  "properties": {
    "branch": {
      "type": "string",
      "description": "分析的目标分支"
    },
    "date_range": {
      "type": "object",
      "properties": {
        "start": { "type": "string", "format": "date", "description": "开始日期" },
        "end": { "type": "string", "format": "date", "description": "结束日期" }
      },
      "description": "分析时间范围，默认最近 90 天"
    },
    "analysis_type": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["trends", "hotspots", "contributors", "branch_health", "all"]
      },
      "default": ["all"],
      "description": "分析类型列表"
    },
    "hotspot_threshold": {
      "type": "integer",
      "default": 10,
      "description": "文件变更次数达到此阈值视为热点"
    },
    "include_merge_commits": {
      "type": "boolean",
      "default": false,
      "description": "是否包含合并提交"
    },
    "branch_list": {
      "type": "array",
      "items": { "type": "string" },
      "description": "分支健康分析时的分支列表（来自 branch-validator）"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["trends", "hotspots", "contributor_stats", "branch_health_report"],
  "properties": {
    "trends": {
      "type": "object",
      "properties": {
        "commit_frequency": {
          "type": "object",
          "properties": {
            "daily_avg": { "type": "number" },
            "weekly_avg": { "type": "number" },
            "peak_day": { "type": "string" },
            "trend_direction": {
              "type": "string",
              "enum": ["increasing", "stable", "decreasing"]
            }
          },
          "description": "提交频率趋势"
        },
        "file_churn": {
          "type": "object",
          "properties": {
            "total_files_changed": { "type": "integer" },
            "avg_files_per_commit": { "type": "number" },
            "churn_rate": { "type": "number", "description": "代码翻转率" }
          },
          "description": "文件变更趋势"
        },
        "size_trend": {
          "type": "object",
          "properties": {
            "avg_additions": { "type": "number" },
            "avg_deletions": { "type": "number" },
            "avg_commit_size": {
              "type": "string",
              "enum": ["small", "medium", "large"]
            }
          },
          "description": "提交规模趋势"
        },
        "timeline": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "period": { "type": "string" },
              "commits": { "type": "integer" },
              "contributors": { "type": "integer" }
            }
          },
          "description": "时间线数据"
        }
      },
      "description": "提交趋势分析"
    },
    "hotspots": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["file", "change_count", "risk_level"],
        "properties": {
          "file": { "type": "string", "description": "文件路径" },
          "change_count": { "type": "integer", "description": "变更次数" },
          "unique_contributors": { "type": "integer", "description": "独立贡献者数" },
          "avg_change_size": { "type": "number", "description": "平均变更规模" },
          "risk_level": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
            "description": "风险等级"
          },
          "last_changed": { "type": "string", "format": "date-time" },
          "recommendation": { "type": "string", "description": "改进建议" }
        }
      },
      "description": "代码热点列表（按变更频率排序）"
    },
    "contributor_stats": {
      "type": "object",
      "properties": {
        "total_contributors": { "type": "integer" },
        "active_contributors": { "type": "integer", "description": "分析周期内有提交的贡献者" },
        "top_contributors": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "commits": { "type": "integer" },
              "additions": { "type": "integer" },
              "deletions": { "type": "integer" },
              "files_touched": { "type": "integer" },
              "primary_areas": { "type": "array", "items": { "type": "string" } }
            }
          },
          "description": "排名靠前的贡献者"
        },
        "bus_factor": {
          "type": "integer",
          "description": "巴士因子（关键人员数量）"
        },
        "knowledge_distribution": {
          "type": "string",
          "enum": ["concentrated", "moderate", "distributed"],
          "description": "知识分布状态"
        }
      },
      "description": "贡献者统计"
    },
    "branch_health_report": {
      "type": "object",
      "properties": {
        "overall_health": {
          "type": "string",
          "enum": ["excellent", "good", "fair", "poor", "critical"]
        },
        "metrics": {
          "type": "object",
          "properties": {
            "merge_frequency": { "type": "number", "description": "合并频率（次/周）" },
            "avg_branch_lifetime": { "type": "number", "description": "分支平均生命周期（天）" },
            "stale_ratio": { "type": "number", "description": "过期分支占比" },
            "conflict_rate": { "type": "number", "description": "冲突率" }
          }
        },
        "recommendations": {
          "type": "array",
          "items": { "type": "string" },
          "description": "改进建议"
        },
        "risk_areas": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "area": { "type": "string" },
              "risk": { "type": "string" },
              "suggestion": { "type": "string" }
            }
          },
          "description": "风险区域"
        }
      },
      "description": "分支健康报告"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analyzed_commits": { "type": "integer" },
        "date_range_actual": { "type": "object" },
        "analysis_duration": { "type": "string" }
      }
    }
  }
}
```

## 执行流程

1. **历史数据采集**
   - 执行 `git log` 获取指定范围内的提交记录
   - 解析提交元数据（作者、时间、文件变更、行数）
   - 过滤合并提交（可选）

2. **趋势分析**
   - 按时间段聚合提交频率
   - 计算代码翻转率
   - 识别提交规模趋势
   - 生成时间线数据

3. **热点识别**
   - 统计每个文件的变更频次
   - 计算独立贡献者数
   - 评估风险等级
   - 生成改进建议

4. **贡献者分析**
   - 统计每位贡献者的提交量和代码量
   - 计算巴士因子
   - 评估知识分布状态
   - 识别关键人员

5. **健康评估**
   - 综合分支存活、合并频率、冲突率等指标
   - 评估整体健康状态
   - 生成改进建议和风险提示

## 热点风险分级

| 等级 | 条件 | 含义 |
|------|------|------|
| critical | 变更 >50 次，贡献者 1 人 | 高频变更且单点依赖 |
| high | 变更 >30 次，贡献者 <=2 人 | 高频变更且知识集中 |
| medium | 变更 >10 次 | 中等频率变更 |
| low | 变更 <=10 次 | 正常变更频率 |

## 分支健康等级

| 等级 | 条件 |
|------|------|
| excellent | 无过期分支，冲突率 <5%，合并频繁 |
| good | 少量过期分支，冲突率 <10% |
| fair | 部分过期，冲突率 <20% |
| poor | 大量过期，冲突率 >20% |
| critical | 过半数过期，频繁冲突 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 覆盖指定范围内所有提交 | 100% |
| 准确性 | 统计数据正确 | >=99% |
| 可操作性 | 每个风险项有改进建议 | >=80% |
| 时效性 | 分析结果反映最新状态 | 数据延迟 <1 天 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| branch-validator | 接收其输出 | 使用分支列表和状态数据 |
| branch-orchestrator | 由其调度 | Step 3 |
| diff-analyzer | 可复用 | 解析变更统计 |
| commit-message-gen | 互补 | 共享提交历史分析 |

## 脚本

- `scripts/analyze_history.py` - 历史分析主脚本
- `scripts/hotspot_detector.py` - 热点检测器
- `scripts/contributor_analyzer.py` - 贡献者分析器
- `scripts/health_reporter.py` - 健康报告生成器

## 参考资料

- `references/git-metrics.md` - Git 指标说明
- `references/health-criteria.md` - 健康评估标准
- `references/bus-factor.md` - 巴士因子计算方法
