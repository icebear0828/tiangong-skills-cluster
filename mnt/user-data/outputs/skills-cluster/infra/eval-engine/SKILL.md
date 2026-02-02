---
name: eval-engine
description: >
  评测引擎。为 skill 集群提供统一的评测能力。当需要：(1) 评测 skill 执行质量，
  (2) A/B 对比两个 skill 或两个版本，(3) 计算适应度分数，(4) 运行锦标赛选拔，
  (5) 执行元评测（评测评测自身）时触发。支持多维度评分、rubric 模板、基准测试。
---

# Eval Engine — 评测引擎

## 评测维度

### 代码类任务

| 维度 | 权重 | 评测方法 |
|------|------|---------|
| 功能正确性 | 40% | 运行测试用例，统计通过率 |
| 代码质量 | 25% | 静态分析 + AI 评审 |
| 架构适配 | 20% | AI 评估与上下文一致性 |
| 效率 | 15% | token 使用量、执行步骤数 |

### 文档类任务

| 维度 | 权重 | 评测方法 |
|------|------|---------|
| 内容完整性 | 35% | 检查关键点覆盖 |
| 准确性 | 30% | 与源码/需求交叉验证 |
| 可读性 | 20% | AI 评估 + 可读性指标 |
| 格式规范 | 15% | 模板符合度 |

### 通用维度（所有任务）

- **契约符合度**：输出是否符合 skill 声明的契约格式
- **幂等性**：相同输入多次执行是否给出一致结果
- **优雅降级**：边界条件/异常输入时是否合理处理

## 操作

### 执行评测

```bash
python scripts/run_eval.py \
  --skill-id <skill-id> \
  --task-type <code|doc|data|general> \
  --input <input-path-or-description> \
  --output <output-path> \
  --expected <expected-path-or-criteria> \
  [--rubric <rubric-name>]
```

### A/B 对比

```bash
python scripts/compare.py \
  --skill-a <skill-id-a> \
  --skill-b <skill-id-b> \
  --test-suite <path-to-tests> \
  --rounds <N>
```

对比逻辑：
1. 在相同测试集上分别执行两个 skill
2. 对每个测试用例，两个输出都评分
3. 统计胜/负/平次数
4. 计算 Cohen's d（效应量）判断差异是否显著

### 计算适应度

```bash
python scripts/score.py \
  --skill-id <skill-id> \
  --eval-results <results-json>
```

适应度 = 加权维度分数的加权平均值，范围 [0, 1]。

### 锦标赛选拔

```bash
python scripts/tournament.py \
  --skill-ids <id1,id2,id3,...> \
  --test-suite <path> \
  --rounds <N>
```

锦标赛规则（Swiss 制）：
1. 第 1 轮：随机配对
2. 后续轮次：相同胜场数的 skill 配对
3. 每对在随机测试子集上 A/B 对比
4. 总轮次后按积分排名

### 元评测

```bash
python scripts/meta_eval.py \
  --eval-history <path-to-eval-history.jsonl> \
  --sample-size <N>
```

元评测指标：
- **一致性**：相同输入的评分方差 < 0.1
- **区分度**：好输出与差输出的评分差 > 0.3
- **校准度**：评分与人类判断的 Spearman 相关性

## Rubric 库

参考 `references/rubrics.md` 获取预定义的评分标准。

常用 rubric：
- `code-quality-rubric`：代码质量通用标准
- `api-design-rubric`：API 设计标准
- `test-coverage-rubric`：测试覆盖率标准
- `doc-completeness-rubric`：文档完整性标准

## 输出

评测结果写入 `../state/eval-history.jsonl`：

```json
{
  "timestamp": "ISO-8601",
  "skill_id": "...",
  "eval_type": "single | compare | tournament | meta",
  "task_type": "code",
  "scores": {
    "correctness": 0.9,
    "quality": 0.8,
    "architecture": 0.85,
    "efficiency": 0.7
  },
  "fitness": 0.84,
  "details": { ... }
}
```
