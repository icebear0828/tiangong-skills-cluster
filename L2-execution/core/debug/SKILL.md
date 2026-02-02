---
name: debug
description: >
  调试修复 Skill。诊断和修复代码中的 bug。当需要：(1) 定位错误原因，(2) 修复 bug，
  (3) 分析崩溃日志，(4) 解决运行时异常时触发。输出诊断报告和修复补丁。
  作为核心 Skill，具有严格契约。
---

# Debug — 调试修复

## 触发条件

- 错误报告/异常信息
- 测试失败
- 用户反馈的问题

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["code", "error_info"],
  "properties": {
    "code": {
      "type": "string",
      "description": "问题代码"
    },
    "error_info": {
      "type": "object",
      "properties": {
        "error_type": { "type": "string" },
        "error_message": { "type": "string" },
        "stack_trace": { "type": "string" },
        "reproduction_steps": { "type": "string" }
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "related_files": { "type": "array" },
        "expected_behavior": { "type": "string" }
      }
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["diagnosis", "fix"],
  "properties": {
    "diagnosis": {
      "type": "object",
      "properties": {
        "root_cause": { "type": "string" },
        "affected_lines": { "type": "array" },
        "bug_type": { "type": "string" },
        "confidence": { "type": "number" }
      }
    },
    "fix": {
      "type": "object",
      "properties": {
        "fixed_code": { "type": "string" },
        "patch": { "type": "string" },
        "explanation": { "type": "string" }
      }
    },
    "prevention": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

## 诊断流程

参考 `references/debugging-strategies.md`：

1. **复现问题**
   - 理解错误信息
   - 确定触发条件
   - 验证问题存在

2. **定位原因**
   - 分析堆栈跟踪
   - 检查相关代码
   - 识别异常模式

3. **生成修复**
   - 设计修复方案
   - 实现修复代码
   - 验证修复效果

4. **预防建议**
   - 提出测试建议
   - 建议代码改进
   - 防止类似问题

## Bug 类型分类

| 类型 | 描述 | 常见原因 |
|-----|------|---------|
| 逻辑错误 | 算法/条件错误 | 边界条件、算法缺陷 |
| 空指针 | 空引用异常 | 未检查 null |
| 类型错误 | 类型不匹配 | 隐式转换、动态类型 |
| 并发错误 | 竞态条件 | 共享状态、锁缺失 |
| 资源错误 | 泄漏/未释放 | 未关闭资源 |
| 边界错误 | 数组/范围越界 | 索引计算错误 |

## 脚本

- `scripts/diagnose.py` - 诊断脚本
- `scripts/fix.py` - 修复脚本
