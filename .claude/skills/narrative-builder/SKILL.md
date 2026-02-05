---
name: narrative-builder
description: >
  叙事结构构建 Skill。基于主题和钩子构建完整叙事，支持多种结构
  （问题解决、故事弧、列表、教程），生成有逻辑有金句的正文内容。
---

# Narrative Builder — 叙事构建

> 详细文档: [_architecture/L2-execution/core/narrative-builder/SKILL.md](_architecture/L2-execution/core/narrative-builder/SKILL.md)

## 执行协议

### 叙事结构模板

| 结构 | 适用场景 | 段落构成 |
|------|---------|---------|
| problem_solution | 行业分析/深度文 | 背景→问题→分析→方案→结论 |
| story_arc | 故事型内容 | 开场→冲突→发展→高潮→启发 |
| listicle | 清单/推荐 | 引入→列表项(3-10)→总结 |
| tutorial | 教程/指南 | 概述→步骤1,2,3→注意事项→总结 |
| thread | Twitter Thread | 钩子→要点(2-8)→CTA |
| xiaohongshu_flow | 小红书种草 | 钩子→共鸣→方案→心得→CTA |

### 输出要素

- 完整正文 (符合字数要求)
- 分段内容 (sections)
- 核心要点 (key_points)
- 金句 (quotes) — 可截图/可引用的亮点句

### 平台风格

- **小红书**: 短段落, emoji 点缀, 口语化, 换行频繁
- **公众号**: 完整段落, 小标题分隔, 逻辑递进, 金句加粗
- **Twitter**: 每条≤280字, 独立成句, 编号连贯

## 构建任务

$ARGUMENTS

---

请根据主题和结构类型，构建完整叙事内容，包含分段、要点和金句。
