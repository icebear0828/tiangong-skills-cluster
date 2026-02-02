---
name: arch-explore
description: >
  架构探索 Skill。探索和比较不同的架构方案。当需要：(1) 技术选型，(2) 架构设计，
  (3) 方案对比，(4) 可行性分析时触发。输出方案对比报告和建议。
  作为实验 Skill，具有灵活契约。
---

# Arch Explore — 架构探索

## 触发条件

- 新项目架构设计
- 技术选型决策
- 架构升级评估
- 可行性研究

## 输入契约 (Flexible)

```json
{
  "type": "object",
  "required": ["problem"],
  "properties": {
    "problem": {
      "type": "string",
      "description": "要解决的问题或目标"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "scale": { "type": "string" },
        "budget": { "type": "string" },
        "team_skills": { "type": "array" },
        "timeline": { "type": "string" }
      }
    },
    "existing_system": {
      "type": "object",
      "description": "现有系统描述"
    }
  }
}
```

## 输出契约 (Flexible)

```json
{
  "type": "object",
  "required": ["analysis"],
  "properties": {
    "analysis": {
      "type": "object",
      "properties": {
        "problem_understanding": { "type": "string" },
        "key_requirements": { "type": "array" }
      }
    },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "pros": { "type": "array" },
          "cons": { "type": "array" },
          "fit_score": { "type": "number" }
        }
      }
    },
    "recommendation": {
      "type": "object"
    },
    "next_steps": {
      "type": "array"
    }
  }
}
```

## 探索维度

参考 `references/architecture-patterns.md`：

### 1. 架构风格
- 单体
- 微服务
- 事件驱动
- Serverless

### 2. 技术栈
- 语言选择
- 框架选择
- 数据库选择

### 3. 部署架构
- 本地部署
- 云部署
- 混合部署

### 4. 质量属性
- 可扩展性
- 可维护性
- 性能
- 安全性
