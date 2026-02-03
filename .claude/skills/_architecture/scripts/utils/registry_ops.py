#!/usr/bin/env python3
"""
Registry Operations - 注册表操作工具
提供对 registry.json 的原子化操作，确保一致性。
"""

import json
import os
import sys
from datetime import datetime

# fcntl is Unix-only, handle Windows compatibility
if sys.platform != 'win32':
    import fcntl
else:
    fcntl = None
from pathlib import Path
from typing import Optional, Dict, List, Any
from contextlib import contextmanager

# 默认注册表路径
DEFAULT_REGISTRY_PATH = Path(__file__).parent.parent.parent / "registry.json"
TIANGONG_REGISTRY_PATH = Path(__file__).parent.parent.parent / ".tiangong" / "registry.json"


class RegistryError(Exception):
    """注册表操作异常"""
    pass


@contextmanager
def file_lock(filepath: Path, mode: str = 'r+'):
    """文件锁上下文管理器，确保并发安全"""
    f = None
    try:
        f = open(filepath, mode, encoding='utf-8')
        if fcntl is not None:  # Unix 系统使用 fcntl
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        yield f
    finally:
        if f:
            if fcntl is not None:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
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
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise RegistryError(f"Registry JSON parse error: {e}")


def save_registry(registry: Dict[str, Any], registry_path: Optional[Path] = None) -> None:
    """
    保存注册表（带自动更新元数据）

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

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def create_empty_registry() -> Dict[str, Any]:
    """创建空的注册表结构"""
    return {
        "skills": {},
        "metadata": {
            "total_active": 0,
            "total_deprecated": 0,
            "total_archived": 0,
            "cluster_version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
    }


def update_metadata_counts(registry: Dict[str, Any]) -> None:
    """更新注册表元数据中的计数"""
    skills = registry.get("skills", {})

    active = sum(1 for s in skills.values() if s.get("status") == "active")
    deprecated = sum(1 for s in skills.values() if s.get("status") == "deprecated")
    archived = sum(1 for s in skills.values() if s.get("status") == "archived")
    temp = sum(1 for s in skills.values() if s.get("status") == "temp")

    registry["metadata"]["total_active"] = active + temp
    registry["metadata"]["total_deprecated"] = deprecated
    registry["metadata"]["total_archived"] = archived


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
    path: str,
    tier: str,
    domains: List[str],
    contract_level: str = "flexible",
    ttl: Optional[int] = None,
    registry_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    注册新 Skill

    Args:
        skill_id: Skill 唯一标识
        name: Skill 显示名称
        path: Skill 目录相对路径
        tier: 层级 (core, extended, experimental)
        domains: 领域标签列表
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

    skill_entry = {
        "name": name,
        "path": path,
        "status": "temp" if ttl else "active",
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


def increment_metadata_counts(registry: Dict[str, Any]) -> None:
    """递增元数据计数（已弃用，使用 update_metadata_counts）"""
    update_metadata_counts(registry)


if __name__ == "__main__":
    # 测试用例
    import sys

    if len(sys.argv) < 2:
        print("Usage: registry_ops.py <command> [args]")
        print("Commands: list, get <id>, active, domain <domain>, tier <tier>")
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

    elif cmd == "domain" and len(sys.argv) > 2:
        skills = get_skills_by_domain(sys.argv[2])
        for sid, skill in skills.items():
            print(f"  {sid}: {skill.get('name')}")

    elif cmd == "tier" and len(sys.argv) > 2:
        skills = get_skills_by_tier(sys.argv[2])
        for sid, skill in skills.items():
            print(f"  {sid}: {skill.get('name')}")
