---
name: sensitive-filter
description: >
  敏感字审查中间件。检测和过滤内容中的敏感词，支持政治、暴力、成人、垃圾营销、
  误导性、平台违禁词等类别。具备自动修复能力，确保内容合规。
---

# Sensitive Filter — 敏感字审查

> 详细文档: [_architecture/L2-execution/core/sensitive-filter-middleware/SKILL.md](_architecture/L2-execution/core/sensitive-filter-middleware/SKILL.md)

## 执行协议

### 1. 审查类别

| 类别 | 严重度 | 自动修复 |
|------|--------|---------|
| political — 政治敏感 | critical | 移除/替换 |
| violence — 暴力内容 | error | 委婉表达 |
| adult — 成人内容 | error | 移除/替换 |
| spam — 垃圾营销 | warning | 弱化/移除 |
| misleading — 误导表述 | warning | 添加限定词 |
| platform_banned — 平台违禁 | error | 替换同义词 |

### 2. 平台特定规则

**小红书**: 禁止"微信/wx/加V/私聊/免费领取/点击链接"，避免绝对化用语("最好的/第一/绝对")
**公众号**: 禁止"关注领红包/诱导分享/不转不是中国人"，避免震惊体
**Twitter**: 禁止"follow for follow/f4f/dm for price"

### 3. 执行流程

```
内容输入 → 多维度扫描 → 风险评估 → 自动修复(可选) → 输出报告
```

### 4. 风险等级

| 等级 | 条件 | 处理 |
|------|------|------|
| safe | 无 findings | 直接通过 |
| low_risk | 仅 warning | 通过，记录 |
| medium_risk | error + 已修复 | 通过，需确认 |
| high_risk | error + 未修复 | 需人工审核 |
| blocked | critical | 拒绝 |

### 5. 上下文感知

避免误报: "杀价/秒杀" 是安全的，"杀人" 不安全。结合上下文判断。

### 6. 输出格式

```json
{
  "passed": true/false,
  "risk_level": "safe|low_risk|medium_risk|high_risk|blocked",
  "findings": [
    {
      "category": "...",
      "severity": "warning|error|critical",
      "location": "title|body|hashtag",
      "original_text": "...",
      "issue_description": "...",
      "suggested_fix": "..."
    }
  ],
  "fixed_content": { "title": "...", "body": "...", "changes_made": ["..."] }
}
```

## 审查任务

$ARGUMENTS

---

请对内容执行全面敏感字审查，输出结构化报告。如启用 auto_fix，同时输出修复后版本。
