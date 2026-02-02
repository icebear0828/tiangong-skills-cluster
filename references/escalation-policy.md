# 异常升级策略

## 概述

本文档定义了 Skills 集群中异常情况的处理和升级流程。

## 异常分级

### Level 1: 可自愈异常 (Self-Recoverable)

**特征**: 可通过重试或简单调整解决

| 异常类型 | 处理策略 | 最大重试次数 |
|---------|---------|------------|
| Skill 执行超时 | 增加 timeout 重试 | 2 |
| 输出格式轻微偏差 | 格式修正后继续 | 1 |
| 非关键资源缺失 | 跳过或使用默认值 | 1 |
| 临时网络/IO 错误 | 指数退避重试 | 3 |

**处理流程**:
```
异常发生 → 记录日志 → 应用处理策略 → 重试
         ↓ (重试失败)
         升级到 Level 2
```

### Level 2: 需编排器介入 (Orchestrator Intervention)

**特征**: 需要更换 Skill 或调整执行计划

| 异常类型 | 处理策略 |
|---------|---------|
| Skill 输出完全不符合契约 | 更换同能力的备选 Skill |
| Skill 连续失败 2 次 | 升级到更高层级编排器 |
| 执行计划某节点阻塞 | 尝试绕过或并行化处理 |
| 资源不足 (context) | 拆分任务或压缩 context |

**处理流程**:
```
L1 异常升级
    ↓
编排器接收 → 分析原因 → 选择策略 → 执行
                        ↓ (策略失败)
                        升级到 Level 3
```

### Level 3: 需人工确认 (Human Confirmation Required)

**特征**: 涉及不可逆操作或无法自动判断的决策

| 异常类型 | 触发条件 | 人工操作选项 |
|---------|---------|-------------|
| Core Skill 修改 | tier=core 的任何修订 | 批准 / 拒绝 / 修改后批准 |
| 安全边界触及 | 修改幅度 > 30% | 批准 / 拒绝 |
| 连续 3 次修订被拒 | RLAIF 迭代冻结 | 手动修复 / 解冻 / 废弃 |
| 适应度骤降 | 下降 > 0.3 | 回滚 / 调查 / 维持 |

**处理流程**:
```
L2 异常升级
    ↓
生成诊断报告 → 暂停执行 → 等待人工确认
                            ↓
              人工响应 → 执行决定 → 记录结果
```

### Level 4: 紧急制动 (Emergency Brake)

**特征**: 系统稳定性受威胁，必须立即停止

| 触发条件 | 自动操作 |
|---------|---------|
| 某 Skill 适应度骤降 > 0.3 | 冻结该 Skill |
| 连续 3 个不同 Skill 修订被拒 | 冻结所有自动迭代 |
| 未捕获异常导致 Skill 不可用 | 标记为 broken，停止路由 |
| state/ 数据一致性校验失败 | 冻结所有写操作 |

**处理流程**:
```
紧急条件触发
    ↓
立即停止相关操作 → 记录 severity=critical → 生成诊断报告
    ↓
冻结相关组件 → 发送告警 → 等待人工介入
```

## 升级链路

```
执行层 Skill 异常
    ↓ (L1 自愈失败)
领域编排器 (code/doc/data-orchestrator)
    ↓ (L2 介入失败)
Multi-Agent Orchestrator
    ↓ (仍失败)
Meta-Commander 重新规划
    ↓ (重规划失败或触发 L3 条件)
人工确认
    ↓ (紧急条件)
紧急制动
```

## 异常日志格式

所有异常记录到相应日志文件：

```json
{
  "timestamp": "ISO-8601",
  "level": "L1 | L2 | L3 | L4",
  "severity": "info | warning | error | critical",
  "source": {
    "skill_id": "...",
    "orchestrator": "...",
    "operation": "..."
  },
  "exception": {
    "type": "...",
    "message": "...",
    "stack_trace": "..."
  },
  "handling": {
    "strategy": "...",
    "attempts": 0,
    "result": "resolved | escalated | pending"
  },
  "context": {
    "task_id": "...",
    "execution_plan_id": "..."
  }
}
```

## 诊断报告模板

Level 3 及以上异常自动生成诊断报告：

```markdown
# 异常诊断报告

## 基本信息
- 报告时间: {timestamp}
- 异常级别: {level}
- 影响范围: {affected_skills}

## 异常描述
{exception_description}

## 根因分析
{root_cause_analysis}

## 尝试的处理措施
{attempted_resolutions}

## 建议操作
{recommended_actions}

## 相关日志
{relevant_logs}
```

## 恢复检查清单

从异常状态恢复后执行：

1. [ ] 验证 registry.json 一致性
2. [ ] 运行受影响 Skill 的健康检查
3. [ ] 确认 eval-history 和 rlaif-log 无损坏
4. [ ] 验证回滚成功（如执行了回滚）
5. [ ] 更新异常日志的最终处理结果
6. [ ] 评估是否需要长期修复措施
