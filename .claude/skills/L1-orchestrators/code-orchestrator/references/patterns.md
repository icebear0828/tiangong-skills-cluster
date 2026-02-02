# 代码任务分解模式

## 概述

本文档定义了常见代码任务的分解模板，供 code-orchestrator 使用。

## 基础模式

### 1. Feature Implementation（功能实现）

**输入**: 功能需求描述
**输出**: 代码文件 + 测试文件

```
需求分析 (内置)
    ↓
code-gen (生成核心代码)
    ↓
test-gen (生成测试)
    ↓
code-review (审查)
```

**分解规则**:
- 如果需求中包含"测试"关键词 → 包含 test-gen
- 如果需求中包含"文档"关键词 → 包含 doc-gen
- 默认总是包含 code-review

### 2. Bug Fix（Bug 修复）

**输入**: 错误描述 + 相关代码
**输出**: 修复补丁 + 验证测试

```
debug (定位并修复)
    ↓
test-gen (验证测试)
    ↓
code-review (确认修复)
```

**分解规则**:
- 如果有明确错误信息 → debug 置信度高
- 如果需要排查 → debug 可能需要多次

### 3. Code Optimization（代码优化）

**输入**: 代码文件 + 优化目标
**输出**: 优化后代码

```
code-review (识别问题)
    ↓
refactor (重构)
    ↓
test-gen (确保行为不变)
    ↓
code-review (验证改进)
```

**分解规则**:
- 如果目标是"可读性" → refactor 侧重结构
- 如果目标是"性能" → 考虑 perf-optimize

### 4. API Endpoint（API 端点）

**输入**: API 需求
**输出**: 端点代码 + 测试 + 文档

```
api-design (可选，如需求不明确)
    ↓
code-gen (生成端点)
    ↓
test-gen (API 测试)
    ↓
doc-gen (API 文档)
```

## 组合模式

### Full Feature（完整功能）

```
api-design ─────────┐
                    ↓
db-schema ──→ code-gen (集成)
                    ↓
               test-gen
                    ↓
               code-review
                    ↓
               doc-gen
```

### TDD 模式

```
test-gen (先写测试)
    ↓
code-gen (实现代码)
    ↓
code-review (审查)
    ↓
refactor (如需要)
```

## 分解决策树

```
任务输入
    │
    ├── 包含"修复"/"bug"/"error"?
    │   └── YES → Bug Fix 模式
    │
    ├── 包含"重构"/"优化结构"?
    │   └── YES → Code Optimization 模式
    │
    ├── 包含"API"/"端点"?
    │   └── YES → API Endpoint 模式
    │
    └── DEFAULT → Feature Implementation 模式
```

## 步骤间数据传递

| 从 | 到 | 传递内容 |
|----|----|---------|
| code-gen | test-gen | 代码文件路径, 函数签名列表 |
| code-gen | code-review | 代码文件路径, 需求摘要 |
| debug | test-gen | 修复的文件, bug 描述 |
| code-review | refactor | 审查报告, 需改进的行号 |
| refactor | test-gen | 修改后的文件, diff |

## 质量检查点

每个模式在关键步骤设置检查点：

| 模式 | 检查点位置 | 检查内容 |
|-----|----------|---------|
| Feature | code-gen 后 | 代码可执行 |
| Feature | test-gen 后 | 测试可运行 |
| Bug Fix | debug 后 | 错误不再复现 |
| Optimization | refactor 后 | 测试仍通过 |
