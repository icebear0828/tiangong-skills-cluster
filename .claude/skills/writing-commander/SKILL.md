---
name: writing-commander
description: >
  写作域总指挥。创意内容写作的第一入口点。分析写作任务，选择蓝图，路由到 adaptive-orchestrator 执行。
  支持小红书、公众号、Twitter 等平台的高传播力内容创作。
---

# Writing Commander — 写作域总指挥

> 详细文档: [_architecture/L0-writing-commander/SKILL.md](_architecture/L0-writing-commander/SKILL.md)

## 执行流程

收到用户写作任务后，按以下步骤执行：

### Step 1: 意图解析

从用户输入中识别：
- **平台**: 小红书/公众号/Twitter/通用
- **内容类型**: 短文案/深度文章/Thread/分析报告
- **复杂度**: S/M/L/XL

### Step 2: 蓝图选择

| 条件 | 蓝图 | 模式 |
|------|------|------|
| 小红书 + 短内容 | `xiaohongshu_viral` | 省钱模式 (~1000 tokens) |
| 公众号 + 长文 | `wechat_longform` | 质量模式 (~3500 tokens) |
| Twitter + Thread | `twitter_thread` | 平衡模式 (~2000 tokens) |
| 深度分析/研究 | `deep_analysis` | 质量模式 (~4000 tokens) |
| 单一任务(写标题) | 直接 L2 | 最小开销 (<500 tokens) |

### Step 3: 路由执行

**S 级 (简单)**: 直接调用对应 L2 skill
- "写标题" → `/hook-generator`
- "评分传播力" → `/virality-scorer`
- "适配平台" → `/platform-adapter`

**M/L 级 (复杂)**: 调用 adaptive-orchestrator 执行蓝图
1. 读取蓝图 JSON: `_architecture/resources/blueprints/{blueprint_id}.json`
2. 初始化黑板 (Blackboard)
3. 按蓝图步骤执行 Workers/Skills
4. 敏感字审查 (sensitive-filter-middleware)
5. 质量关卡检查
6. 输出最终内容

### Step 4: 三阶段写作框架

对于完整写作任务，遵循三阶段：

**Stage 1 策划** (并行扇出):
- 使用 `content-curator` 收集素材
- 使用 `trend-tracker` 追踪热点
- 两个 subagent 并行执行，汇合策略

**Stage 2 创作** (混合模式):
- Step 2.1: 钩子生成 — 竞争模式，生成多版本标题，选最佳
- Step 2.2: 叙事构建 — 串行，基于最佳钩子构建正文
- Step 2.3: 验证 — 并行执行 `virality-scorer` + `sensitive-filter`
- 质量关卡: score >= target AND filter.passed? 否则回到 2.1 (最多 3 次)

**Stage 3 分发** (并行扇出):
- Step 3.1: 平台适配 — 多平台并行适配
- Step 3.2: 最终敏感字审查 — 逐版本检查
- 输出最终内容

### Step 5: 敏感字审查

所有路径强制经过 `sensitive-filter-middleware`:
- 创作验证 (Stage 2): 与评分并行，早期发现
- 最终审查 (Stage 3): 确保适配后仍合规
- auto_fix=true: 自动修复问题

## 平台策略

| 平台 | 标题 | 正文 | 特殊要求 |
|------|------|------|---------|
| 小红书 | ≤20字 | 500-1000字 | emoji密度高, 话题标签3-8个 |
| 公众号 | ≤64字 | 1500-3000字 | 段落分明, 小标题, 金句加粗 |
| Twitter | ≤280字/条 | 3-15条Thread | Hook-first, 观点鲜明 |

## 质量标准

| 维度 | 阈值 |
|------|------|
| 传播力评分 | ≥75 |
| 敏感字审查 | passed=true |
| 平台合规 | 100% |
| 路由准确 | ≥95% |

## 用户任务

$ARGUMENTS

---

请分析写作任务，选择蓝图，按上述流程执行完整写作。最终输出包含：标题、正文、CTA、话题标签、传播力评分、敏感字审查结果。
