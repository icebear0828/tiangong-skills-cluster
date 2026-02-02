# 代码质量门禁

## 概述

质量门禁定义了每个 skill 输出必须满足的最低标准。未通过门禁的输出需要修复或重试。

## 门禁定义

### code-gen 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 语法正确性 | BLOCKER | 尝试解析代码 |
| 导入完整性 | CRITICAL | 检查所有引用是否有对应导入 |
| 函数签名匹配 | CRITICAL | 对照需求检查参数 |
| 基础注释 | MAJOR | 检查函数/类有 docstring |
| 无明显安全问题 | CRITICAL | 简单模式匹配（eval, exec 等）|

**通过标准**: 无 BLOCKER，CRITICAL ≤ 1

### test-gen 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 测试可解析 | BLOCKER | 尝试解析测试代码 |
| 测试框架正确 | CRITICAL | 匹配项目使用的框架 |
| 覆盖主路径 | MAJOR | 检查是否测试主要函数 |
| Mock 正确 | MAJOR | 检查外部依赖是否 mock |
| 断言有意义 | MINOR | 检查断言非空 |

**通过标准**: 无 BLOCKER，CRITICAL = 0，MAJOR ≤ 2

### code-review 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 报告非空 | BLOCKER | 检查输出长度 |
| 包含具体位置 | CRITICAL | 检查是否有行号引用 |
| 包含建议 | MAJOR | 检查是否有改进建议 |
| 结构化输出 | MAJOR | 检查是否按类别组织 |

**通过标准**: 无 BLOCKER，CRITICAL = 0

### refactor 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 代码可解析 | BLOCKER | 尝试解析 |
| 行为等价 | CRITICAL | 原测试仍通过 |
| 复杂度降低 | MAJOR | 对比前后复杂度 |
| 无新警告 | MINOR | 静态分析对比 |

**通过标准**: 无 BLOCKER，CRITICAL = 0

### debug 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 修复可用 | BLOCKER | 补丁可应用 |
| 原错误消失 | CRITICAL | 重现测试通过 |
| 无新错误 | CRITICAL | 其他测试不变 |
| 解释清晰 | MAJOR | 包含原因分析 |

**通过标准**: 无 BLOCKER，CRITICAL = 0

## 门禁执行流程

```
Skill 执行完成
    ↓
运行门禁检查
    ↓
├── 全部通过 → 继续下一步
│
├── BLOCKER 存在 → 立即失败，不重试
│
├── CRITICAL > 阈值 → 重试（最多 2 次）
│   ├── 重试成功 → 继续
│   └── 重试失败 → 升级处理
│
└── 仅 MAJOR/MINOR → 记录警告，继续
```

## 门禁报告格式

```json
{
  "skill_id": "code-gen",
  "passed": false,
  "checks": [
    {
      "name": "语法正确性",
      "severity": "BLOCKER",
      "passed": true,
      "message": null
    },
    {
      "name": "导入完整性",
      "severity": "CRITICAL",
      "passed": false,
      "message": "Missing import: requests"
    }
  ],
  "summary": {
    "blocker": 0,
    "critical": 1,
    "major": 0,
    "minor": 0
  }
}
```

## 质量分数计算

```
quality_score = 1.0 - (blocker * 0.5 + critical * 0.2 + major * 0.05 + minor * 0.01)
```

质量分数用于：
- 决定是否通过门禁（≥ 0.7 通过）
- 决定是否需要迭代（≥ 0.8 无需迭代）
- 记录到适应度历史

## 门禁豁免

某些情况下可豁免门禁：

| 豁免条件 | 可豁免级别 |
|---------|----------|
| 快速原型模式 | MAJOR, MINOR |
| 探索性任务 | MAJOR, MINOR |
| 用户明确跳过 | CRITICAL（需确认）|

豁免需记录到执行日志。
