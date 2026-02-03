---
name: prototype
description: >
  快速原型 Skill。快速构建可运行的原型。当需要：(1) 验证想法，(2) 快速演示，
  (3) MVP 开发，(4) 概念验证时触发。强调速度和核心功能，不追求完美。
  作为实验 Skill，具有灵活契约。
---

# Prototype — 快速原型

## 触发条件

- 想法验证
- 快速演示需求
- MVP 开发
- 概念验证 (PoC)

## 输入契约 (Flexible)

```json
{
  "type": "object",
  "required": ["idea"],
  "properties": {
    "idea": {
      "type": "string",
      "description": "想法描述"
    },
    "scope": {
      "type": "string",
      "enum": ["minimal", "basic", "functional"]
    },
    "target_platform": {
      "type": "string",
      "enum": ["web", "cli", "api", "mobile"]
    },
    "time_constraint": {
      "type": "string",
      "description": "时间约束"
    }
  }
}
```

## 输出契约 (Flexible)

```json
{
  "type": "object",
  "required": ["prototype"],
  "properties": {
    "prototype": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "files": { "type": "array" },
        "run_instructions": { "type": "string" }
      }
    },
    "limitations": {
      "type": "array",
      "description": "当前原型的限制"
    },
    "next_steps": {
      "type": "array",
      "description": "后续完善方向"
    }
  }
}
```

## 原型原则

参考 `references/prototyping-guide.md`：

### 1. 快速迭代
- 先跑起来
- 快速反馈
- 逐步完善

### 2. 最小可行
- 核心功能优先
- 跳过非必要
- 硬编码可接受

### 3. 技术负债可接受
- 不追求完美代码
- 文档可简化
- 测试可省略

### 4. 验证优先
- 验证核心假设
- 收集用户反馈
- 评估可行性
