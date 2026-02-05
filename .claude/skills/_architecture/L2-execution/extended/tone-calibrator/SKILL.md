---
name: tone-calibrator
description: >
  语气校准器 Skill (L2 Extended)。校准和调整内容的语气风格，确保语气一致性。
  当需要：(1) 调整内容语气，(2) 统一风格，(3) 适应不同受众时触发。
  支持多种语气风格和细粒度调整。作为扩展写作 Skill，具有标准契约。
---

# Tone Calibrator — 语气校准器

## 触发条件

- 写作任务中包含"调整语气"、"改变风格"、"更加...的语气"等关键词
- 由 writing-orchestrator 调度（Stage 3，可选）
- 需要确保内容语气一致或适应特定受众

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["content", "target_tone"],
  "properties": {
    "content": {
      "type": "string",
      "description": "待校准内容"
    },
    "target_tone": {
      "type": "object",
      "required": ["primary"],
      "properties": {
        "primary": {
          "type": "string",
          "enum": ["professional", "casual", "humorous", "inspirational", "educational", "empathetic", "authoritative", "friendly"],
          "description": "主要语气"
        },
        "secondary": {
          "type": "string",
          "description": "次要语气特征"
        },
        "formality_level": {
          "type": "integer",
          "minimum": 1,
          "maximum": 5,
          "default": 3,
          "description": "正式度 1-5"
        },
        "energy_level": {
          "type": "integer",
          "minimum": 1,
          "maximum": 5,
          "default": 3,
          "description": "活力度 1-5"
        }
      },
      "description": "目标语气"
    },
    "calibration_config": {
      "type": "object",
      "properties": {
        "preserve_meaning": {
          "type": "boolean",
          "default": true
        },
        "adjustment_strength": {
          "type": "string",
          "enum": ["subtle", "moderate", "strong"],
          "default": "moderate"
        },
        "focus_areas": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["vocabulary", "sentence_structure", "punctuation", "expressions"]
          }
        }
      },
      "description": "校准配置"
    },
    "context": {
      "type": "object",
      "properties": {
        "platform": { "type": "string" },
        "audience": { "type": "string" },
        "brand_voice": { "type": "string" }
      },
      "description": "上下文信息"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["calibrated_content", "tone_analysis"],
  "properties": {
    "calibrated_content": {
      "type": "string",
      "description": "校准后内容"
    },
    "tone_analysis": {
      "type": "object",
      "properties": {
        "before": {
          "type": "object",
          "properties": {
            "detected_tone": { "type": "string" },
            "formality_score": { "type": "number" },
            "energy_score": { "type": "number" },
            "consistency_score": { "type": "number" }
          }
        },
        "after": {
          "type": "object",
          "properties": {
            "achieved_tone": { "type": "string" },
            "formality_score": { "type": "number" },
            "energy_score": { "type": "number" },
            "consistency_score": { "type": "number" }
          }
        },
        "changes_summary": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "area": { "type": "string" },
              "original": { "type": "string" },
              "calibrated": { "type": "string" },
              "reason": { "type": "string" }
            }
          }
        }
      },
      "description": "语气分析"
    },
    "consistency_report": {
      "type": "object",
      "properties": {
        "overall_consistency": { "type": "number" },
        "inconsistent_sections": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "location": { "type": "string" },
              "issue": { "type": "string" },
              "suggestion": { "type": "string" }
            }
          }
        }
      },
      "description": "一致性报告"
    }
  }
}
```

## 语气维度

### 正式度谱系
```
1 (非正式) ←──────────→ 5 (正式)
口语化        中性        书面语
"超棒"      "很好"      "优秀"
```

### 活力度谱系
```
1 (平静) ←──────────→ 5 (激昂)
沉稳        中性        热情
"可以考虑"  "建议尝试"  "强烈推荐！"
```

## 语气风格对照

| 语气 | 特征 | 典型词汇 | 适用场景 |
|------|------|---------|---------|
| professional | 专业、克制 | 表明、建议、认为 | 商务、报告 |
| casual | 轻松、亲切 | 其实、感觉、蛮 | 社交媒体 |
| humorous | 幽默、调侃 | 哈哈、绝了、笑死 | 娱乐内容 |
| inspirational | 励志、鼓舞 | 相信、勇敢、突破 | 成长类 |
| educational | 清晰、耐心 | 首先、简单说、举例 | 教程 |
| empathetic | 理解、温暖 | 理解、明白、不容易 | 情感类 |
| authoritative | 权威、自信 | 必须、毫无疑问、事实 | 专家观点 |
| friendly | 友好、平等 | 一起、咱们、分享 | 社群内容 |

## 校准策略

### 词汇替换
```
正式化:
  好 → 优秀
  说 → 表示、阐述
  很多 → 大量、众多

口语化:
  优秀 → 超棒
  表示 → 说
  大量 → 超多
```

### 句式调整
```
正式化:
  "我觉得这个方法很有用" → "该方法具有较高实用价值"

口语化:
  "该方法具有较高实用价值" → "这方法真的超好用"
```

### 语气词调整
```
增加活力: 添加 "！"、"真的"、"超"
降低活力: 移除感叹号、减少副词
```

## 执行流程

1. **语气检测**
   - 分析当前语气
   - 计算各维度得分

2. **差距分析**
   - 对比目标语气
   - 识别调整点

3. **分层校准**
   - 词汇层面调整
   - 句式层面调整
   - 标点层面调整

4. **一致性检查**
   - 验证全文语气统一
   - 标记不一致处

5. **质量验证**
   - 确保语义保留
   - 确认风格达标

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| writing-orchestrator | 由其调度 |
| platform-adapter | 协同工作 |
| narrative-builder | 校准其输出 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 语义保留 | 意思不变 | ≥95% |
| 目标匹配 | 达到目标语气 | ≥80% |
| 一致性 | 全文语气统一 | ≥90% |

## 脚本

- `scripts/calibrate_tone.py` - 语气校准主脚本
- `scripts/tone_analyzer.py` - 语气分析器
- `scripts/vocabulary_mapper.py` - 词汇映射器

## 参考资料

- `references/tone-vocabulary.md` - 语气词汇库
- `references/style-guide.md` - 风格指南
