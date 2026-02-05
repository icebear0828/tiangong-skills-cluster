---
name: tone-calibrator
description: >
  语气校准 Skill。分析和调整内容语气风格，支持专业、轻松、幽默、
  励志、教育等多种目标语气。
---

# Tone Calibrator — 语气校准

> 详细文档: [_architecture/L2-execution/extended/tone-calibrator/SKILL.md](_architecture/L2-execution/extended/tone-calibrator/SKILL.md)

## 执行协议

### 支持的语气

| 语气 | 特征 | 适用 |
|------|------|------|
| professional | 正式、严谨 | 行业报告、B端 |
| casual | 轻松、亲切 | 小红书、生活类 |
| humorous | 幽默、诙谐 | 娱乐、段子类 |
| inspirational | 励志、鼓舞 | 个人成长类 |
| educational | 教学、客观 | 科普、教程类 |

### 输出

- 校准后内容
- 语气分析报告 (原始 vs 目标 vs 实际)

## 校准任务

$ARGUMENTS

---

请分析内容当前语气，按目标语气校准，输出调整后版本和分析报告。
