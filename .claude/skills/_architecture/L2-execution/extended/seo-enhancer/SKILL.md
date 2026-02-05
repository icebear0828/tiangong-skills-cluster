---
name: seo-enhancer
description: >
  SEO 增强器 Skill (L2 Extended)。优化内容的搜索引擎可见性，提升搜索排名潜力。
  当需要：(1) 优化搜索排名，(2) 增加内容曝光，(3) 关键词优化时触发。
  支持多平台 SEO 策略。作为扩展写作 Skill，具有标准契约。
---

# SEO Enhancer — SEO 增强器

## 触发条件

- 写作任务中包含"SEO"、"搜索优化"、"关键词"、"排名"等关键词
- 由 writing-orchestrator 调度（Stage 3，可选）
- 需要提升内容的搜索可见性

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["content", "seo_config"],
  "properties": {
    "content": {
      "type": "object",
      "required": ["title", "body"],
      "properties": {
        "title": { "type": "string" },
        "body": { "type": "string" },
        "meta_description": { "type": "string" },
        "current_keywords": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "待优化内容"
    },
    "seo_config": {
      "type": "object",
      "properties": {
        "target_keywords": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "keyword": { "type": "string" },
              "priority": { "type": "string", "enum": ["primary", "secondary", "long_tail"] },
              "search_volume": { "type": "string" }
            }
          },
          "description": "目标关键词"
        },
        "platform": {
          "type": "string",
          "enum": ["google", "baidu", "xiaohongshu", "wechat", "general"],
          "default": "general"
        },
        "optimization_level": {
          "type": "string",
          "enum": ["light", "moderate", "aggressive"],
          "default": "moderate"
        },
        "preserve_readability": {
          "type": "boolean",
          "default": true
        }
      },
      "description": "SEO 配置"
    },
    "context": {
      "type": "object",
      "properties": {
        "industry": { "type": "string" },
        "competitors": {
          "type": "array",
          "items": { "type": "string" }
        },
        "content_type": { "type": "string" }
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
  "required": ["enhanced_content", "seo_report"],
  "properties": {
    "enhanced_content": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "body": { "type": "string" },
        "meta_description": { "type": "string", "maxLength": 160 },
        "meta_keywords": {
          "type": "array",
          "items": { "type": "string" }
        },
        "suggested_slug": { "type": "string" },
        "heading_structure": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "level": { "type": "string", "enum": ["h1", "h2", "h3"] },
              "text": { "type": "string" }
            }
          }
        }
      },
      "description": "优化后内容"
    },
    "seo_report": {
      "type": "object",
      "properties": {
        "overall_score": { "type": "number", "minimum": 0, "maximum": 100 },
        "keyword_analysis": {
          "type": "object",
          "properties": {
            "primary_keyword_density": { "type": "number" },
            "keyword_placement": {
              "type": "object",
              "properties": {
                "in_title": { "type": "boolean" },
                "in_first_paragraph": { "type": "boolean" },
                "in_headings": { "type": "boolean" },
                "in_conclusion": { "type": "boolean" }
              }
            },
            "related_keywords_used": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        },
        "readability_score": { "type": "number" },
        "content_structure_score": { "type": "number" },
        "optimization_actions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "action": { "type": "string" },
              "before": { "type": "string" },
              "after": { "type": "string" },
              "impact": { "type": "string" }
            }
          }
        }
      },
      "description": "SEO 报告"
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "area": { "type": "string" },
          "suggestion": { "type": "string" },
          "priority": { "type": "string", "enum": ["high", "medium", "low"] }
        }
      },
      "description": "优化建议"
    }
  }
}
```

## SEO 优化维度

### 1. 关键词优化
```
关键词密度: 1-3% (主关键词)
关键词位置:
├─ 标题 (必须)
├─ 首段 (强烈建议)
├─ 小标题 (建议)
├─ 正文 (自然分布)
└─ 结尾 (建议)
```

### 2. 标题优化
```
标题长度: 50-60字符 (Google) / 30字以内 (百度)
包含元素:
├─ 主关键词
├─ 数字 (可选，提升点击率)
├─ 情感词 (可选)
└─ 品牌词 (可选)
```

### 3. 内容结构优化
```
H1: 仅一个，包含主关键词
H2: 3-5个，包含次要关键词
H3: 适量，包含长尾关键词
段落: 每段100-200字
```

### 4. Meta 描述优化
```
长度: 120-160字符
包含:
├─ 主关键词
├─ 价值承诺
└─ 行动召唤
```

## 平台特化 SEO

### Google/通用
- 关注 E-E-A-T (经验、专业、权威、可信)
- 语义相关词覆盖
- 长尾关键词策略

### 百度
- 标题控制在30字以内
- 关注原创度
- 内链策略

### 小红书站内搜索
- 关键词自然融入
- 话题标签覆盖
- 封面图包含关键词

### 公众号搜一搜
- 标题包含搜索词
- 正文首段关键词
- 文章标签优化

## 执行流程

1. **关键词分析**
   - 验证目标关键词
   - 确定密度目标
   - 规划分布位置

2. **标题优化**
   - 融入主关键词
   - 保持吸引力
   - 控制长度

3. **内容优化**
   - 首段关键词植入
   - 小标题优化
   - 自然密度控制

4. **结构优化**
   - 调整标题层级
   - 添加结构化元素

5. **Meta 优化**
   - 生成 meta description
   - 优化 URL slug

6. **可读性检查**
   - 确保自然流畅
   - 避免关键词堆砌

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| writing-orchestrator | 由其调度 |
| platform-adapter | 协同工作 |
| narrative-builder | 优化其输出 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 关键词覆盖 | 主关键词出现 | 必须 |
| 关键词密度 | 1-3% | 在范围内 |
| 可读性 | 自然流畅 | ≥80分 |
| 结构完整 | 标题层级清晰 | 100% |

## 脚本

- `scripts/enhance_seo.py` - SEO 增强主脚本
- `scripts/keyword_analyzer.py` - 关键词分析器
- `scripts/readability_checker.py` - 可读性检查器

## 参考资料

- `references/seo-best-practices.md` - SEO 最佳实践
- `references/keyword-research.md` - 关键词研究指南
