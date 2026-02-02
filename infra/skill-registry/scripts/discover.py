#!/usr/bin/env python3
"""
Discover Skills - 发现 Skills
搜索和发现注册的 Skills，也可扫描未注册的 Skills。
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import (
    load_registry, get_active_skills, get_skills_by_domain, get_skills_by_tier
)


def scan_unregistered(scan_path: Path, registry: dict) -> list:
    """扫描未注册的 Skills"""
    registered_paths = set(
        Path(s.get("path", "")) for s in registry.get("skills", {}).values()
    )

    unregistered = []

    # 扫描 L2-execution 目录
    for category in ["core", "extended", "experimental"]:
        category_path = scan_path / "L2-execution" / category
        if category_path.exists():
            for skill_dir in category_path.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        rel_path = skill_dir.relative_to(scan_path)
                        if rel_path not in registered_paths:
                            unregistered.append({
                                "path": str(rel_path),
                                "name": skill_dir.name,
                                "suggested_tier": category
                            })

    # 扫描 L1-orchestrators
    orchestrators_path = scan_path / "L1-orchestrators"
    if orchestrators_path.exists():
        for skill_dir in orchestrators_path.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    rel_path = skill_dir.relative_to(scan_path)
                    if rel_path not in registered_paths:
                        unregistered.append({
                            "path": str(rel_path),
                            "name": skill_dir.name,
                            "suggested_tier": "core"
                        })

    return unregistered


def main():
    parser = argparse.ArgumentParser(description="Discover skills")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--tier", choices=["core", "extended", "experimental"])
    parser.add_argument("--status", choices=["active", "deprecated", "temp", "all"], default="active")
    parser.add_argument("--min-fitness", type=float, help="Minimum fitness score")
    parser.add_argument("--scan", action="store_true", help="Scan for unregistered skills")
    parser.add_argument("--scan-path", default=".", help="Path to scan")
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
        unregistered = scan_unregistered(scan_path, registry)

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
            print(f"  {sid}: [{status}] [{tier}] domains=[{domains}] fitness={fitness_str}")

        if args.scan and unregistered:
            print(f"\nFound {len(unregistered)} unregistered skill(s):")
            for skill in unregistered:
                print(f"  {skill['name']} ({skill['path']}) - suggested tier: {skill['suggested_tier']}")
            print("\nTo register, run:")
            print("  python register.py --id <skill-id> --path <path> --tier <tier> --domains <domains>")


if __name__ == "__main__":
    main()
