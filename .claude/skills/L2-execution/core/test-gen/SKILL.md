---
name: test-gen
description: >
  测试生成 Skill。为代码自动生成测试用例。当需要：(1) 为新代码生成测试，(2) 增加测试覆盖率，
  (3) 生成边界测试，(4) 生成集成测试时触发。支持多种测试框架，生成单元测试、
  集成测试和属性测试。作为核心 Skill，具有严格契约。
---

# Test Gen — 测试生成

## 触发条件

- 代码生成后自动触发
- 需求描述包含"测试"关键词
- 由 code-orchestrator 调度

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["code"],
  "properties": {
    "code": {
      "type": "string",
      "description": "要测试的代码"
    },
    "file_path": {
      "type": "string"
    },
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "typescript", "java", "go"]
    },
    "test_framework": {
      "type": "string",
      "description": "测试框架 (pytest, jest, junit, etc.)"
    },
    "functions": {
      "type": "array",
      "description": "要测试的函数签名列表"
    },
    "test_types": {
      "type": "array",
      "items": {
        "enum": ["unit", "integration", "property", "edge_case"]
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["test_code", "test_files"],
  "properties": {
    "test_code": {
      "type": "string"
    },
    "test_files": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "content": { "type": "string" }
        }
      }
    },
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "function_under_test": { "type": "string" },
          "test_type": { "type": "string" },
          "description": { "type": "string" }
        }
      }
    },
    "coverage_estimate": {
      "type": "number"
    }
  }
}
```

## 测试类型

参考 `references/test-patterns.md`：

### 1. 单元测试 (Unit Tests)
- 测试单个函数/方法
- 隔离外部依赖
- 快速执行

### 2. 集成测试 (Integration Tests)
- 测试组件交互
- 使用真实依赖或 Test Double
- 验证契约

### 3. 属性测试 (Property Tests)
- 基于属性的随机测试
- 发现边界情况
- 使用 hypothesis/fast-check

### 4. 边界测试 (Edge Case Tests)
- 空值/null
- 空集合
- 极值
- 特殊字符

## 执行流程

1. **解析代码**
   - 提取函数/类定义
   - 分析参数类型
   - 识别依赖

2. **生成测试策略**
   - 确定测试类型
   - 规划测试用例
   - 准备 mock/fixture

3. **生成测试代码**
   - 创建测试类/函数
   - 编写 setup/teardown
   - 添加断言

4. **优化**
   - 去重
   - 添加参数化
   - 补充边界用例

## 测试框架支持

| 语言 | 框架 | Mock 库 |
|-----|------|--------|
| Python | pytest | unittest.mock |
| JavaScript | Jest | jest.mock |
| TypeScript | Jest / Vitest | jest.mock |
| Java | JUnit 5 | Mockito |
| Go | testing | testify/mock |

## 脚本

- `scripts/generate_tests.py` - 测试生成主脚本
