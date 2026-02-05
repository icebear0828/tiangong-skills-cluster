---
name: adaptive-orchestrator
description: >
  自适应蓝图编排器 (L1)。作为蓝图虚拟机，根据 Blueprint JSON 配置动态编排工作流。
  核心机制：黑板模式 (Blackboard) + 切片器 (Context Slicer) + 中间件管道 (Middleware Pipeline)。
  支持省钱模式 (Worker 链) 和深度模式 (Skill 链)，实现一套代码无限场景。
  由 writing-commander 或其他 L0 层调度触发。
---

# Adaptive Orchestrator — 自适应蓝图编排器

## 核心概念

### 蓝图虚拟机

Adaptive-Orchestrator 是一个"蓝图虚拟机"，它：
1. 接收 Blueprint JSON 配置文件
2. 解析步骤定义和依赖关系
3. 动态调度 Workers 或 Skills
4. 通过黑板模式管理状态
5. 通过切片器实现最小 Context 传递

### 设计原则

| 原则 | 说明 | 收益 |
|------|------|------|
| 黑板模式 | 组件不直接传递 Context，产出写入黑板 | 物理阻断 Token 累积 |
| 切片器 | 只抓取当前步骤声明需要的字段 | 消除幻觉来源 |
| 嵌入式中间件 | 敏感字检查作为切面逻辑 | 100% 覆盖 + 自愈 |
| 蓝图驱动 | JSON 配置业务逻辑 | 一套代码，无限场景 |

## 触发条件

- 由 writing-commander 传递 Blueprint ID + 用户输入
- 进入完整写作流程（非单一任务）
- 需要动态编排多个 Workers/Skills

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["blueprint_id", "user_input"],
  "properties": {
    "blueprint_id": {
      "type": "string",
      "description": "蓝图配置文件 ID",
      "enum": ["xiaohongshu_viral", "wechat_longform", "twitter_thread", "deep_analysis"]
    },
    "user_input": {
      "type": "object",
      "required": ["topic"],
      "properties": {
        "topic": { "type": "string", "description": "写作主题" },
        "platform": {
          "type": "string",
          "enum": ["xiaohongshu", "wechat", "twitter", "general"],
          "description": "目标平台"
        },
        "intent": { "type": "string", "description": "用户意图" },
        "style": { "type": "string", "description": "风格偏好" },
        "constraints": {
          "type": "object",
          "properties": {
            "word_count": { "type": "object" },
            "tone": { "type": "string" },
            "must_include": { "type": "array", "items": { "type": "string" } }
          }
        },
        "reference_materials": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "execution_config": {
      "type": "object",
      "properties": {
        "max_retries": { "type": "integer", "default": 3 },
        "quality_threshold": { "type": "number", "default": 75 },
        "enable_middleware": { "type": "boolean", "default": true },
        "parallel_execution": { "type": "boolean", "default": true }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["execution_result", "blackboard_snapshot", "quality_report"],
  "properties": {
    "execution_result": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["success", "partial", "failed"] },
        "blueprint_id": { "type": "string" },
        "steps_executed": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "step_id": { "type": "string" },
              "component": { "type": "string" },
              "component_type": { "type": "string", "enum": ["worker", "skill"] },
              "status": { "type": "string", "enum": ["completed", "skipped", "failed", "retried"] },
              "retries": { "type": "integer" },
              "output_key": { "type": "string" }
            }
          }
        },
        "total_tokens_used": { "type": "integer" },
        "execution_time_ms": { "type": "integer" }
      }
    },
    "blackboard_snapshot": {
      "type": "object",
      "description": "黑板最终状态快照",
      "properties": {
        "meta_zone": {
          "type": "object",
          "properties": {
            "intent": { "type": "string" },
            "style": { "type": "string" },
            "platform": { "type": "string" }
          }
        },
        "content_zone": {
          "type": "object",
          "properties": {
            "hook": { "type": "string" },
            "body": { "type": "string" },
            "cta": { "type": "string" },
            "hashtags": { "type": "array", "items": { "type": "string" } }
          }
        },
        "control_zone": {
          "type": "object",
          "properties": {
            "errors": { "type": "array", "items": { "type": "string" } },
            "retries": { "type": "integer" },
            "quality_scores": { "type": "object" }
          }
        }
      }
    },
    "quality_report": {
      "type": "object",
      "properties": {
        "overall_score": { "type": "number" },
        "virality_score": { "type": "number" },
        "sensitive_filter_passed": { "type": "boolean" },
        "platform_compliance": { "type": "boolean" },
        "improvements_applied": { "type": "array", "items": { "type": "string" } }
      }
    },
    "final_content": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "body": { "type": "string" },
        "platform_versions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "platform": { "type": "string" },
              "content": { "type": "string" },
              "hashtags": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      }
    }
  }
}
```

## 架构设计

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Adaptive-Orchestrator (L1) - 蓝图虚拟机                                  │
│                                                                          │
│  [Shared Blackboard (共享黑板)]                                          │
│  ┌───────────────────────┬──────────────────────┬─────────────────────┐  │
│  │ Meta Zone             │ Content Zone         │ Control Zone        │  │
│  │ - Intent/Style        │ - Hook / Body / CTA  │ - Errors / Retries  │  │
│  │ - Platform            │ - Hashtags           │ - Quality Scores    │  │
│  │ - Constraints         │ - Versions           │ - Step Status       │  │
│  └───────────────────────┴──────────────────────┴─────────────────────┘  │
│                                                                          │
│  [Context Slicer (切片器)] - 只切出当前步骤所需的最小数据包                │
│  [Middleware Pipeline] - 敏感词拦截 + 质量门控 (切面逻辑)                 │
└──────────────────────────────────────────────────────────────────────────┘
           │ Dispatch (Input_Slice)
           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  L2 Components (执行单元) - 多态设计                                      │
│                                                                          │
│  A. Workers (轻工)                B. Skills (技工)                        │
│  - 特性: 无状态, 纯函数            - 特性: 有记忆, 强推理                  │
│  - 消耗: <500 tokens              - 消耗: >3000 tokens                   │
│  - 场景: 标准化文案, 格式化        - 场景: 策略规划, 深度长文               │
└──────────────────────────────────────────────────────────────────────────┘
```

## 蓝图类型

### 静态线性蓝图 (static_linear)
```json
{
  "type": "static_linear",
  "steps": [
    { "id": "hook", "worker": "title-worker", "scope": ["intent"] },
    { "id": "body", "worker": "body-worker", "scope": ["intent", "hook.output"] }
  ]
}
```
- 适用场景：小红书短文案、标准营销内容
- 特点：步骤固定，执行快速，Token 消耗低
- 预计消耗：~1000 tokens

### 自适应蓝图 (adaptive)
```json
{
  "type": "adaptive",
  "steps": [
    { "id": "strategy", "skill": "strategy-skill", "scope": "all" },
    { "id": "content", "skill": "narrative-skill", "scope": "all", "retry": 3 }
  ]
}
```
- 适用场景：深度分析、公众号长文
- 特点：支持迭代、质量门控、条件分支
- 预计消耗：~3000+ tokens

## 执行流程

### Phase 1: 蓝图加载
1. 根据 blueprint_id 加载对应 JSON 配置
2. 解析步骤依赖关系
3. 初始化黑板数据结构

### Phase 2: 步骤执行
```
for each step in blueprint.steps:
    1. Context Slicer 切出所需字段
    2. 调用 Worker/Skill
    3. 结果写入黑板
    4. Middleware 检查 (敏感字/质量)
    5. 如未通过，触发修复或重试
```

### Phase 3: 质量关卡
| 检查点 | 标准 | 未通过处理 |
|--------|------|-----------|
| 敏感字审查 | passed=true | 自动修复后重试 |
| 传播力评分 | ≥目标分 | 迭代优化 |
| 平台合规 | 100% | 调整格式 |

### Phase 4: 输出组装
1. 从黑板收集最终内容
2. 组装平台版本
3. 生成质量报告

## Subagent 调度策略

### 并行模式

| 模式 | 说明 | 使用场景 |
|------|------|---------|
| 并行扇出 | 独立任务并行，汇合结果 | Stage 1 策划, Stage 3 分发 |
| 竞争生成 | 多版本候选，选择最佳 | Stage 2 hook 生成 |
| 验证并行 | 独立验证任务并行 | Stage 2 验证 |

### Context 管理

- 每个 subagent 接收最小必要 context (通过切片器)
- subagent 间通过黑板传递结构化摘要
- 编排器 context 预算: ≤20% 总 context

## Skill 调用表

| Skill/Worker | 调用阶段 | 执行模式 | Token 预算 |
|--------------|---------|---------|-----------|
| content-curator | Stage 1 | subagent 并行 | ~800 |
| trend-tracker | Stage 1 | subagent 并行 | ~600 |
| title-worker | Stage 2.1 | Worker 竞争 (3个) | ~300×3 |
| hook-generator | Stage 2.1 | Skill 模式 | ~1000 |
| body-worker | Stage 2.2 | Worker 串行 | ~500 |
| narrative-builder | Stage 2.2 | Skill 模式 | ~2000 |
| virality-scorer | Stage 2.3 | subagent 并行 | ~500 |
| sensitive-filter-middleware | Stage 2.3, 3.2 | Middleware | ~200 |
| platform-adapter | Stage 3.1 | subagent 并行 | ~600×N |
| cta-worker | Stage 3.1 | Worker 串行 | ~200 |

## 质量关卡 (更新版)

| 阶段 | 检查点 | 标准 | 未通过处理 |
|------|--------|------|-----------|
| Stage 2 | 传播力评分 | ≥目标分 | 迭代优化 |
| Stage 2 | **敏感字审查** | passed=true | 修复后重新生成 |
| Stage 3 | 平台合规 | 100% | 调整格式 |
| Stage 3 | **最终敏感字检查** | passed=true | 修复违规内容 |

## 与其他组件的关系

| 组件 | 关系 | 说明 |
|------|------|------|
| writing-commander | 被调用 | 由其选择蓝图并触发 |
| blackboard | 内部组件 | 状态管理 |
| context-slicer | 内部组件 | 最小 Context 传递 |
| sensitive-filter-middleware | 调用 | 切面式敏感字检查 |
| title-worker | 调用 | Worker 模式执行 |
| body-worker | 调用 | Worker 模式执行 |
| cta-worker | 调用 | Worker 模式执行 |
| hook-generator | 调用 | Skill 模式执行 |
| narrative-builder | 调用 | Skill 模式执行 |
| virality-scorer | 调用 | 评分验证 |
| platform-adapter | 调用 | 平台适配 |

## 错误处理

### 重试策略
```
max_retries: 3
retry_conditions:
  - sensitive_filter_failed (auto_fix 后重试)
  - quality_below_threshold (重新生成)
  - component_timeout (重试同一组件)
```

### 降级策略
```
fallback_chain:
  - Worker 失败 → 切换到 Skill 模式
  - Skill 失败 → 返回部分结果 + 错误报告
  - 全部失败 → 返回原始输入 + 详细诊断
```

## 配置文件

- `blackboard.md` - 黑板数据结构定义
- `context-slicer.md` - 切片器逻辑定义
- `resources/blueprints/*.json` - 蓝图配置文件

## 参考资料

- `references/orchestration-patterns.md` - 编排模式
- `references/quality-gates.md` - 质量关卡定义
