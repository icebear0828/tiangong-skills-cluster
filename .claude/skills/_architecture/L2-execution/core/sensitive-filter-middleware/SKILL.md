---
name: sensitive-filter-middleware
description: >
  敏感字审查中间件 (L2 Core)。作为切面逻辑嵌入写作流程，负责检测和过滤敏感内容。
  支持政治敏感、暴力、成人内容、垃圾营销、误导性表述、平台违禁词等类别。
  具备自动修复能力，确保内容在各平台合规发布。作为必须执行的审查环节，具有严格契约。
---

# Sensitive Filter Middleware — 敏感字审查中间件

## 触发条件

- Stage 2 创作阶段：与 virality-scorer 并行执行
- Stage 3 分发阶段：各平台版本最终检查
- 任何内容变更后的自动检查

## 集成点

| 集成点 | 阶段 | 执行模式 | 目的 |
|--------|------|---------|------|
| 创作验证 | Stage 2 | 与 virality-scorer 并行 | 早期发现，避免无效迭代 |
| 最终审查 | Stage 3 | 串行 | 确保适配后内容仍合规 |

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["content", "platform"],
  "properties": {
    "content": {
      "type": "object",
      "required": ["title", "body"],
      "properties": {
        "title": {
          "type": "string",
          "description": "内容标题"
        },
        "body": {
          "type": "string",
          "description": "内容正文"
        },
        "hashtags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "话题标签"
        }
      },
      "description": "待审查内容"
    },
    "platform": {
      "type": "string",
      "enum": ["xiaohongshu", "wechat", "twitter", "general"],
      "description": "目标发布平台"
    },
    "filter_config": {
      "type": "object",
      "properties": {
        "strictness": {
          "type": "string",
          "enum": ["standard", "strict", "platform_specific"],
          "default": "standard",
          "description": "审查严格程度"
        },
        "categories": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["political", "violence", "adult", "spam", "misleading", "platform_banned"]
          },
          "default": ["political", "violence", "adult", "spam"],
          "description": "启用的审查类别"
        },
        "auto_fix": {
          "type": "boolean",
          "default": true,
          "description": "是否自动修复问题"
        },
        "fix_strategy": {
          "type": "string",
          "enum": ["replace", "remove", "rephrase"],
          "default": "replace",
          "description": "修复策略"
        }
      },
      "description": "过滤器配置"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["passed", "risk_level", "findings"],
  "properties": {
    "passed": {
      "type": "boolean",
      "description": "是否通过审查"
    },
    "risk_level": {
      "type": "string",
      "enum": ["safe", "low_risk", "medium_risk", "high_risk", "blocked"],
      "description": "风险等级"
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["category", "severity", "location", "original_text", "issue_description"],
        "properties": {
          "category": {
            "type": "string",
            "description": "问题类别"
          },
          "severity": {
            "type": "string",
            "enum": ["warning", "error", "critical"],
            "description": "严重程度"
          },
          "location": {
            "type": "string",
            "enum": ["title", "body", "hashtag"],
            "description": "问题位置"
          },
          "original_text": {
            "type": "string",
            "description": "原始文本片段"
          },
          "issue_description": {
            "type": "string",
            "description": "问题描述"
          },
          "suggested_fix": {
            "type": "string",
            "description": "建议修复"
          }
        }
      },
      "description": "发现的问题列表"
    },
    "fixed_content": {
      "type": "object",
      "description": "auto_fix=true 时返回修复后的内容",
      "properties": {
        "title": {
          "type": "string",
          "description": "修复后标题"
        },
        "body": {
          "type": "string",
          "description": "修复后正文"
        },
        "hashtags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "修复后标签"
        },
        "changes_made": {
          "type": "array",
          "items": { "type": "string" },
          "description": "所做的修改说明"
        }
      }
    },
    "audit_trail": {
      "type": "object",
      "properties": {
        "timestamp": { "type": "string" },
        "platform": { "type": "string" },
        "strictness": { "type": "string" },
        "categories_checked": { "type": "array", "items": { "type": "string" } },
        "total_issues": { "type": "integer" },
        "auto_fixed": { "type": "integer" }
      },
      "description": "审计追踪记录"
    }
  }
}
```

## 审查类别

| 类别 | 说明 | 严重度 | 自动修复策略 |
|------|------|--------|-------------|
| political | 政治敏感词、争议性政治话题 | critical | 移除/替换 |
| violence | 暴力、血腥、恐怖内容 | error | 移除/委婉表达 |
| adult | 成人内容、色情暗示 | error | 移除/替换 |
| spam | 垃圾营销、诱导关注、过度促销 | warning | 弱化/移除 |
| misleading | 误导性表述、虚假声明 | warning | 添加限定词 |
| platform_banned | 平台特定违禁词 | error | 替换同义词 |

## 平台特定规则

### 小红书 (xiaohongshu)

```json
{
  "platform": "xiaohongshu",
  "banned_patterns": [
    "微信", "wx", "加V", "私聊",
    "免费领取", "点击链接",
    "最好的", "第一", "绝对"
  ],
  "required_disclaimers": {
    "ad_content": "含广告",
    "sponsored": "赞助合作"
  },
  "word_restrictions": {
    "max_title_length": 20,
    "banned_emojis": []
  }
}
```

### 微信公众号 (wechat)

```json
{
  "platform": "wechat",
  "banned_patterns": [
    "关注领红包", "诱导分享",
    "不转不是中国人", "转发有好运",
    "最新消息", "震惊"
  ],
  "required_disclaimers": {
    "medical_content": "仅供参考，不构成医疗建议",
    "financial_content": "投资有风险"
  },
  "word_restrictions": {
    "max_title_length": 64
  }
}
```

### Twitter/X

```json
{
  "platform": "twitter",
  "banned_patterns": [
    "follow for follow", "f4f",
    "dm for price", "link in bio"
  ],
  "required_disclaimers": {
    "ad_content": "#ad",
    "sponsored": "#sponsored"
  },
  "word_restrictions": {
    "max_tweet_length": 280
  }
}
```

## 执行流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. 内容接收与解析                                                           │
│     - 解析 title, body, hashtags                                            │
│     - 加载平台特定规则                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. 多维度扫描                                                               │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  政治敏感   │  │  暴力内容   │  │  成人内容   │  │  垃圾营销   │        │
│  │  Detector   │  │  Detector   │  │  Detector   │  │  Detector   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│         └────────────────┼────────────────┼────────────────┘               │
│                          ▼                ▼                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                         │
│  │  误导表述   │  │  平台违禁   │  │  上下文分析  │                         │
│  │  Detector   │  │  Detector   │  │  Analyzer   │                         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                         │
│         └────────────────┼────────────────┘                                │
│                          ▼                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. 风险评估                                                                │
│     - 汇总所有 findings                                                     │
│     - 计算综合风险等级                                                       │
│     - 判定是否通过                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. 自动修复 (如果启用)                                                      │
│     - 对每个 finding 应用修复策略                                            │
│     - 验证修复后内容                                                        │
│     - 记录修改说明                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. 输出结果                                                                │
│     - 生成审查报告                                                          │
│     - 返回修复后内容 (如适用)                                               │
│     - 记录审计追踪                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 风险等级判定

| 风险等级 | 条件 | 处理方式 |
|---------|------|---------|
| safe | 无任何 findings | 直接通过 |
| low_risk | 仅有 warning 级 findings | 通过，记录警告 |
| medium_risk | 有 error 级 findings，已自动修复 | 通过，需确认 |
| high_risk | 有 error 级 findings，无法完全修复 | 需人工审核 |
| blocked | 有 critical 级 findings | 拒绝，必须修改 |

## 修复策略

### Replace 策略 (替换)
```json
{
  "strategy": "replace",
  "mappings": {
    "最好的": "优质的",
    "第一": "领先的",
    "免费": "限时",
    "微信": "私信"
  }
}
```

### Remove 策略 (移除)
```json
{
  "strategy": "remove",
  "patterns": [
    "点击链接.*",
    "关注领取.*",
    "#f4f"
  ]
}
```

### Rephrase 策略 (改写)
```json
{
  "strategy": "rephrase",
  "rules": [
    {
      "pattern": "这是最好的.*",
      "replacement": "这是一款优质的{product}",
      "context_aware": true
    }
  ]
}
```

## 与黑板的交互

### 读取

```json
{
  "scope": [
    "meta.platform",
    "content.hook.selected",
    "content.body.content",
    "content.hashtags"
  ]
}
```

### 写入

```json
{
  "target": "control_zone.sensitive_filter",
  "data": {
    "passed": true,
    "findings": [],
    "fixes_applied": []
  }
}
```

## 与其他 Skill 的关系

| Skill | 关系 | 交互方式 |
|-------|------|---------|
| adaptive-orchestrator | 被调用 | 作为 Middleware 嵌入 |
| virality-scorer | 并行执行 | Stage 2 同时进行 |
| platform-adapter | 串行后执行 | Stage 3 最终检查 |
| title-worker | 输出检查 | 检查生成的标题 |
| body-worker | 输出检查 | 检查生成的正文 |

## 上下文感知检测

### 误报降低机制

某些词在特定上下文中是安全的：

```json
{
  "context_rules": [
    {
      "word": "杀",
      "safe_contexts": ["杀价", "秒杀", "杀手级"],
      "dangerous_contexts": ["杀人", "自杀"]
    },
    {
      "word": "死",
      "safe_contexts": ["死忠粉", "死磕"],
      "dangerous_contexts": ["去死", "死亡"]
    }
  ]
}
```

### 情感分析辅助

结合情感分析判断内容意图：
- 正面情感 + 争议词 → 降低风险等级
- 负面情感 + 争议词 → 提高风险等级

## 审计与合规

### 审计日志格式

```json
{
  "audit_log": {
    "execution_id": "uuid",
    "timestamp": "ISO-8601",
    "platform": "xiaohongshu",
    "input_hash": "sha256",
    "findings_count": 2,
    "risk_level": "medium_risk",
    "auto_fixes_applied": 2,
    "manual_review_required": false,
    "compliance_version": "v2.0"
  }
}
```

### 合规报告

用于内容合规审计的详细报告：
- 原始内容快照
- 所有检测结果
- 修复前后对比
- 审核人/系统签名

## 性能指标

| 指标 | 目标值 |
|------|--------|
| 检测延迟 | <500ms |
| Token 消耗 | ~200 tokens |
| 误报率 | <5% |
| 漏报率 | <1% |

## 配置文件

- `rules/political.json` - 政治敏感词库
- `rules/violence.json` - 暴力内容词库
- `rules/adult.json` - 成人内容词库
- `rules/spam.json` - 垃圾营销词库
- `rules/platform/*.json` - 平台特定规则

## 扩展点

### 自定义检测器

```python
class CustomDetector:
    def detect(self, content, platform):
        """自定义检测逻辑"""
        findings = []
        # 实现检测逻辑
        return findings
```

### 自定义修复器

```python
class CustomFixer:
    def fix(self, finding, content):
        """自定义修复逻辑"""
        fixed_content = content
        # 实现修复逻辑
        return fixed_content, change_description
```
