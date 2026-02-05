# Context Slicer 切片器逻辑定义

## 概述

Context Slicer (切片器) 是 Adaptive-Orchestrator 的核心组件，负责从黑板中精准提取当前步骤所需的最小数据集。
通过切片机制，实现 Context 消耗的物理控制，消除因全量传递导致的 Token 累积和幻觉问题。

## 设计原则

| 原则 | 说明 | 收益 |
|------|------|------|
| 最小必要 | 只提取声明的字段 | 减少 Token 消耗 |
| 精准定位 | 支持嵌套路径访问 | 避免冗余数据 |
| 类型安全 | 验证切片数据类型 | 减少运行时错误 |
| 可追溯 | 记录切片来源 | 便于调试 |

## 架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Context Slicer                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Scope Declaration (作用域声明)                    │   │
│  │                                                                     │   │
│  │  Blueprint Step Definition:                                         │   │
│  │  { "id": "body", "worker": "body-worker",                          │   │
│  │    "scope": ["meta.intent", "content.hook.selected"] }             │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                               │                                             │
│                               ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Path Resolver (路径解析器)                        │   │
│  │                                                                     │   │
│  │  "meta.intent"           → blackboard.meta_zone.intent             │   │
│  │  "content.hook.selected" → blackboard.content_zone.hook.selected   │   │
│  │  "control.retries"       → blackboard.control_zone.retries         │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                               │                                             │
│                               ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Slice Builder (切片构建器)                        │   │
│  │                                                                     │   │
│  │  Output Slice:                                                      │   │
│  │  {                                                                  │   │
│  │    "intent": "写一篇关于AI的小红书",                                 │   │
│  │    "hook": "5个AI工具让你效率翻倍"                                  │   │
│  │  }                                                                  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Scope 语法

### 基本语法

```
scope_path := zone "." key ("." nested_key)*
zone       := "meta" | "content" | "control"
key        := alphanumeric string
nested_key := alphanumeric string
```

### 示例

| Scope Path | 解析为 | 数据类型 |
|------------|--------|----------|
| `meta.intent` | `blackboard.meta_zone.intent` | string |
| `meta.platform` | `blackboard.meta_zone.platform` | enum |
| `meta.constraints.word_count` | `blackboard.meta_zone.constraints.word_count` | object |
| `content.hook.selected` | `blackboard.content_zone.hook.selected` | string |
| `content.hook.variants` | `blackboard.content_zone.hook.variants` | array |
| `content.body.content` | `blackboard.content_zone.body.content` | string |
| `content.body.sections` | `blackboard.content_zone.body.sections` | array |
| `control.quality_scores.virality` | `blackboard.control_zone.quality_scores.virality` | number |
| `control.step_status` | `blackboard.control_zone.step_status` | object |

### 特殊 Scope

| Scope | 说明 | 包含内容 |
|-------|------|---------|
| `all` | 完整黑板 | 仅用于需要全量上下文的 Skill |
| `meta.*` | 所有元数据 | meta_zone 全部内容 |
| `content.*` | 所有内容 | content_zone 全部内容 |
| `control.*` | 所有控制状态 | control_zone 全部内容 |

## 切片策略

### Worker 模式 (轻量)

Workers 采用最小切片策略：

```json
{
  "title-worker": {
    "scope": ["meta.intent", "meta.platform", "meta.style"],
    "max_tokens": 200
  },
  "body-worker": {
    "scope": ["meta.intent", "content.hook.selected", "meta.constraints"],
    "max_tokens": 400
  },
  "cta-worker": {
    "scope": ["meta.platform", "content.hook.selected"],
    "max_tokens": 100
  }
}
```

### Skill 模式 (丰富)

Skills 可声明更大范围的切片：

```json
{
  "narrative-builder": {
    "scope": ["meta.*", "content.hook.*", "content.body.key_points"],
    "max_tokens": 1500
  },
  "hook-generator": {
    "scope": ["meta.*", "control.quality_scores"],
    "max_tokens": 800
  }
}
```

## 切片流程

### 1. 声明解析

```python
def parse_scope(scope_list):
    """解析 scope 声明列表"""
    paths = []
    for scope in scope_list:
        if scope == "all":
            return ["meta_zone", "content_zone", "control_zone"]
        elif scope.endswith(".*"):
            zone = scope.split(".")[0]
            paths.append(f"{zone}_zone.*")
        else:
            paths.append(scope)
    return paths
```

### 2. 路径解析

```python
def resolve_path(path, blackboard):
    """解析路径获取值"""
    parts = path.split(".")
    zone_map = {
        "meta": "meta_zone",
        "content": "content_zone",
        "control": "control_zone"
    }

    current = blackboard[zone_map[parts[0]]]
    for part in parts[1:]:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current
```

### 3. 切片构建

```python
def build_slice(scope_list, blackboard):
    """构建切片数据包"""
    slice_data = {}

    for scope in scope_list:
        path_parts = scope.split(".")
        key = path_parts[-1]  # 使用最后一级作为键
        value = resolve_path(scope, blackboard)

        if value is not None:
            slice_data[key] = value

    return slice_data
```

### 4. Token 预算检查

```python
def check_token_budget(slice_data, max_tokens):
    """检查切片是否超出 Token 预算"""
    estimated_tokens = estimate_tokens(slice_data)

    if estimated_tokens > max_tokens:
        # 触发压缩策略
        return compress_slice(slice_data, max_tokens)

    return slice_data
```

## 压缩策略

当切片超出 Token 预算时，按优先级压缩：

| 优先级 | 策略 | 说明 |
|--------|------|------|
| 1 | 截断长文本 | 保留前 N 字符 + "..." |
| 2 | 移除 variants | 只保留 selected |
| 3 | 摘要替换 | 用摘要替换详细内容 |
| 4 | 移除可选字段 | 保留必需字段 |

### 压缩示例

```json
// 原始切片
{
  "intent": "写一篇关于AI的小红书文章，介绍5个提升效率的AI工具...(省略500字)",
  "hook_variants": [
    {"type": "numeric", "content": "5个AI工具...", "score": 85},
    {"type": "suspense", "content": "用了这些工具...", "score": 78},
    {"type": "pain_point", "content": "还在手动...", "score": 72}
  ]
}

// 压缩后切片
{
  "intent": "写一篇关于AI的小红书文章，介绍5个提升效率的AI工具...",  // 截断到200字
  "hook": "5个AI工具..."  // 只保留最高分
}
```

## 预定义切片模板

### 标题生成切片

```json
{
  "template_id": "title_generation",
  "scope": ["meta.intent", "meta.platform", "meta.style"],
  "flatten": true,
  "output_format": {
    "topic": "{intent}",
    "platform": "{platform}",
    "style": "{style}"
  }
}
```

### 正文生成切片

```json
{
  "template_id": "body_generation",
  "scope": [
    "meta.intent",
    "meta.constraints.word_count",
    "content.hook.selected"
  ],
  "flatten": true,
  "output_format": {
    "topic": "{intent}",
    "title": "{hook.selected}",
    "word_limit": "{constraints.word_count.max}"
  }
}
```

### 平台适配切片

```json
{
  "template_id": "platform_adaptation",
  "scope": [
    "meta.platform",
    "content.hook.selected",
    "content.body.content",
    "content.cta.primary"
  ],
  "flatten": true,
  "output_format": {
    "platform": "{platform}",
    "title": "{hook.selected}",
    "body": "{body.content}",
    "cta": "{cta.primary}"
  }
}
```

### 敏感字检查切片

```json
{
  "template_id": "sensitive_check",
  "scope": [
    "meta.platform",
    "content.hook.selected",
    "content.body.content",
    "content.hashtags"
  ],
  "flatten": false,
  "output_format": {
    "platform": "{platform}",
    "content": {
      "title": "{hook.selected}",
      "body": "{body.content}",
      "hashtags": "{hashtags}"
    }
  }
}
```

## Token 预算参考

| 组件类型 | 典型切片大小 | Token 预算 |
|----------|--------------|-----------|
| title-worker | 50-100 字 | ~150 tokens |
| body-worker | 200-400 字 | ~500 tokens |
| cta-worker | 30-50 字 | ~100 tokens |
| hook-generator | 300-500 字 | ~800 tokens |
| narrative-builder | 800-1200 字 | ~1500 tokens |
| sensitive-filter | 500-1000 字 | ~1200 tokens |
| platform-adapter | 600-1000 字 | ~1200 tokens |

## 调试接口

### 切片预览

```python
def preview_slice(step_id, blueprint, blackboard):
    """预览某步骤的切片内容"""
    step = blueprint.get_step(step_id)
    scope = step.get("scope", [])
    slice_data = build_slice(scope, blackboard)

    return {
        "step_id": step_id,
        "scope": scope,
        "slice_data": slice_data,
        "estimated_tokens": estimate_tokens(slice_data),
        "budget": step.get("max_tokens", "unlimited")
    }
```

### 切片历史

```python
def get_slice_history(execution_id):
    """获取执行过程中所有切片记录"""
    return [
        {
            "step_id": "title",
            "timestamp": "...",
            "scope": ["meta.intent", "meta.platform"],
            "tokens_used": 120
        },
        # ...
    ]
```

## 最佳实践

### 1. 声明明确的 Scope
避免使用 `all`，明确列出所需字段

### 2. 使用切片模板
对于常见场景，使用预定义模板确保一致性

### 3. 监控 Token 消耗
记录每个切片的 Token 消耗，优化 Scope 定义

### 4. 版本化切片
对于迭代场景，保留切片版本便于对比
