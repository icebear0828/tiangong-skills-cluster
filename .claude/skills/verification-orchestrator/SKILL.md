---
name: verification-orchestrator
description: >
  内化验证编排器。编排 Phase 3 内化阶段：自我解释验证→苏格拉底对话→类比检验→掌握度评估。
  由 learning-commander 调度触发。支持自适应难度调整和补救循环。
---

# Verification Orchestrator — 内化验证编排器

> 详细文档: [_architecture/L1-orchestrators/verification-orchestrator/SKILL.md](_architecture/L1-orchestrators/verification-orchestrator/SKILL.md)

## 编排流程 (Phase 3: 内化)

### Step 1: 自我解释验证
- 要求学习者解释核心概念
- 调用 `/self-explanation-validator` 识别误解

### Step 2: 苏格拉底对话
- 调用 `/socratic-questioner` 引导深入思考
- 自适应调整问题难度

### Step 3: 类比检验
- 调用 `/analogy-explainer` 澄清误解

### Step 4: 掌握度评估
- 综合验证结果、计算掌握度分数
- 等级: mastered / proficient / developing / beginning / misconceived

### Step 5: 补救建议
- 验证失败 → 返回 Phase 1/2 补救
- 通过 → 进入 Phase 4 应用

## 验证模式

| 模式 | 轮次 | 适用场景 |
|------|------|---------|
| quick_check | 1-2 | 快速确认 |
| standard | 3-5 | 常规验证 |
| thorough | 5-8 | 重要概念 |
| mastery_test | 8+ | 认证级别 |

## 用户任务

$ARGUMENTS
