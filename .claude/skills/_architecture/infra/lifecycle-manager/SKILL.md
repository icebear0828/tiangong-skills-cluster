---
name: lifecycle-manager
description: >
  Skill 生命周期管理器。管理 skill 在不同阶段间的转换：提议→实验→扩展→核心→废弃→归档。
  当需要：(1) 晋升 skill 到更高 tier，(2) 降级 skill，(3) 归档废弃 skill，
  (4) 执行健康检查时触发。与 skill-registry 和 eval-engine 协作。
---

# Lifecycle Manager — 生命周期管理器

## Skill 生命周期状态图

```
proposed → experimental → extended → core
    ↓           ↓            ↓        ↓
    └───────────┴────────────┴────────┘
                    ↓
               deprecated → archived
```

## 操作

### 晋升 (promote.py)

```bash
python scripts/promote.py --skill-id <skill-id>
```

晋升条件（自动检查）：

| 从 → 到 | 最低适应度 | 最少调用次数 | 额外条件 |
|---------|-----------|------------|---------|
| experimental → extended | 0.70 | 20 | 无连续失败 |
| extended → core | 0.90 | 50 | 契约验证通过 + 人工确认 |

晋升效果：
- 更新 registry.json 中的 tier
- 调整契约等级（flexible → standard → strict）
- 移动 skill 到对应目录
- 记录晋升日志

### 降级 (demote.py)

```bash
python scripts/demote.py --skill-id <skill-id> --reason "..."
```

降级触发条件：
- 适应度连续 3 次评测下降
- 出现严重错误（安全/正确性问题）
- 被更优 skill 替代

### 归档 (archive.py)

```bash
python scripts/archive.py --skill-id <skill-id>
```

- deprecated 状态超过 30 天自动归档
- 移动到归档目录（保留文件但不参与发现和路由）
- 可通过 restore 操作恢复

### 健康检查 (health_check.py)

```bash
python scripts/health_check.py [--skill-id <specific>] [--all]
```

检查项：
1. **存活性**：SKILL.md 存在且格式正确
2. **注册一致性**：registry.json 与实际文件系统一致
3. **适应度趋势**：过去 5 次评测的趋势（上升/稳定/下降）
4. **临时 skill 过期**：检查 TTL 是否到期
5. **孤儿 skill**：存在于文件系统但未在 registry 中注册的 skill

输出：健康报告 + 建议操作列表
