---
name: content-curator
description: >
  内容策展器 Skill。为学习主题策展高质量学习资源。当需要：(1) 查找学习材料，
  (2) 评估资源质量，(3) 规划学习路径时触发。支持多来源搜索、质量评估、
  路径推荐。作为扩展学习 Skill，具有标准契约。
---

# Content Curator — 内容策展器

## 触发条件

- 学习任务开始时需要获取资源
- 由 learning-orchestrator 调度
- 需要为学习主题找到优质内容

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["topic"],
  "properties": {
    "topic": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "domain": { "type": "string" },
        "keywords": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "学习主题"
    },
    "source_types": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["documentation", "tutorial", "article", "video", "paper", "code", "book"]
      },
      "default": ["documentation", "tutorial", "article"],
      "description": "资源类型偏好"
    },
    "quality_criteria": {
      "type": "object",
      "properties": {
        "min_quality_score": {
          "type": "number",
          "default": 0.7
        },
        "prefer_official": {
          "type": "boolean",
          "default": true
        },
        "prefer_recent": {
          "type": "boolean",
          "default": true
        },
        "max_age_years": {
          "type": "integer",
          "default": 3
        }
      },
      "description": "质量标准"
    },
    "learner_context": {
      "type": "object",
      "properties": {
        "level": {
          "type": "string",
          "enum": ["beginner", "intermediate", "advanced"]
        },
        "language_preference": { "type": "string" },
        "time_available": { "type": "string" }
      },
      "description": "学习者上下文"
    },
    "max_results": {
      "type": "integer",
      "default": 10
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["curated_resources", "learning_path"],
  "properties": {
    "curated_resources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "type", "quality_score"],
        "properties": {
          "id": { "type": "string" },
          "title": { "type": "string" },
          "type": { "type": "string" },
          "source": { "type": "string" },
          "url": { "type": "string" },
          "description": { "type": "string" },
          "quality_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "quality_breakdown": {
            "type": "object",
            "properties": {
              "authority": { "type": "number" },
              "relevance": { "type": "number" },
              "clarity": { "type": "number" },
              "completeness": { "type": "number" },
              "recency": { "type": "number" }
            }
          },
          "target_level": { "type": "string" },
          "estimated_time": { "type": "string" },
          "key_topics_covered": {
            "type": "array",
            "items": { "type": "string" }
          },
          "prerequisites": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "description": "策展的资源列表"
    },
    "learning_path": {
      "type": "object",
      "properties": {
        "recommended_sequence": {
          "type": "array",
          "items": { "type": "string" },
          "description": "推荐学习顺序（资源 ID）"
        },
        "stages": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "resources": { "type": "array" },
              "objective": { "type": "string" }
            }
          }
        },
        "alternative_paths": {
          "type": "array",
          "items": { "type": "object" }
        }
      },
      "description": "学习路径建议"
    },
    "gaps_identified": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "topic": { "type": "string" },
          "description": { "type": "string" },
          "severity": { "type": "string" }
        }
      },
      "description": "识别的内容空白"
    },
    "curation_metadata": {
      "type": "object",
      "properties": {
        "sources_searched": { "type": "array" },
        "total_candidates": { "type": "integer" },
        "filtered_out": { "type": "integer" },
        "curation_criteria_applied": { "type": "array" }
      }
    }
  }
}
```

## 质量评估维度

| 维度 | 权重 | 评估标准 |
|------|------|---------|
| authority | 25% | 来源权威性、作者专业度 |
| relevance | 30% | 与主题的相关性 |
| clarity | 20% | 表述清晰度、结构性 |
| completeness | 15% | 内容完整性 |
| recency | 10% | 时效性 |

## 数据源接口

采用模拟接口模式，实际调用由 MCP 工具完成：

```python
class ContentSource(Protocol):
    def search(self, query: str, filters: dict) -> List[Resource]:
        """搜索资源"""
        ...

    def fetch(self, url: str) -> Content:
        """获取内容"""
        ...
```

### 支持的数据源

| 数据源 | 类型 | 说明 |
|--------|------|------|
| arxiv | 学术论文 | 通过 MCP 扩展 |
| github | 代码仓库 | 通过 MCP 扩展 |
| web | 通用网页 | 使用 WebFetch |
| local | 本地文件 | 直接读取 |

## 执行流程

1. **查询构建**
   - 分析主题
   - 生成搜索关键词
   - 确定搜索范围

2. **资源搜索**
   - 在各数据源搜索
   - 收集候选资源

3. **质量评估**
   - 评估各维度得分
   - 计算综合质量分
   - 过滤低质量资源

4. **排序策展**
   - 按质量分排序
   - 考虑多样性
   - 避免重复

5. **路径规划**
   - 分析资源依赖
   - 规划学习顺序
   - 生成路径建议

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 结果数量 | 返回足够资源 | ≥3 |
| 质量平均 | 平均质量分 | ≥0.7 |
| 覆盖度 | 覆盖主要概念 | ≥80% |
| 多样性 | 类型多样 | ≥2种类型 |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| knowledge-extractor | 为其提供内容 |
| learning-orchestrator | 由其调度 |

## 脚本

- `scripts/curate.py` - 策展主脚本
- `scripts/quality_scorer.py` - 质量评分器
- `scripts/path_planner.py` - 路径规划器

## 参考资料

- `references/source-quality-criteria.md` - 来源质量标准
- `references/curation-strategies.md` - 策展策略
