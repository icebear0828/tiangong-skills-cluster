---
name: trend-tracker
description: >
  热点追踪器 Skill (L2 Extended)。追踪和分析各平台热点趋势，发现内容机会。
  当需要：(1) 追踪热门话题，(2) 发现内容机会，(3) 蹭热点策划时触发。
  支持多平台热点监测和内容机会识别。作为扩展写作 Skill，具有标准契约。
---

# Trend Tracker — 热点追踪器

## 触发条件

- 写作任务中包含"热点"、"趋势"、"热门话题"、"蹭热点"等关键词
- 由 writing-orchestrator 调度（Stage 1）
- 需要了解当前热门话题或发现内容机会

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["topic_area"],
  "properties": {
    "topic_area": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "领域/行业"
        },
        "keywords": {
          "type": "array",
          "items": { "type": "string" },
          "description": "相关关键词"
        },
        "exclude_topics": {
          "type": "array",
          "items": { "type": "string" },
          "description": "排除的话题"
        }
      },
      "description": "关注的话题领域"
    },
    "platforms": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["xiaohongshu", "wechat", "weibo", "twitter", "douyin", "zhihu", "general"]
      },
      "default": ["general"],
      "description": "目标平台"
    },
    "tracking_config": {
      "type": "object",
      "properties": {
        "time_range": {
          "type": "string",
          "enum": ["real_time", "24h", "7d", "30d"],
          "default": "7d"
        },
        "trend_type": {
          "type": "string",
          "enum": ["rising", "stable_hot", "emerging", "all"],
          "default": "all"
        },
        "min_relevance": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.5
        }
      },
      "description": "追踪配置"
    },
    "content_goal": {
      "type": "object",
      "properties": {
        "purpose": {
          "type": "string",
          "enum": ["viral_potential", "education", "engagement", "brand_relevance"]
        },
        "audience": { "type": "string" }
      },
      "description": "内容目标"
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["trends", "content_opportunities"],
  "properties": {
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "topic": { "type": "string" },
          "description": { "type": "string" },
          "platforms": {
            "type": "array",
            "items": { "type": "string" }
          },
          "trend_metrics": {
            "type": "object",
            "properties": {
              "heat_score": { "type": "number", "minimum": 0, "maximum": 100 },
              "growth_rate": { "type": "string" },
              "lifecycle_stage": {
                "type": "string",
                "enum": ["emerging", "growing", "peak", "declining"]
              },
              "estimated_duration": { "type": "string" }
            }
          },
          "relevance_score": { "type": "number" },
          "related_keywords": {
            "type": "array",
            "items": { "type": "string" }
          },
          "example_content": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "title": { "type": "string" },
                "platform": { "type": "string" },
                "engagement": { "type": "string" }
              }
            }
          }
        }
      },
      "description": "热点趋势列表"
    },
    "content_opportunities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "opportunity_id": { "type": "string" },
          "trend_ref": { "type": "string" },
          "angle": { "type": "string", "description": "切入角度" },
          "content_idea": { "type": "string", "description": "内容创意" },
          "suggested_format": {
            "type": "string",
            "enum": ["article", "listicle", "tutorial", "opinion", "story", "comparison"]
          },
          "target_platform": { "type": "string" },
          "timing_advice": {
            "type": "object",
            "properties": {
              "urgency": { "type": "string", "enum": ["immediate", "this_week", "flexible"] },
              "best_window": { "type": "string" }
            }
          },
          "potential_score": { "type": "number" },
          "risk_level": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "蹭热点风险"
          },
          "title_suggestions": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "description": "内容机会"
    },
    "trend_summary": {
      "type": "object",
      "properties": {
        "total_trends_found": { "type": "integer" },
        "top_categories": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "category": { "type": "string" },
              "count": { "type": "integer" }
            }
          }
        },
        "platform_distribution": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "overall_recommendation": { "type": "string" }
      },
      "description": "趋势概览"
    },
    "timing_insights": {
      "type": "object",
      "properties": {
        "hot_now": {
          "type": "array",
          "items": { "type": "string" }
        },
        "rising_fast": {
          "type": "array",
          "items": { "type": "string" }
        },
        "about_to_peak": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "时机洞察"
    }
  }
}
```

## 热点分类

### 按生命周期

| 阶段 | 特征 | 内容策略 |
|------|------|---------|
| emerging | 刚出现，关注度上升 | 抢先发布，建立权威 |
| growing | 快速增长，讨论激烈 | 提供独特角度 |
| peak | 达到顶峰，人人都在讨论 | 总结类、观点类 |
| declining | 热度下降 | 反思类、后续跟进 |

### 按类型

| 类型 | 特征 | 示例 |
|------|------|------|
| 新闻事件 | 突发、时效性强 | 行业大事件 |
| 周期热点 | 可预测、定期出现 | 节日、考试季 |
| 话题讨论 | 争议性、参与度高 | XX该不该 |
| 文化现象 | 持续性、影响广泛 | 流行语、meme |
| 产品发布 | 商业相关、关注度集中 | 新品发布 |

## 蹭热点策略

### 关联度矩阵

| 关联度 | 策略 | 风险 |
|--------|------|------|
| 强关联 | 直接切入，提供专业视角 | 低 |
| 中关联 | 找到连接点，自然引入 | 中 |
| 弱关联 | 慎重，可能显得牵强 | 高 |

### 内容角度

```
角度选择:
├─ 解读角度 - 解释为什么会这样
├─ 实用角度 - 这对你有什么用
├─ 观点角度 - 我对此的看法
├─ 盘点角度 - 类似事件汇总
├─ 预测角度 - 接下来会怎样
└─ 幕后角度 - 背后的故事
```

## 平台热点来源

| 平台 | 热点来源 | 特征 |
|------|---------|------|
| 微博 | 热搜榜 | 社会热点、娱乐 |
| 小红书 | 热门话题 | 生活方式、种草 |
| 抖音 | 热榜、挑战 | 娱乐、创意 |
| 知乎 | 热榜 | 知识、观点 |
| 公众号 | 原创热文 | 深度内容 |
| Twitter | Trending | 国际、科技 |

## 执行流程

1. **数据收集**
   - 获取各平台热点数据
   - 筛选相关领域

2. **趋势分析**
   - 计算热度分数
   - 判断生命周期阶段
   - 评估持续时间

3. **关联匹配**
   - 计算与领域的关联度
   - 筛选高关联热点

4. **机会识别**
   - 生成内容角度
   - 评估潜力和风险

5. **建议生成**
   - 提供时机建议
   - 生成标题创意

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| writing-orchestrator | 由其调度 |
| writing-commander | 提供策划输入 |
| content-curator | 协同收集素材 |
| hook-generator | 提供热点关键词 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 热点准确性 | 确实是当前热点 | 100% |
| 关联度判断 | 关联判断准确 | ≥85% |
| 机会可行性 | 建议可执行 | 100% |
| 风险提示 | 提示潜在风险 | 100% |

## 脚本

- `scripts/track_trends.py` - 趋势追踪主脚本
- `scripts/trend_analyzer.py` - 趋势分析器
- `scripts/opportunity_generator.py` - 机会生成器

## 参考资料

- `references/trend-sources.md` - 热点来源
- `references/content-timing.md` - 内容时机策略
