---
name: refactor
description: >
  代码重构 Skill。在保持行为不变的前提下改进代码结构。当需要：(1) 改善代码可读性，
  (2) 降低复杂度，(3) 消除重复，(4) 应用设计模式时触发。输出重构后的代码和变更说明。
  必须确保重构前后行为等价。作为核心 Skill，具有严格契约。
---

# Refactor — 代码重构

## 触发条件

- code-review 后发现需要改进
- 复杂度超过阈值
- 由 code-orchestrator 调度

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["code"],
  "properties": {
    "code": {
      "type": "string",
      "description": "要重构的代码"
    },
    "file_path": {
      "type": "string"
    },
    "refactor_goals": {
      "type": "array",
      "items": {
        "enum": ["readability", "complexity", "duplication", "pattern", "performance"]
      }
    },
    "review_report": {
      "type": "object",
      "description": "code-review 的审查报告"
    },
    "preserve_interface": {
      "type": "boolean",
      "default": true,
      "description": "是否保持公共接口不变"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["refactored_code", "changes"],
  "properties": {
    "refactored_code": {
      "type": "string"
    },
    "changes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "description": { "type": "string" },
          "before": { "type": "string" },
          "after": { "type": "string" }
        }
      }
    },
    "metrics_before": {
      "type": "object"
    },
    "metrics_after": {
      "type": "object"
    },
    "breaking_changes": {
      "type": "array"
    }
  }
}
```

## 重构类型

参考 `references/refactoring-catalog.md`：

### 1. 提取方法 (Extract Method)
将代码块提取为独立函数

### 2. 内联方法 (Inline Method)
将简单函数内联到调用处

### 3. 重命名 (Rename)
改善命名清晰度

### 4. 移动 (Move)
将代码移到更合适的位置

### 5. 提取类/接口 (Extract Class/Interface)
分离职责

### 6. 消除重复 (Remove Duplication)
提取公共代码

### 7. 简化条件 (Simplify Conditional)
减少嵌套和复杂条件

## 行为等价保证

1. **测试验证**: 重构前后测试结果一致
2. **接口保持**: 公共接口签名不变
3. **语义保持**: 输入输出映射不变

## 脚本

- `scripts/refactor.py` - 重构主脚本
