---
name: rlaif-engine
description: >
  RLAIF（Reinforcement Learning from AI Feedback）自我迭代引擎。驱动 skill 的持续自我改进。
  当需要：(1) 基于执行反馈优化 skill，(2) 自动提议 skill 修订，(3) 验证修订效果，
  (4) 应用或回滚修订，(5) 执行进化循环（选择/变异/交叉/淘汰）时触发。
  这是整个 skill 集群实现自我进化的核心机制。
---

# RLAIF Engine — 自我迭代引擎

## 概述

RLAIF 引擎使 skill 能够从自身的执行经验中学习和改进。
它结合了结构化反馈循环（天工模式）和进化算法（造化模式）两种策略。

## 迭代模式

### 模式 1: 反馈驱动迭代（Feedback-Driven）

适用于单个 skill 的定向改进。

```
执行 → 反馈 → 提议修订 → 验证 → 应用/回滚
```

#### Step 1: 生成反馈

```bash
python scripts/generate_feedback.py \
  --skill-id <skill-id> \
  --execution-log <path-to-log> \
  --expected-output <path-or-description>
```

反馈维度：
- **正确性差距**：输出与预期的差异
- **效率差距**：token 使用、步骤数是否可优化
- **模式识别**：多次执行中的反复出现的问题
- **改进建议**：具体的、可操作的改进方向

输出：结构化反馈报告（JSON）

#### Step 2: 提议修订

```bash
python scripts/propose_revision.py \
  --skill-id <skill-id> \
  --feedback <feedback-json>
```

修订类型：
- **指令修订**：修改 SKILL.md 中的指令措辞、流程描述
- **脚本修订**：修改 scripts/ 中的代码逻辑
- **参考修订**：更新 references/ 中的参考资料
- **结构修订**：调整 skill 的整体组织结构

输出：修订提案（diff 格式）+ 预估改进幅度

#### Step 3: 验证修订

```bash
python scripts/validate_revision.py \
  --skill-id <skill-id> \
  --revision <revision-diff> \
  --test-cases <path-to-test-cases>
```

验证流程：
1. 创建修订后的 skill 副本（不影响原始 skill）
2. 在保留测试集上运行修订版
3. 同时运行原始版作为基线
4. 对比评分：修订版 vs 原始版
5. 检查安全边界（参考 `references/safety-bounds.md`）

判定：
- 修订版评分 > 原始版 + 0.05 → **accept**
- 修订版评分在 ±0.05 → **need-human-review**
- 修订版评分 < 原始版 - 0.05 → **reject**

#### Step 4: 应用或回滚

```bash
# 应用
python scripts/apply_revision.py --skill-id <skill-id> --revision <revision-diff>

# 回滚（如果应用后发现问题）
python scripts/rollback.py --skill-id <skill-id> --to-version <version>
```

### 模式 2: 进化循环（Evolutionary）

适用于一组同类 skill 的种群进化。

```bash
python scripts/evolve.py \
  --population <skill-ids-comma-separated> \
  --generations <N> \
  --test-suite <path-to-tests>
```

进化步骤：

1. **选择（Selection）**
   - 按适应度排序种群中所有 skill
   - 保留 top 70%
   - 标记 bottom 30% 为候选淘汰

2. **变异（Mutation）** — 调用 prime-mover/scripts/mutate_skill.py
   - 小变异（高适应度 skill）：微调指令措辞、参数
   - 大变异（低适应度 skill）：重写核心逻辑

3. **交叉（Crossover）** — 调用 prime-mover/scripts/merge_skills.py
   - 选择两个高适应度 skill
   - 提取各自优势模块
   - 融合为新 skill

4. **评测（Fitness Evaluation）** — 调用 eval-engine
   - 所有新生/变异 skill 在测试集上评测
   - 计算适应度分数

5. **淘汰（Culling）**
   - 连续 3 代适应度低于阈值 → 归档
   - 被优势 skill 完全功能覆盖 → 废弃
   - 种群超过上限 → 淘汰最低适应度

## 安全边界

参考 `references/safety-bounds.md`，关键规则：

1. **修改幅度限制**：单次迭代的 diff 不超过原始 skill 的 30%
2. **连续失败阈值**：连续 3 次修订被 reject → 冻结迭代，等待人工介入
3. **核心 skill 保护**：tier=core 的 skill 修订必须人工确认
4. **回滚能力**：所有修订必须可回滚，保留至少 3 个历史版本
5. **评测基线**：修订不得导致任何已通过测试用例回退为失败

## 日志

所有迭代记录写入 `../state/rlaif-log.jsonl`：

```json
{
  "timestamp": "ISO-8601",
  "skill_id": "...",
  "mode": "feedback-driven | evolutionary",
  "action": "propose | validate | accept | reject | rollback",
  "details": { ... },
  "fitness_before": 0.75,
  "fitness_after": 0.82
}
```
