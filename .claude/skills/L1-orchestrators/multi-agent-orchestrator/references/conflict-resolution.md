# 冲突解决策略

## 概述

当多个 Skill 的输出存在冲突时，需要有明确的解决策略。

## 冲突类型

### 1. 文件冲突 (File Conflict)

多个 Skill 尝试修改同一文件。

**检测方法**:
```python
def detect_file_conflict(outputs):
    file_map = {}
    for skill_id, output in outputs.items():
        for file in output.files:
            if file in file_map:
                return Conflict("file", file, [file_map[file], skill_id])
            file_map[file] = skill_id
    return None
```

**解决策略**:

| 策略 | 适用场景 | 实现 |
|-----|---------|------|
| 顺序执行 | 修改不重叠 | 转为 sequential |
| 合并 | 修改可合并 | 3-way merge |
| 优先级 | 有主导方 | 保留高优先级 |
| 人工 | 复杂冲突 | 升级到 L3 |

### 2. 语义冲突 (Semantic Conflict)

输出在语义上矛盾。

**示例**:
- api-design 定义字段为 `user_id`
- db-schema 定义字段为 `userId`

**检测方法**:
- 提取两个输出的关键实体
- 检查命名一致性
- 检查类型一致性

**解决策略**:

| 策略 | 实现 |
|-----|------|
| 命名标准化 | 应用项目命名规范 |
| 主导对齐 | 以上游 Skill 为准 |
| 投票 | 多数决定 |

### 3. 依赖冲突 (Dependency Conflict)

Skill 之间的依赖关系矛盾。

**示例**:
- A depends_on B
- B depends_on A

**检测方法**:
```python
def detect_cycle(dag):
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in dag[node].depends_on:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    for node in dag:
        if node not in visited:
            if dfs(node):
                return True
    return False
```

**解决策略**:
- 打破循环：移除优先级最低的依赖
- 合并节点：将循环中的节点合并

### 4. 资源冲突 (Resource Conflict)

Context 或 token 资源不足。

**检测方法**:
```python
def check_resource(dag, budget):
    total_tokens = sum(skill.estimated_tokens for skill in dag.values())
    return total_tokens <= budget
```

**解决策略**:
- 压缩：减少 context 传递
- 分阶段：拆分为多个独立 DAG
- 简化：移除非核心 Skill

## 解决流程

```
检测到冲突
    ↓
分类冲突类型
    ↓
├── 文件冲突 → 尝试合并 → 成功/升级
├── 语义冲突 → 应用标准化 → 验证
├── 依赖冲突 → 重排序 → 验证
└── 资源冲突 → 压缩/拆分 → 验证
    ↓
验证解决方案
    ↓
├── 通过 → 继续执行
└── 失败 → 升级到人工
```

## 合并算法

### 代码合并

使用 3-way merge 算法：

```python
def three_way_merge(base, ours, theirs):
    """
    base: 原始版本
    ours: 第一个 skill 的修改
    theirs: 第二个 skill 的修改
    """
    # 1. 计算 diff
    diff_ours = compute_diff(base, ours)
    diff_theirs = compute_diff(base, theirs)

    # 2. 检测冲突区域
    conflicts = find_overlapping_hunks(diff_ours, diff_theirs)

    # 3. 非冲突区域直接合并
    merged = apply_non_conflicting(base, diff_ours, diff_theirs)

    # 4. 冲突区域标记
    for conflict in conflicts:
        mark_conflict(merged, conflict)

    return merged, conflicts
```

### 配置合并

JSON/YAML 配置合并：

```python
def merge_configs(configs):
    """合并多个配置文件"""
    result = {}
    for config in configs:
        for key, value in config.items():
            if key not in result:
                result[key] = value
            elif isinstance(value, dict) and isinstance(result[key], dict):
                result[key] = merge_configs([result[key], value])
            elif isinstance(value, list) and isinstance(result[key], list):
                result[key] = list(set(result[key] + value))
            else:
                # 冲突：使用后来的值（或标记冲突）
                result[key] = value
    return result
```

## 冲突日志

记录所有冲突及其解决方案：

```json
{
  "timestamp": "2026-02-02T00:00:00Z",
  "dag_id": "...",
  "conflicts": [
    {
      "type": "file",
      "involved_skills": ["code-gen-1", "code-gen-2"],
      "resource": "src/main.py",
      "resolution": "three_way_merge",
      "success": true
    }
  ]
}
```

## 预防措施

### 设计时预防

1. **明确职责边界**: 每个 Skill 负责不同的文件/模块
2. **使用命名空间**: 不同 Skill 输出到不同目录
3. **定义主导 Skill**: 同领域任务指定主导方

### 运行时预防

1. **依赖检查**: 执行前验证 DAG 无冲突
2. **锁机制**: 对共享资源加锁
3. **版本控制**: 保留每个 Skill 输出的版本
