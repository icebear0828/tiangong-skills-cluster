---
name: code-review
description: >
  代码审查 Skill。对代码进行全面审查，检查质量、安全性、性能和最佳实践。当需要：
  (1) 审查新代码，(2) PR 评审，(3) 安全检查，(4) 代码质量评估时触发。
  输出结构化的审查报告，包含问题列表和改进建议。作为核心 Skill，具有严格契约。
---

# Code Review — 代码审查

## 触发条件

- 代码生成后的质量检查
- PR/MR 评审请求
- 重构前的现状分析
- 定期代码健康检查

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["code"],
  "properties": {
    "code": {
      "type": "string",
      "description": "要审查的代码内容"
    },
    "file_path": {
      "type": "string",
      "description": "代码文件路径"
    },
    "language": {
      "type": "string",
      "description": "编程语言"
    },
    "context": {
      "type": "object",
      "description": "上下文信息",
      "properties": {
        "requirement": { "type": "string" },
        "related_files": { "type": "array" }
      }
    },
    "focus_areas": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["security", "performance", "style", "logic", "all"]
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["issues", "summary"],
  "properties": {
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "severity": { "enum": ["critical", "major", "minor", "suggestion"] },
          "category": { "enum": ["security", "bug", "performance", "style", "maintainability"] },
          "line_number": { "type": "integer" },
          "code_snippet": { "type": "string" },
          "description": { "type": "string" },
          "suggestion": { "type": "string" }
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_issues": { "type": "integer" },
        "critical_count": { "type": "integer" },
        "quality_score": { "type": "number" }
      }
    },
    "recommendations": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

## 审查维度

参考 `references/review-checklist.md`：

### 1. 安全性 (Security)
- SQL 注入风险
- XSS 漏洞
- 硬编码凭证
- 不安全的随机数
- 路径遍历

### 2. 正确性 (Correctness)
- 逻辑错误
- 边界条件
- 空指针/空引用
- 资源泄漏
- 并发问题

### 3. 性能 (Performance)
- 不必要的循环
- N+1 查询
- 内存泄漏
- 不当的数据结构

### 4. 可维护性 (Maintainability)
- 代码复杂度
- 重复代码
- 命名清晰度
- 注释质量

### 5. 风格 (Style)
- 格式一致性
- 命名规范
- 导入顺序
- 文件组织

## 严重级别定义

| 级别 | 描述 | 示例 |
|-----|------|------|
| critical | 必须立即修复 | SQL 注入、数据泄露 |
| major | 应该修复 | 逻辑错误、性能问题 |
| minor | 建议修复 | 代码重复、命名不佳 |
| suggestion | 可选改进 | 风格建议、优化提示 |

## 执行流程

1. **解析代码**
   - 识别语言和框架
   - 构建 AST（如可能）
   - 提取函数和类结构

2. **执行检查**
   - 运行各维度检查
   - 记录发现的问题
   - 标记行号和代码片段

3. **评估严重性**
   - 根据规则判断级别
   - 考虑上下文影响

4. **生成报告**
   - 汇总问题
   - 计算质量分数
   - 提供改进建议

## 质量分数计算

```
quality_score = 1.0 - (
    critical * 0.3 +
    major * 0.15 +
    minor * 0.05 +
    suggestion * 0.01
) / max(lines_of_code / 100, 1)
```

## 脚本

- `scripts/review.py` - 代码审查主脚本
- `scripts/security_check.py` - 安全检查脚本
