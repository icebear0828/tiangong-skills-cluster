---
name: devils-advocate
description: >
  对抗评审员 Skill。专门攻击当前排名第一的方案，寻找致命缺陷。当需要：
  (1) 对抗性审视领先方案，(2) 挖掘隐藏风险，(3) 验证方案稳健性时触发。
  执行 7 个必答攻击问题，生成 Critical 缺陷清单。作为核心评审 Skill，具有严格契约。
---

# Devil's Advocate — 对抗评审员

## 触发条件

- 评审任务进入 Round 3 对抗评审阶段
- 由 multi-round-eval-orchestrator 调度
- 需要压力测试领先方案时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["target_plan", "attack_questions"],
  "properties": {
    "target_plan": {
      "type": "object",
      "required": ["name", "path"],
      "properties": {
        "name": { "type": "string" },
        "path": { "type": "string" },
        "content": { "type": "string" },
        "current_rank": { "type": "integer" },
        "existing_defects": {
          "type": "array",
          "items": { "type": "object" }
        }
      },
      "description": "攻击目标方案"
    },
    "attack_questions": {
      "type": "array",
      "minItems": 7,
      "items": { "type": "string" },
      "description": "必答攻击问题列表",
      "default": [
        "致命缺陷: 是否存在使其完全无法工作的问题？",
        "隐藏成本: 实施中可能出现哪些未预料的工作量？",
        "技术债务: 是否会引入难以偿还的技术债务？",
        "扩展瓶颈: 50+ Skill时是否仍可维护？",
        "外部依赖风险: API不可用时影响范围？",
        "测试盲区: 哪些部分最难测试？",
        "团队能力匹配: 是否需要不具备的技能？"
      ]
    },
    "context": {
      "type": "object",
      "properties": {
        "other_candidates": {
          "type": "array",
          "items": { "type": "string" }
        },
        "constraints": { "type": "array", "items": { "type": "string" } },
        "known_risks": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["target", "attack_report", "final_judgment"],
  "properties": {
    "target": {
      "type": "string",
      "description": "攻击目标方案名"
    },
    "attack_report": {
      "type": "object",
      "required": [
        "fatal_defects",
        "hidden_costs",
        "tech_debt",
        "scaling_bottlenecks",
        "external_risks",
        "test_blind_spots",
        "team_skill_gaps"
      ],
      "properties": {
        "fatal_defects": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "description": { "type": "string" },
              "evidence": { "type": "string" },
              "impact": { "type": "string" }
            }
          },
          "description": "致命缺陷列表"
        },
        "hidden_costs": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "description": { "type": "string" },
              "estimated_effort": { "type": "string" },
              "when_discovered": { "type": "string" }
            }
          },
          "description": "隐藏成本列表"
        },
        "tech_debt": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "description": { "type": "string" },
              "interest_rate": { "type": "string" },
              "repayment_difficulty": { "type": "string" }
            }
          },
          "description": "技术债务列表"
        },
        "scaling_bottlenecks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "description": { "type": "string" },
              "threshold": { "type": "string" },
              "mitigation": { "type": "string" }
            }
          },
          "description": "扩展瓶颈列表"
        },
        "external_risks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "description": { "type": "string" },
              "probability": { "type": "string" },
              "impact_scope": { "type": "string" }
            }
          },
          "description": "外部依赖风险列表"
        },
        "test_blind_spots": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "description": { "type": "string" },
              "reason": { "type": "string" },
              "risk_level": { "type": "string" }
            }
          },
          "description": "测试盲区列表"
        },
        "team_skill_gaps": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "skill": { "type": "string" },
              "current_level": { "type": "string" },
              "required_level": { "type": "string" }
            }
          },
          "description": "团队能力缺口列表"
        }
      }
    },
    "final_judgment": {
      "type": "object",
      "required": ["recommendation", "critical_defect_count", "confidence"],
      "properties": {
        "recommendation": {
          "type": "string",
          "enum": ["eliminate", "continue", "require_mitigation"],
          "description": "最终建议"
        },
        "critical_defect_count": {
          "type": "integer",
          "minimum": 0,
          "description": "Critical 级缺陷数量"
        },
        "confidence": {
          "type": "string",
          "pattern": "^(High|Medium|Low)\\s*\\(\\d+%\\)$",
          "description": "判断置信度，如 'High (92%)'"
        },
        "reasoning": {
          "type": "string",
          "description": "判断理由"
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "attack_intensity": {
          "type": "string",
          "enum": ["gentle", "moderate", "aggressive"]
        },
        "questions_answered": { "type": "integer" },
        "new_defects_found": { "type": "integer" }
      }
    }
  }
}
```

## 执行流程

1. **准备攻击**
   - 阅读目标方案
   - 了解已知缺陷
   - 制定攻击策略

2. **系统性攻击**
   - 逐个回答 7 个必答问题
   - 每个问题深挖至少 2 个潜在问题
   - 收集支持证据

3. **缺陷分级**
   - 评估每个发现的严重度
   - 识别 Critical 级缺陷
   - 判断是否致命

4. **最终裁决**
   - 综合所有发现
   - 给出淘汰/继续建议
   - 评估置信度

## 7 个必答攻击问题

| # | 问题 | 目标 |
|---|------|------|
| 1 | 致命缺陷 | 发现使方案完全失效的问题 |
| 2 | 隐藏成本 | 揭示未预料的工作量 |
| 3 | 技术债务 | 识别难以偿还的债务 |
| 4 | 扩展瓶颈 | 测试规模增长时的限制 |
| 5 | 外部依赖 | 评估第三方风险 |
| 6 | 测试盲区 | 找出难以测试的部分 |
| 7 | 能力匹配 | 检查团队技能缺口 |

## 攻击强度

| 强度 | 描述 | 适用场景 |
|------|------|---------|
| gentle | 温和质疑 | 明显领先的方案 |
| moderate | 中等压力 | 常规对抗评审 |
| aggressive | 激烈攻击 | 方案间差距小 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 7 个问题全部回答 | 100% |
| 深度 | 每个问题至少 2 个发现 | ≥85% |
| 客观性 | 攻击有证据支持 | ≥90% |
| 公正性 | 承认方案优势 | 必须 |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| defect-analyzer | 接收其发现的已知缺陷 |
| final-candidate-reviewer | 与其协作审查其他方案 |
| resurrection-evaluator | 可能触发方案复活 |
| consensus-builder | 输出参与最终共识 |

## 脚本

- `scripts/attack.py` - 对抗攻击主脚本
- `scripts/evidence_collector.py` - 证据收集器

## 参考资料

- `references/attack-patterns.md` - 攻击模式库
- `references/critical-criteria.md` - Critical 缺陷判定标准
