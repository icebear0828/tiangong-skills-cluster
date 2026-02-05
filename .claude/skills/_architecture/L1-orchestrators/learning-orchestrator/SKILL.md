---
name: learning-orchestrator
description: >
  学习流程编排器。编排四阶段学习流程的消化阶段（消化→结构→内化→验证）。
  当需要：(1) 系统性学习新知识，(2) 整合多种学习资源，(3) 构建初步理解时触发。
  支持内容获取、知识提取、类比生成。由 learning-commander 调度触发。
---

# Learning Orchestrator — 学习流程编排器

## 触发条件

- 进入 Phase 1 消化阶段
- 由 learning-commander 调度
- 需要将外部知识转化为内部表征

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["topic", "learner_profile"],
  "properties": {
    "topic": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "domain": { "type": "string" },
        "scope": {
          "type": "string",
          "enum": ["narrow", "medium", "broad"]
        }
      },
      "description": "学习主题"
    },
    "learner_profile": {
      "type": "object",
      "properties": {
        "level": {
          "type": "string",
          "enum": ["beginner", "intermediate", "advanced"]
        },
        "background": {
          "type": "array",
          "items": { "type": "string" }
        },
        "preferred_style": { "type": "string" },
        "time_budget": { "type": "string" }
      },
      "description": "学习者画像"
    },
    "content_sources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "path_or_url": { "type": "string" }
        }
      },
      "description": "指定的内容来源（可选）"
    },
    "config": {
      "type": "object",
      "properties": {
        "depth": {
          "type": "string",
          "enum": ["overview", "standard", "comprehensive"],
          "default": "standard"
        },
        "include_analogies": {
          "type": "boolean",
          "default": true
        },
        "max_concepts": {
          "type": "integer",
          "default": 15
        }
      },
      "description": "学习配置"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["knowledge_base", "summary", "analogies"],
  "properties": {
    "knowledge_base": {
      "type": "object",
      "properties": {
        "concepts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "definition": { "type": "string" },
              "importance": { "type": "string" },
              "prerequisites": { "type": "array" }
            }
          }
        },
        "relationships": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "from": { "type": "string" },
              "to": { "type": "string" },
              "type": { "type": "string" }
            }
          }
        },
        "hierarchy": {
          "type": "object",
          "description": "概念层次结构"
        }
      },
      "description": "构建的知识库"
    },
    "summary": {
      "type": "object",
      "properties": {
        "one_liner": { "type": "string" },
        "paragraph": { "type": "string" },
        "key_takeaways": {
          "type": "array",
          "items": { "type": "string" },
          "maxItems": 5
        },
        "learning_objectives": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "学习摘要"
    },
    "analogies": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "concept": { "type": "string" },
          "analogy": { "type": "string" },
          "mapping": { "type": "object" },
          "limitations": { "type": "array" }
        }
      },
      "description": "生成的类比"
    },
    "curated_resources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "title": { "type": "string" },
          "source": { "type": "string" },
          "relevance": { "type": "number" }
        }
      },
      "description": "策展的资源"
    },
    "quality_metrics": {
      "type": "object",
      "properties": {
        "coverage": { "type": "number" },
        "depth": { "type": "string" },
        "coherence": { "type": "number" }
      }
    }
  }
}
```

## 编排流程

```
┌─────────────────────────────────────────────┐
│  Phase 1: 消化 (Digest)                      │
│                                             │
│  Step 1: 内容获取                            │
│  ├─ 调用 content-curator                    │
│  └─ 收集、排序学习资源                       │
│                                             │
│  Step 2: 知识提取                            │
│  ├─ 调用 knowledge-extractor                │
│  └─ 提取结构化知识项                         │
│                                             │
│  Step 3: 类比生成                            │
│  ├─ 调用 analogy-explainer                  │
│  └─ 为核心概念生成类比                       │
│                                             │
│  Step 4: 质量检查                            │
│  ├─ 验证知识覆盖度                           │
│  └─ 确保结构完整性                           │
│                                             │
│  输出 → knowledge-graph-orchestrator (Phase 2)│
└─────────────────────────────────────────────┘
```

## 深度配置

| 深度 | 概念数 | 类比数 | 资源数 |
|------|--------|--------|--------|
| overview | 5-8 | 2-3 | 2-3 |
| standard | 10-15 | 4-6 | 5-8 |
| comprehensive | 20-30 | 8-12 | 10-15 |

## 质量关卡

| 检查点 | 标准 | 未通过处理 |
|--------|------|-----------|
| 资源获取 | ≥2 个有效资源 | 扩大搜索范围 |
| 知识提取 | 覆盖主要概念 | 增加资源 |
| 类比生成 | 核心概念有类比 | 重新生成 |
| 结构完整 | 有层次结构 | 补充关系 |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| content-curator | 调用 | Step 1 |
| knowledge-extractor | 调用 | Step 2 |
| analogy-explainer | 调用 | Step 3 |
| learning-commander | 被调用 | 由其调度 |
| knowledge-graph-orchestrator | 后续 | 输出传递 |

## 脚本

- `scripts/orchestrate_digest.py` - 消化编排主脚本
- `scripts/quality_checker.py` - 质量检查器

## 参考资料

- `references/learning-patterns.md` - 学习模式
- `references/quality-gates.md` - 质量关卡定义
