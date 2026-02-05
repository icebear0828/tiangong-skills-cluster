---
name: narrative-builder
description: >
  叙事结构构建器 Skill (L2 Core)。构建完整的内容叙事结构，组织故事线和论证逻辑。
  当需要：(1) 构建内容框架，(2) 组织叙事结构，(3) 写作完整内容时触发。
  支持多种叙事模式和内容类型。作为核心写作 Skill，具有严格契约。
---

# Narrative Builder — 叙事结构构建器

## 触发条件

- 写作任务中包含"写内容"、"构建结构"、"完整文章"等关键词
- 由 writing-orchestrator 调度（Stage 2）
- 需要构建完整内容结构和正文

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["topic", "structure_type"],
  "properties": {
    "topic": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string", "description": "主题名称" },
        "description": { "type": "string", "description": "主题描述" },
        "key_points": {
          "type": "array",
          "items": { "type": "string" },
          "description": "关键要点"
        },
        "angle": { "type": "string", "description": "切入角度" }
      },
      "description": "写作主题"
    },
    "structure_type": {
      "type": "string",
      "enum": ["problem_solution", "listicle", "story", "tutorial", "comparison", "opinion", "news"],
      "description": "结构类型"
    },
    "hook": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "opening": { "type": "string" }
      },
      "description": "由 hook-generator 提供的钩子"
    },
    "content_config": {
      "type": "object",
      "properties": {
        "length": {
          "type": "string",
          "enum": ["short", "medium", "long"],
          "default": "medium"
        },
        "tone": {
          "type": "string",
          "enum": ["professional", "casual", "humorous", "inspirational", "educational"],
          "default": "casual"
        },
        "include_examples": {
          "type": "boolean",
          "default": true
        },
        "include_quotes": {
          "type": "boolean",
          "default": false
        },
        "sections_count": {
          "type": "integer",
          "minimum": 2,
          "maximum": 10,
          "default": 4
        }
      },
      "description": "内容配置"
    },
    "audience": {
      "type": "object",
      "properties": {
        "knowledge_level": {
          "type": "string",
          "enum": ["beginner", "intermediate", "expert"]
        },
        "interests": { "type": "array", "items": { "type": "string" } },
        "pain_points": { "type": "array", "items": { "type": "string" } }
      },
      "description": "目标受众"
    },
    "materials": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "content": { "type": "string" },
          "use_for": { "type": "string" }
        }
      },
      "description": "参考素材"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["narrative", "sections"],
  "properties": {
    "narrative": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "subtitle": { "type": "string" },
        "full_content": { "type": "string", "description": "完整正文" },
        "word_count": { "type": "integer" },
        "reading_time": { "type": "string" }
      },
      "description": "完整叙事"
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["opening", "body", "transition", "climax", "conclusion", "cta"]
          },
          "heading": { "type": "string" },
          "content": { "type": "string" },
          "purpose": { "type": "string" },
          "key_message": { "type": "string" },
          "emotional_beat": { "type": "string" }
        }
      },
      "description": "分段内容"
    },
    "structure_analysis": {
      "type": "object",
      "properties": {
        "structure_used": { "type": "string" },
        "flow_quality": { "type": "number" },
        "logic_coherence": { "type": "number" },
        "emotional_arc": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "section": { "type": "string" },
              "emotion": { "type": "string" },
              "intensity": { "type": "number" }
            }
          }
        }
      },
      "description": "结构分析"
    },
    "highlights": {
      "type": "object",
      "properties": {
        "golden_sentences": {
          "type": "array",
          "items": { "type": "string" },
          "description": "金句列表"
        },
        "key_takeaways": {
          "type": "array",
          "items": { "type": "string" },
          "description": "核心要点"
        },
        "quotable_moments": {
          "type": "array",
          "items": { "type": "string" },
          "description": "可引用片段"
        }
      },
      "description": "内容亮点"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "keywords": { "type": "array", "items": { "type": "string" } },
        "topics_covered": { "type": "array", "items": { "type": "string" } },
        "content_type": { "type": "string" }
      }
    }
  }
}
```

## 叙事结构模板

### 1. 问题-解决型 (Problem-Solution)
```
开头: 痛点共鸣
  └─ 描述问题，引发共鸣
过渡: 原因分析
  └─ 解释为什么会有这个问题
主体: 解决方案
  └─ 分步骤提供解决方法
结尾: 行动召唤
  └─ 鼓励尝试，提供下一步
```

### 2. 清单型 (Listicle)
```
开头: 价值承诺
  └─ 说明将获得什么
主体: 条目展开
  ├─ Point 1 + 例证
  ├─ Point 2 + 例证
  ├─ ...
  └─ Point N + 例证
结尾: 总结 + CTA
  └─ 强化价值，引导行动
```

### 3. 故事型 (Story)
```
开头: 场景设置
  └─ 引入人物、时间、背景
发展: 冲突升级
  └─ 描述遭遇的困难
高潮: 转折点
  └─ 关键发现或突破
结尾: 启示总结
  └─ 提炼教训和感悟
```

### 4. 教程型 (Tutorial)
```
开头: 目标设定
  └─ 说明将学会什么
准备: 前置条件
  └─ 需要准备什么
主体: 步骤详解
  ├─ Step 1 + 说明 + 注意事项
  ├─ Step 2 + 说明 + 注意事项
  └─ ...
结尾: 验证 + 进阶
  └─ 如何确认成功，下一步学什么
```

### 5. 对比型 (Comparison)
```
开头: 选择困境
  └─ 描述常见的选择场景
主体: 维度对比
  ├─ 维度 A: Option 1 vs Option 2
  ├─ 维度 B: Option 1 vs Option 2
  └─ ...
分析: 适用场景
  └─ 什么情况选什么
结尾: 推荐建议
  └─ 给出明确建议
```

### 6. 观点型 (Opinion)
```
开头: 抛出观点
  └─ 鲜明立场
论证1: 支持论据 A
  └─ 证据 + 分析
论证2: 支持论据 B
  └─ 证据 + 分析
回应: 反驳质疑
  └─ 预见并回应反对意见
结尾: 重申立场
  └─ 强化观点，呼吁认同
```

## 长度规格

| 长度 | 字数范围 | 典型段落数 | 阅读时间 |
|------|---------|-----------|---------|
| short | 300-600 | 3-4 | 1-2分钟 |
| medium | 800-1500 | 5-7 | 3-5分钟 |
| long | 2000-3500 | 8-12 | 7-12分钟 |

## 情感弧线设计

```
强度
 │     ┌─高潮─┐
 │    /       \
 │   /  发展   \ 收尾
 │  /           \
 │ 开头──────────结尾
 └─────────────────── 段落
```

每个段落应有明确的情感定位：
- **开头**: 好奇/共鸣
- **发展**: 期待/紧张
- **高潮**: 惊喜/恍然大悟
- **结尾**: 满足/行动欲

## 金句生成策略

| 类型 | 特征 | 示例模式 |
|------|------|---------|
| 对比金句 | 反差强烈 | "不是...而是..." |
| 洞察金句 | 揭示本质 | "本质上是..." |
| 行动金句 | 简洁有力 | "记住：..." |
| 比喻金句 | 形象生动 | "...就像..." |

## 执行流程

1. **结构选择**
   - 根据主题和类型选择模板
   - 确定段落数量

2. **大纲生成**
   - 规划每段主题
   - 确定情感弧线

3. **内容填充**
   - 逐段撰写内容
   - 融入 hook 和素材

4. **金句提炼**
   - 识别亮点句子
   - 优化可引用片段

5. **结构检验**
   - 验证逻辑连贯
   - 检查情感流动

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| writing-orchestrator | 由其调度 |
| hook-generator | 接收其标题和开头 |
| virality-scorer | 输出供其评估 |
| platform-adapter | 输出供其适配 |
| knowledge-extractor | 可接收其提取的要点 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 结构完整 | 包含必要段落 | 100% |
| 逻辑连贯 | 段落衔接自然 | ≥85分 |
| 情感流动 | 有明确弧线 | 100% |
| 金句数量 | 有可引用片段 | ≥2个 |

## 脚本

- `scripts/build_narrative.py` - 叙事构建主脚本
- `scripts/structure_templates.py` - 结构模板库
- `scripts/golden_sentence_extractor.py` - 金句提取器

## 参考资料

- `references/narrative-patterns.md` - 叙事模式详解
- `references/emotional-arc.md` - 情感弧线设计
