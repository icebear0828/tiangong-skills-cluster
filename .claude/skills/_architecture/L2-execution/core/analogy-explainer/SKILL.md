---
name: analogy-explainer
description: >
  类比解释器 Skill。为复杂概念生成易懂的类比解释。当需要：(1) 解释抽象概念，
  (2) 连接新旧知识，(3) 增强理解深度时触发。支持多领域类比、适应学习者背景、
  标注类比局限性。作为核心学习 Skill，具有严格契约。
---

# Analogy Explainer — 类比解释器

## 触发条件

- 学习任务中包含"解释"、"讲解"、"比喻"等关键词
- 由 learning-orchestrator 或 verification-orchestrator 调度
- 学习者对某概念理解困难时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["concept", "learner_background"],
  "properties": {
    "concept": {
      "type": "object",
      "required": ["name", "definition"],
      "properties": {
        "name": { "type": "string" },
        "definition": { "type": "string" },
        "domain": { "type": "string" },
        "complexity": {
          "type": "string",
          "enum": ["low", "medium", "high"]
        },
        "key_properties": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "description": "待解释的概念"
    },
    "learner_background": {
      "type": "object",
      "properties": {
        "level": {
          "type": "string",
          "enum": ["beginner", "intermediate", "advanced"],
          "default": "beginner"
        },
        "familiar_domains": {
          "type": "array",
          "items": { "type": "string" },
          "description": "学习者熟悉的领域"
        },
        "prior_knowledge": {
          "type": "array",
          "items": { "type": "string" },
          "description": "已掌握的相关概念"
        },
        "preferred_style": {
          "type": "string",
          "enum": ["visual", "verbal", "logical", "experiential"],
          "default": "visual"
        }
      },
      "description": "学习者背景"
    },
    "analogy_config": {
      "type": "object",
      "properties": {
        "num_analogies": {
          "type": "integer",
          "default": 2,
          "description": "生成类比数量"
        },
        "include_visual": {
          "type": "boolean",
          "default": true,
          "description": "是否包含可视化描述"
        },
        "max_complexity": {
          "type": "string",
          "enum": ["simple", "moderate", "detailed"],
          "default": "moderate"
        }
      },
      "description": "类比配置"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["analogies", "explanation", "concept_mapping"],
  "properties": {
    "analogies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source_domain", "analogy_text", "mapping", "limitations"],
        "properties": {
          "source_domain": {
            "type": "string",
            "description": "类比来源领域"
          },
          "analogy_text": {
            "type": "string",
            "description": "类比描述文本"
          },
          "mapping": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "source_element": { "type": "string" },
                "target_element": { "type": "string" },
                "correspondence": { "type": "string" }
              }
            },
            "description": "元素对应关系"
          },
          "limitations": {
            "type": "array",
            "items": { "type": "string" },
            "description": "类比的局限性"
          },
          "visual_description": {
            "type": "string",
            "description": "可视化描述（可选）"
          },
          "strength": {
            "type": "string",
            "enum": ["strong", "moderate", "weak"],
            "description": "类比强度"
          }
        }
      },
      "description": "生成的类比列表"
    },
    "explanation": {
      "type": "object",
      "properties": {
        "simple": {
          "type": "string",
          "description": "简化解释（1-2句）"
        },
        "detailed": {
          "type": "string",
          "description": "详细解释"
        },
        "technical": {
          "type": "string",
          "description": "技术性解释（可选）"
        }
      },
      "description": "多层次解释"
    },
    "concept_mapping": {
      "type": "object",
      "properties": {
        "core_insight": {
          "type": "string",
          "description": "核心洞察"
        },
        "key_properties_explained": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "property": { "type": "string" },
              "explanation": { "type": "string" }
            }
          }
        },
        "common_misconceptions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "常见误解"
        }
      },
      "description": "概念映射"
    },
    "follow_up_questions": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 3,
      "description": "引导思考的问题"
    }
  }
}
```

## 类比来源域库

| 领域 | 适用概念类型 | 示例 |
|------|-------------|------|
| 日常生活 | 基础概念 | 变量 → 盒子 |
| 建筑/工程 | 架构/结构 | 软件架构 → 建筑设计 |
| 生物/自然 | 系统/演化 | 神经网络 → 大脑神经元 |
| 交通/物流 | 流程/传输 | 数据流 → 物流系统 |
| 社会/组织 | 协作/治理 | 微服务 → 公司部门 |
| 厨房/烹饪 | 过程/转换 | 编译 → 烹饪食谱 |
| 图书馆 | 存储/检索 | 数据库 → 图书馆 |
| 游戏 | 规则/策略 | 算法 → 游戏策略 |

## 执行流程

1. **概念分析**
   - 提取概念核心属性
   - 识别关键特征
   - 评估复杂度

2. **学习者适配**
   - 分析熟悉领域
   - 评估知识水平
   - 选择合适的类比域

3. **类比生成**
   - 从类比库匹配候选
   - 生成元素映射
   - 撰写类比文本

4. **质量检查**
   - 验证映射准确性
   - 识别局限性
   - 标注潜在误导

5. **解释生成**
   - 生成多层次解释
   - 添加引导问题
   - 标注常见误解

## 类比质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 相关性 | 源域与目标域有结构相似性 | 高 |
| 熟悉度 | 源域为学习者所熟悉 | ≥80% |
| 准确性 | 映射关系正确 | 100% |
| 清晰度 | 表述易于理解 | 高 |
| 完整性 | 标注局限性 | 必须 |

## 类比强度评级

| 强度 | 定义 | 映射比例 |
|------|------|---------|
| strong | 多个核心属性对应 | ≥80% |
| moderate | 主要属性对应 | 50-80% |
| weak | 仅部分属性对应 | <50% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| knowledge-extractor | 接收其提取的概念 |
| self-explanation-validator | 验证类比理解 |
| socratic-questioner | 可基于类比提问 |
| learning-orchestrator | 由其调度 |
| verification-orchestrator | 由其调度 |

## 脚本

- `scripts/generate_analogy.py` - 类比生成主脚本
- `scripts/domain_matcher.py` - 领域匹配器
- `scripts/mapping_validator.py` - 映射验证器

## 参考资料

- `references/analogy-bank.md` - 类比库
- `references/domain-mappings.md` - 领域映射规则
- `references/misconception-patterns.md` - 常见误解模式
