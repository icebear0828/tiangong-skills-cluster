---
name: defect-analyzer
description: >
  缺陷分析器 Skill。深度分析方案缺陷，生成 Top3 缺陷清单和严重度评级。当需要：
  (1) 深度缺陷挖掘，(2) 风险评估，(3) 方案质量分析时触发。
  支持多角度分析、严重度分级、缺陷分类。作为核心评审 Skill，具有严格契约。
---

# Defect Analyzer — 缺陷分析器

## 触发条件

- 评审任务进入 Round 2 深度分析阶段
- 由 multi-round-eval-orchestrator 调度
- 需要详细缺陷报告时

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["candidate", "analysis_angles"],
  "properties": {
    "candidate": {
      "type": "object",
      "required": ["name", "path"],
      "properties": {
        "name": { "type": "string" },
        "path": { "type": "string" },
        "content": { "type": "string" }
      },
      "description": "待分析的方案"
    },
    "analysis_angles": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "architecture",
          "implementation",
          "scalability",
          "maintainability",
          "security",
          "performance",
          "compatibility",
          "cost"
        ]
      },
      "description": "分析角度列表"
    },
    "evaluator_id": {
      "type": "string",
      "description": "分析员标识"
    },
    "context": {
      "type": "object",
      "properties": {
        "existing_system": { "type": "string" },
        "constraints": { "type": "array", "items": { "type": "string" } },
        "priorities": { "type": "object" }
      },
      "description": "分析上下文"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["analyzer_id", "candidate", "defects", "overall_score", "ranking"],
  "properties": {
    "analyzer_id": {
      "type": "string",
      "description": "分析员标识"
    },
    "candidate": {
      "type": "string",
      "description": "分析的方案名"
    },
    "defects": {
      "type": "array",
      "maxItems": 5,
      "items": {
        "type": "object",
        "required": ["id", "title", "severity", "category", "description"],
        "properties": {
          "id": { "type": "string" },
          "title": { "type": "string", "maxLength": 100 },
          "severity": {
            "type": "string",
            "enum": ["Critical", "High", "Medium", "Low"],
            "description": "严重度等级"
          },
          "category": {
            "type": "string",
            "description": "缺陷类别"
          },
          "description": {
            "type": "string",
            "description": "详细描述"
          },
          "impact": {
            "type": "string",
            "description": "影响范围"
          },
          "mitigation": {
            "type": "string",
            "description": "缓解建议"
          },
          "evidence": {
            "type": "array",
            "items": { "type": "string" },
            "description": "支持证据"
          }
        }
      },
      "description": "Top 缺陷清单（按严重度排序）"
    },
    "overall_score": {
      "type": "object",
      "properties": {
        "total": { "type": "number", "minimum": 0, "maximum": 10 },
        "by_angle": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        }
      },
      "description": "综合评分"
    },
    "ranking": {
      "type": "integer",
      "minimum": 1,
      "description": "在当前候选集中的排名建议"
    },
    "strengths": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 3,
      "description": "方案优势"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_depth": { "type": "string", "enum": ["quick", "standard", "deep"] },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}
```

## 执行流程

1. **深度阅读**
   - 完整阅读方案文档
   - 理解核心设计思想
   - 标记关键决策点

2. **多角度分析**
   - 按指定分析角度逐个审视
   - 识别潜在问题点
   - 记录具体证据

3. **缺陷分级**
   - 评估每个缺陷的严重度
   - 分析影响范围
   - 提出缓解建议

4. **综合评分**
   - 计算各维度得分
   - 生成总分
   - 确定排名建议

## 严重度定义

| 等级 | 定义 | 影响 |
|------|------|------|
| Critical | 致命缺陷 | 使方案完全无法工作 |
| High | 严重缺陷 | 需要重大修改才能使用 |
| Medium | 中等缺陷 | 需要一定工作量修复 |
| Low | 轻微缺陷 | 可接受或易修复 |

## 分析角度说明

| 角度 | 关注点 |
|------|--------|
| architecture | 架构设计合理性、层次清晰度 |
| implementation | 实现复杂度、技术债务 |
| scalability | 扩展性、容量规划 |
| maintainability | 可维护性、代码/文档质量 |
| security | 安全隐患、权限控制 |
| performance | 性能瓶颈、资源消耗 |
| compatibility | 兼容性、迁移成本 |
| cost | 实施成本、运维成本 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 深度 | 每个角度至少分析 3 个方面 | 100% |
| 客观性 | 缺陷有证据支持 | ≥90% |
| 可操作性 | 缺陷有缓解建议 | ≥80% |
| 一致性 | 评分与缺陷数量逻辑一致 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| initial-screener | 在其后执行，处理存活方案 |
| ranking-synthesizer | 输出排名被其综合 |
| devils-advocate | 为其提供缺陷基础 |
| eval-engine | 复用评分标准 |

## 脚本

- `scripts/analyze.py` - 缺陷分析主脚本
- `scripts/severity_scorer.py` - 严重度评分器

## 参考资料

- `references/defect-taxonomy.md` - 缺陷分类学
- `references/severity-matrix.md` - 严重度矩阵
