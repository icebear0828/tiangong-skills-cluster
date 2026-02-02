---
name: creative-code
description: >
  创意编程 Skill。进行探索性、创造性的编程任务。当需要：(1) 实验性代码，
  (2) 创新解决方案，(3) 艺术编程，(4) 原型探索时触发。不受严格约束，
  鼓励创新和实验。作为实验 Skill，具有灵活契约。
---

# Creative Code — 创意编程

## 触发条件

- 探索性任务
- 需要创新解决方案
- 实验性功能
- 艺术/可视化编程

## 输入契约 (Flexible)

```json
{
  "type": "object",
  "required": ["inspiration"],
  "properties": {
    "inspiration": {
      "type": "string",
      "description": "灵感描述或目标"
    },
    "constraints": {
      "type": "object",
      "description": "可选约束"
    },
    "style": {
      "type": "string",
      "enum": ["experimental", "artistic", "generative", "playful"]
    }
  }
}
```

## 输出契约 (Flexible)

```json
{
  "type": "object",
  "required": ["code"],
  "properties": {
    "code": {
      "type": "string"
    },
    "explanation": {
      "type": "string",
      "description": "创意思路说明"
    },
    "variations": {
      "type": "array",
      "description": "可能的变体"
    }
  }
}
```

## 创意方向

参考 `references/creative-patterns.md`：

### 1. 生成艺术
- 分形
- 粒子系统
- 程序化图形

### 2. 数据可视化
- 交互式可视化
- 信息图表
- 实时数据艺术

### 3. 算法音乐
- 程序化音乐
- 音频可视化

### 4. 实验性代码
- 元编程
- DSL 设计
- 新范式探索

## 特点

- 不追求"正确"答案
- 鼓励多种尝试
- 重视过程和探索
- 接受不完美
