---
name: code-orchestrator
description: >
  代码领域编排器。当代码相关的多步骤任务需要协调执行时触发。负责分解代码任务为子任务，
  协调 code-gen、test-gen、code-review、refactor、debug 等核心 skill 的执行顺序，
  管理代码质量门禁，确保输出满足质量标准。支持顺序链和迭代精炼两种模式。
---

# Code Orchestrator — 代码领域编排器

## 触发条件

由 Meta-Commander 路由触发，当任务满足以下条件时：
- 复杂度为 M 级
- 主要领域为 code
- 需要多个代码相关 skill 协作

## 输入格式

```json
{
  "task_id": "...",
  "task_description": "...",
  "complexity": "M",
  "domains": ["code", "test"],
  "context": {
    "language": "python",
    "framework": "fastapi",
    "existing_files": []
  }
}
```

## 编排模式

### 模式 1: Sequential Chain（顺序链）

适用场景：标准代码开发流程

```
code-gen → test-gen → code-review
```

执行流程：
1. 接收任务描述
2. 运行 `scripts/decompose_task.py` 分解为子任务
3. 按顺序执行每个子任务对应的 skill
4. 每个 skill 完成后检查质量门禁
5. 通过门禁后传递输出到下一个 skill
6. 全部完成后运行 `scripts/merge_outputs.py` 合并输出

### 模式 2: Iterative Refinement（迭代精炼）

适用场景：质量驱动的代码开发

```
code-gen → code-review → 评分 < 阈值? → refactor → code-review (loop max 3)
```

执行流程：
1. 执行 code-gen 生成初始代码
2. 执行 code-review 评审
3. 如果评审分数 < 0.8，提取改进建议
4. 执行 refactor 应用改进
5. 重新 code-review
6. 最多迭代 3 次

## 子任务分解规则

参考 `references/patterns.md` 中的任务分解模板。

常见分解模式：

| 任务类型 | 分解为 |
|---------|-------|
| 实现功能并测试 | code-gen → test-gen |
| 实现功能并文档 | code-gen → doc-gen |
| 修复并验证 | debug → test-gen → code-review |
| 优化代码 | code-review → refactor → test-gen |

## 质量门禁

每个步骤完成后执行质量检查，参考 `references/quality-gates.md`：

### code-gen 门禁
- [ ] 生成的代码可解析（无语法错误）
- [ ] 包含必要的导入
- [ ] 函数/类有基本注释

### test-gen 门禁
- [ ] 测试代码可解析
- [ ] 至少覆盖主要功能路径
- [ ] mock 依赖正确

### code-review 门禁
- [ ] 评审报告包含具体行号
- [ ] 给出改进建议
- [ ] 安全问题标记

## 输出合并

`scripts/merge_outputs.py` 负责合并多个 skill 的输出：

```json
{
  "task_id": "...",
  "status": "completed",
  "outputs": {
    "code_files": ["path/to/code.py"],
    "test_files": ["path/to/test_code.py"],
    "review_report": "path/to/review.md"
  },
  "quality_scores": {
    "code-gen": 0.85,
    "test-gen": 0.80,
    "code-review": 0.90
  },
  "execution_log": [...]
}
```

## 异常处理

- Skill 执行失败：重试 1 次，仍失败则跳过该 skill 并记录
- 质量门禁未通过：尝试迭代修复，3 次后升级到 multi-agent-orchestrator
- Context 超限：压缩前序输出，只保留关键信息

## 与其他组件交互

- 查阅 `../references/capability-map.md` 确认 skill 能力
- 调用 `../scripts/task_analyzer.py` 分析子任务
- 报告执行结果到 Meta-Commander
