---
name: virality-scorer
description: >
  传播力评分器 Skill (L2 Core)。分析内容的病毒传播潜力，评估传播系数，优化互动元素。
  当需要：(1) 评估内容传播力，(2) 识别优化点，(3) 预测内容表现时触发。
  整合了病毒分析和互动优化功能。作为核心写作 Skill，具有严格契约。
---

# Virality Scorer — 传播力评分器

## 触发条件

- 写作任务中包含"评分"、"传播力"、"爆款分析"等关键词
- 由 writing-orchestrator 调度（Stage 2）
- 需要评估或优化内容传播潜力

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["content", "platform"],
  "properties": {
    "content": {
      "type": "object",
      "required": ["title", "body"],
      "properties": {
        "title": { "type": "string", "description": "标题" },
        "subtitle": { "type": "string", "description": "副标题" },
        "body": { "type": "string", "description": "正文内容" },
        "opening": { "type": "string", "description": "开头部分" },
        "cta": { "type": "string", "description": "行动召唤" }
      },
      "description": "待评估内容"
    },
    "platform": {
      "type": "string",
      "enum": ["xiaohongshu", "wechat", "twitter", "general"],
      "description": "目标平台"
    },
    "evaluation_config": {
      "type": "object",
      "properties": {
        "depth": {
          "type": "string",
          "enum": ["quick", "standard", "comprehensive"],
          "default": "standard",
          "description": "评估深度"
        },
        "include_optimization": {
          "type": "boolean",
          "default": true,
          "description": "是否包含优化建议"
        },
        "benchmark_category": {
          "type": "string",
          "description": "对标类目"
        }
      },
      "description": "评估配置"
    },
    "context": {
      "type": "object",
      "properties": {
        "content_type": {
          "type": "string",
          "enum": ["article", "post", "thread", "story", "tutorial"]
        },
        "target_audience": { "type": "string" },
        "competitor_benchmarks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": { "type": "string" },
              "engagement": { "type": "number" }
            }
          }
        }
      },
      "description": "评估上下文"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["overall_score", "dimension_scores"],
  "properties": {
    "overall_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "综合传播力评分"
    },
    "dimension_scores": {
      "type": "object",
      "properties": {
        "hook_appeal": {
          "type": "object",
          "properties": {
            "score": { "type": "number" },
            "weight": { "type": "number", "const": 0.25 },
            "analysis": { "type": "string" },
            "strengths": { "type": "array", "items": { "type": "string" } },
            "weaknesses": { "type": "array", "items": { "type": "string" } }
          },
          "description": "Hook 吸引力 (25%)"
        },
        "emotional_resonance": {
          "type": "object",
          "properties": {
            "score": { "type": "number" },
            "weight": { "type": "number", "const": 0.25 },
            "emotions_detected": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "emotion": { "type": "string" },
                  "intensity": { "type": "number" }
                }
              }
            },
            "analysis": { "type": "string" }
          },
          "description": "情感共鸣度 (25%)"
        },
        "social_currency": {
          "type": "object",
          "properties": {
            "score": { "type": "number" },
            "weight": { "type": "number", "const": 0.20 },
            "shareability_factors": { "type": "array", "items": { "type": "string" } },
            "analysis": { "type": "string" }
          },
          "description": "社交货币 (20%)"
        },
        "practical_value": {
          "type": "object",
          "properties": {
            "score": { "type": "number" },
            "weight": { "type": "number", "const": 0.15 },
            "value_elements": { "type": "array", "items": { "type": "string" } },
            "analysis": { "type": "string" }
          },
          "description": "实用价值 (15%)"
        },
        "discussion_potential": {
          "type": "object",
          "properties": {
            "score": { "type": "number" },
            "weight": { "type": "number", "const": 0.15 },
            "controversy_level": { "type": "string", "enum": ["low", "medium", "high"] },
            "discussion_hooks": { "type": "array", "items": { "type": "string" } },
            "analysis": { "type": "string" }
          },
          "description": "话题讨论性 (15%)"
        }
      },
      "description": "维度得分"
    },
    "engagement_optimization": {
      "type": "object",
      "properties": {
        "comment_triggers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "current": { "type": "string" },
              "suggestion": { "type": "string" }
            }
          },
          "description": "评论触发器"
        },
        "share_motivators": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "motivator": { "type": "string" },
              "current_strength": { "type": "string" },
              "enhancement": { "type": "string" }
            }
          },
          "description": "分享动机"
        },
        "cta_optimization": {
          "type": "object",
          "properties": {
            "current_cta": { "type": "string" },
            "effectiveness": { "type": "number" },
            "improved_cta": { "type": "string" },
            "rationale": { "type": "string" }
          },
          "description": "CTA 优化"
        }
      },
      "description": "互动优化建议"
    },
    "improvement_roadmap": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "priority": { "type": "integer", "minimum": 1, "maximum": 5 },
          "dimension": { "type": "string" },
          "issue": { "type": "string" },
          "recommendation": { "type": "string" },
          "expected_impact": {
            "type": "object",
            "properties": {
              "score_increase": { "type": "number" },
              "confidence": { "type": "number" }
            }
          }
        }
      },
      "description": "改进路线图"
    },
    "platform_specific_insights": {
      "type": "object",
      "properties": {
        "platform": { "type": "string" },
        "algorithm_fit": { "type": "number" },
        "optimal_posting_strategy": { "type": "string" },
        "hashtag_suggestions": { "type": "array", "items": { "type": "string" } },
        "format_recommendations": { "type": "array", "items": { "type": "string" } }
      },
      "description": "平台特化洞察"
    },
    "prediction": {
      "type": "object",
      "properties": {
        "engagement_range": {
          "type": "object",
          "properties": {
            "low": { "type": "integer" },
            "mid": { "type": "integer" },
            "high": { "type": "integer" }
          }
        },
        "viral_probability": {
          "type": "string",
          "enum": ["low", "medium", "high", "very_high"]
        },
        "confidence": { "type": "number" }
      },
      "description": "表现预测"
    }
  }
}
```

## 评分维度详解

### 1. Hook 吸引力 (25%)
评估标题和开头的吸引力

**评分因素**:
- 好奇心缺口 - 是否让人想知道更多
- 情感冲击 - 是否引发即时情感反应
- 清晰承诺 - 是否明确传达价值
- 紧迫感 - 是否创造阅读紧迫性

### 2. 情感共鸣度 (25%)
评估内容引发的情感反应

**评分因素**:
- 情感类型 - 识别引发的具体情感
- 情感强度 - 情感反应的程度
- 共鸣广度 - 能引起多少人共鸣
- 情感一致性 - 全文情感是否连贯

### 3. 社交货币 (20%)
评估分享动机强度

**评分因素**:
- 身份认同 - 分享能否彰显身份
- 实用转发 - 是否值得"转给朋友"
- 话题参与 - 是否能参与热门话题
- 独特洞察 - 是否提供新颖观点

### 4. 实用价值 (15%)
评估内容的实用性

**评分因素**:
- 可操作性 - 是否有具体步骤
- 问题解决 - 是否解决实际问题
- 学习收获 - 是否有新知识
- 即时可用 - 是否能立即应用

### 5. 话题讨论性 (15%)
评估引发讨论的潜力

**评分因素**:
- 争议性 - 是否有可争论的观点
- 开放问题 - 是否留有讨论空间
- 个人相关 - 是否与读者相关
- 互动邀请 - 是否有明确的互动邀请

## 互动优化策略

### 评论引导设计
```
类型 | 示例
-----|-----
提问结尾 | "你们遇到过类似情况吗？"
观点对立 | "你觉得A对还是B对？"
经验征集 | "评论区说说你的经历"
投票选择 | "1还是2？评论区告诉我"
```

### 分享动机强化
```
动机 | 强化方法
-----|--------
自我表达 | 加入身份标签、观点金句
社交互惠 | 提供实用资源、工具
信息传递 | 增加新闻性、时效性
情感宣泄 | 引发共鸣、情感释放
```

## 执行流程

1. **内容解析**
   - 提取标题、开头、正文、CTA
   - 识别结构和关键元素

2. **维度评估**
   - 逐维度分析评分
   - 识别优势和不足

3. **互动分析**
   - 识别当前互动元素
   - 评估互动设计有效性

4. **优化建议**
   - 生成改进建议
   - 排序优先级

5. **预测生成**
   - 估算表现范围
   - 评估病毒概率

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| writing-orchestrator | 由其调度 |
| hook-generator | 评估其输出 |
| narrative-builder | 评估其输出 |
| platform-adapter | 提供平台特化建议 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 评分准确性 | 与实际表现相关 | 相关系数≥0.7 |
| 建议可行性 | 建议可执行 | 100% |
| 优先级合理 | 高优先级影响大 | 100% |
| 覆盖完整 | 覆盖所有维度 | 100% |

## 脚本

- `scripts/score_virality.py` - 传播力评分主脚本
- `scripts/dimension_analyzer.py` - 维度分析器
- `scripts/optimization_engine.py` - 优化引擎

## 参考资料

- `references/scoring-model.md` - 评分模型详解
- `references/optimization-patterns.md` - 优化模式库
