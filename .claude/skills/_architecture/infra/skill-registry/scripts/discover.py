#!/usr/bin/env python3
"""
Discover Skills - 发现 Skills
搜索和发现注册的 Skills，也可扫描未注册的 Skills。
支持扫描 _architecture/ 和 .claude/skills/ 两层目录。
"""

import json
import sys
import argparse
from pathlib import Path

# 使用环境变量或相对路径定位项目根，避免硬编码层级深度
_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR
# 向上查找直到找到包含 registry.json 的 _architecture 目录
for _ in range(10):
    if (PROJECT_ROOT / "registry.json").exists():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    # 回退到原始的 4 级向上
    PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent.parent

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import (
    load_registry, get_active_skills, get_skills_by_domain, get_skills_by_tier
)


def scan_unregistered_arch(scan_path: Path, registry: dict) -> list:
    """扫描 _architecture/ 内未注册的 Skills"""
    registered_arch_paths = set()
    for s in registry.get("skills", {}).values():
        arch_path = s.get("arch_path", "")
        # 规范化：去掉尾部斜杠后比较
        registered_arch_paths.add(arch_path.rstrip("/"))

    unregistered = []

    # 扫描 L2-execution 目录
    for category in ["core", "extended", "experimental", "workers"]:
        category_path = scan_path / "L2-execution" / category
        if category_path.exists():
            for skill_dir in category_path.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        rel_path = str(skill_dir.relative_to(scan_path)).replace("\\", "/")
                        if rel_path not in registered_arch_paths:
                            unregistered.append({
                                "path": rel_path,
                                "name": skill_dir.name,
                                "suggested_tier": category if category != "workers" else "core",
                                "source": "architecture"
                            })

    # 扫描 L1-orchestrators
    orchestrators_path = scan_path / "L1-orchestrators"
    if orchestrators_path.exists():
        for skill_dir in orchestrators_path.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    rel_path = str(skill_dir.relative_to(scan_path)).replace("\\", "/")
                    if rel_path not in registered_arch_paths:
                        unregistered.append({
                            "path": rel_path,
                            "name": skill_dir.name,
                            "suggested_tier": "core",
                            "source": "architecture"
                        })

    # 扫描 L0-* commanders
    for item in scan_path.iterdir():
        if item.is_dir() and item.name.startswith("L0-"):
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                rel_path = str(item.relative_to(scan_path)).replace("\\", "/")
                if rel_path not in registered_arch_paths:
                    unregistered.append({
                        "path": rel_path,
                        "name": item.name,
                        "suggested_tier": "core",
                        "source": "architecture"
                    })

    return unregistered


def scan_unregistered_deploy(deploy_root: Path, registry: dict) -> list:
    """扫描 .claude/skills/ 下未在注册表中的已部署 Skills"""
    registered_deploy_paths = set()
    registered_ids = set()
    for sid, s in registry.get("skills", {}).items():
        deploy_path = s.get("deploy_path", "")
        if deploy_path:
            registered_deploy_paths.add(deploy_path.rstrip("/"))
        registered_ids.add(sid)

    unregistered = []

    if not deploy_root.exists():
        return unregistered

    for skill_dir in deploy_root.iterdir():
        if skill_dir.is_dir() and skill_dir.name != "_architecture":
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                dir_name = skill_dir.name
                if dir_name not in registered_deploy_paths and dir_name not in registered_ids:
                    unregistered.append({
                        "path": f"{dir_name}/",
                        "name": dir_name,
                        "suggested_tier": "experimental",
                        "source": "deploy"
                    })

    return unregistered


def main():
    parser = argparse.ArgumentParser(description="Discover skills")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--tier", choices=["core", "extended", "experimental"])
    parser.add_argument("--status", choices=["active", "deprecated", "planned", "temp", "all"], default="active")
    parser.add_argument("--min-fitness", type=float, help="Minimum fitness score")
    parser.add_argument("--scan", action="store_true", help="Scan for unregistered skills")
    parser.add_argument("--scan-path", default=".", help="Architecture path to scan")
    parser.add_argument("--deploy-path", help="Deploy root (.claude/skills/) to scan")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    registry = load_registry()

    # 获取 Skills
    if args.domain:
        skills = get_skills_by_domain(args.domain)
    elif args.tier:
        skills = get_skills_by_tier(args.tier)
    else:
        skills = registry.get("skills", {})

    # 过滤状态
    if args.status != "all":
        skills = {
            sid: s for sid, s in skills.items()
            if s.get("status") == args.status
        }

    # 过滤适应度
    if args.min_fitness is not None:
        skills = {
            sid: s for sid, s in skills.items()
            if (s.get("fitness_score") or 0) >= args.min_fitness
        }

    # 扫描未注册
    unregistered = []
    if args.scan:
        scan_path = Path(args.scan_path).resolve()
        unregistered.extend(scan_unregistered_arch(scan_path, registry))
        if args.deploy_path:
            deploy_path = Path(args.deploy_path).resolve()
            unregistered.extend(scan_unregistered_deploy(deploy_path, registry))

    # 输出
    if args.json:
        result = {
            "registered": skills,
            "count": len(skills)
        }
        if args.scan:
            result["unregistered"] = unregistered
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Found {len(skills)} registered skill(s):")
        for sid, skill in skills.items():
            status = skill.get("status", "?")
            tier = skill.get("tier", "?")
            domains = ", ".join(skill.get("domains", []))
            fitness = skill.get("fitness_score")
            fitness_str = f"{fitness:.2f}" if fitness else "N/A"
            deployed = "Y" if skill.get("deploy_path") else "N"
            print(f"  {sid}: [{status}] [{tier}] deployed={deployed} domains=[{domains}] fitness={fitness_str}")

        if args.scan and unregistered:
            print(f"\nFound {len(unregistered)} unregistered skill(s):")
            for skill in unregistered:
                print(f"  {skill['name']} ({skill['path']}) - tier: {skill['suggested_tier']} source: {skill['source']}")
            print("\nTo register, run:")
            print("  python register.py --id <skill-id> --arch-path <path> --tier <tier> --domains <domains>")


if __name__ == "__main__":
    main()
