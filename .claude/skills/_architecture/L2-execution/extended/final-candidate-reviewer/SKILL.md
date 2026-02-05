---
name: final-candidate-reviewer
description: >
  最终候选评审器 Skill。对未被攻击的方案执行 Critical 缺陷检查，确保所有最终候选
  都经过同等严格的审视。当 Round 3 对第一名攻击后需要检查其他候选时触发。
  作为扩展评审 Skill，具有标准契约。
---

# Final Candidate Reviewer — 最终候选评审器

## 触发条件

- Round 3 对第一名执行对抗评审后
- 需要确保其他候选同等严格审视
- 由 multi-round-eval-orchestrator 调度

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["candidates", "critical_checklist"],
  "properties": {
    "candidates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "path"],
        "properties": {
          "name": { "type": "string" },
          "path": { "type": "string" },
          "current_rank": { "type": "integer" },
          "known_defects": {
            "type": "array",
            "items": { "type": "object" }
          },
          "was_attacked": {
            "type": "boolean",
            "default": false
          }
        }
      },
      "description": "待检查的候选方案"
    },
    "critical_checklist": {
      "type": "array",
      "items": { "type": "string" },
      "default": [
        "是否存在使方案完全无法工作的致命缺陷？",
        "是否存在无法接受的安全风险？",
        "是否存在严重的扩展性限制？",
        "是否存在不可逾越的技术债务？",
        "是否存在关键的外部依赖风险？"
      ],
      "description": "Critical 缺陷检查项"
    },
    "comparison_baseline": {
      "type": "object",
      "properties": {
        "attacked_candidate": { "type": "string" },
        "attack_findings": { "type": "array" }
      },
      "description": "对比基准（已被攻击的方案）"
    },
    "review_depth": {
      "type": "string",
      "enum": ["quick", "standard", "thorough"],
      "default": "standard",
      "description": "检查深度"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["review_results", "summary"],
  "properties": {
    "review_results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["candidate", "checklist_results", "judgment"],
        "properties": {
          "candidate": { "type": "string" },
          "checklist_results": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "check_item": { "type": "string" },
                "result": {
                  "type": "string",
                  "enum": ["pass", "warning", "fail"]
                },
                "findings": { "type": "array", "items": { "type": "string" } },
                "severity": { "type": "string" }
              }
            }
          },
          "critical_defects_found": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "description": { "type": "string" },
                "severity": { "type": "string" },
                "evidence": { "type": "string" },
                "comparable_to_baseline": { "type": "boolean" }
              }
            }
          },
          "judgment": {
            "type": "object",
            "properties": {
              "status": {
                "type": "string",
                "enum": ["qualified", "needs_mitigation", "disqualified"]
              },
              "confidence": { "type": "string" },
              "reasoning": { "type": "string" }
            }
          },
          "comparison_with_baseline": {
            "type": "object",
            "properties": {
              "relative_risk": {
                "type": "string",
                "enum": ["lower", "similar", "higher"]
              },
              "unique_advantages": { "type": "array", "items": { "type": "string" } },
              "unique_risks": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      },
      "description": "各候选的评审结果"
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_reviewed": { "type": "integer" },
        "qualified_count": { "type": "integer" },
        "disqualified_count": { "type": "integer" },
        "needs_mitigation_count": { "type": "integer" },
        "qualified_list": { "type": "array", "items": { "type": "string" } },
        "recommended_next_first": { "type": "string" }
      },
      "description": "评审摘要"
    }
  }
}
```

## 检查项说明

| 检查项 | 目标 | 失败条件 |
|--------|------|---------|
| 致命缺陷 | 发现使方案无法工作的问题 | 存在无法修复的致命问题 |
| 安全风险 | 评估安全隐患 | 存在高危安全漏洞 |
| 扩展性限制 | 检查规模增长时的限制 | 无法满足目标规模 |
| 技术债务 | 评估难以偿还的债务 | 债务超过可接受阈值 |
| 外部依赖 | 检查第三方风险 | 关键依赖不可控 |

## 执行流程

1. **候选筛选**
   - 识别未被攻击的候选
   - 按当前排名排序

2. **逐项检查**
   - 对每个候选执行检查清单
   - 记录发现和证据

3. **对比分析**
   - 与已被攻击方案对比
   - 评估相对风险

4. **判定生成**
   - 综合检查结果
   - 给出资格判定

## 判定等级

| 等级 | 定义 | 后续处理 |
|------|------|---------|
| qualified | 通过所有检查 | 可进入最终轮 |
| needs_mitigation | 有问题但可缓解 | 需记录缓解措施 |
| disqualified | 存在 Critical 缺陷 | 被淘汰 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 检查所有检查项 | 100% |
| 一致性 | 使用与攻击相同的标准 | 100% |
| 公平性 | 所有候选同等对待 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| devils-advocate | 使用类似检查标准 |
| defect-analyzer | 复用缺陷分类 |
| consensus-builder | 输出参与最终共识 |
| multi-round-eval-orchestrator | 由其调度 |

## 脚本

- `scripts/review_candidates.py` - 候选评审主脚本
- `scripts/checklist_executor.py` - 检查清单执行器
- `scripts/comparison_analyzer.py` - 对比分析器

## 参考资料

- `references/critical-checklist.md` - Critical 检查清单详解
- `references/qualification-criteria.md` - 资格判定标准
