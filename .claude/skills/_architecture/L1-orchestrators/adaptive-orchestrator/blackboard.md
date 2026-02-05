# Blackboard 数据结构定义

## 概述

黑板 (Blackboard) 是 Adaptive-Orchestrator 的核心状态管理机制。所有组件不直接传递 Context，
而是将产出写入黑板，由切片器按需提取。这种设计物理阻断了 Token 累积问题。

## 架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Shared Blackboard                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Meta Zone (元数据区)                          │  │
│  │  ┌─────────────┬─────────────┬─────────────┬─────────────────────┐   │  │
│  │  │   Intent    │    Style    │  Platform   │    Constraints      │   │  │
│  │  │  用户意图    │   风格偏好   │  目标平台    │     写作约束        │   │  │
│  │  └─────────────┴─────────────┴─────────────┴─────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Content Zone (内容区)                          │  │
│  │  ┌─────────────┬─────────────┬─────────────┬─────────────────────┐   │  │
│  │  │    Hook     │    Body     │     CTA     │     Hashtags        │   │  │
│  │  │  标题/钩子   │   正文内容   │  行动号召    │     话题标签        │   │  │
│  │  ├─────────────┴─────────────┴─────────────┴─────────────────────┤   │  │
│  │  │                    Platform Versions (平台版本)                │   │  │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │   │  │
│  │  │  │小红书版本 │ │公众号版本 │ │Twitter版 │ │ 通用版本 │         │   │  │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │   │  │
│  │  └───────────────────────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Control Zone (控制区)                          │  │
│  │  ┌─────────────┬─────────────┬─────────────┬─────────────────────┐   │  │
│  │  │   Errors    │   Retries   │Quality Score│    Step Status      │   │  │
│  │  │  错误记录    │  重试计数    │  质量评分    │     步骤状态        │   │  │
│  │  └─────────────┴─────────────┴─────────────┴─────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 数据结构定义

### Schema

```json
{
  "type": "object",
  "properties": {
    "meta_zone": {
      "type": "object",
      "description": "元数据区 - 存储任务元信息",
      "properties": {
        "intent": {
          "type": "string",
          "description": "用户意图摘要"
        },
        "style": {
          "type": "string",
          "description": "风格偏好",
          "enum": ["professional", "casual", "humorous", "inspirational", "educational"]
        },
        "platform": {
          "type": "string",
          "description": "目标平台",
          "enum": ["xiaohongshu", "wechat", "twitter", "general"]
        },
        "constraints": {
          "type": "object",
          "properties": {
            "word_count": {
              "type": "object",
              "properties": {
                "min": { "type": "integer" },
                "max": { "type": "integer" }
              }
            },
            "tone": { "type": "string" },
            "must_include": { "type": "array", "items": { "type": "string" } },
            "must_avoid": { "type": "array", "items": { "type": "string" } }
          }
        },
        "topic": {
          "type": "string",
          "description": "写作主题"
        },
        "reference_summary": {
          "type": "string",
          "description": "参考资料摘要"
        }
      }
    },
    "content_zone": {
      "type": "object",
      "description": "内容区 - 存储生成的内容",
      "properties": {
        "hook": {
          "type": "object",
          "properties": {
            "title": { "type": "string" },
            "opening": { "type": "string" },
            "variants": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "type": { "type": "string" },
                  "content": { "type": "string" },
                  "score": { "type": "number" }
                }
              }
            },
            "selected": { "type": "string" }
          }
        },
        "body": {
          "type": "object",
          "properties": {
            "content": { "type": "string" },
            "sections": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "title": { "type": "string" },
                  "content": { "type": "string" }
                }
              }
            },
            "key_points": { "type": "array", "items": { "type": "string" } },
            "quotes": { "type": "array", "items": { "type": "string" } }
          }
        },
        "cta": {
          "type": "object",
          "properties": {
            "primary": { "type": "string" },
            "secondary": { "type": "string" },
            "type": { "type": "string", "enum": ["follow", "share", "comment", "save", "click"] }
          }
        },
        "hashtags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "platform_versions": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "title": { "type": "string" },
              "body": { "type": "string" },
              "hashtags": { "type": "array", "items": { "type": "string" } },
              "word_count": { "type": "integer" },
              "emoji_density": { "type": "string" }
            }
          }
        }
      }
    },
    "control_zone": {
      "type": "object",
      "description": "控制区 - 存储执行状态",
      "properties": {
        "errors": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "step_id": { "type": "string" },
              "error_type": { "type": "string" },
              "message": { "type": "string" },
              "timestamp": { "type": "string" }
            }
          }
        },
        "retries": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "quality_scores": {
          "type": "object",
          "properties": {
            "virality": { "type": "number" },
            "hook_strength": { "type": "number" },
            "emotional_resonance": { "type": "number" },
            "platform_fit": { "type": "number" }
          }
        },
        "step_status": {
          "type": "object",
          "additionalProperties": {
            "type": "string",
            "enum": ["pending", "running", "completed", "failed", "skipped"]
          }
        },
        "sensitive_filter": {
          "type": "object",
          "properties": {
            "passed": { "type": "boolean" },
            "findings": { "type": "array" },
            "fixes_applied": { "type": "array", "items": { "type": "string" } }
          }
        },
        "iteration_count": { "type": "integer" },
        "current_stage": { "type": "string" }
      }
    }
  }
}
```

## 操作接口

### 写入操作

| 操作 | 描述 | 调用者 |
|------|------|--------|
| `write_meta(key, value)` | 写入元数据 | Orchestrator |
| `write_content(zone, key, value)` | 写入内容 | Workers/Skills |
| `write_control(key, value)` | 写入控制状态 | Middleware |
| `append_error(error)` | 追加错误记录 | 所有组件 |
| `update_step_status(step_id, status)` | 更新步骤状态 | Orchestrator |

### 读取操作

| 操作 | 描述 | 调用者 |
|------|------|--------|
| `read_meta(key)` | 读取元数据 | Context Slicer |
| `read_content(zone, key)` | 读取内容 | Context Slicer |
| `read_control(key)` | 读取控制状态 | Orchestrator |
| `get_slice(scope)` | 获取切片 | Context Slicer |
| `snapshot()` | 获取完整快照 | 最终输出 |

## 数据流示例

### 标题生成流程

```
1. 用户输入 → Meta Zone
   write_meta("intent", "写一篇关于AI的小红书")
   write_meta("platform", "xiaohongshu")

2. Title Worker 执行
   slice = get_slice(["meta.intent", "meta.platform"])
   result = title_worker.execute(slice)
   write_content("hook", "variants", result.variants)

3. 选择最佳标题
   best = select_best(read_content("hook", "variants"))
   write_content("hook", "selected", best)

4. 敏感字检查 (Middleware)
   content = read_content("hook", "selected")
   filter_result = sensitive_filter.check(content)
   write_control("sensitive_filter", filter_result)
```

### Body 生成流程

```
1. 获取必要上下文
   slice = get_slice([
     "meta.intent",
     "meta.style",
     "content.hook.selected"
   ])

2. Body Worker 执行
   result = body_worker.execute(slice)
   write_content("body", "content", result.body)
   write_content("body", "sections", result.sections)

3. 质量评分
   score = virality_scorer.score(read_content("body", "content"))
   write_control("quality_scores.virality", score)
```

## Zone 访问权限

| 组件类型 | Meta Zone | Content Zone | Control Zone |
|----------|-----------|--------------|--------------|
| Orchestrator | R/W | R | R/W |
| Workers | R (via slice) | W | - |
| Skills | R (via slice) | R/W | R |
| Middleware | R | R/W | R/W |
| Slicer | R | R | R |

## 生命周期

```
┌────────────────────────────────────────────────────────────────┐
│  1. 初始化                                                      │
│     - 创建空黑板                                                 │
│     - 写入用户输入到 Meta Zone                                   │
│     - 设置所有步骤状态为 pending                                 │
└────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│  2. 执行阶段                                                    │
│     - 组件读取切片执行任务                                       │
│     - 结果写入 Content Zone                                     │
│     - 状态更新到 Control Zone                                   │
│     - Middleware 执行检查和修复                                  │
└────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│  3. 完成阶段                                                    │
│     - 生成快照                                                  │
│     - 组装最终输出                                              │
│     - 清理临时数据                                              │
└────────────────────────────────────────────────────────────────┘
```

## 最佳实践

### 1. 最小写入原则
只写入后续步骤需要的数据，避免冗余存储

### 2. 结构化数据
使用结构化格式而非纯文本，便于切片器精准提取

### 3. 错误隔离
错误记录在 Control Zone，不污染 Content Zone

### 4. 版本追踪
对于多次迭代的内容，保留版本历史便于回溯
