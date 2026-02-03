#!/usr/bin/env python3
"""
Modify Skill - 修改 Skill 元数据
更新已注册 Skill 的元数据。
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import load_registry, save_registry, skill_exists, update_skill, get_skill


def main():
    parser = argparse.ArgumentParser(description="Modify skill metadata")
    parser.add_argument("--id", required=True, help="Skill ID")
    parser.add_argument("--tier", choices=["core", "extended", "experimental"])
    parser.add_argument("--domains", help="Comma-separated domains")
    parser.add_argument("--fitness", type=float, help="Fitness score (0-1)")
    parser.add_argument("--status", choices=["active", "deprecated", "temp"])
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")

    args = parser.parse_args()

    if not skill_exists(args.id):
        print(f"Error: Skill '{args.id}' not found")
        sys.exit(1)

    updates = {}

    if args.tier:
        updates["tier"] = args.tier
        # 更新契约等级
        contract_map = {
            "core": "strict",
            "extended": "standard",
            "experimental": "flexible"
        }
        updates["contract_level"] = contract_map[args.tier]

    if args.domains:
        updates["domains"] = [d.strip() for d in args.domains.split(",")]

    if args.fitness is not None:
        if not 0 <= args.fitness <= 1:
            print("Error: Fitness must be between 0 and 1")
            sys.exit(1)
        updates["fitness_score"] = args.fitness

    if args.status:
        updates["status"] = args.status

    if not updates:
        print("No modifications specified")
        sys.exit(1)

    current = get_skill(args.id)

    if args.dry_run:
        print(f"Dry run - would modify skill: {args.id}")
        print("Changes:")
        for key, value in updates.items():
            print(f"  {key}: {current.get(key)} -> {value}")
        return

    try:
        update_skill(args.id, updates)
        print(f"Successfully modified skill: {args.id}")
        print("Updated fields:")
        for key, value in updates.items():
            print(f"  {key}: {value}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
