---
name: perf-optimize
description: >
  性能优化 Skill。分析和优化代码性能。当需要：(1) 分析性能瓶颈，(2) 优化算法复杂度，
  (3) 减少内存使用，(4) 提升响应速度时触发。输出性能分析报告和优化建议。
  作为扩展 Skill，具有标准契约。
---

# Perf Optimize — 性能优化

## 触发条件

- 性能问题报告
- 代码审查发现性能问题
- 主动性能优化需求

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["code"],
  "properties": {
    "code": {
      "type": "string"
    },
    "performance_data": {
      "type": "object",
      "properties": {
        "profile_data": { "type": "object" },
        "metrics": { "type": "object" },
        "bottlenecks": { "type": "array" }
      }
    },
    "optimization_goals": {
      "type": "array",
      "items": {
        "enum": ["time", "memory", "io", "network"]
      }
    },
    "constraints": {
      "type": "object",
      "properties": {
        "max_complexity": { "type": "string" },
        "memory_limit": { "type": "string" }
      }
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["analysis", "optimizations"],
  "properties": {
    "analysis": {
      "type": "object",
      "properties": {
        "bottlenecks": { "type": "array" },
        "complexity": { "type": "object" },
        "hotspots": { "type": "array" }
      }
    },
    "optimizations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "description": { "type": "string" },
          "impact": { "type": "string" },
          "code_change": { "type": "string" }
        }
      }
    },
    "optimized_code": {
      "type": "string"
    },
    "expected_improvement": {
      "type": "object"
    }
  }
}
```

## 优化领域

参考 `references/optimization-techniques.md`：

### 1. 算法优化
- 降低时间复杂度
- 选择合适数据结构
- 减少不必要计算

### 2. 内存优化
- 减少对象创建
- 使用生成器
- 及时释放资源

### 3. I/O 优化
- 批量操作
- 缓存
- 异步处理

### 4. 数据库优化
- 查询优化
- 索引优化
- 连接池

## 脚本

- `scripts/analyze_perf.py` - 性能分析脚本
