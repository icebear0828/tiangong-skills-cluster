---
name: knowledge-extractor
description: >
  知识提取器 Skill。从文本内容中提取结构化知识项。当需要：(1) 从文档中提取核心概念，
  (2) 生成知识摘要，(3) 构建知识层次结构时触发。支持多种内容类型、层次化提取、
  关系识别。作为核心学习 Skill，具有严格契约。
---

# Knowledge Extractor — 知识提取器

## 触发条件

- 学习任务中包含"提取要点"、"总结"、"提炼"等关键词
- 由 learning-orchestrator 或 knowledge-graph-orchestrator 调度
- 需要将非结构化内容转为结构化知识时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["content", "content_type"],
  "properties": {
    "content": {
      "type": "string",
      "description": "待提取的文本内容",
      "minLength": 100
    },
    "content_type": {
      "type": "string",
      "enum": ["article", "paper", "documentation", "tutorial", "video_transcript", "book_chapter", "code"],
      "description": "内容类型"
    },
    "extraction_config": {
      "type": "object",
      "properties": {
        "max_concepts": {
          "type": "integer",
          "default": 20,
          "description": "最多提取的概念数"
        },
        "min_confidence": {
          "type": "number",
          "default": 0.7,
          "description": "最低置信度阈值"
        },
        "include_examples": {
          "type": "boolean",
          "default": true,
          "description": "是否提取示例"
        },
        "include_relationships": {
          "type": "boolean",
          "default": true,
          "description": "是否提取关系"
        },
        "depth": {
          "type": "string",
          "enum": ["shallow", "standard", "deep"],
          "default": "standard",
          "description": "提取深度"
        }
      },
      "description": "提取配置"
    },
    "domain_context": {
      "type": "object",
      "properties": {
        "domain": { "type": "string" },
        "existing_concepts": { "type": "array", "items": { "type": "string" } },
        "learner_level": { "type": "string", "enum": ["beginner", "intermediate", "advanced"] }
      },
      "description": "领域上下文"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["knowledge_items", "summary", "hierarchy"],
  "properties": {
    "knowledge_items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "name", "definition"],
        "properties": {
          "id": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["concept", "principle", "fact", "procedure", "skill", "pattern"]
          },
          "name": { "type": "string", "maxLength": 100 },
          "definition": { "type": "string" },
          "key_points": {
            "type": "array",
            "items": { "type": "string" },
            "maxItems": 5
          },
          "examples": {
            "type": "array",
            "items": { "type": "string" }
          },
          "prerequisites": {
            "type": "array",
            "items": { "type": "string" }
          },
          "importance": {
            "type": "string",
            "enum": ["critical", "important", "supplementary"]
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "source_location": { "type": "string" }
        }
      },
      "description": "提取的知识项"
    },
    "summary": {
      "type": "object",
      "properties": {
        "one_sentence": { "type": "string", "maxLength": 200 },
        "paragraph": { "type": "string", "maxLength": 1000 },
        "key_takeaways": {
          "type": "array",
          "items": { "type": "string" },
          "maxItems": 5
        }
      },
      "description": "内容摘要"
    },
    "hierarchy": {
      "type": "object",
      "properties": {
        "root_concepts": {
          "type": "array",
          "items": { "type": "string" }
        },
        "concept_tree": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "parent": { "type": "string" },
              "children": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "depth": { "type": "integer" }
      },
      "description": "知识层次结构"
    },
    "relationships": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "from": { "type": "string" },
          "to": { "type": "string" },
          "relation_type": {
            "type": "string",
            "enum": ["is_a", "part_of", "depends_on", "related_to", "contrasts_with", "example_of", "applies_to"]
          },
          "description": { "type": "string" }
        }
      },
      "description": "概念关系"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "total_extracted": { "type": "integer" },
        "content_coverage": { "type": "number" },
        "extraction_quality": { "type": "string" }
      }
    }
  }
}
```

## 知识类型定义

| 类型 | 定义 | 示例 |
|------|------|------|
| concept | 抽象概念 | "函数式编程" |
| principle | 原则/规律 | "单一职责原则" |
| fact | 具体事实 | "JavaScript 是单线程的" |
| procedure | 操作步骤 | "创建 React 组件的步骤" |
| skill | 技能/能力 | "调试技巧" |
| pattern | 模式/范式 | "观察者模式" |

## 执行流程

1. **预处理**
   - 清洗文本
   - 识别结构（标题、段落、代码块）
   - 确定内容边界

2. **概念识别**
   - 使用 NER 识别实体
   - 识别领域术语
   - 标记重要概念

3. **关系提取**
   - 识别概念间关系
   - 构建知识图谱
   - 验证关系合理性

4. **层次构建**
   - 识别父子关系
   - 构建概念树
   - 确定根节点

5. **摘要生成**
   - 提炼核心观点
   - 生成多粒度摘要
   - 列出关键要点

## 内容类型适配

| 内容类型 | 提取侧重 | 特殊处理 |
|---------|---------|---------|
| article | 观点、论据 | 识别作者立场 |
| paper | 方法、结论 | 提取摘要、贡献 |
| documentation | API、用法 | 提取签名、参数 |
| tutorial | 步骤、技巧 | 保留操作顺序 |
| video_transcript | 口语化概念 | 去除冗余、整理 |
| book_chapter | 系统知识 | 保留章节结构 |
| code | 模式、技术 | 分析代码结构 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 完整性 | 覆盖主要概念 | ≥80% |
| 准确性 | 定义正确 | ≥95% |
| 结构性 | 层次清晰 | 100% |
| 精炼性 | 去除冗余 | 冗余 <10% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| analogy-explainer | 为其提供概念输入 |
| spatial-mapper | 为其提供知识项 |
| content-curator | 接收其推荐内容 |
| learning-orchestrator | 由其调度 |
| knowledge-graph-orchestrator | 由其调度 |

## 脚本

- `scripts/extract.py` - 知识提取主脚本
- `scripts/relation_extractor.py` - 关系提取器
- `scripts/hierarchy_builder.py` - 层次构建器

## 参考资料

- `references/extraction-patterns.md` - 提取模式库
- `references/knowledge-types.md` - 知识类型详解
