#!/usr/bin/env python3
"""
Registry Operations - 注册表操作工具
提供对 registry.json 的原子化操作，确保一致性。
"""

import json
import os
import sys
from datetime import datetime

# 跨平台文件锁支持
if sys.platform == 'win32':
    import msvcrt
    fcntl = None
else:
    import fcntl
    msvcrt = None
from pathlib import Path
from typing import Optional, Dict, List, Any
from contextlib import contextmanager

# 默认注册表路径
DEFAULT_REGISTRY_PATH = Path(__file__).parent.parent.parent / "registry.json"

# Layer 分类规则（基于 arch_path 前缀）
LAYER_PREFIXES = {
    "L0": "L0-",
    "L1": "L1-orchestrators/",
    "L2_core": "L2-execution/core/",
    "L2_extended": "L2-execution/extended/",
    "L2_experimental": "L2-execution/experimental/",
    "L2_workers": "L2-execution/workers/",
    "infra": "infra/",
    "genesis": "genesis/",
}


class RegistryError(Exception):
    """注册表操作异常"""
    pass


@contextmanager
def file_lock(filepath: Path, mode: str = 'r+'):
    """文件锁上下文管理器，确保并发安全（跨平台）"""
    f = None
    try:
        f = open(filepath, mode, encoding='utf-8')
        if fcntl is not None:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        elif msvcrt is not None:
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
        yield f
    finally:
        if f:
            if fcntl is not None:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            elif msvcrt is not None:
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
            f.close()


def load_registry(registry_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    加载注册表

    Args:
        registry_path: 注册表文件路径，默认为根目录 registry.json

    Returns:
        注册表字典
    """
    path = Path(registry_path) if registry_path else DEFAULT_REGISTRY_PATH

    if not path.exists():
        return create_empty_registry()

    try:
        with file_lock(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise RegistryError(f"Registry JSON parse error: {e}")


def save_registry(registry: Dict[str, Any], registry_path: Optional[Path] = None) -> None:
    """
    保存注册表（带文件锁和自动更新元数据）

    Args:
        registry: 注册表字典
        registry_path: 保存路径
    """
    path = Path(registry_path) if registry_path else DEFAULT_REGISTRY_PATH

    # 更新元数据
    registry["metadata"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    update_metadata_counts(registry)

    # 确保目录存在
    path.parent.mkdir(parents=True, exist_ok=True)

    # 如果文件不存在，先创建再加锁
    if not path.exists():
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        return

    with file_lock(path, 'r+') as f:
        f.seek(0)
        f.truncate()
        json.dump(registry, f, indent=2, ensure_ascii=False)


def create_empty_registry() -> Dict[str, Any]:
    """创建空的注册表结构（包含所有统计字段）"""
    return {
        "skills": {},
        "metadata": {
            "total_active": 0,
            "total_deprecated": 0,
            "total_archived": 0,
            "total_planned": 0,
            "cluster_version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "tier_breakdown": {
                "core": 0,
                "extended": 0,
                "experimental": 0,
                "core_planned": 0,
                "extended_planned": 0,
                "experimental_planned": 0
            },
            "layer_breakdown": {},
            "domain_breakdown": {}
        }
    }


def _classify_layer(arch_path: str) -> str:
    """根据 arch_path 确定 skill 所在层"""
    for layer, prefix in LAYER_PREFIXES.items():
        if arch_path.startswith(prefix):
            return layer
    return "unknown"


def update_metadata_counts(registry: Dict[str, Any]) -> None:
    """更新注册表元数据中的所有计数（含 tier/layer/domain breakdown）"""
    skills = registry.get("skills", {})

    active = sum(1 for s in skills.values() if s.get("status") == "active")
    deprecated = sum(1 for s in skills.values() if s.get("status") == "deprecated")
    archived = sum(1 for s in skills.values() if s.get("status") == "archived")
    planned = sum(1 for s in skills.values() if s.get("status") == "planned")
    temp = sum(1 for s in skills.values() if s.get("status") == "temp")

    registry["metadata"]["total_active"] = active + temp
    registry["metadata"]["total_deprecated"] = deprecated
    registry["metadata"]["total_archived"] = archived
    registry["metadata"]["total_planned"] = planned

    # Tier breakdown
    tier_breakdown = {}
    for s in skills.values():
        tier = s.get("tier", "unknown")
        status = s.get("status", "unknown")
        if status in ("active", "temp"):
            tier_breakdown[tier] = tier_breakdown.get(tier, 0) + 1
        elif status == "planned":
            key = f"{tier}_planned"
            tier_breakdown[key] = tier_breakdown.get(key, 0) + 1
    registry["metadata"]["tier_breakdown"] = tier_breakdown

    # Layer breakdown
    layer_breakdown = {}
    for s in skills.values():
        arch_path = s.get("arch_path", "")
        layer = _classify_layer(arch_path)
        status = s.get("status", "unknown")
        if status in ("active", "temp"):
            layer_breakdown[layer] = layer_breakdown.get(layer, 0) + 1
        elif status == "planned":
            key = f"{layer}_planned"
            layer_breakdown[key] = layer_breakdown.get(key, 0) + 1
    registry["metadata"]["layer_breakdown"] = layer_breakdown

    # Domain breakdown
    domain_breakdown = {}
    for s in skills.values():
        status = s.get("status", "unknown")
        for domain in s.get("domains", []):
            if status in ("active", "temp"):
                domain_breakdown[domain] = domain_breakdown.get(domain, 0) + 1
            elif status == "planned":
                key = f"{domain}_planned"
                domain_breakdown[key] = domain_breakdown.get(key, 0) + 1
    registry["metadata"]["domain_breakdown"] = domain_breakdown


def skill_exists(skill_id: str, registry_path: Optional[Path] = None) -> bool:
    """检查 Skill 是否存在"""
    registry = load_registry(registry_path)
    return skill_id in registry.get("skills", {})


def get_skill(skill_id: str, registry_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    获取单个 Skill 信息

    Args:
        skill_id: Skill ID
        registry_path: 注册表路径

    Returns:
        Skill 字典或 None
    """
    registry = load_registry(registry_path)
    return registry.get("skills", {}).get(skill_id)


def update_skill(skill_id: str, updates: Dict[str, Any], registry_path: Optional[Path] = None) -> None:
    """
    更新 Skill 信息

    Args:
        skill_id: Skill ID
        updates: 要更新的字段字典
        registry_path: 注册表路径
    """
    registry = load_registry(registry_path)

    if skill_id not in registry.get("skills", {}):
        raise RegistryError(f"Skill '{skill_id}' not found")

    registry["skills"][skill_id].update(updates)
    registry["skills"][skill_id]["updated_at"] = datetime.utcnow().isoformat() + "Z"

    save_registry(registry, registry_path)


def register_skill(
    skill_id: str,
    name: str,
    arch_path: str,
    tier: str,
    domains: List[str],
    deploy_path: Optional[str] = None,
    contract_level: str = "flexible",
    ttl: Optional[int] = None,
    registry_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    注册新 Skill

    Args:
        skill_id: Skill 唯一标识
        name: Skill 显示名称
        arch_path: Skill 架构目录相对路径
        tier: 层级 (core, extended, experimental)
        domains: 领域标签列表
        deploy_path: 部署目录相对路径 (.claude/skills/<name>/)，None 表示未部署
        contract_level: 契约等级 (strict, standard, flexible)
        ttl: 临时 Skill 的生存时间（小时），None 表示永久
        registry_path: 注册表路径

    Returns:
        新注册的 Skill 信息
    """
    registry = load_registry(registry_path)

    if skill_id in registry.get("skills", {}):
        raise RegistryError(f"Skill '{skill_id}' already exists")

    now = datetime.utcnow().isoformat() + "Z"

    # 根据是否有 deploy_path 和 ttl 决定状态
    if ttl:
        status = "temp"
    elif deploy_path:
        status = "active"
    else:
        status = "planned"

    skill_entry = {
        "name": name,
        "arch_path": arch_path,
        "deploy_path": deploy_path,
        "status": status,
        "tier": tier,
        "contract_level": contract_level,
        "version": "1.0.0",
        "domains": domains,
        "fitness_score": None,
        "created_at": now,
        "updated_at": now,
        "ttl": ttl,
        "deprecated_at": None,
        "deprecated_reason": None,
        "lineage": {
            "parent": None,
            "children": [],
            "mutation_of": None,
            "merged_from": []
        }
    }

    registry["skills"][skill_id] = skill_entry
    save_registry(registry, registry_path)

    return skill_entry


def get_active_skills(registry_path: Optional[Path] = None) -> Dict[str, Any]:
    """获取所有活跃的 Skill"""
    registry = load_registry(registry_path)
    return {
        sid: skill for sid, skill in registry.get("skills", {}).items()
        if skill.get("status") in ("active", "temp")
    }


def get_deployed_skills(registry_path: Optional[Path] = None) -> Dict[str, Any]:
    """获取所有已部署的 Skill（有 deploy_path 的活跃 skill）"""
    registry = load_registry(registry_path)
    return {
        sid: skill for sid, skill in registry.get("skills", {}).items()
        if skill.get("deploy_path") and skill.get("status") in ("active", "temp")
    }


def get_skills_by_domain(domain: str, registry_path: Optional[Path] = None) -> Dict[str, Any]:
    """获取指定领域的 Skill"""
    registry = load_registry(registry_path)
    return {
        sid: skill for sid, skill in registry.get("skills", {}).items()
        if domain in skill.get("domains", []) and skill.get("status") == "active"
    }


def get_skills_by_tier(tier: str, registry_path: Optional[Path] = None) -> Dict[str, Any]:
    """获取指定层级的 Skill"""
    registry = load_registry(registry_path)
    return {
        sid: skill for sid, skill in registry.get("skills", {}).items()
        if skill.get("tier") == tier and skill.get("status") == "active"
    }


def deprecate_skill(
    skill_id: str,
    reason: str,
    registry_path: Optional[Path] = None
) -> None:
    """
    废弃 Skill

    Args:
        skill_id: Skill ID
        reason: 废弃原因
        registry_path: 注册表路径
    """
    registry = load_registry(registry_path)

    if skill_id not in registry.get("skills", {}):
        raise RegistryError(f"Skill '{skill_id}' not found")

    now = datetime.utcnow().isoformat() + "Z"

    registry["skills"][skill_id]["status"] = "deprecated"
    registry["skills"][skill_id]["deprecated_at"] = now
    registry["skills"][skill_id]["deprecated_reason"] = reason
    registry["skills"][skill_id]["updated_at"] = now

    save_registry(registry, registry_path)


def archive_skill(skill_id: str, registry_path: Optional[Path] = None) -> None:
    """归档 Skill"""
    update_skill(skill_id, {"status": "archived"}, registry_path)


def bump_version(skill_id: str, bump_type: str = "patch", registry_path: Optional[Path] = None) -> str:
    """
    升级 Skill 版本号

    Args:
        skill_id: Skill ID
        bump_type: 升级类型 (major, minor, patch)
        registry_path: 注册表路径

    Returns:
        新版本号
    """
    registry = load_registry(registry_path)

    if skill_id not in registry.get("skills", {}):
        raise RegistryError(f"Skill '{skill_id}' not found")

    current = registry["skills"][skill_id].get("version", "1.0.0")
    parts = current.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    update_skill(skill_id, {"version": new_version}, registry_path)
    return new_version


if __name__ == "__main__":
    # 测试用例
    import sys

    if len(sys.argv) < 2:
        print("Usage: registry_ops.py <command> [args]")
        print("Commands: list, get <id>, active, deployed, domain <domain>, tier <tier>, bump <id> [major|minor|patch]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        registry = load_registry()
        for sid, skill in registry.get("skills", {}).items():
            print(f"  {sid}: {skill.get('name')} ({skill.get('status')})")

    elif cmd == "get" and len(sys.argv) > 2:
        skill = get_skill(sys.argv[2])
        print(json.dumps(skill, indent=2, ensure_ascii=False))

    elif cmd == "active":
        skills = get_active_skills()
        for sid, skill in skills.items():
            print(f"  {sid}: {skill.get('name')}")

    elif cmd == "deployed":
        skills = get_deployed_skills()
        for sid, skill in skills.items():
            print(f"  {sid}: {skill.get('name')} -> {skill.get('deploy_path')}")

    elif cmd == "domain" and len(sys.argv) > 2:
        skills = get_skills_by_domain(sys.argv[2])
        for sid, skill in skills.items():
            print(f"  {sid}: {skill.get('name')}")

    elif cmd == "tier" and len(sys.argv) > 2:
        skills = get_skills_by_tier(sys.argv[2])
        for sid, skill in skills.items():
            print(f"  {sid}: {skill.get('name')}")

    elif cmd == "bump" and len(sys.argv) > 2:
        bump_type = sys.argv[3] if len(sys.argv) > 3 else "patch"
        new_ver = bump_version(sys.argv[2], bump_type)
        print(f"  {sys.argv[2]}: bumped to {new_ver}")
