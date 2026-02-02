---
name: skill-registry
description: >
  Skill 注册中心。管理所有 skill 的注册、发现、废弃、临时激活和元数据修改。
  当需要：(1) 注册新 skill，(2) 查询可用 skill，(3) 废弃/归档 skill，
  (4) 创建临时 skill，(5) 修改 skill 元数据时触发。
  维护全局 registry.json 作为 skill 的唯一真相源。
---

# Skill Registry — 注册中心

## 注册表结构

位置：`../state/registry.json`

```json
{
  "skills": {
    "<skill-id>": {
      "name": "...",
      "path": "relative/path/to/skill/",
      "status": "active | deprecated | archived | temp",
      "tier": "core | extended | experimental",
      "contract_level": "strict | standard | flexible",
      "version": "1.0.0",
      "domains": ["code", "test"],
      "fitness_score": 0.85,
      "created_at": "ISO-8601",
      "updated_at": "ISO-8601",
      "ttl": null,
      "deprecated_at": null,
      "deprecated_reason": null,
      "lineage": {
        "parent": null,
        "children": [],
        "mutation_of": null,
        "merged_from": []
      }
    }
  },
  "metadata": {
    "total_active": 0,
    "total_deprecated": 0,
    "last_updated": "ISO-8601"
  }
}
```

## 操作

### 注册新 Skill

```bash
python scripts/register.py \
  --id <skill-id> \
  --path <relative-path> \
  --tier <core|extended|experimental> \
  --domains <domain1,domain2> \
  [--ttl <hours>]  # 如果是临时 skill
```

验证步骤：
1. 检查 skill 目录存在且包含有效 SKILL.md
2. 检查 SKILL.md frontmatter 包含 name 和 description
3. 检查 skill-id 在 registry 中唯一
4. 根据 tier 检查契约符合性
5. 写入 registry.json

### 废弃 Skill

```bash
python scripts/deprecate.py --id <skill-id> --reason "..."
```

- 将 status 设为 "deprecated"
- 记录废弃时间和原因
- 不删除文件，仅标记
- 30 天后由 lifecycle-manager 的 archive.py 归档

### 临时 Skill

```bash
python scripts/activate_temp.py \
  --id <skill-id> \
  --path <relative-path> \
  --ttl <hours> \
  --domains <domain1>
```

- status 设为 "temp"
- 设置 TTL（生存时间）
- 过期后自动标记为 deprecated
- 可通过 `--promote` 标志在过期前转为正式 skill

### 修改 Skill 元数据

```bash
python scripts/modify.py --id <skill-id> \
  [--tier <new-tier>] \
  [--domains <new-domains>] \
  [--fitness <new-score>] \
  [--status <new-status>]
```

### 发现 Skill

```bash
python scripts/discover.py \
  [--domain <domain>] \
  [--tier <tier>] \
  [--status active] \
  [--min-fitness 0.7]
```

- 支持按领域、tier、状态、适应度过滤
- 也可扫描目录发现未注册的 skill 并提示注册

## 一致性保证

- registry.json 是唯一真相源
- 每次修改前先加锁（文件锁），操作完成后释放
- 每次修改后更新 metadata 中的计数和时间戳
- 提供 `--dry-run` 选项预览变更
