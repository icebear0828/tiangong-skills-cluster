---
name: adaptive-orchestrator
description: >
  蓝图编排器。根据 Blueprint JSON 配置动态编排 Worker/Skill 工作流。
  核心机制：黑板模式 + 切片器 + 中间件管道。支持省钱模式和质量模式。
---

# Adaptive Orchestrator — 蓝图编排器

> 详细文档: [_architecture/L1-orchestrators/adaptive-orchestrator/SKILL.md](_architecture/L1-orchestrators/adaptive-orchestrator/SKILL.md)

## 执行协议

收到蓝图 ID 和用户输入后，按以下步骤执行：

### 1. 加载蓝图

从 `_architecture/resources/blueprints/{blueprint_id}.json` 加载配置。

可用蓝图:
- `xiaohongshu_viral` — 小红书爆款 (static_linear, ~1000 tokens)
- `wechat_longform` — 公众号长文 (adaptive, ~3500 tokens)
- `twitter_thread` — Twitter Thread (adaptive, ~2000 tokens)
- `deep_analysis` — 深度分析 (adaptive, ~4000 tokens)

### 2. 初始化黑板

```
Blackboard:
├── Meta Zone: intent, platform, style, constraints
├── Content Zone: hook, body, cta, hashtags, platform_versions
└── Control Zone: errors, retries, quality_scores, step_status
```

将用户输入写入 Meta Zone，将蓝图默认值合并。

### 3. 步骤执行循环

对蓝图中每个 step:

```
for step in blueprint.steps:
  1. Context Slice: 只提取 step.scope 声明的字段
  2. 调度组件:
     - worker → 轻量无状态执行 (<500 tokens)
     - skill  → 深度有状态推理 (>1000 tokens)
  3. 结果写入黑板 → step.output.target
  4. Middleware 检查:
     - sensitive-filter → 敏感字拦截
     - quality-gate → 质量门控
  5. 未通过 → 触发 on_failure 策略
```

### 4. 切片器规则

只给组件传递它声明需要的数据:
- `meta.intent` → 用户意图
- `meta.platform` → 目标平台
- `content.hook.selected` → 已选标题
- 不传无关数据，阻断 Token 累积

### 5. 质量关卡

每个阶段结束后检查:

| 检查 | 标准 | 未通过 |
|------|------|--------|
| 敏感字 | passed=true | auto_fix 后重试 |
| 传播力 | ≥目标分 | 回到钩子生成 |
| 平台合规 | 100% | 格式调整 |

最多重试 3 次，超过则返回部分结果 + 错误报告。

### 6. 输出组装

从黑板收集最终内容，按蓝图 output_assembly 格式组装。

## Worker 与 Skill 的区别

| | Worker | Skill |
|---|--------|-------|
| 状态 | 无状态 | 有状态 |
| Token | <500 | >1000 |
| 场景 | 标准化文案 | 策略规划 |
| 并行 | 支持竞争 | 串行优先 |

## 蓝图执行任务

$ARGUMENTS

---

请加载指定蓝图，初始化黑板，按步骤执行并输出最终内容。
