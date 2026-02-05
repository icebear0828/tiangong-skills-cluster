---
name: branch-orchestrator
description: >
  分支管理编排器。编排分支验证→冲突解决→历史分析的完整分支管理流程。当需要：
  (1) 分支健康检查，(2) 批量分支管理，(3) 合并前预检，(4) 仓库维护时触发。
  采用黑板模式管理分支健康数据，支持条件分支和质量关卡。由 git-commander 或用户直接调度。
---

# Branch Orchestrator — 分支管理编排器

## 触发条件

- 用户执行分支管理任务时
- 由 git-commander 路由调度
- 定期分支健康检查
- PR 合并前的完整预检

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["repo_root"],
  "properties": {
    "repo_root": {
      "type": "string",
      "description": "仓库根目录路径"
    },
    "target_branch": {
      "type": "string",
      "default": "main",
      "description": "目标主分支"
    },
    "scope": {
      "type": "string",
      "enum": ["all", "active", "stale", "specific"],
      "default": "all",
      "description": "分析范围"
    },
    "specific_branches": {
      "type": "array",
      "items": { "type": "string" },
      "description": "scope=specific 时指定的分支列表"
    },
    "config_path": {
      "type": "string",
      "default": ".claude/git-config.json",
      "description": "Git 配置文件路径"
    },
    "analysis_options": {
      "type": "object",
      "properties": {
        "check_conflicts": { "type": "boolean", "default": true },
        "analyze_history": { "type": "boolean", "default": true },
        "date_range_days": { "type": "integer", "default": 90 },
        "hotspot_threshold": { "type": "integer", "default": 10 }
      },
      "description": "分析选项"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["validation_result", "overall_health"],
  "properties": {
    "validation_result": {
      "type": "object",
      "description": "来自 branch-validator 的验证结果"
    },
    "conflict_resolution": {
      "type": "object",
      "description": "来自 conflict-resolver 的冲突解决结果（条件输出）"
    },
    "history_analysis": {
      "type": "object",
      "description": "来自 commit-history-analyzer 的历史分析结果"
    },
    "overall_health": {
      "type": "object",
      "required": ["score", "level", "action_items"],
      "properties": {
        "score": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "综合健康分数"
        },
        "level": {
          "type": "string",
          "enum": ["excellent", "good", "fair", "poor", "critical"]
        },
        "action_items": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "priority": { "type": "string", "enum": ["high", "medium", "low"] },
              "action": { "type": "string" },
              "target": { "type": "string" }
            }
          },
          "description": "待办事项列表"
        }
      }
    },
    "execution_log": {
      "type": "object",
      "properties": {
        "steps_executed": { "type": "array", "items": { "type": "string" } },
        "steps_skipped": { "type": "array", "items": { "type": "string" } },
        "total_duration": { "type": "string" }
      }
    }
  }
}
```

## 编排流程

```
┌─────────────────────────────────────────────────────────┐
│  Branch Management Workflow                              │
│                                                         │
│  Step 1: 分支验证 (branch-validator)                    │
│  ├─ 加载 .claude/git-config.json 配置                   │
│  ├─ 验证分支命名合规                                     │
│  ├─ 检测过期分支                                         │
│  ├─ 检查合并冲突                                         │
│  ├─ 验证保护分支状态                                     │
│  └─ 输出 → blackboard.validation_result                 │
│                                                         │
│  ┌── Quality Gate: naming_compliance ──┐                │
│  │  检查: naming_violations.length == 0  │               │
│  │  失败: 生成违规报告，继续执行          │               │
│  └─────────────────────────────────────┘                │
│                                                         │
│  Step 2: 冲突解决 (conflict-resolver) [条件触发]         │
│  ├─ 条件: blackboard.validation_result.conflicts > 0    │
│  ├─ 分析每个冲突文件                                     │
│  ├─ 生成解决方案（自动/手动/重构）                        │
│  ├─ 如需重构 → 调用 refactor skill                      │
│  └─ 输出 → blackboard.conflict_resolution               │
│                                                         │
│  Step 3: 历史分析 (commit-history-analyzer)              │
│  ├─ 分析提交趋势                                         │
│  ├─ 识别代码热点                                         │
│  ├─ 生成贡献者统计                                       │
│  ├─ 生成分支健康报告                                     │
│  └─ 输出 → blackboard.history_analysis                  │
│                                                         │
│  汇总: 综合健康评估                                      │
│  ├─ 合并三步结果                                         │
│  ├─ 计算综合健康分数                                     │
│  └─ 生成优先级排序的待办事项                              │
└─────────────────────────────────────────────────────────┘
```

## 黑板模式 (Blackboard)

```json
{
  "meta_zone": {
    "repo_root": "",
    "target_branch": "main",
    "config": {},
    "branch_list": []
  },
  "data_zone": {
    "validation_result": null,
    "conflict_resolution": null,
    "history_analysis": null
  },
  "control_zone": {
    "current_step": "",
    "conflicts_detected": false,
    "naming_compliant": true,
    "quality_gates_passed": [],
    "steps_executed": [],
    "steps_skipped": []
  },
  "result_zone": {
    "overall_health": null,
    "action_items": []
  }
}
```

## 质量关卡

| 关卡 | 位置 | 检查项 | 失败处理 |
|------|------|--------|---------|
| naming_compliance | Step 1 后 | naming_violations 为空 | 记录违规，生成修复建议，继续执行 |
| conflict_severity | Step 2 后 | 无 critical 冲突 | 标记高优先级待办，发出警告 |
| health_threshold | Step 3 后 | 健康分数 >= 60 | 生成紧急改进计划 |

## 条件分支逻辑

| 条件 | 触发 | 说明 |
|------|------|------|
| `conflicts.length > 0` | 执行 Step 2 | 有冲突时才调用 conflict-resolver |
| `conflicts.length == 0` | 跳过 Step 2 | 无冲突直接进入 Step 3 |
| `refactor_needed == true` | 调用 refactor | conflict-resolver 判断需要重构时 |

## 健康分数计算

```
score = (naming_score * 0.2) + (staleness_score * 0.25) + (conflict_score * 0.3) + (activity_score * 0.25)

naming_score    = (1 - violations / total_branches) * 100
staleness_score = (1 - stale / total_branches) * 100
conflict_score  = (1 - conflicting / total_branches) * 100
activity_score  = 根据 commit-history-analyzer 的趋势指标计算
```

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| branch-validator | 调用 | Step 1 |
| conflict-resolver | 条件调用 | Step 2（有冲突时） |
| commit-history-analyzer | 调用 | Step 3 |
| refactor | 间接调用 | 由 conflict-resolver 按需触发 |
| diff-analyzer | 可复用 | 被子 skill 使用 |

## 蓝图引用

- Blueprint: `branch_management.json`
- Type: `static_linear`
- Platform: `git`

## 脚本

- `scripts/orchestrate_branch.py` - 分支编排主脚本
- `scripts/health_scorer.py` - 健康分数计算器
- `scripts/action_planner.py` - 待办事项规划器

## 参考资料

- `references/branch-workflow.md` - 分支管理工作流
- `references/health-scoring.md` - 健康评分标准
