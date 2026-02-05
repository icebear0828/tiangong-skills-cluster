---
name: conflict-resolver
description: >
  冲突解决器 Skill。分析分支间合并冲突，提供智能解决方案，区分自动可解决和需人工介入的冲突。
  当需要：(1) 合并冲突分析，(2) 自动解决简单冲突，(3) 复杂结构冲突重构建议时触发。
  支持调用 refactor skill 处理复杂结构冲突。作为核心分支管理 Skill，具有严格契约。
---

# Conflict Resolver — 冲突解决器

## 触发条件

- branch-validator 检测到合并冲突时
- 由 branch-orchestrator 条件调度
- 用户手动请求冲突分析时
- PR 合并前的冲突预检

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["base_branch", "head_branch", "conflict_files"],
  "properties": {
    "base_branch": {
      "type": "string",
      "description": "目标分支（合并入的分支）"
    },
    "head_branch": {
      "type": "string",
      "description": "源分支（被合并的分支）"
    },
    "conflict_files": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "conflict_type"],
        "properties": {
          "path": { "type": "string", "description": "冲突文件路径" },
          "conflict_type": {
            "type": "string",
            "enum": ["content", "rename", "delete", "mode"],
            "description": "冲突类型"
          },
          "base_content": { "type": "string", "description": "基准版本内容" },
          "ours_content": { "type": "string", "description": "目标分支内容" },
          "theirs_content": { "type": "string", "description": "源分支内容" }
        }
      },
      "minItems": 1,
      "description": "冲突文件列表"
    },
    "resolution_strategy": {
      "type": "string",
      "enum": ["auto_prefer_base", "auto_prefer_head", "smart_merge", "manual_only"],
      "default": "smart_merge",
      "description": "解决策略偏好"
    },
    "context": {
      "type": "object",
      "properties": {
        "repo_root": { "type": "string" },
        "file_owners": { "type": "object", "additionalProperties": { "type": "string" } },
        "recent_changes": { "type": "array", "items": { "type": "string" } }
      },
      "description": "仓库上下文信息"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["conflicts", "resolutions", "auto_resolvable", "refactor_needed"],
  "properties": {
    "conflicts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["file", "type", "severity", "analysis"],
        "properties": {
          "file": { "type": "string", "description": "冲突文件路径" },
          "type": {
            "type": "string",
            "enum": ["content", "rename", "delete", "mode", "structural"],
            "description": "冲突类型"
          },
          "severity": {
            "type": "string",
            "enum": ["trivial", "low", "medium", "high", "critical"],
            "description": "冲突严重度"
          },
          "analysis": {
            "type": "string",
            "description": "冲突原因分析"
          },
          "affected_lines": {
            "type": "object",
            "properties": {
              "start": { "type": "integer" },
              "end": { "type": "integer" },
              "count": { "type": "integer" }
            }
          }
        }
      },
      "description": "冲突详细分析"
    },
    "resolutions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["file", "strategy", "confidence"],
        "properties": {
          "file": { "type": "string" },
          "strategy": {
            "type": "string",
            "enum": ["accept_ours", "accept_theirs", "smart_merge", "manual", "refactor"],
            "description": "建议的解决策略"
          },
          "merged_content": {
            "type": "string",
            "description": "自动合并后的内容（仅当 auto_resolvable 时）"
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "解决方案置信度"
          },
          "explanation": {
            "type": "string",
            "description": "解决思路说明"
          },
          "warnings": {
            "type": "array",
            "items": { "type": "string" },
            "description": "潜在风险提示"
          }
        }
      },
      "description": "解决方案列表"
    },
    "auto_resolvable": {
      "type": "boolean",
      "description": "是否所有冲突均可自动解决"
    },
    "refactor_needed": {
      "type": "boolean",
      "description": "是否需要调用 refactor skill 处理结构性冲突"
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_conflicts": { "type": "integer" },
        "auto_resolved": { "type": "integer" },
        "manual_required": { "type": "integer" },
        "refactor_required": { "type": "integer" },
        "overall_risk": {
          "type": "string",
          "enum": ["low", "medium", "high"]
        }
      },
      "description": "解决汇总"
    }
  }
}
```

## 执行流程

1. **冲突分类**
   - 解析每个冲突文件的类型
   - 区分内容冲突、重命名冲突、删除冲突、权限冲突
   - 识别结构性冲突（大范围重构导致）

2. **逐文件分析**
   - 对比三方内容（base / ours / theirs）
   - 分析冲突根因（并行修改 / 逻辑冲突 / 重构冲突）
   - 评估冲突严重度

3. **解决方案生成**
   - trivial 冲突：自动合并（空白、注释、导入顺序）
   - 低复杂度冲突：智能合并（非重叠修改）
   - 中等冲突：生成建议，标记需人工确认
   - 高复杂度冲突：标记需 refactor skill 介入

4. **结构冲突检测**
   - 识别因大规模重构导致的冲突
   - 评估是否需要调用 refactor skill
   - 生成重构建议

5. **风险评估**
   - 综合评估解决方案风险
   - 生成警告信息
   - 输出置信度评分

## 冲突严重度定义

| 等级 | 定义 | 示例 |
|------|------|------|
| trivial | 无语义影响 | 空白差异、注释变更 |
| low | 简单非重叠修改 | 不同区域的独立修改 |
| medium | 有重叠但可推断 | 同一函数的不同参数修改 |
| high | 语义冲突需判断 | 同一逻辑的不同实现 |
| critical | 结构性冲突 | 大规模重构 vs 功能添加 |

## 质量标准

| 维度 | 标准 | 阈值 |
|-----|------|------|
| 安全性 | 自动合并不引入错误 | 100% |
| 准确性 | 冲突分类正确 | >=95% |
| 透明度 | 每个解决方案有解释 | 100% |
| 谨慎性 | 不确定时标记为手动 | 100% |

## 与其他 Skill 的关系

| Skill | 关系 | 调用时机 |
|-------|------|---------|
| branch-validator | 接收输入 | 由其检测到冲突后调度 |
| refactor | 调用 | 结构性冲突需重构时 |
| branch-orchestrator | 由其调度 | Step 2 条件触发 |
| diff-analyzer | 可复用 | 解析冲突差异 |

## 脚本

- `scripts/resolve_conflicts.py` - 冲突解决主脚本
- `scripts/three_way_merge.py` - 三方合并引擎
- `scripts/structural_detector.py` - 结构性冲突检测器

## 参考资料

- `references/merge-strategies.md` - 合并策略说明
- `references/conflict-taxonomy.md` - 冲突分类学
