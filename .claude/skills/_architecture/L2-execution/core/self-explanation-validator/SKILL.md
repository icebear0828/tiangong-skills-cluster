---
name: self-explanation-validator
description: >
  自我解释验证器 Skill。验证学习者的自我解释是否正确，识别误解并提供改进建议。
  当需要：(1) 检验学习者理解，(2) 识别知识盲点，(3) 反向图灵测试时触发。
  支持多维度评估、误解识别、针对性反馈。作为核心学习 Skill，具有严格契约。
---

# Self-Explanation Validator — 自我解释验证器

## 触发条件

- 学习任务中包含"检验理解"、"验证"、"测试掌握"等关键词
- 由 verification-orchestrator 调度
- 学习者提交自我解释后

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["learner_explanation", "reference_explanation"],
  "properties": {
    "learner_explanation": {
      "type": "object",
      "required": ["concept", "explanation"],
      "properties": {
        "concept": { "type": "string" },
        "explanation": {
          "type": "string",
          "description": "学习者的解释"
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "学习者自评置信度"
        },
        "format": {
          "type": "string",
          "enum": ["text", "diagram", "code", "example"],
          "default": "text"
        }
      },
      "description": "学习者的自我解释"
    },
    "reference_explanation": {
      "type": "object",
      "properties": {
        "concept": { "type": "string" },
        "definition": { "type": "string" },
        "key_points": {
          "type": "array",
          "items": { "type": "string" }
        },
        "common_misconceptions": {
          "type": "array",
          "items": { "type": "string" }
        },
        "examples": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "参考解释"
    },
    "validation_config": {
      "type": "object",
      "properties": {
        "strictness": {
          "type": "string",
          "enum": ["lenient", "standard", "strict"],
          "default": "standard"
        },
        "focus_areas": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["accuracy", "completeness", "clarity", "depth", "application"]
          },
          "default": ["accuracy", "completeness"]
        },
        "provide_hints": {
          "type": "boolean",
          "default": true
        }
      },
      "description": "验证配置"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["score", "assessment", "misconceptions", "improvements"],
  "properties": {
    "score": {
      "type": "object",
      "properties": {
        "overall": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "总分"
        },
        "by_dimension": {
          "type": "object",
          "properties": {
            "accuracy": { "type": "number" },
            "completeness": { "type": "number" },
            "clarity": { "type": "number" },
            "depth": { "type": "number" },
            "application": { "type": "number" }
          },
          "description": "各维度得分"
        },
        "mastery_level": {
          "type": "string",
          "enum": ["mastered", "proficient", "developing", "beginning", "misconceived"],
          "description": "掌握等级"
        }
      },
      "description": "评分结果"
    },
    "assessment": {
      "type": "object",
      "properties": {
        "correct_points": {
          "type": "array",
          "items": { "type": "string" },
          "description": "正确的要点"
        },
        "missing_points": {
          "type": "array",
          "items": { "type": "string" },
          "description": "缺失的要点"
        },
        "partially_correct": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "point": { "type": "string" },
              "issue": { "type": "string" },
              "correction": { "type": "string" }
            }
          },
          "description": "部分正确的内容"
        },
        "feedback_summary": {
          "type": "string",
          "description": "反馈总结"
        }
      },
      "description": "评估详情"
    },
    "misconceptions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["description", "severity", "correction"],
        "properties": {
          "id": { "type": "string" },
          "description": { "type": "string" },
          "severity": {
            "type": "string",
            "enum": ["critical", "moderate", "minor"]
          },
          "detected_text": { "type": "string" },
          "correction": { "type": "string" },
          "root_cause": { "type": "string" },
          "remediation": { "type": "string" }
        }
      },
      "description": "识别的误解"
    },
    "improvements": {
      "type": "object",
      "properties": {
        "suggestions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "改进建议"
        },
        "learning_resources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "description": { "type": "string" },
              "target_gap": { "type": "string" }
            }
          },
          "description": "推荐学习资源"
        },
        "practice_exercises": {
          "type": "array",
          "items": { "type": "string" },
          "description": "建议练习"
        },
        "follow_up_questions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "后续思考问题"
        }
      },
      "description": "改进建议"
    },
    "calibration": {
      "type": "object",
      "properties": {
        "learner_confidence": { "type": "number" },
        "actual_accuracy": { "type": "number" },
        "calibration_gap": { "type": "number" },
        "calibration_advice": { "type": "string" }
      },
      "description": "元认知校准"
    }
  }
}
```

## 评估维度

| 维度 | 定义 | 评分标准 |
|------|------|---------|
| accuracy | 准确性 | 概念理解是否正确 |
| completeness | 完整性 | 是否覆盖所有要点 |
| clarity | 清晰度 | 表述是否清晰 |
| depth | 深度 | 理解是否深入 |
| application | 应用 | 能否正确应用 |

## 掌握等级

| 等级 | 分数范围 | 描述 |
|------|---------|------|
| mastered | ≥90 | 完全掌握 |
| proficient | 75-89 | 熟练 |
| developing | 60-74 | 发展中 |
| beginning | 40-59 | 初步理解 |
| misconceived | <40 | 存在严重误解 |

## 误解严重度

| 等级 | 定义 | 处理 |
|------|------|------|
| critical | 根本性错误理解 | 必须立即纠正 |
| moderate | 部分错误或遗漏 | 需要澄清 |
| minor | 表述不精确 | 建议改进 |

## 执行流程

1. **解析输入**
   - 提取学习者解释的关键点
   - 加载参考解释

2. **对比分析**
   - 逐点比较准确性
   - 检查完整性
   - 评估清晰度

3. **误解检测**
   - 匹配常见误解模式
   - 识别概念混淆
   - 分析错误根源

4. **评分计算**
   - 各维度评分
   - 加权汇总
   - 确定掌握等级

5. **反馈生成**
   - 撰写反馈总结
   - 提供改进建议
   - 推荐学习资源

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 公正性 | 评分标准一致 | 100% |
| 建设性 | 反馈有助改进 | 100% |
| 精确性 | 误解识别准确 | ≥90% |
| 完整性 | 覆盖所有要点 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| analogy-explainer | 接收其生成的类比作为参考 |
| socratic-questioner | 与其协作深化理解 |
| knowledge-extractor | 使用其提取的知识点 |
| verification-orchestrator | 由其调度 |
| learning-orchestrator | 间接关联 |

## 脚本

- `scripts/validate.py` - 验证主脚本
- `scripts/misconception_detector.py` - 误解检测器
- `scripts/feedback_generator.py` - 反馈生成器

## 参考资料

- `references/validation-rubrics.md` - 验证评分标准
- `references/common-misconceptions.md` - 常见误解库
- `references/remediation-strategies.md` - 补救策略
